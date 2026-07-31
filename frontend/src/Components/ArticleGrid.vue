<template>
  <div class="grid-wrapper">
    <div v-if="loading" class="loading-state">Loading articles...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <div v-else class="grid">
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
            <span>{{ (a.words || 0).toLocaleString() }}</span
            ><span class="collected">{{ a.collected }}</span>
          </div>
          <div class="collection-label" :style="{ color: a.color }">
            <div class="sq" :style="{ background: a.color }"></div>
            {{ a.collection }}
          </div>
        </div>
      </div>
    </div>

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
          <b>{{ selected.words }}</b
          ><span class="ml-auto muted">{{ selected.collected }}</span>
        </div>
        <div class="modal-actions">
          <button
            class="btn-black large"
            :disabled="!getArticleUrl(selected)"
            @click.stop="openFullArticle"
          >
            {{
              getArticleUrl(selected)
                ? "OPEN FULL ARTICLE ↗"
                : "NO LINK AVAILABLE"
            }}</button
          ><button class="btn-outline">FLAG</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import { getArticles } from "@/api/fakearticles";

const props = defineProps({
  search: String,
  sort: String,
  category: String,
  flaggedOnly: Boolean,
});
const emit = defineEmits(["search-tag", "update:count"]);

const selected = ref(null);
const articles = ref([]);
const loading = ref(false);
const error = ref(null);

// Group 1 palette
const group1Palette = [
  "#ff5a1f",
  "#2d5bff",
  "#22c55e",
  "#7c3aed",
  "#facc15",
  "#ef4444",
  "#06b6d4",
  "#111",
];

function isUrl(str) {
  return typeof str === "string" && /^https?:\/\//.test(str);
}
function getArticleUrl(a) {
  if (!a) return null;
  const candidate = a.url || a.link || a.href || null;
  if (candidate) return candidate;
  if (isUrl(a.id)) return a.id;
  return null;
}
function normalizeArticle(raw, index) {
  const content = raw.content || raw.summary || "";
  const color = group1Palette[index % group1Palette.length];
  const isDark =
    color === "#111" ||
    color === "#2d5bff" ||
    color === "#7c3aed" ||
    color === "#ef4444";

  const tagPalette = group1Palette;
  return {
    id: raw.id || raw.url || raw.link || index,
    source: (raw.source || raw.source_name || "WEB").toUpperCase(),
    author: raw.author || "Scraped",
    badge: raw.badge || "WIRE",
    badgeStyle: `background:${color}; color:${isDark ? "#fff" : "#111"}; border:1px solid #111; font-weight:800;`,
    title: raw.title || "Untitled",
    summary:
      raw.summary ||
      content.slice(0, 180) + (content.length > 180 ? "..." : ""),
    tags: Array.isArray(raw.tags)
      ? raw.tags.map((t, i) => {
          const c = tagPalette[i % tagPalette.length];
          const dark =
            c === "#111" ||
            c === "#2d5bff" ||
            c === "#7c3aed" ||
            c === "#ef4444";
          return typeof t === "string"
            ? {
                t: t.toUpperCase(),
                s: `background:${c}; color:${dark ? "#fff" : "#111"}; border:1px solid #111;`,
              }
            : {
                t: t.t,
                s:
                  t.s ||
                  `background:${c}; color:${dark ? "#fff" : "#111"}; border:1px solid #111;`,
              };
        })
      : (raw.keywords || []).slice(0, 3).map((k, i) => {
          const c = tagPalette[i % tagPalette.length];
          const dark =
            c === "#111" ||
            c === "#2d5bff" ||
            c === "#7c3aed" ||
            c === "#ef4444";
          return {
            t: typeof k === "string" ? k.toUpperCase() : k.t,
            s: `background:${c}; color:${dark ? "#fff" : "#111"}; border:1px solid #111;`,
          };
        }),
    relevance: raw.relevance ?? 82,
    words: raw.words || (content ? content.split(/\s+/).length : 0),
    collected:
      raw.collected ||
      raw.scraped_at ||
      new Date().toISOString().slice(0, 16).replace("T", " "),
    collection: raw.collection || "SCRAPED",
    flagged: raw.flagged || false,
    color: color,
    category: raw.category || raw.source_name || "All Sources",
    url:
      raw.url ||
      raw.link ||
      raw.href ||
      raw.original_url ||
      raw.canonical_url ||
      null,
    link: raw.link || null,
    href: raw.href || null,
  };
}

const fetchArticles = async () => {
  loading.value = true;
  error.value = null;
  try {
    const res = await getArticles();
    // Robust handling - fixes "map is not a function"
    let rawList = [];
    if (Array.isArray(res)) rawList = res;
    else if (Array.isArray(res?.data)) rawList = res.data;
    else if (Array.isArray(res?.articles)) rawList = res.articles;
    else if (Array.isArray(res?.items)) rawList = res.items;
    else rawList = [];
    articles.value = rawList.map(normalizeArticle);
  } catch (e) {
    console.error(e);
    error.value = e.message || "Failed to fetch";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchArticles);

const filteredArticles = computed(() => {
  let list = articles.value.filter((a) => {
    if (props.flaggedOnly && !a.flagged) return false;
    if (
      props.category &&
      props.category !== "All Sources" &&
      a.category !== props.category
    )
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

function openArticle(a) {
  selected.value = a;
}
function openFullArticle() {
  const url = getArticleUrl(selected.value);
  if (!url) {
    console.warn("No URL found for article:", selected.value);
    return;
  }
  window.open(url, "_blank", "noopener,noreferrer");
}
watch(filteredArticles, (list) => emit("update:count", list.length), {
  immediate: true,
});
defineExpose({ fetchArticles, loading, error });
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
  gap: 12px;
  align-content: start;
}
.card {
  background: #fefefd;

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
  padding: 3px 6px;
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
  line-clamp: 3;
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
  line-clamp: 3;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 14px;
  flex-shrink: 0;
}
.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  min-height: 22px;
  margin-bottom: 16px;
  flex-shrink: 0;
}
.tag {
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  padding: 4px 8px;
  cursor: pointer;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.tag:hover {
  transform: translateY(-1px);
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
.loading-state,
.error-state {
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  padding: 20px;
}
</style>
