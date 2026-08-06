<template>
  <div class="page-root">
    <!-- ==================== DASHBOARD (FIRST) ==================== -->
    <div class="dashboard-section">
      <Header />

      <main class="dashboard">
        <Cards />
        <section class="charts-row">
          <Charts />
          <EngagementChart />
        </section>
        <section class="bottom-row">
          <WebsiteManager />
          <Insights />
          <ProvinceTable />
        </section>
      </main>
    </div>

    <!-- ==================== COLLECTION (SECOND, SAME PAGE) ==================== -->
    <div class="app-root">
      <SearchBar
        :count="filteredCount"
        :bookmarked-total="bookmarkedTotal"
        :bookmarked-only="bookmarkedOnly"
        :sync-time="syncTime"
        :search="searchQuery"
        :show-filters="showFilters"
        :has-active-filters="hasActiveFilters"
        :sources-count="uniqueSources"
        @update:search="searchQuery = $event"
        @update:bookmarked-only="bookmarkedOnly = $event"
        @toggle-filters="showFilters = !showFilters"
        @clear="clearAll"
        @export="handleExport"
        @filter-change="handleFilterChange"
      />

      <div class="main-layout">
        <div
          v-if="showFilters"
          class="collection-filter-wrapper"
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
          :status="selectedStatus"
          :priority="selectedPriority"
          :bookmarked-only="bookmarkedOnly"
          @update:count="handleCountUpdate"
          @search-tag="searchQuery = $event"
        />
      </div>

      <div class="footer">
        <div class="footer-left">
          <span class="live">
            <span class="dot"></span>LIVE COLLECTION ACTIVE
          </span>
          <span>
            {{ filteredCount }} articles • {{ uniqueSources }} sources •
            {{ bookmarkedCount }} bookmarked
          </span>
        </div>
        <div>Miscellaneous v0.4.1 © 2026</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import api from "./services/api";
import WebsiteManager from "./Components/WebsiteManager.vue";
import SearchBar from "./Components/SearchBar.vue";
import ArticleGrid from "./Components/ArticleGrid.vue";
import Header from "./Components/Header.vue";
import Cards from "./Components/Cards.vue";
import Charts from "./Components/Charts.vue";
import EngagementChart from "./Components/EngagementChart.vue";
import Insights from "./Components/Insights.vue";
import ProvinceTable from "./Components/ProvinceTable.vue";
import FilterBar from "./Components/FilterBar.vue";

interface CountPayload {
  count?: number;
  bookmarked?: number;
  sources?: number;
  totalBookmarked?: number;
}

const showFilters = ref(false);
const searchQuery = ref("");
const sortBy = ref("newest");
const selectedCategory = ref("All Sources");
const selectedStatus = ref<string[]>([]);
const selectedPriority = ref<string[]>([]);
const bookmarkedOnly = ref(false);
const syncTime = ref("09:22");

const filteredCount = ref(8);
const bookmarkedCount = ref(3);
const uniqueSources = ref(8);
const bookmarkedTotal = ref(3);

const hasActiveFilters = computed(
  () =>
    selectedCategory.value !== "All Sources" ||
    selectedStatus.value.length > 0 ||
    selectedPriority.value.length > 0 ||
    bookmarkedOnly.value ||
    searchQuery.value.trim().length > 0,
);

function handleCountUpdate(payload: number | CountPayload) {
  if (typeof payload === "number") {
    filteredCount.value = payload;
  } else if (payload && typeof payload === "object") {
    filteredCount.value = payload.count ?? filteredCount.value;
    bookmarkedCount.value = payload.bookmarked ?? bookmarkedCount.value;
    uniqueSources.value = payload.sources ?? uniqueSources.value;
    if (payload.totalBookmarked !== undefined)
      bookmarkedTotal.value = payload.totalBookmarked;
  }
}

function handleFilterChange(payload: {
  search: string;
  bookmarkedOnly: boolean;
}) {
  searchQuery.value = payload.search;
  bookmarkedOnly.value = payload.bookmarkedOnly;
}

function clearAll() {
  searchQuery.value = "";
  selectedCategory.value = "All Sources";
  selectedStatus.value = [];
  selectedPriority.value = [];
  bookmarkedOnly.value = false;
  showFilters.value = false;
}

async function handleExport(format: string) {
  try {
    // Pass current filters to API so export matches what's filtered
    const params = new URLSearchParams({
      search: searchQuery.value,
      sort: sortBy.value,
      category: selectedCategory.value,
      bookmarkedOnly: String(bookmarkedOnly.value),
    });

    if (selectedStatus.value.length)
      params.append("status", selectedStatus.value.join(","));
    if (selectedPriority.value.length)
      params.append("priority", selectedPriority.value.join(","));

    const { data } = await api.get(`/items?${params.toString()}`);
    const articles = data.items;

    if (!articles || articles.length === 0) return;

    let blob: Blob;
    if (format === "csv") {
      const header = Object.keys(articles[0]).join(",");
      const rows = articles.map((a: Record<string, unknown>) =>
        Object.values(a)
          .map((v) => `"${String(v).replace(/"/g, '""')}"`)
          .join(","),
      );
      blob = new Blob([header + "\n" + rows.join("\n")], { type: "text/csv" });
    } else {
      blob = new Blob([JSON.stringify(articles, null, 2)], {
        type: "application/json",
      });
    }

    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `articles.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  } catch (err) {
    console.error("Export failed:", err);
  }
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

.charts-row {
  display: flex;
  gap: 20px;
  padding: 20px;
  align-items: stretch;
}

.charts-row > * {
  flex: 1 1 50%;
  min-width: 450px;
}

.bottom-row {
  display: flex;
  gap: 20px;
  padding: 20px;
  align-items: stretch;
}

.bottom-row > * {
  flex: 1 1 33.333%;
  min-width: 380px;
}

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

.collection-filter-wrapper {
  position: fixed;
  inset: 0;
  top: 84px; /* SearchBar height: 36px + 38px + padding */
  z-index: 100;
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
  /* Fixed: added space */
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
}

/* ================= MOBILE ================= */
@media (max-width: 768px) {

  *{
    box-sizing:border-box;
  }

  .page-root{
    width:100%;
    overflow-x:hidden;
  }

  .dashboard{
    padding:10px;
  }

  .charts-row,
  .bottom-row{
    display:flex;
    flex-direction:column;
    gap:15px;
    padding:10px;
  }

  .charts-row>*,
  .bottom-row>*{
    width:100%;
    min-width:0;
    flex:none;
  }

  .main-layout{
    display:block;
    width:100%;
  }

  .app-root{
    overflow-x:hidden;
  }

  .footer{
    flex-direction:column;
    align-items:flex-start;
    gap:8px;
    height:auto;
    padding:10px;
  }

  img,
  canvas{
    max-width:100%;
    height:auto;
  }

}
</style>
