# FilterBar Component

A slide-in filter panel for the article/news dashboard. Lets users search, sort, and filter articles by category, status, and priority.

## Overview

`FilterBar.vue` renders as an overlay panel anchored to the top-left of the viewport. It's fully controlled — all state (search text, sort order, selected category, status/priority checkboxes) lives in the parent component and is passed in via props, with changes communicated back up through emitted events.

## Props

| Prop | Type | Description |
|---|---|---|
| `isOpen` | `boolean` | Controls whether the panel is visible (drives the `v-if` + slide transition). |
| `search` | `string` | Current search query text. |
| `sort` | `string` | Current sort mode. One of `newest`, `collected`, `relevance`. |
| `category` | `string` | Currently selected category filter. |
| `status` | `string[]` | Currently selected status filters (multi-select). |
| `priority` | `string[]` | Currently selected priority filters (multi-select). |

## Emitted Events

| Event | Payload | Fired when |
|---|---|---|
| `update:search` | `string` | The search input changes. |
| `update:sort` | `string` | A new sort option is selected. |
| `update:category` | `string` | A category item is clicked. |
| `update:status` | `string[]` | A status checkbox is toggled. |
| `update:priority` | `string[]` | A priority checkbox is toggled. |
| `clear` | — | "Clear All Filters" is clicked. |
| `close` | — | The panel is closed (✕ button, clicking outside, or after Clear). |

This follows Vue's `v-model`-style convention, so a parent can bind each filter with `v-model:search`, `v-model:sort`, etc., or handle the events individually.

## Built-in Options

These are currently hardcoded inside the component:

- **Categories**: All Sources, Reuters, AP News, BBC, The Guardian, Bloomberg, Politico, Al Jazeera
- **Status**: Active, In Review, Blocked, Closed
- **Priority**: Critical, High, Medium, Low

## Behavior Notes

- **Status/Priority toggling**: `toggleStatus` and `togglePriority` add or remove a value from the respective array and emit the updated array — the parent owns the actual state.
- **Clear All Filters**: emits both `clear` (reset filter state) and `close` (dismiss the panel) in one action.
- **Transition**: wrapped in a `<Transition name="slide">` with a 0.25s ease slide/fade defined in the `<style>` block (`.slide-enter-*` / `.slide-leave-*`).
- **Click-outside to close**: the outer `.filter-overlay` div listens for `@click.self`, so clicking the dimmed backdrop area (not the panel itself) closes the filter bar.

## Usage Example

```vue
<FilterBar
  :is-open="showFilters"
  :search="searchQuery"
  :sort="sortBy"
  :category="selectedCategory"
  :status="selectedStatus"
  :priority="selectedPriority"
  @update:search="searchQuery = $event"
  @update:sort="sortBy = $event"
  @update:category="selectedCategory = $event"
  @update:status="selectedStatus = $event"
  @update:priority="selectedPriority = $event"
  @close="showFilters = false"
  @clear="clearAll"
/>
```

## Styling

- Font: `IBM Plex Mono`, monospace — panel uses a compact, technical/dashboard aesthetic.
- Panel is `position: absolute`, anchored `16px` from the left and `12px` from the top of its nearest positioned ancestor — the parent is responsible for providing a correctly positioned wrapper (e.g. `position: fixed` with an appropriate `top` offset) so the panel lands where intended.
- `z-index: 101` on `.filter-bar`, `z-index: 100` on `.filter-overlay` — keep these above your app's other overlay/z-index layers if you have any.
- Note: `.filter-backdrop` styles are defined in this file but the class isn't actually used in the template — the dimmed backdrop is instead handled by the parent (`App.vue`'s `.filter-overlay::before`).

## Known Gotchas

- The component's own `.filter-overlay` wrapper duplicates the class name used in the parent (`App.vue`). Because styles are `scoped`, this doesn't cause a CSS collision, but it does mean two nested elements share the same class name in the DOM — worth renaming one if it causes confusion during debugging.
- Panel positioning is relative to its nearest positioned ancestor, not the viewport — if the panel appears in the wrong place or off-screen, check the parent's overlay wrapper's `position` and `top` values first.