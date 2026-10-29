// Voice-over per scene: ElevenLabs, OpenAI TTS or macOS `say` (draft). Writes out/vo/<id>.wav and
// out/vo.json with the duration of every clip — the recorder holds each scene for exactly its narration.
// Engine: VOICE=elevenlabs|openai|say; default ElevenLabs when script.voice.elevenlabs and a key exist,
// else OpenAI when a key exists, else say.
// Keys (never printed): ELEVENLABS_API_KEY / OPENAI_API_KEY in the environment, the nearest .env
// above the tutorial folder, or the macOS keychain ("elevenlabs-api-key" / "openai-api-key").
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

const keychainKey = (service) => {
	try {
		return execFileSync("security", ["find-generic-password", "-s", service, "-w"], {
			encoding: "utf8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
	} catch {
		return "";
	}
};
/** NAME=value from the nearest .env above the tutorial folder (the value is never printed). */
const dotenvKey = (name) => {
	let dir = base;
	for (let i = 0; i < 8; i++) {
		try {
			const line = readFileSync(join(dir, ".env"), "utf8")
				.split("\n")
				.find((l) => l.startsWith(`${name}=`));
			if (line) return line.slice(name.length + 1).trim().replace(/^["']|["']$/g, "");
		} catch {
			// no .env here
		}
		const up = dirname(dir);
		if (up === dir) break;
		dir = up;
	}
	return "";
};
const keyOf = (name, service) => process.env[name] || dotenvKey(name) || keychainKey(service);
const openaiKey = keyOf("OPENAI_API_KEY", "openai-api-key");
const elevenKey = keyOf("ELEVENLABS_API_KEY", "elevenlabs-api-key");
const engine =
	process.env.VOICE ??
	(script.voice.elevenlabs && elevenKey ? "elevenlabs" : openaiKey ? "openai" : "say");
if (engine === "elevenlabs" && !(elevenKey && script.voice.elevenlabs?.voiceId)) {
	throw new Error("ElevenLabs needs ELEVENLABS_API_KEY and script.voice.elevenlabs.voiceId");
}
if (engine === "openai" && !openaiKey) throw new Error("OpenAI needs OPENAI_API_KEY");

/** Trims the silence a model leaves at both ends (keeps 120 ms at the end), 48 kHz mono wav. */
const trimToWav = (raw, wav) =>
	execFileSync("ffmpeg", [
		"-y", "-loglevel", "error", "-i", raw,
		"-af", "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,apad=pad_dur=0.12,areverse",
		"-ar", "48000", "-ac", "1", wav,
	]);

/**
 * ElevenLabs text-to-speech, default model `eleven_v4` with `language_code` (German pronunciation
 * and number/date normalisation). v4 takes only stability and similarity_boost; the v2/flash models
 * also take style/speed and get each scene's neighbours (`previous_text` / `next_text`), so the
 * intonation runs on across scenes. `eleven_multilingual_v2` refuses
 * `language_code`, so it is left out there.
 */
const eleven = async (scene, i) => {
	const cfg = script.voice.elevenlabs;
	const model = cfg.model ?? "eleven_v4";
	const v4 = model.startsWith("eleven_v4") || model === "eleven_v3";
	const settings = { stability: 0.5, similarity_boost: 0.75, ...cfg.settings };
	const url = new URL(`https://api.elevenlabs.io/v1/text-to-speech/${cfg.voiceId}`);
	url.searchParams.set("output_format", "mp3_44100_192");
	const res = await fetch(url, {
		method: "POST",
		headers: { "xi-api-key": elevenKey, "Content-Type": "application/json" },
		body: JSON.stringify({
			text: scene.vo,
			model_id: model,
			...(model === "eleven_multilingual_v2" ? {} : { language_code: cfg.languageCode ?? lang }),
			apply_text_normalization: "on",
			...(v4
				? {
						voice_settings: {
							stability: settings.stability,
							similarity_boost: settings.similarity_boost,
						},
					}
				: {
						previous_text: script.scenes[i - 1]?.vo,
						next_text: script.scenes[i + 1]?.vo,
						voice_settings: { style: 0, speed: 1, use_speaker_boost: true, ...settings },
					}),
		}),
	});
	if (!res.ok) throw new Error(`ElevenLabs TTS ${res.status}: ${await res.text()}`);
	return Buffer.from(await res.arrayBuffer());
};

const duration = (file) =>
	Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", file], { encoding: "utf8" }).trim());

const result = { engine, scenes: {} };
for (const [i, scene] of script.scenes.entries()) {
	const wav = join(out, `${scene.id}.wav`);
	if (engine === "elevenlabs") {
		const raw = wav.replace(/\.wav$/, ".raw.mp3");
		writeFileSync(raw, await eleven(scene, i));
		trimToWav(raw, wav);
	} else if (engine === "openai") {
		const res = await fetch("https://api.openai.com/v1/audio/speech", {
			method: "POST",
			headers: { Authorization: `Bearer ${openaiKey}`, "Content-Type": "application/json" },
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
		trimToWav(raw, wav);
	} else {
		const aiff = wav.replace(/\.wav$/, ".aiff");
		execFileSync("say", ["-v", script.voice.say, "-r", String(script.voice.rate), "-o", aiff, scene.vo]);
		execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", aiff, "-ar", "48000", "-ac", "1", wav]);
	}
	result.scenes[scene.id] = { file: wav, duration: duration(wav) };
	console.log(`${scene.id}: ${result.scenes[scene.id].duration.toFixed(2)} s (${engine})`);
}
writeFileSync(join(dirname(out), "vo.json"), JSON.stringify(result, null, "\t"));
