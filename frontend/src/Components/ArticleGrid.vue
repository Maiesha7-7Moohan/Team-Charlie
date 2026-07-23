<template>
  <div class="grid-wrapper">
    <div class="grid">
      <div
        v-for="a in filteredArticles"
        :key="a.id"
        class="card"
        @click="openArticle(a)"
      >
        <div v-if="a.flagged" class="flag-line"></div>
        <div class="card-top">
          <div class="card-source">
            <span class="src">{{ a.source }}</span
            ><span class="author">| {{ a.author }}</span
            ><span v-if="a.flagged" class="flag-badge">FLAGGED</span>
          </div>
          <div class="card-badges">
            <span class="badge" :style="a.badgeStyle">{{ a.badge }}</span
            ><span class="open-btn">↗</span>
          </div>
        </div>
        <div class="card-title">{{ a.title }}</div>
        <div class="card-summary">{{ a.summary }}</div>
        <div class="card-tags">
          <span
            v-for="tag in a.tags"
            :key="tag.t"
            class="tag"
            :style="tag.s"
            @click.stop="emit('search-tag', tag.t)"
            >{{ tag.t }}</span
          >
        </div>
        <div class="card-foot">
          <div class="foot-labels">
            <span>RELEVANCE</span><span>WORDS</span
            ><span class="ml-auto">COLLECTED</span>
          </div>
          <div class="foot-values">
            <div class="relevance">
              <div class="bar">
                <div :style="{ width: a.relevance + '%' }"></div>
              </div>
              <span>{{ a.relevance }}</span>
            </div>
            <span>{{ a.words.toLocaleString() }}</span
            ><span class="collected">{{ a.collected }}</span>
          </div>
          <div class="collection-label" :style="{ color: a.color }">
            <div class="sq" :style="{ background: a.color }"></div>
            {{ a.collection }}
          </div>
        </div>
      </div>
      <div class="add-card">+ Add source</div>
    </div>

    <!-- CLICKABLE MODAL BACK -->
    <div v-if="selected" class="modal" @click.self="selected = null">
      <div class="modal-content">
        <div class="modal-head">
          <div class="card-source">
            <span class="src">{{ selected.source }}</span
            ><span class="author">| {{ selected.author }}</span>
          </div>
          <span class="close" @click="selected = null">✕</span>
        </div>
        <h1 class="modal-title">{{ selected.title }}</h1>
        <p class="modal-summary">{{ selected.summary }}</p>
        <div class="modal-meta">
          RELEVANCE: <b>{{ selected.relevance }}</b> WORDS:
          <b>{{ selected.words }}</b>
          <span class="ml-auto muted">{{ selected.collected }}</span>
        </div>
        <div class="modal-actions">
          <button class="btn-black large">OPEN FULL ARTICLE ↗</button
          ><button class="btn-outline">FLAG</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";

const props = defineProps<{
  search: string;
  sort: string;
  category: string;
  flaggedOnly: boolean;
}>();
const emit = defineEmits(["search-tag", "update:count"]);

const selected = ref<any>(null);

