// Voice-over per scene: macOS `say` (draft) or OpenAI TTS when OPENAI_API_KEY is set (or the key
// is in the macOS keychain as "openai-api-key"). Writes out/vo/<id>.wav and out/vo.json with the
// duration of every clip — the recorder holds each scene for exactly its narration.
// Key: OPENAI_API_KEY in the environment, the repo root .env, or the keychain.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const lang = process.argv[2] ?? "de";
// The tutorial folder (script.<lang>.json, out/): second argument, default the current directory.
const base = resolve(process.argv[3] ?? process.cwd());
const script = JSON.parse(readFileSync(join(base, `script.${lang}.json`), "utf8"));
const out = join(base, "out", lang, "vo");
mkdirSync(out, { recursive: true });

const keychainKey = () => {
	try {
		return execFileSync("security", ["find-generic-password", "-s", "openai-api-key", "-w"], {
			encoding: "utf8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
	} catch {
		return "";
	}
};
/** OPENAI_API_KEY from the nearest .env above the tutorial folder (the value is never printed). */
const dotenvKey = () => {
	let dir = base;
	for (let i = 0; i < 8; i++) {
		try {
			const line = readFileSync(join(dir, ".env"), "utf8")
				.split("\n")
				.find((l) => l.startsWith("OPENAI_API_KEY="));
			if (line) return line.slice("OPENAI_API_KEY=".length).trim().replace(/^["']|["']$/g, "");
		} catch {
			// no .env here
		}
		const up = dirname(dir);
		if (up === dir) break;
		dir = up;
	}
	return "";
};
const apiKey = process.env.OPENAI_API_KEY || dotenvKey() || keychainKey();
const engine = process.env.VOICE === "say" || !apiKey ? "say" : "openai";

const duration = (file) =>
	Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file], { encoding: "utf8" }).trim());

const result = { engine, scenes: {} };
for (const scene of script.scenes) {
	const wav = join(out, `${scene.id}.wav`);
	if (engine === "openai") {
		const res = await fetch("https://api.openai.com/v1/audio/speech", {
			method: "POST",
			headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
			body: JSON.stringify({
				model: script.voice.openai.model,
				voice: script.voice.openai.voice,
				instructions: script.voice.openai.instructions,
				input: scene.vo,
				response_format: "wav",
			}),
		});
		if (!res.ok) throw new Error(`OpenAI TTS ${res.status}: ${await res.text()}`);
		const raw = wav.replace(/\.wav$/, ".raw.wav");
		writeFileSync(raw, Buffer.from(await res.arrayBuffer()));
		// Trim the silence the model leaves at both ends, keep 120 ms at the end.
		execFileSync("ffmpeg", [
			"-y", "-loglevel", "error", "-i", raw,
			"-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,apad=pad_dur=0.12,areverse",
			"-ar", "48000", "-ac", "1", wav,
		]);
	} else {
		const aiff = wav.replace(/\.wav$/, ".aiff");
		execFileSync("say", ["-v", script.voice.say, "-r", String(script.voice.rate), "-o", aiff, scene.vo]);
		execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", aiff, "-ar", "48000", "-ac", "1", wav]);
	}
	result.scenes[scene.id] = { file: wav, duration: duration(wav) };
	console.log(`${scene.id}: ${result.scenes[scene.id].duration.toFixed(2)} s (${engine})`);
}
writeFileSync(join(dirname(out), "vo.json"), JSON.stringify(result, null, "\t"));
