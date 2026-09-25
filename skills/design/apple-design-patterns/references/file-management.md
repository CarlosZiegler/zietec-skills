# File management

- Integrate with the platform’s document model and familiar create, open, save, and preview interfaces.
- Generally autosave periodically while editing, when closing a file, and when switching apps. Keep unsaved and conflicting states understandable.
- Design local save, cloud synchronization, and failure as distinct states when relevant; preserve pending work and provide recovery before closing would lose it.
- Use Quick Look for previews where appropriate, including content the app cannot edit.
- If a custom browser is necessary, preserve expected file-system relationships and relevant document filtering.
- Let people choose export or move destinations and appropriate save details.

Consider how documents are opened from outside the app, renamed, relocated, and revisited. A custom in-app gallery should not break the person’s understanding of files stored elsewhere in the system.

Source: [Apple HIG — File management](https://developer.apple.com/design/human-interface-guidelines/file-management). Checked 2026-09-08.
