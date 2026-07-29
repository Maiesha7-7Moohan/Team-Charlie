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
          <span
            class="flagged-btn"
            :class="{ active: flaggedOnly }"
            @click="emit('toggle-flagged')"
            >● {{ flaggedTotal }} flagged</span
          >
          <span class="muted">LAST SYNC: {{ syncTime }} • LIVE</span>
        </div>
      </div>
      <div class="header-right">
        <span class="live-dot"><span class="dot"></span>8 sources</span
        ><span class="link">Export</span>
      </div>
    </div>

    <div class="search-bar">
      <button
        class="filter-trigger-btn"
        :class="{ active: showFilters }"
        @click="emit('toggle-filters')"
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
            :value="search"
            @input="
              emit('update:search', ($event.target as HTMLInputElement).value)
            "
            type="text"
            placeholder="Search headlines, summaries, sources, tags..."
          />
        </div>
        <button class="btn-black">SEARCH</button>
      </div>
      <div class="search-actions">
        <button
          v-if="search || hasActiveFilters"
          class="btn-clear"
          @click="emit('clear')"
        >
          CLEAR ✕
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  count?: number;
  flaggedTotal?: number;
  flaggedOnly?: boolean;
  syncTime?: string;
  search?: string;
  sort?: string;
  showFilters?: boolean;
  hasActiveFilters?: boolean;
}>();
const emit = defineEmits([
  "update:search",
  "update:sort",
  "toggle-filters",
  "toggle-flagged",
  "clear",
]);
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
<<<<<<< HEAD
  background: linear-gradient(90deg, #2d5bff 36%);
=======
  background: linear-gradient(
    90deg,
    #ff5a1f 0%,
    #ff5a1f 18%,
    #2d5bff 18%,
    #2d5bff 36%,
    #22c55e 36%,
    #22c55e 54%,
    #7c3aed 54%,
    #7c3aed 72%,
    #facc15 72%,
    #facc15 100%
  );
>>>>>>> ce16e9e0d48e69b6de39ed309f6c7028e2ec0e47
  color: #fff;
  padding: 4px 8px;
  text-shadow: 0 1px 0 rgba(0, 0, 0, 0.3);
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
.search-actions select {
  height: 38px;
  border: 1.5px solid #e5e2de;
  background: #fff;
  padding: 0 12px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
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
</style>
