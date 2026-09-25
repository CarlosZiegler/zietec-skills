# iOS Implementation and Review

Use this reference for an actual iPhone screen, flow, or implementation. These are author-created review procedures informed by the linked HIG topics, not an Apple certification checklist.

## Define the interaction

Identify the primary task, the content it operates on, and the expected result. Separate app destinations from commands and local choices. Preserve navigation state when switching destinations, returning from a detail, or reopening the app.

Read [Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars), [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars), and [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields) when deciding those structures. Verify current platform sections before prescribing the location of search or the appearance of navigation.

## Specify meaningful states

For each state that the feature can actually enter, define visible content, available actions, and the way out. Include loading, empty, partial, error, success, and permission-denied states as relevant. Preserve entered data when an operation fails. Avoid inventing states for services the product does not use.

Read [Loading](https://developer.apple.com/design/human-interface-guidelines/loading), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback), and [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) for the corresponding decisions.

## Check adaptation

| Context | Observable question |
| --- | --- |
| Smaller screen or landscape | Are content, navigation, and important actions still available? |
| Accessibility text sizes | Does the layout reflow while preserving essential text and actions? |
| Light, dark, and increased contrast | Are text, symbols, and states distinguishable over actual content? |
| Keyboard shown or dismissed | Can people reach the active field, validation message, and next action? |
| VoiceOver or alternate input | Can someone complete the task and understand its result? |
| Background and return | Is the correct context restored, with truthful operation state? |
| Long translation or RTL | Do labels fit and directional relationships retain their meaning? |

Use [Layout](https://developer.apple.com/design/human-interface-guidelines/layout), [Typography](https://developer.apple.com/design/human-interface-guidelines/typography), [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), and [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) for platform-specific recommendations, including exact target and text-size guidance.

## Implement and report

Keep the chosen framework and deployment target. Map system semantics into that framework, use native components when appropriate, and verify SDK availability for new APIs or symbols. In current material design, distinguish controls and navigation from content; consult [Materials](https://developer.apple.com/design/human-interface-guidelines/materials) before adding glass effects.

Validate the changed task using the environment actually available. Report observed behavior, the smallest remaining risks, and any checks that still require a real device. Do not claim accessibility, performance, or HIG compliance solely from a screenshot or a successful compilation.