const articles = ref([
  {
    id: 1,
    source: "REUTERS",
    author: "Sarah Chen",
    badge: "WIRE",
    badgeStyle: "background:#111;color:#fff;",
    title:
      "Central banks signal coordinated pause as inflation data diverges across G7 economies",
    summary:
      "Fed, ECB, and Bank of England officials have all indicated rates will hold through Q3 as diverging CPI readings complicate a unified policy path.",
    tags: [{ t: "MONETARY POLICY", s: "background:#E8E6E3;" }],
    relevance: 84,
    words: 847,
    collected: "2026-07-21 09:22",
    collection: "MACRO WATCH",
    flagged: true,
    color: "#FF5A1F",
    category: "Reuters",
  },
  {
    id: 2,
    source: "POLITICO",
    author: "Mark Ostrowski",
    badge: "ARTICLE",
    badgeStyle: "border:1px solid #E5E2DE;color:#999;",
    title:
      "Pentagon confirms deployment of additional electronic warfare units to eastern European bases",
    summary: "Three additional EW battalions will be pre-positioned.",
    tags: [{ t: "NATO", s: "background:#E8E6E3;" }],
    relevance: 89,
    words: 1203,
    collected: "2026-07-21 09:01",
    collection: "SECURITY DESK",
    flagged: true,
    color: "#FF5A1F",
    category: "Politico",
  },
  {
    id: 3,
    source: "BLOOMBERG",
    author: "Claire Dubois",
    badge: "ARTICLE",
    badgeStyle: "border:1px solid #E5E2DE;color:#999;",
    title: "OpenAI competitor Mistral raises €600m at €6bn valuation",
    summary: "The Series C round was led by General Atlantic.",
    tags: [{ t: "AI", s: "background:#E8E6E3;" }],
    relevance: 91,
    words: 689,
    collected: "2026-07-21 07:55",
    collection: "AI MONITOR",
    flagged: false,
    color: "#111",
    category: "Bloomberg",
  },
  {
    id: 4,
    source: "THE GUARDIAN",
    author: "Priya Subramaniam",
    badge: "ANALYSIS",
    badgeStyle: "border:1px solid #E5E2DE;color:#999;",
    title:
      "Arctic ice extent hits record July low as Greenland melt accelerates",
    summary: "July sea-ice extent is 340,000 km² below the previous record.",
    tags: [{ t: "ARCTIC", s: "background:#BFEFFF;" }],
    relevance: 79,
    words: 1104,
    collected: "2026-07-20 18:44",
    collection: "CLIMATE TRACKER",
    flagged: false,
    color: "#111",
    category: "The Guardian",
  },
  {
    id: 5,
    source: "AP NEWS",
    author: "James Patel",
    badge: "WIRE",
    badgeStyle: "background:#111;color:#fff;",
    title: "WHO declares mpox variant clade Ib a public health emergency",
    summary: "The emergency declaration triggers accelerated vaccine-sharing.",
    tags: [{ t: "WHO", s: "background:#E8E6E3;" }],
    relevance: 90,
    words: 512,
    collected: "2026-07-20 15:31",
    collection: "HEALTH WATCH",
    flagged: true,
    color: "#FF5A1F",
    category: "AP News",
  },
  {
    id: 6,
    source: "BBC",
    author: "Asha Krishnamurthy",
    badge: "ANALYSIS",
    badgeStyle: "border:1px solid #E5E2DE;color:#999;",
    title: "India's ruling coalition faces internal rupture over caste census",
    summary: "Two regional coalition partners have threatened to withdraw.",
    tags: [{ t: "INDIA", s: "background:#E8E6E3;" }],
    relevance: 82,
    words: 1768,
    collected: "2026-07-20 12:20",
    collection: "ASIA POLITICS",
    flagged: false,
    color: "#111",
    category: "BBC",
  },
  {
    id: 7,
    source: "REUTERS",
    author: "Kevin Wu",
    badge: "WIRE",
    badgeStyle: "border:1px solid #E5E2DE;color:#999;",
    title: "Taiwan Semiconductor expands Arizona fab to 2nm",
    summary: "TSMC confirmed a $12bn expansion.",
    tags: [{ t: "TSMC", s: "background:#FF5A1F;color:#111;" }],
    relevance: 87,
    words: 634,
    collected: "2026-07-20 11:02",
    collection: "SUPPLY CHAIN",
    flagged: false,
    color: "#111",
    category: "Reuters",
  },
  {
    id: 8,
    source: "AL JAZEERA",
    author: "Nadia Petrova",
    badge: "REPORT",
    badgeStyle: "background:#FFF0E8;color:#CC5A2A;border:1px solid #FFD1C0;",
    title: "Russian state media amplifies unverified claims ahead of UN vote",
    summary:
      "Several Telegram channels with links to RT amplified disputed figures.",
    tags: [{ t: "RUSSIA", s: "background:#FF5A1F;color:#111;" }],
    relevance: 73,
    words: 1456,
    collected: "2026-07-20 09:35",
    collection: "DISINFO DESK",
    flagged: false,
    color: "#111",
    category: "Al Jazeera",
  },
]);

const filteredArticles = computed(() => {
  let list = articles.value.filter((a) => {
    if (props.flaggedOnly && !a.flagged) return false;
    if (props.category !== "All Sources" && a.category !== props.category)
      return false;
    if (props.search) {
      const q = props.search.toLowerCase();
      if (!`${a.title} ${a.summary} ${a.source}`.toLowerCase().includes(q))
        return false;
    }
    return true;
  });
  if (props.sort === "relevance")
    list.sort((a, b) => b.relevance - a.relevance);
  else if (props.sort === "words") list.sort((a, b) => b.words - a.words);
  else
    list.sort(
      (a, b) =>
        new Date(b.collected).getTime() - new Date(a.collected).getTime(),
    );
  return list;
});

