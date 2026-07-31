<script setup>
import { ref, onMounted } from "vue";
import api from "./services/api";

const articles = ref([]);

onMounted(async () => {
  try {
    const response = await api.get("/items");
    articles.value = response.data;
  } catch (error) {
    console.error("Failed to load articles:", error);
  }
});
</script>

<template>
  <div class="container">
    <h1>Team Charlie News</h1>

    <div v-if="articles.length === 0">
      <p>No articles available.</p>
    </div>

    <div v-else>
      <div
        v-for="article in articles"
        :key="article.id"
        class="article"
      >
        <h2>{{ article.title }}</h2>

        <p><strong>Author:</strong> {{ article.author }}</p>

        <p><strong>Source:</strong> {{ article.source }}</p>

        <p><strong>Date:</strong> {{ article.date }}</p>

        <p>{{ article.summary }}</p>

        <hr>
<template>
  <div class="page-root">
    <!-- ==================== DASHBOARD (FIRST) ==================== -->
    <div class="dashboard-section">
      <Header />

      <main class="dashboard">
        <!-- Statistics Cards -->
        <Cards />

        <!-- Charts -->
        <section class="charts-row">
          <Charts />
          <EngagementChart />
        </section>

        <!-- Bottom Section -->
        <section class="bottom-row">
          <Insights />
          <ProvinceTable />
        </section>
      </main>
    </div>

    <!-- ==================== COLLECTION (SECOND, SAME PAGE) ==================== -->
    <div class="app-root">
      <SearchBar
        :count="filteredCount"
        :flagged-total="flaggedTotal"
        :flagged-only="flaggedOnly"
        :sync-time="syncTime"
        :search="searchQuery"
        :sort="sortBy"
        :show-filters="showFilters"
        :has-active-filters="hasActiveFilters"
        @update:search="searchQuery = $event"
        @update:sort="sortBy = $event"
        @toggle-filters="showFilters = !showFilters"
        @toggle-flagged="flaggedOnly = !flaggedOnly"
        @clear="clearAll"
      />

      <div class="main-layout">
        <div
          v-if="showFilters"
          class="filter-overlay"
          @click.self="showFilters = false"
        >
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
        </div>

        <ArticleGrid
          :search="searchQuery"
          :sort="sortBy"
          :category="selectedCategory"
          :flagged-only="flaggedOnly"
          @update:count="handleCountUpdate"
          @search-tag="searchQuery = $event"
        />
      </div>

      <div class="footer">
        <div class="footer-left">
          <span class="live"
            ><span class="dot"></span>LIVE COLLECTION ACTIVE</span
          ><span
            >{{ filteredCount }} articles • {{ uniqueSources }} sources •
            {{ flaggedCount }} flagged</span
          >
        </div>
        <div>Miscellaneous v0.4.1 © 2026</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.article {
  margin-bottom: 20px;
}
</style>
<script setup lang="ts">
import { ref, computed } from "vue";
import SearchBar from "./Components/SearchBar.vue";
import ArticleGrid from "./Components/ArticleGrid.vue";
import Header from "./Components/Header.vue";
import Cards from "./Components/Cards.vue";
import Charts from "./Components/Charts.vue";
import EngagementChart from "./Components/EngagementChart.vue";
import Insights from "./Components/Insights.vue";
import ProvinceTable from "./Components/ProvinceTable.vue";

const showFilters = ref(false);
const searchQuery = ref("");
const sortBy = ref("newest");
const selectedCategory = ref("All Sources");
const selectedStatus = ref<string[]>([]);
const selectedPriority = ref<string[]>([]);
const flaggedOnly = ref(false);
const syncTime = ref("09:22");

const filteredCount = ref(8);
const flaggedCount = ref(3);
const uniqueSources = ref(8);
const flaggedTotal = ref(3);

const hasActiveFilters = computed(
  () =>
    selectedCategory.value !== "All Sources" ||
    selectedStatus.value.length > 0 ||
    flaggedOnly.value,
);

function handleCountUpdate(payload: any) {
  if (typeof payload === "number") {
    filteredCount.value = payload;
  } else if (payload && typeof payload === "object") {
    filteredCount.value = payload.count ?? filteredCount.value;
    flaggedCount.value = payload.flagged ?? flaggedCount.value;
    uniqueSources.value = payload.sources ?? uniqueSources.value;
    if (payload.totalFlagged !== undefined)
      flaggedTotal.value = payload.totalFlagged;
  }
}

function clearAll() {
  searchQuery.value = "";
  selectedCategory.value = "All Sources";
  selectedStatus.value = [];
  selectedPriority.value = [];
  flaggedOnly.value = false;
  showFilters.value = false;
}
</script>

<style scoped>
.page-root {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-section {
  background: #ffffff;
  width: 100%;
}
.dashboard {
  padding: 0;
  background: #fff;
}
.dashboard-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: stretch;
}
.charts-row {
  display: flex;
  gap: 20px;
  padding: 0 20px;
  flex-wrap: wrap;
}
.charts-row > * {
  flex: 1;
}
.bottom-row {
  display: flex;
  gap: 20px;
  padding: 0 20px 20px 20px;
  flex-wrap: wrap;
}
.bottom-row > * {
  flex: 1;
}

/* --- Collection Section --- Keeps original look --- */
.app-root {
  background: #f7f7f5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  color: #111827;
  font-family: "Inter", sans-serif;
}
.main-layout {
  display: flex;
  flex: 1;
  align-items: stretch;
  position: relative;
}
.filter-overlay {
  position: fixed;
  inset: 0;
  top: 84px;
  z-index: 100;
  pointer-events: none;
}
.filter-overlay::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(3px);
  pointer-events: auto;
}
.filter-overlay :deep(.filter-bar) {
  pointer-events: auto;
}
.footer {
  height: 28px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  background: #111;
  color: #888;
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.footer-left {
  display: flex;
  gap: 12px;
  align-items: center;
}
.live {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #aaa;
}
.live .dot {
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
}
</style>
