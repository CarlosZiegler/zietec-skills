# ZieTec Skills

A [skills.sh](https://skills.sh)-compatible collection of agent skills. Layout follows the Matt Pocock skills monorepo: each skill lives at `skills/<bucket>/<skill-name>/SKILL.md`, with optional `references/`, `agents/`, and `scripts/` trees copied intact from the source.

This repository is a **collection**, not a replacement. Source repositories stay the originals. Skills were copied here so they can be installed together with:

```sh
npx skills@latest add CarlosZiegler/zietec-skills
```

## Buckets

**Product** (`skills/product/`): deciding what to build and what to call it (`produto`, `nome`).

**Design** (`skills/design/`): product and design orchestration (`design-maestro`, `product-studio`, `forja`, `forja-v1`, `tempera`), interface simplification (`simplificar-design`) plus Apple Human Interface Guidelines skills (`apple-design-*`).

**Docs** (`docs/`): not skills. Changelogs (`docs/forja/`) and reference surveys (`docs/referencias/`).

**Print** (`skills/print/`): Blender-to-FDM modeling, preflight, Bambu Lab H2C slicing, and print troubleshooting.

**Video** (`skills/video/`): narrated product tutorial videos recorded for real (`tutorial-video`) and short app ads with voice, music and sound effects (`ads-video`).

**Agents** (`skills/agents/`): delegation skills that keep Claude Code as coordinator (`grok-first`, `opencode-first`).

There is no `skills/media/` bucket in this collection. Media / Google Video Creator skills are intentionally excluded and remain in their original repository; `skills/video/` holds only the tutorial-video and ads-video skills.

## Language

**Skill**: a folder with `SKILL.md` (required) and any bundled references, agent configs, or scripts.

**Frozen version**: a copy of a skill kept under `<name>-v<N>` and the commit it was frozen from, so a new version can be tried and rolled back.

**Bucket**: a thematic grouping under `skills/`. Installers discover skills by walking these folders.

**Source repository**: the original project a skill was copied from. This monorepo does not archive, rename, or supersede those repos.

**Plugin manifest**: `.claude-plugin/` exists so Claude Code can load the repo as a local plugin. It is not a claim that ZieTec is listed on Anthropic’s official marketplace.
