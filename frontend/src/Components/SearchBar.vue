<template>
  <div class="search-wrapper">
    <div class="top-header">
      <div class="header-left">
        <div class="brand">
          <span class="brand-orange">MISCELLANEOUS</span
          ><span class="brand-muted">COLLECTION INDEX</span>
        </div>
        <div class="v-divider"></div>
        <div class="meta-small">
          <span>{{ count }} items</span>
          <button
            class="bookmark-btn"
            :class="{ active: internalBookmarkedOnly }"
            @click="toggleBookmarks"
            type="button"
          >
            {{ bookmarkedTotal }} BOOKMARKS
          </button>
          <span class="muted">LAST SYNC: {{ syncTime }} • LIVE</span>
        </div>
      </div>
      <div class="header-right">
        <span class="live-dot"
          ><span class="dot"></span>{{ sourcesCount ?? 8 }} sources</span
        >
        <span class="link" @click="emit('export', 'csv')">Export</span>
      </div>
    </div>

    <div class="search-bar">
      <button
        class="filter-trigger-btn"
        :class="{ active: showFilters }"
        @click="emit('toggle-filters')"
        type="button"
      >
        <svg
          width="14"
          height="14"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
        >
          <path d="M3 6h18M6 12h12M10 18h4" />
        </svg>
        FILTERS <span v-if="hasActiveFilters" class="active-dot"></span>
      </button>
      <div class="search-box">
        <div class="search-input-wrap">
          <span>⌕</span
          ><input
            :value="internalSearch"
            @input="handleSearchInput"
            type="text"
            placeholder="Search headlines, summaries, sources, tags, bookmarks..."
          />
        </div>
        <button class="btn-black" type="button" @click="handleSearch">
          SEARCH
        </button>
      </div>
      <div class="search-actions">
        <button
          v-if="internalSearch || hasActiveFilters || internalBookmarkedOnly"
          class="btn-clear"
          @click="clearAll"
          type="button"
        >
          CLEAR ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed } from "vue";

const props = defineProps<{
  count?: number;
  bookmarkedTotal?: number;
  syncTime?: string;
  search?: string;
  bookmarkedOnly?: boolean;
  sort?: string;
  showFilters?: boolean;
  hasActiveFilters?: boolean;
  sourcesCount?: number;
}>();

const emit = defineEmits([
  "update:search",
  "update:bookmarkedOnly",
  "update:sort",
  "toggle-filters",
  "clear",
  "export",
  "filter-change", // emits both search + bookmarkedOnly together
]);

// Internal state - can be controlled or uncontrolled
const internalSearch = ref(props.search ?? "");
const internalBookmarkedOnly = ref(props.bookmarkedOnly ?? false);

// Sync with parent if parent passes props
watch(
  () => props.search,
  (val) => {
    if (val !== undefined) internalSearch.value = val;
  },
);

watch(
  () => props.bookmarkedOnly,
  (val) => {
    if (val !== undefined) internalBookmarkedOnly.value = val;
  },
);

// Check if "bookmarks" is typed in search
const searchIsBookmarks = computed(() => {
  const q = internalSearch.value.toLowerCase().trim();
  return q === "bookmarks" || q === "bookmark";
});

function toggleBookmarks() {
  internalBookmarkedOnly.value = !internalBookmarkedOnly.value;
  emit("update:bookmarkedOnly", internalBookmarkedOnly.value);
  emitFilterChange();
}

function handleSearchInput(e: Event) {
  const val = (e.target as HTMLInputElement).value;
  internalSearch.value = val;
  emit("update:search", val);

  // If user types "bookmarks", auto-toggle the button
  if (searchIsBookmarks.value && !internalBookmarkedOnly.value) {
    internalBookmarkedOnly.value = true;
    emit("update:bookmarkedOnly", true);
  }
  // If user clears "bookmarks" keyword, untoggle
  else if (
    !searchIsBookmarks.value &&
    internalBookmarkedOnly.value &&
    props.search === "bookmarks"
  ) {
    internalBookmarkedOnly.value = false;
    emit("update:bookmarkedOnly", false);
  }

  emitFilterChange();
}

function handleSearch() {
  emitFilterChange();
}

function clearAll() {
  internalSearch.value = "";
  internalBookmarkedOnly.value = false;
  emit("update:search", "");
  emit("update:bookmarkedOnly", false);
  emit("clear");
  emitFilterChange();
}

function emitFilterChange() {
  emit("filter-change", {
    search: internalSearch.value,
    bookmarkedOnly: internalBookmarkedOnly.value || searchIsBookmarks.value,
  });
}
</script>

