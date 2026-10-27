# Designing for iPhone Duo

iPhone Duo folds around a center hinge. Closed, people use the outer display, which is wider and shorter than other iPhones. Open, the inner display is larger. Between the two, the device can rest half-open like a book or stand on an edge.

## Layout

- Design for size classes, not poses: compact width on the outer display, regular width on the inner display. Do not build a separate layout per pose.
- Let the existing layout grow or shrink into the available space. Avoid fixed widths and assumptions about a specific display.
- Keep functionality and element state identical across displays. The inner display may show one extra level of the hierarchy (for example, a list and its detail side by side) when the content supports it.
- Keep text and control sizes stable while the window changes. Prefer an even column count in grids so content divides cleanly around the fold.
- Games fill the display in every pose. Change the aspect ratio instead of letterboxing; if padding is unavoidable, fill it with artwork.

## Reserved regions

- **Outer camera:** always present on the outer display, and it expands into the Dynamic Island. Side controls align with it.
- **Inner camera:** appears only while the camera is active; the interface moves aside.
- **Fold:** present while the device is partially open. It divides the inner display, and the center is not usable for content people must read or tap.
- System alerts, menus, sheets, and split views already avoid the fold. Custom components must use the reserved-region API to keep important elements clear, and should move only what is necessary.

## Containers

- Use the system split view for list-detail structures. It collapses to one pane on the outer display and adjusts column widths around the fold.
- Use an arrangement view when a screen already behaves like a horizontal or vertical stack (split arrangement) or a layered stack (overlay arrangement). Keep navigation containers, such as split views and tab views, outside arrangement views.

## Vertical bars

On the outer display, and on the inner display in landscape, the system moves the status bar, Dynamic Island, toolbar, navigation buttons, and tab bar into a vertical rail beside the content. The inner display in portrait keeps horizontal bars.

- Keep the default bar placement. The rail stays on the camera's physical edge, including in right-to-left languages, so content space is asymmetric; rely on safe areas.
- Order rail items from the top: primary navigation (Back, Close), then prominent actions such as Done. Keep existing toolbar groups intact and use the system grouping instead of manual spacing.
- Give every icon item both a title and a symbol. Text-only buttons stay in a horizontal bar, so minimize them.
- Items overflow from the bottom up. Set visibility priorities for groups first, then items, so frequent actions and status badges stay visible longest.
- Choose a compression behavior. Navigation-focused apps keep the tab bar and move toolbar items to overflow (the default); task-focused apps minimize the tab bar to keep actions available.
- Put your own overflow actions into the system overflow menu. Use the ellipsis only for overflow.
- Bar-less, immersive, non-scrolling screens may use the full display width if they stay clear of the Dynamic Island and status bar.

## Multitasking

In Split View on the inner display, each app places its controls on its outer edge. The width available to each app varies, so respect safe areas on both sides.

## Framework mapping

| Concern | SwiftUI | UIKit |
| --- | --- | --- |
| Avoid reserved areas | `ReservedRegion` | `UIView.ReservedRegion` |
| List and detail | `NavigationSplitView` | `UISplitViewController` |
| Two related views | `ArrangementView` | `UIArrangementViewController` |
| Toolbar groups | `ToolbarItemGroup` | `UIBarButtonItemGroup` |
| Overflow order | `ToolbarItemVisibilityPriority` | `UIBarButtonItemVisibilityPriority` |
| Rail compression | `ToolbarVerticalCompressionBehavior` | `UIVerticalBarCompressionBehavior` |
| System overflow menu | `ToolbarOverflowMenu` | `additionalOverflowItems` |

**React Native / Expo (SDK 58, iOS 27, Xcode 27.1):** prefer Expo Router `Stack` and `NativeTabs` so iOS places the bars and the rail. JS headers and custom tab bars render inside safe areas but do not follow the rail conventions. Pad content, not the scroll view, with left and right safe-area insets (the rail reserves about 84 pt), position floating views from `insets.left`/`insets.right`, and read `useWindowDimensions` at render time. Related packages: `<SplitView>` (experimental), `ArrangementView` from `@expo/ui/swift-ui`, `react-native-reserved-regions`, `expo-hinge`, and `verticalBarBehaviorIOS` on `expo-status-bar` for screens that must disable the rail. Source: [Expo — Supporting iPhone Duo](https://expo.dev/blog/supporting-iphone-duo), checked 2026-10-27.

## Verify

In the iPhone Duo simulator (Device Hub in Xcode 27.1), check: closed (nothing important under the rail), open in both orientations (no design switch, bars return in portrait), partially open (nothing needed in the fold), Split View (content clear of the rail on each window), folding with a screen open (scroll position, state, and pending actions persist), and a standard iPhone (unchanged).

Source: [Apple HIG — Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo). Checked 2026-10-27.
