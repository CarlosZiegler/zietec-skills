# ZieTec Skills

A [skills.sh](https://skills.sh)-compatible collection of agent skills. Layout follows the Matt Pocock skills monorepo: each skill lives at `skills/<bucket>/<skill-name>/SKILL.md`, with optional `references/`, `agents/`, and `scripts/` trees copied intact from the source.

This repository is a **collection**, not a replacement. Source repositories stay the originals. Skills were copied here so they can be installed together with:

```sh
npx skills@latest add CarlosZiegler/zietec-skills
```

## Buckets

**Design** (`skills/design/`): product and design orchestration (`design-maestro`, `product-studio`) plus Apple Human Interface Guidelines skills (`apple-design-*`).

**Print** (`skills/print/`): Blender-to-FDM modeling, preflight, Bambu Lab H2C slicing, and print troubleshooting.

**Video** (`skills/video/`): narrated product tutorial videos recorded for real (`tutorial-video`).

**Agents** (`skills/agents/`): delegation skills that keep Claude Code as coordinator (`grok-first`, `opencode-first`).

There is no `skills/media/` bucket in this collection. Media / Google Video Creator skills are intentionally excluded and remain in their original repository; `skills/video/` holds only the tutorial-video skill.

## Language

**Skill**: a folder with `SKILL.md` (required) and any bundled references, agent configs, or scripts.

**Bucket**: a thematic grouping under `skills/`. Installers discover skills by walking these folders.

**Source repository**: the original project a skill was copied from. This monorepo does not archive, rename, or supersede those repos.

**Plugin manifest**: `.claude-plugin/` exists so Claude Code can load the repo as a local plugin. It is not a claim that ZieTec is listed on Anthropic’s official marketplace.