function openArticle(a: any) {
  selected.value = a;
}

// update parent footer counts
watch(
  filteredArticles,
  (list) => {
    // @ts-ignore - emit counts for footer
    emit("update:count", list.length);
  },
  { immediate: true },
);
</script>

<style scoped>
.grid-wrapper {
  flex: 1;
  background: #f7f7f5;
  padding: 16px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 12px; /* TINY SPACE BETWEEN CARDS - FIXED */
  align-content: start;
}
.card {
  background: #fefefd;
  border: 1px solid #e8e3de;
  padding: 16px 16px 12px;
  display: flex;
  flex-direction: column;
  min-height: 260px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.18s ease;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  z-index: 2;
}
.flag-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: #ff5a1f;
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  flex-shrink: 0;
}
.card-source {
  display: flex;
  gap: 8px;
  align-items: center;
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.src {
  font-weight: 800;
  color: #111;
  font-size: 9px;
}
.author {
  color: #999;
}
.flag-badge {
  background: #ff5a1f;
  color: #111;
  padding: 1px 4px;
  font-weight: 700;
  font-size: 7px;
}
.card-badges {
  display: flex;
  gap: 4px;
  align-items: center;
}
.badge {
  font-family: "IBM Plex Mono", monospace;
  font-size: 7px;
  padding: 2px 5px;
}
.open-btn {
  font-size: 11px;
  color: #999;
  border: 1px solid #e5e2de;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.card-title {
  font-size: 13.5px;
  font-weight: 700;
  line-height: 1.28;
  min-height: 51.8px;
  max-height: 51.8px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 10px;
  flex-shrink: 0;
}
.card-summary {
  font-size: 11px;
  line-height: 1.5;
  color: #666;
  min-height: 49.5px;
  max-height: 49.5px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 14px;
  flex-shrink: 0;
}
.card-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  height: 20px;
  min-height: 20px;
  max-height: 20px;
  overflow: hidden;
  margin-bottom: 16px;
  flex-shrink: 0;
}
.tag {
  font-family: "IBM Plex Mono", monospace;
  font-size: 7px;
  padding: 3px 6px;
  cursor: pointer;
}
.card-foot {
  margin-top: auto;
  flex-shrink: 0;
}
.foot-labels {
  display: flex;
  justify-content: space-between;
  font-family: "IBM Plex Mono", monospace;
  font-size: 7px;
  color: #aaa;
  margin-bottom: 4px;
  text-transform: uppercase;
  gap: 12px;
}
.foot-values {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
}
.relevance {
  display: flex;
  align-items: center;
  gap: 5px;
}
.bar {
  width: 36px;
  height: 3px;
  background: #e5e2de;
  border-radius: 2px;
  overflow: hidden;
}
.bar div {
  height: 100%;
  background: #111;
}
.collected {
  color: #999;
  font-size: 8px;
}
.collection-label {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  font-weight: 600;
}
.sq {
  width: 6px;
  height: 6px;
}
.add-card {
  background: #e8e3de;
  border: 1px dashed #d1c7bc;
  min-height: 260px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  color: #aaa;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  cursor: pointer;
}

.modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  display: flex;
  z-index: 200;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.modal-content {
  background: #fefefd;
  width: 100%;
  max-width: 640px;
  max-height: 90vh;
  overflow: auto;
  border: 1.5px solid #111;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.modal-head {
  padding: 24px 24px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  text-transform: uppercase;
}
.close {
  cursor: pointer;
  font-size: 14px;
  border: 1px solid #e5e2de;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-title {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.25;
  margin: 16px 24px 12px;
  letter-spacing: -0.02em;
}
.modal-summary {
  font-size: 14px;
  line-height: 1.6;
  color: #444;
  margin: 0 24px;
}
.modal-meta {
  padding: 16px 24px;
  background: #faf8f5;
  display: flex;
  gap: 16px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  margin-top: 18px;
  flex-wrap: wrap;
}
.modal-actions {
  padding: 16px 24px;
  display: flex;
  gap: 10px;
}
.btn-black.large {
  flex: 1;
  height: 42px;
  background: #111;
  color: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.btn-outline {
  height: 42px;
  padding: 0 18px;
  background: #fff;
  border: 1.5px solid #111;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}
.ml-auto {
  margin-left: auto;
}
.muted {
  color: #aaa;
}
</style>