<style scoped>
.search-wrapper {
  position: sticky;
  top: 0;
  z-index: 60;
  background: #fefefd;
  border-bottom: 1px solid #111;
}
.top-header {
  height: 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: #fefefd;
  font-family: "IBM Plex Mono", monospace;
  border-bottom: 1px solid #e5e2de;
}
.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand {
  display: flex;
  gap: 0;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  border: 1.5px solid #111;
}
.brand-orange {
  background: #ff5a1f;
  color: #111;
  padding: 3px 6px;
}
.brand-muted {
  color: #111;
  background: #fff;
  padding: 4px 8px;
}
.v-divider {
  width: 1px;
  height: 14px;
  background: #e5e2de;
}
.meta-small {
  display: flex;
  gap: 6px;
  font-size: 9px;
  color: #666;
  align-items: center;
}
.bookmark-btn {
  color: #111;
  cursor: pointer;
  background: #fff;
  border: 1.5px solid #111;
  padding: 3px 8px;
  font-weight: 700;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  text-transform: uppercase;
  transition: all 0.15s ease;
  line-height: 1;
}
.bookmark-btn:hover {
  background: #111;
  color: #fff;
}
.bookmark-btn.active {
  background: #3b82f6;
  color: #fff;
  border-color: #3b82f6;
}
.bookmark-btn.active:hover {
  background: #2563eb;
  border-color: #2563eb;
}
.muted {
  color: #aaa;
}
.header-right {
  gap: 16px;
  font-size: 9px;
  color: #999;
  text-transform: uppercase;
}
.live-dot {
  display: flex;
  align-items: center;
  gap: 5px;
}
.dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border: 1px solid #111;
}
.link {
  cursor: pointer;
  text-decoration: underline;
}
.link:hover {
  color: #111;
}
.search-bar {
  padding: 14px 16px;
  display: flex;
  gap: 12px;
  align-items: center;
  background: #fefefd;
  width: 100%;
}
.filter-trigger-btn {
  height: 38px;
  padding: 0 14px;
  border: 1.5px solid #111;
  background: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  flex-shrink: 0;
}
.filter-trigger-btn:hover,
.filter-trigger-btn.active {
  background: #111;
  color: #fff;
}
.active-dot {
  width: 6px;
  height: 6px;
  background: #ff5a1f;
  border-radius: 50%;
}
.search-box {
  flex: 1;
  display: flex;
  height: 38px;
  border: 1.5px solid #111;
  background: #fff;
  min-width: 0;
}
.search-input-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 0 14px;
  gap: 10px;
  min-width: 0;
}
.search-input-wrap input {
  flex: 1;
  border: none;
  outline: none;
  font-family: "IBM Plex Mono", monospace;
  font-size: 12px;
  background: transparent;
  min-width: 0;
}
.btn-black {
  background: #111;
  color: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 600;
  padding: 0 22px;
  border: none;
  cursor: pointer;
  border-left: 4px solid #ff5a1f;
  flex-shrink: 0;
}
.search-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}
.btn-clear {
  height: 38px;
  padding: 0 10px;
  border: 1.5px solid #111;
  background: #facc15;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
}
.btn-clear:hover {
  background: #eab308;
}
.search-wrapper {
  position: sticky;
  top: 0;
  z-index: 60;
  background: #fefefd;
  border-bottom: 1px solid #111;
}
.top-header {
  height: 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: #fefefd;
  font-family: "IBM Plex Mono", monospace;
  border-bottom: 1px solid #e5e2de;
}
.header-left,
.header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand {
  display: flex;
  gap: 0;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.08em;
  border: 1.5px solid #111;
}
.brand-orange {
  background: #ff5a1f;
  color: #111;
  padding: 3px 6px;
}
.brand-muted {
  color: #111;
  background: #fff;
  padding: 4px 8px;
}
.v-divider {
  width: 1px;
  height: 14px;
  background: #e5e2de;
}
.meta-small {
  display: flex;
  gap: 6px;
  font-size: 9px;
  color: #666;
  align-items: center;
}
.flagged-btn {
  color: #111;
  cursor: pointer;
  opacity: 0.8;
  background: #facc15;
  border: 1px solid #111;
  padding: 2px 6px;
  font-weight: 700;
}
.flagged-btn.active {
  background: #ef4444;
  color: #fff;
}
.muted {
  color: #aaa;
}
.header-right {
  gap: 20px;
  font-size: 9px;
  color: #999;
  text-transform: uppercase;
}
.live-dot {
  display: flex;
  align-items: center;
  gap: 5px;
}
.dot {
  width: 8px;
  height: 8px;
  background: #22c55e;
  border: 1px solid #111;
}
.search-bar {
  padding: 14px 16px;
  display: flex;
  gap: 12px;
  align-items: center;
  background: #fefefd;
  width: 100%;
}
.filter-trigger-btn {
  height: 38px;
  padding: 0 14px;
  border: 1.5px solid #111;
  background: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  flex-shrink: 0;
}
.filter-trigger-btn:hover,
.filter-trigger-btn.active {
  background: #111;
  color: #fff;
}
.active-dot {
  width: 6px;
  height: 6px;
  background: #ff5a1f;
  border-radius: 50%;
}
.search-box {
  flex: 1;
  display: flex;
  height: 38px;
  border: 1.5px solid #111;
  background: #fff;
  min-width: 0;
}
.search-input-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 0 14px;
  gap: 10px;
  min-width: 0;
}
.search-input-wrap input {
  flex: 1;
  border: none;
  outline: none;
  font-family: "IBM Plex Mono", monospace;
  font-size: 12px;
  background: transparent;
  min-width: 0;
}
.btn-black {
  background: #111;
  color: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 600;
  padding: 0 22px;
  border: none;
  cursor: pointer;
  border-left: 4px solid #ff5a1f;
  flex-shrink: 0;
}
.search-actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-shrink: 0;
}
.btn-clear {
  height: 38px;
  padding: 0 10px;
  border: 1.5px solid #111;
  background: #facc15;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  cursor: pointer;
}
.link {
  color: #111;
  cursor: pointer;
  opacity: 0.8;
  background: #facc15;
  border: 1px solid #111;
  padding: 7px;
  font-weight: 700;
}
</style>
