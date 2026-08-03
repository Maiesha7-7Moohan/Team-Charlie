<template>
  <div class="grid-wrapper">
    <div class="cluster-section">
      <div class="cluster-header">
        <span>CLUSTER MAP — {{ stats.total }} NODES ({{ stats.cats }} CAT / {{ stats.kw }} KW / {{ stats.sites }}
          SITES)</span>
        <div class="legend">
          <span><i style="background: #ff5a1f"></i> CATEGORY</span>
          <span><i style="background: #2d5bff"></i> KEYWORD</span>
          <span><i style="background: #111"></i> SITE</span>
        </div>
      </div>
      <div ref="canvasContainer" class="graph-canvas"></div>
    </div>

    <div v-if="loading" class="loading-state">Loading articles...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>
    <div v-else class="grid">
      <div v-for="a in filteredArticles" :key="a.id" class="card" @click="openArticle(a)">
        <div v-if="a.flagged" class="flag-line"></div>
        <div class="card-top">
          <div class="card-source">
            <span class="src">{{ a.source }}</span><span class="author">| {{ a.author }}</span><span v-if="a.flagged"
              class="flag-badge">FLAGGED</span>
          </div>
          <div class="card-badges">
            <span class="badge" :style="a.badgeStyle">{{ a.badge }}</span><span class="open-btn">↗</span>
          </div>
        </div>
        <div class="card-title">{{ a.title }}</div>
        <div class="card-summary">{{ a.summary }}</div>
        <div class="card-tags">
          <span v-for="tag in a.tags" :key="tag.t" class="tag" :style="tag.s" @click.stop="emit('search-tag', tag.t)">{{
            tag.t }}</span>
        </div>
        <div class="card-foot">
          <div class="foot-labels"><span>RELEVANCE</span><span>WORDS</span><span class="ml-auto">COLLECTED</span></div>
          <div class="foot-values">
            <div class="relevance">
              <div class="bar">
                <div :style="{ width: a.relevance + '%' }"></div>
              </div><span>{{ a.relevance }}</span>
            </div>
            <span>{{ (a.words || 0).toLocaleString() }}</span><span class="collected">{{ a.collected }}</span>
          </div>
          <div class="collection-label" :style="{ color: a.color }">
            <div class="sq" :style="{ background: a.color }"></div>{{ a.collection }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="selected" class="modal" @click.self="selected = null">
      <div class="modal-content">
        <div class="modal-head">
          <div class="card-source"><span class="src">{{ selected.source }}</span><span class="author">| {{
            selected.author }}</span></div>
          <span class="close" @click="selected = null">✕</span>
        </div>
        <h1 class="modal-title">{{ selected.title }}</h1>
        <p class="modal-summary">{{ selected.summary }}</p>
        <div class="modal-meta">RELEVANCE: <b>{{ selected.relevance }}</b> WORDS: <b>{{ selected.words }}</b><span
            class="ml-auto muted">{{ selected.collected }}</span></div>
        <div class="modal-actions">
          <button class="btn-black large" :disabled="!getArticleUrl(selected)" @click.stop="openFullArticle">{{
            getArticleUrl(selected) ? "OPEN FULL ARTICLE ↗" : "NO LINK AVAILABLE" }}</button><button
            class="btn-outline">FLAG</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from "vue";
import * as THREE from "three";
import api from "../services/api";


const props = defineProps({
  search: String,
  sort: String,
  category: String,
  status: { type: Array, default: () => [] },
  priority: { type: Array, default: () => [] },
  flaggedOnly: Boolean,
});
const emit = defineEmits(["search-tag", "update:count"]);

const selected = ref(null);
const articles = ref([]);
const loading = ref(false);
const error = ref(null);
const canvasContainer = ref(null);
const stats = ref({ total: 0, cats: 0, kw: 0, sites: 0 });
let scene, camera, renderer, animationId, graphGroup;
const group1Palette = ["#ff5a1f", "#2d5bff", "#22c55e", "#7c3aed", "#facc15", "#ef4444", "#06b6d4", "#111"];

async function getArticles() {
  const { data } = await api.get("/items?limit=1000");
  return data.items;
}

function getArticleUrl(a) { return a ? a.url || a.link || a.href || null : null; }
function normalizeArticle(raw, index) {
  const content = raw.article || raw.description || "";   // was raw.content || raw.summary
  const color = group1Palette[index % group1Palette.length];
  const isDark = ["#111", "#2D5BFF", "#7C3AED", "#EF4444"].includes(color);
  return {
    id: raw.id ?? raw.link ?? index,                        // raw.url doesn't exist; use raw.link
    source: (raw.source || "WEB").toUpperCase(),             // raw.source_name doesn't exist
    author: raw.author || "Scraped",
    badge: raw.category || "WIRE",                           // no real "badge" field — derive from category
    badgeStyle: `background:${color}; color:${isDark ? "#fff" : "#111"}; border:1px solid #111; font-weight:800;`,
    title: raw.title || "Untitled",
    summary: raw.description || content.slice(0, 180) + (content.length > 180 ? "..." : ""),
    tags: [raw.category].filter(Boolean).map((t, i) => {
      const c = group1Palette[i % group1Palette.length];
      const dark = ["#111", "#2D5BFF", "#7C3AED", "#EF4444"].includes(c);
      return { t: t.toUpperCase(), s: `background:${c};color:${dark ? "#fff" : "#111"};border:1px solid #111;` };
    }),
    relevance: raw.relevance ?? 82,       // no real scoring data exists — see note below
    words: content ? content.split(/\s+/).length : 0,
    collected: raw.published || "",       // was raw.date/collected/scraped_at
    collection: raw.source || "SCRAPED",
    flagged: raw.flagged || false,        // no real flag data — see note below
    color,
    category: raw.category || "All Sources",
    status: raw.status || "Active",       // no real status data — see note below
    priority: raw.priority || "Medium",   // no real priority data — see note below
    url: raw.link || null,
    link: raw.link || null,
    href: raw.link || null,
  };
}

function buildCluster() {
  const cats = new Map(), kws = new Map(), sites = new Map();
  const links = [];
  articles.value.forEach((a) => {
    if (!cats.has(a.category)) cats.set(a.category, { id: `cat_${a.category}`, label: a.category, type: "category", count: 0 });
    cats.get(a.category).count++;
    if (!sites.has(a.source)) sites.set(a.source, { id: `site_${a.source}`, label: a.source, type: "site", count: 0 });
    sites.get(a.source).count++;
    (a.tags || []).forEach((t) => {
      const label = (typeof t === "string" ? t : t.t).toUpperCase();
      if (!kws.has(label)) kws.set(label, { id: `kw_${label}`, label, type: "keyword", count: 0 });
      kws.get(label).count++;
      links.push({ source: `cat_${a.category}`, target: `kw_${label}` });
      links.push({ source: `kw_${label}`, target: `site_${a.source}` });
    });
  });
  const topKws = [...kws.values()].sort((a, b) => b.count - a.count).slice(0, 30);
  const topKwIds = new Set(topKws.map((k) => k.id));
  const filteredLinks = links.filter((l) => topKwIds.has(l.source) || topKwIds.has(l.target) || l.source.startsWith("cat_"));
  const nodes = [...cats.values(), ...topKws, ...sites.values()];
  stats.value = { total: nodes.length, cats: cats.size, kw: topKws.length, sites: sites.size };
  return { nodes, links: filteredLinks };
}

function initThree() {
  if (!canvasContainer.value) return;
  const container = canvasContainer.value;
  const W = container.clientWidth, H = 460;
  if (renderer) { container.innerHTML = ""; cancelAnimationFrame(animationId); }
  scene = new THREE.Scene(); scene.background = new THREE.Color("#fefefd"); scene.fog = new THREE.Fog("#fefefd", 35, 85);
  camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 1000); camera.position.set(0, 0, 38);
  renderer = new THREE.WebGLRenderer({ antialias: true }); renderer.setSize(W, H); renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);
  scene.add(new THREE.AmbientLight(0xffffff, 1));
  const dl = new THREE.DirectionalLight(0xffffff, 0.6); dl.position.set(10, 10, 10); scene.add(dl);
  graphGroup = new THREE.Group(); scene.add(graphGroup);
  const { nodes, links } = buildCluster();
  const nodeMap = new Map();
  nodes.forEach((n, i) => {
    const radius = n.type === "category" ? 1.6 + n.count * 0.1 : n.type === "keyword" ? 0.55 + n.count * 0.12 : 0.4 + n.count * 0.03;
    const geo = new THREE.SphereGeometry(radius, 18, 18);
    const mat = new THREE.MeshStandardMaterial({ color: n.type === "category" ? 0xff5a1f : n.type === "keyword" ? 0x2d5bff : 0x111111 });
    const mesh = new THREE.Mesh(geo, mat);
    const angle = (i / nodes.length) * Math.PI * 2 * 4;
    const r = n.type === "category" ? 5 : n.type === "keyword" ? 13 + Math.random() * 5 : 22 + Math.random() * 4;
    mesh.position.set(Math.cos(angle) * r + (Math.random() - 0.5) * 3, Math.sin(angle) * r + (Math.random() - 0.5) * 3, (Math.random() - 0.5) * 8);
    mesh.userData = n; graphGroup.add(mesh); nodeMap.set(n.id, mesh);
  });
  const lineMat = new THREE.LineBasicMaterial({ color: 0xd8d4cf, transparent: true, opacity: 0.35 });
  links.forEach((l) => {
    const a = nodeMap.get(l.source), b = nodeMap.get(l.target); if (!a || !b) return;
    const geo = new THREE.BufferGeometry().setFromPoints([a.position, b.position]);
    const line = new THREE.Line(geo, lineMat); graphGroup.add(line);
  });
  const animate = () => { animationId = requestAnimationFrame(animate); graphGroup.rotation.y += 0.0007; graphGroup.rotation.x += 0.0002; renderer.render(scene, camera); };
  animate();
  window.addEventListener("resize", () => {
    if (!canvasContainer.value) return;
    const w = canvasContainer.value.clientWidth; camera.aspect = w / H; camera.updateProjectionMatrix(); renderer.setSize(w, H);
  });
}

