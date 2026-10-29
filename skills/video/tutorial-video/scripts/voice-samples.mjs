// Voices to pick by ear, before a tutorial is voiced.
//   node voice-samples.mjs <out-dir> [lang=de] ["sentence"] [count=12]
// ElevenLabs: the shared voice library filtered by language (native speakers, their free preview
// clips — no credits spent, nothing added to the account) plus the account's own voices, which also
// speak `sentence` (credits). Writes <out-dir>/voices.json and the mp3s; build a page of <audio>
// players from it and let the user choose. A shared voice must be added to the account
// (POST /v1/voices/add/{public_owner_id}/{voice_id}) before TTS can use it — ask first.
// Key: ELEVENLABS_API_KEY (env, nearest .env, keychain "elevenlabs-api-key"); never printed.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const outDir = resolve(process.argv[2] ?? "voice-samples");
const lang = process.argv[3] ?? "de";
const sentence =
	process.argv[4] ??
	"Willkommen. In zwei Minuten zeigen wir Ihnen, wie Sie die App im Alltag nutzen.";
const count = Number(process.argv[5] ?? 12);
mkdirSync(outDir, { recursive: true });

const fromDotenv = (name) => {
	let dir = process.cwd();
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
const fromKeychain = (service) => {
	try {
		return execFileSync("security", ["find-generic-password", "-s", service, "-w"], {
			encoding: "utf8",
			stdio: ["ignore", "pipe", "ignore"],
		}).trim();
	} catch {
		return "";
	}
};
const key =
	process.env.ELEVENLABS_API_KEY || fromDotenv("ELEVENLABS_API_KEY") || fromKeychain("elevenlabs-api-key");
if (!key) throw new Error("ELEVENLABS_API_KEY missing");

const api = async (path, init = {}) => {
	const res = await fetch(`https://api.elevenlabs.io${path}`, {
		...init,
		headers: { "xi-api-key": key, "Content-Type": "application/json", ...init.headers },
	});
	if (!res.ok) throw new Error(`ElevenLabs ${path} ${res.status}: ${await res.text()}`);
	return res;
};
const save = async (url, file) => {
	const res = await fetch(url);
	if (!res.ok) return null;
	writeFileSync(join(outDir, file), Buffer.from(await res.arrayBuffer()));
	return file;
};

const voices = [];

// 1. Shared library: native speakers of `lang`, narration first.
const shared = await (
	await api(`/v1/shared-voices?language=${lang}&page_size=${count * 2}&sort=trending`)
).json();
const narrators = shared.voices
	.filter((v) => !v.use_case || /narrat|informative|educational|conversational/i.test(v.use_case))
	.slice(0, count);
for (const v of narrators) {
	const file = v.preview_url ? await save(v.preview_url, `shared-${v.voice_id}.mp3`) : null;
	voices.push({
		source: "shared",
		voiceId: v.voice_id,
		publicOwnerId: v.public_owner_id,
		name: v.name,
		gender: v.gender,
		age: v.age,
		accent: v.accent,
		useCase: v.use_case,
		category: v.category,
		description: v.description,
		file,
		sentence: null,
	});
}

// 2. The account's own voices: `sentence` in the multilingual model.
const mine = await (await api("/v2/voices?page_size=50")).json();
// Premade voices count too; capped, every sample costs credits. A voice the plan may not use
// (e.g. an instant clone on a free plan) is listed with its refusal instead of a file.
for (const v of (mine.voices ?? []).slice(0, count)) {
	const entry = {
		source: "mine",
		voiceId: v.voice_id,
		name: v.name,
		category: v.category,
		gender: v.labels?.gender,
		age: v.labels?.age,
		accent: v.labels?.accent,
		useCase: v.labels?.use_case,
		description: v.description,
		file: null,
		sentence,
	};
	try {
		const res = await api(`/v1/text-to-speech/${v.voice_id}?output_format=mp3_44100_128`, {
			method: "POST",
			body: JSON.stringify({ text: sentence, model_id: "eleven_v4", language_code: lang }),
		});
		entry.file = `mine-${v.voice_id}.mp3`;
		writeFileSync(join(outDir, entry.file), Buffer.from(await res.arrayBuffer()));
	} catch (e) {
		entry.refused = String(e.message).match(/"status":"([^"]+)"/)?.[1] ?? "error";
	}
	voices.push(entry);
}

writeFileSync(join(outDir, "voices.json"), JSON.stringify({ lang, sentence, voices }, null, "\t"));
console.log(`${voices.length} voices → ${outDir}/voices.json`);
