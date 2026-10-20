# ZieTec Skills

Agent skills from [ZieTec](https://github.com/CarlosZiegler) for design, print, video, and coding-agent workflows. Compatible with [skills.sh](https://skills.sh).

[![skills.sh](https://skills.sh/b/CarlosZiegler/zietec-skills)](https://skills.sh/CarlosZiegler/zietec-skills)

Install into any project:

```sh
npx skills@latest add CarlosZiegler/zietec-skills
```

Pick the skills you want and which coding agents to install them on. List without installing:

```sh
npx skills@latest add CarlosZiegler/zietec-skills --list
```

Add `--global` to install for your user account instead of the current project.

This repository follows the folder layout supported by the [Skills CLI](https://github.com/vercel-labs/skills): `skills/<bucket>/<skill-name>/SKILL.md`. No npm publish is required.

`.claude-plugin/` is included so Claude Code can load the collection as a **local** plugin. It is not listed on Anthropic’s official Claude marketplace.

## Design

Product and design orchestration, plus Apple Human Interface Guidelines skills.

- **[design-maestro](./skills/design/design-maestro/SKILL.md)**: Direct product, brand, website, landing-page, dashboard, and interface design work from brief to handoff.
- **[product-studio](./skills/design/product-studio/SKILL.md)**: Run a persistent product-and-design operating system for multi-session website, app, brand, and digital-product work.
- **[forja](./skills/design/forja/SKILL.md)**: Turn an app or micro-SaaS idea into a complete product package in Claude Design (research, 9 mobile + 9 desktop screens with motion, printable A4 product documentation and a 14-slide pitch) in EN · PT · DE, with its own art direction per product, delegated build, pitch completeness gate and in-place updates.
- **[tempera](./skills/design/tempera/SKILL.md)**: Turn an app or micro-SaaS idea into a verified product package in Claude Design (research with an evidence registry, mobile and desktop screens with motion, printable docs, pitch, build handoff), with traceability, flow replay and a report of what remains unverified.
- **[apple-design-principles](./skills/design/apple-design-principles/SKILL.md)**: Apply Apple’s Human Interface Guidelines design principles to product concepts, design tradeoffs, or interface critiques for Apple platforms. Use for reasoning about experience quality rather than detailed component specifications.
- **[apple-design-ios](./skills/design/apple-design-ios/SKILL.md)**: Design, implement, or review iPhone interfaces using Apple’s iOS Human Interface Guidelines. Use for iOS screen structure, touch ergonomics, adaptive behavior, and integration with iPhone system experiences.
- **[apple-design-platforms](./skills/design/apple-design-platforms/SKILL.md)**: Adapt an Apple-platform product for iPadOS, macOS, watchOS, or tvOS, including Mac Catalyst. Use when platform conventions, windowing, viewing distance, and input models affect the design.
- **[apple-design-foundations](./skills/design/apple-design-foundations/SKILL.md)**: Design or review the visual foundations of an Apple-platform interface: layout, typography, color, appearance, materials, motion, icons, imagery, branding, and interface writing.
- **[apple-design-accessibility](./skills/design/apple-design-accessibility/SKILL.md)**: Design or audit accessible and inclusive Apple-platform interfaces, including VoiceOver, larger text, alternate inputs, motion accommodations, and right-to-left localization.
- **[apple-design-navigation](./skills/design/apple-design-navigation/SKILL.md)**: Choose or review navigation and search structures for Apple apps, including tabs, sidebars, split views, toolbars, hierarchical browsers, and search placement and scope.
- **[apple-design-controls](./skills/design/apple-design-controls/SKILL.md)**: Choose and specify Apple UI controls for actions, selection, values, text entry, and forms. Use for button semantics, pickers, toggles, fields, sliders, and keyboard behavior.
- **[apple-design-menus](./skills/design/apple-design-menus/SKILL.md)**: Design Apple app command menus, context and edit menus, menu bars, Dock menus, and Home Screen quick actions, with discoverable commands and platform-correct organization.
- **[apple-design-presentation](./skills/design/apple-design-presentation/SKILL.md)**: Choose and review Apple presentation containers: alerts, action sheets, sheets, popovers, panels, windows, and share sheets. Use when interruption, task scope, dismissal, or window behavior matters.
- **[apple-design-content](./skills/design/apple-design-content/SKILL.md)**: Design Apple app content presentation using lists, tables, collections, charts, images, scroll views, labels, gauges, and progress indicators. Use for information display and content interaction.
- **[apple-design-patterns](./skills/design/apple-design-patterns/SKILL.md)**: Design common Apple app flows such as onboarding, launching, loading, collaboration, file management, feedback, settings, multitasking, and undo. Use for task behavior across screens and states.
- **[apple-design-media](./skills/design/apple-design-media/SKILL.md)**: Design Apple audio, video, live-viewing, haptic, photo-editing, AirPlay, SharePlay, or audio-recognition experiences, including playback transitions and media-specific feedback.
- **[apple-design-inputs](./skills/design/apple-design-inputs/SKILL.md)**: Design and review Apple app input behavior for gestures, physical keyboards, pointers, Apple Pencil, focus, remotes, device motion, and hardware buttons.
- **[apple-design-spatial](./skills/design/apple-design-spatial/SKILL.md)**: Design visionOS, spatial, immersive, or augmented-reality interfaces using Apple HIG guidance for windows, depth, eye targeting, gestures, immersion, and physical comfort.
- **[apple-design-system-experiences](./skills/design/apple-design-system-experiences/SKILL.md)**: Design an Apple app’s experiences outside its main window: widgets, Live Activities, notifications, Control Center controls, Siri, App Shortcuts, App Clips, complications, and Top Shelf.
- **[apple-design-privacy-identity](./skills/design/apple-design-privacy-identity/SKILL.md)**: Design Apple app privacy and identity flows: contextual permissions, account creation and deletion, Sign in with Apple, and in-person ID verification. Focuses on user experience rather than backend security implementation.
- **[apple-design-commerce](./skills/design/apple-design-commerce/SKILL.md)**: Design Apple Pay checkout, in-app purchases and subscriptions, Wallet passes, or Tap to Pay on iPhone merchant experiences using Apple’s commerce HIG guidance.
- **[apple-design-health](./skills/design/apple-design-health/SKILL.md)**: Design Apple health and fitness experiences involving HealthKit, CareKit, ResearchKit, workouts, or Activity rings, with appropriate data-access UX and domain-specific presentation.
- **[apple-design-connected-technologies](./skills/design/apple-design-connected-technologies/SKILL.md)**: Design Apple HIG experiences for connected technologies such as CarPlay, HomeKit, maps, iCloud, NFC, and iMessage apps or stickers. Use when integration behavior changes the user experience.
- **[apple-design-ai](./skills/design/apple-design-ai/SKILL.md)**: Design or review generative AI, recommendations, predictions, and machine-learning features in Apple apps, including transparency, correction, feedback, and non-AI fallback behavior.
- **[apple-design-games](./skills/design/apple-design-games/SKILL.md)**: Design or adapt game interfaces for Apple platforms, including onboarding through play, input alternatives, platform-specific controls, accessibility, and Game Center integration.

## Print

Blender modeling through Bambu Lab H2C slicing and troubleshooting.

- **[blender-print-ready](./skills/print/blender-print-ready/SKILL.md)**: Use when creating, adjusting or exporting Blender models for FDM printing, especially separate assembly parts, supports, clearances and color-separated plates for a Bambu Lab H2C.
- **[fdm-print-preflight](./skills/print/fdm-print-preflight/SKILL.md)**: Use before delivering an FDM model or sliced project, or after changing geometry, orientation or supports, to check actual bed contact, elevated undersides, critical layers and the saved print artifact.
- **[bambu-h2c-slice-print](./skills/print/bambu-h2c-slice-print/SKILL.md)**: Use when preparing, slicing or validating a Bambu Studio project for the H2C, including per-object supports, color-separated plates and AMS/nozzle mapping, or operating a print the user has authorized.
- **[bambu-print-troubleshoot](./skills/print/bambu-print-troubleshoot/SKILL.md)**: Use when a Bambu H2C print fails, spaghetti or floating-cantilever warnings appear, an HMS code is reported, or a printed part has adhesion, extrusion, dimensional or support defects.

## Video

Narrated product tutorial videos, produced automatically.

- **[tutorial-video](./skills/video/tutorial-video/SKILL.md)**: Produce narrated product tutorial videos automatically — script, OpenAI voice-over in a native accent, a real recording driven by Playwright (web app, browser-extension popup) or the iOS simulator (mobile app), cursor and tap highlights, captions, ducked music, title and end cards, 1080p mp4.

## Agents

Delegation skills that keep Claude Code as coordinator.

- **[grok-first](./skills/agents/grok-first/SKILL.md)**: Use when Claude Code should delegate implementation, fixes, exploration, and approved git mechanics to Grok Build CLI while Claude specifies, decides, reviews, and verifies.
- **[opencode-first](./skills/agents/opencode-first/SKILL.md)**: Use when Claude Code should delegate a bounded implementation to OpenCode while retaining design and final verification.

## Sources

Skill bodies were **copied** into this monorepo. The original repositories remain the sources of truth and were not deleted, archived, renamed, or modified as part of this collection:

- [`CarlosZiegler/apple-hig-skills`](https://github.com/CarlosZiegler/apple-hig-skills) → `skills/design/apple-design-*`
- [`CarlosZiegler/bambu-h2c-skills`](https://github.com/CarlosZiegler/bambu-h2c-skills) → `skills/print/*`
- [`CarlosZiegler/grok-first`](https://github.com/CarlosZiegler/grok-first) → `skills/agents/grok-first`
- [`CarlosZiegler/opencode-first`](https://github.com/CarlosZiegler/opencode-first) → `skills/agents/opencode-first`
- [`CarlosZiegler/tutorial-video-skill`](https://github.com/CarlosZiegler/tutorial-video-skill) → `skills/video/tutorial-video` (templates here are generic examples)
- `design-maestro` and `product-studio` are new design skills added here under `skills/design/`

See [CONTEXT.md](./CONTEXT.md) for how the buckets are organized. Licensed under [MIT](./LICENSE).