const fetchArticles = async () => {
  loading.value = true; error.value = null;
  try {
    const res = await getArticles();
    let rawList = Array.isArray(res) ? res : res?.data || res?.articles || res?.items || [];
    articles.value = rawList.map(normalizeArticle);
    await nextTick(); initThree();
  } catch (e) { error.value = e.message || "Failed to fetch"; }
  finally { loading.value = false; }
};
onMounted(fetchArticles);
onBeforeUnmount(() => { cancelAnimationFrame(animationId); renderer?.dispose(); });

const filteredArticles = computed(() => {
  let list = articles.value.filter((a) => {
    if (props.flaggedOnly && !a.flagged) return false;
    if (props.category && props.category !== "All Sources" && a.category !== props.category) return false;
    if (props.status && props.status.length > 0 && !props.status.includes(a.status)) return false;
    if (props.priority && props.priority.length > 0 && !props.priority.includes(a.priority)) return false;
    if (props.search) {
      const q = props.search.toLowerCase();
      const haystack = `${a.title} ${a.summary} ${a.source} ${a.tags.map(t => t.t).join(" ")} ${a.category}`.toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });
  if (props.sort === "relevance") list = [...list].sort((a, b) => b.relevance - a.relevance);
  else if (props.sort === "words") list = [...list].sort((a, b) => b.words - a.words);
  else list = [...list].sort((a, b) => {
    const da = new Date(a.collected).getTime() || 0;
    const db = new Date(b.collected).getTime() || 0;
    return db - da;
  });
  return list;
});

function openArticle(a) { selected.value = a; }
function openFullArticle() {
  const url = getArticleUrl(selected.value);
  if (url) window.open(url, "_blank", "noopener,noreferrer");
}

watch(filteredArticles, (l) => {
  const flagged = l.filter(a => a.flagged).length;
  const sources = new Set(l.map(a => a.source)).size;
  const totalFlagged = articles.value.filter(a => a.flagged).length;
  emit("update:count", { count: l.length, flagged, sources, totalFlagged });
}, { immediate: true });

defineExpose({ fetchArticles, loading, error });
</script>

<style scoped>
.grid-wrapper {
  flex: 1;
  background: #f7f7f5;
  padding: 16px;
}

.cluster-section {
  background: #fefefd;
  border: 1.5px solid #111;
  margin-bottom: 16px;
}

.cluster-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  border-bottom: 1.5px solid #111;
  flex-wrap: wrap;
  gap: 8px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  font-weight: 700;
}

.legend {
  display: flex;
  gap: 12px;
  font-size: 8px;
  font-weight: 400;
}

.legend i {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 4px;
}

.graph-canvas {
  width: 100%;
  height: 460px;
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
  border: 1px solid #e5e2de;
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