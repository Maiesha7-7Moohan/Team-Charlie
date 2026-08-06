<template>
  <div class="grid-wrapper">
    <div class="cluster-section">
      <div class="cluster-header">
        <span
          >CLUSTER MAP — {{ stats.total }} NODES ({{ stats.sites }} SITES /
          {{ stats.kw }} KEYWORDS)</span
        >
        <div class="legend">
          <span><i style="background: #ff5a1f"></i> SITE</span>
          <span><i style="background: #2d5bff"></i> KEYWORD</span>
          <div v-if="activeFilters.length" class="active-filters">
            <span
              v-for="(f, i) in activeFilters"
              :key="i"
              class="filter-chip"
              @click="removeFilter(i)"
            >
              {{ f.label }} ✕
            </span>
            <button class="btn-reset" @click="resetDrillDown">RESET</button>
          </div>
        </div>
      </div>
      <div ref="canvasContainer" class="graph-canvas">
        <div class="zoom-controls">
          <button class="zoom-btn" @click="zoomIn" title="Zoom in">+</button>
          <button class="zoom-btn" @click="zoomOut" title="Zoom out">−</button>
          <button
            class="zoom-btn reset-btn"
            @click="resetView"
            title="Reset view"
          >
            ⟳
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state">Loading articles...</div>
    <div v-else-if="error" class="error-state">{{ error }}</div>

    <div v-else-if="filteredArticles.length === 0" class="empty-state">
      <div class="empty-icon">∅</div>
      <div class="empty-title">NO RESULTS FOUND</div>
      <div class="empty-message">
        <span v-if="props.search">
          No articles match "<b>{{ props.search }}</b
          >"
        </span>
        <span v-else-if="activeFilters.length > 0">
          No articles match the current filters
        </span>
        <span v-else> No articles available </span>
      </div>
      <button
        v-if="props.search || activeFilters.length > 0"
        class="btn-clear-search"
        @click="clearAllFilters"
      >
        CLEAR FILTERS
      </button>
    </div>

    <div v-else class="grid">
      <div
        v-for="a in filteredArticles"
        :key="a.id"
        class="card"
        @click="openArticle(a)"
      >
        <div v-if="a.bookmarked" class="bookmark-line"></div>
        <div class="card-top">
          <div class="card-source">
            <span class="src">{{ a.source }}</span
            ><span class="author">| {{ a.author }}</span
            ><span v-if="a.bookmarked" class="bookmark-badge">SAVED</span>
          </div>
          <div class="card-badges">
            <span class="badge" :style="a.badgeStyle">{{ a.badge }}</span
            ><span class="open-btn">↗</span>
          </div>
        </div>
        <div class="card-title">{{ a.title }}</div>
        <div class="card-summary">{{ a.summary }}</div>
        <div class="card-foot">
          <div class="foot-labels">
            <span>WORDS</span><span class="ml-auto">COLLECTED</span>
          </div>
          <div class="foot-values">
            <span class="words-value">{{
              (a.words || 0).toLocaleString()
            }}</span
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
          WORDS: <b>{{ selected.words }}</b
          ><span class="ml-auto muted">{{ selected.collected }}</span>
        </div>
        <div class="modal-actions">
          <button
            class="btn-bookmark"
            :class="{ active: selected.bookmarked }"
            @click.stop="toggleBookmark(selected)"
          >
            {{ selected.bookmarked ? "★ SAVED" : "☆ BOOKMARK" }}
          </button>
          <button
            class="btn-black large"
            :disabled="!getArticleUrl(selected)"
            @click.stop="openFullArticle"
          >
            {{
              getArticleUrl(selected)
                ? "OPEN FULL ARTICLE ↗"
                : "NO LINK AVAILABLE"
            }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  ref,
  computed,
  watch,
  onMounted,
  onBeforeUnmount,
  nextTick,
} from "vue";
import * as THREE from "three";
import {
  CSS2DRenderer,
  CSS2DObject,
} from "three/examples/jsm/renderers/CSS2DRenderer.js";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import api from "../services/api";

// after
const props = defineProps({
  search: String,
  sort: String,
  categories: { type: Array, default: () => [] },
  author: { type: String, default: "" },
  dateFrom: { type: String, default: "" },
  dateTo: { type: String, default: "" },
  bookmarkedOnly: Boolean,
});
const emit = defineEmits(["search-tag", "update:count", "clear-search", "update:meta"]);

const selected = ref(null);
const articles = ref([]);
const loading = ref(false);
const error = ref(null);
const canvasContainer = ref(null);
const stats = ref({ total: 0, sites: 0, kw: 0 });
const activeFilters = ref([]);
const bookmarkedIds = ref(new Set()); // persistent bookmark IDs
let scene,
  camera,
  renderer,
  labelRenderer,
  animationId,
  graphGroup,
  raycaster,
  mouse,
  controls;
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

const STORAGE_KEY = "article_bookmarks_v1";

function loadBookmarks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) bookmarkedIds.value = new Set(JSON.parse(raw));
  } catch (e) {
    console.warn("Failed to load bookmarks:", e);
  }
}

function saveBookmarks() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...bookmarkedIds.value]));
  } catch (e) {
    console.warn("Failed to save bookmarks:", e);
  }
}

function toggleBookmark(article) {
  if (bookmarkedIds.value.has(article.id)) {
    bookmarkedIds.value.delete(article.id);
    article.bookmarked = false;
  } else {
    bookmarkedIds.value.add(article.id);
    article.bookmarked = true;
  }
  saveBookmarks();
  // Force reactivity
  articles.value = [...articles.value];
}

async function getArticles() {
  const { data } = await api.get("/items?limit=1000");
  return data.items;
}

function getArticleUrl(a) {
  return a ? a.url || a.link || a.href || null : null;
}
function normalizeArticle(raw, index) {
  const content = raw.article || raw.description || "";

  const categoryColors = {
    MARKETS: "#ff5a1f",
    AI: "#2d5bff",
    CRYPTO: "#7c3aed",
    TECH: "#22c55e",
    WIRE: "#facc15",
    POLITICS: "#ef4444",
    BUSINESS: "#06b6d4",
    SPORTS: "#111",
  };

  const category = (raw.category || "WIRE").toUpperCase();
  const color =
    categoryColors[category] || group1Palette[index % group1Palette.length];
  const isDark = ["#111", "#2D5BFF", "#7C3AED", "#EF4444"].includes(
    color.toUpperCase(),
  );

  const keywordSource =
    raw.keywords || raw.tags || raw.topics || raw.category || [];
  const keywords = Array.isArray(keywordSource)
    ? keywordSource
    : typeof keywordSource === "string"
      ? keywordSource.split(",").map((k) => k.trim())
      : [];

  const id = raw.id ?? raw.link ?? index;
  return {
    id,
    source: (raw.source || "WEB").toUpperCase(),
    author: raw.author || "Scraped",
    badge: category,
    badgeStyle: `background:${color}; color:${isDark ? "#fff" : "#111"}; border:1px solid #111; font-weight:800;`,
    title: raw.title || "Untitled",
    summary:
      raw.description ||
      content.slice(0, 180) + (content.length > 180 ? "..." : ""),
    tags: keywords.filter(Boolean).map((t) => {
      return {
        t: t.toUpperCase(),
        s: `background:#2d5bff;color:#111;border:1px solid #111;`,
      };
    }),
    relevance: raw.relevance ?? 82,
    words: content ? content.split(/\s+/).length : 0,
    collected: raw.published || "",
    collection: raw.source || "SCRAPED",
    bookmarked: bookmarkedIds.value.has(id), // load from localStorage
    color,
    category: raw.category || "All Sources",
    status: raw.status || "Active",
    priority: raw.priority || "Medium",
    url: raw.link || null,
    link: raw.link || null,
    href: raw.link || null,
  };
}
function buildClusterFromList(list) {
  const sites = new Map(),
    kws = new Map();
  const links = [];

  list.forEach((a) => {
    if (!sites.has(a.source)) {
      sites.set(a.source, {
        id: `site_${a.source}`,
        label: a.source,
        type: "site",
        count: 0,
      });
    }
    sites.get(a.source).count++;

    (a.tags || []).forEach((t) => {
      const label = (typeof t === "string" ? t : t.t).toUpperCase();
      const kwId = `kw_${label}`;
      if (!kws.has(label)) {
        kws.set(label, { id: kwId, label, type: "keyword", count: 0 });
      }
      kws.get(label).count++;
      links.push({ source: `site_${a.source}`, target: kwId });
    });
  });

  let filteredNodes = [];
  let filteredLinks = links;

  if (activeFilters.value.length > 0) {
    const clickedSite = activeFilters.value.find((f) => f.type === "site");

    if (clickedSite) {
      const siteNode = sites.get(clickedSite.label);
      if (siteNode) {
        filteredNodes.push(siteNode);
        const connectedKwIds = new Set();
        links.forEach((l) => {
          if (l.source === clickedSite.id) {
            connectedKwIds.add(l.target);
          }
        });
        connectedKwIds.forEach((kwId) => {
          const kwLabel = kwId.split("_")[1];
          if (kws.has(kwLabel)) filteredNodes.push(kws.get(kwLabel));
        });
        filteredLinks = links.filter(
          (l) => l.source === clickedSite.id && connectedKwIds.has(l.target),
        );
      }
    } else {
      const keywordFilters = activeFilters.value.filter(
        (f) => f.type === "keyword",
      );
      const siteIds = new Set();
      const kwIds = new Set(keywordFilters.map((f) => f.id));

      links.forEach((l) => {
        if (kwIds.has(l.target)) siteIds.add(l.source);
      });

      filteredNodes = [
        ...[...sites.values()].filter((n) => siteIds.has(n.id)),
        ...[...kws.values()].filter((n) => kwIds.has(n.id)),
      ];
      filteredLinks = links.filter(
        (l) => siteIds.has(l.source) && kwIds.has(l.target),
      );
    }
  } else {
    const topKws = [...kws.values()]
      .sort((a, b) => b.count - a.count)
      .slice(0, 40);
    const topKwIds = new Set(topKws.map((k) => k.id));
    filteredLinks = links.filter(
      (l) => topKwIds.has(l.target) || l.source.startsWith("site_"),
    );
    filteredNodes = [...sites.values(), ...topKws];
  }

  const nodeSites = filteredNodes.filter((n) => n.type === "site").length;
  const nodeKws = filteredNodes.filter((n) => n.type === "keyword").length;
  stats.value = { total: filteredNodes.length, sites: nodeSites, kw: nodeKws };

  return { nodes: filteredNodes, links: filteredLinks };
}

function handleNodeClick(event) {
  if (!renderer || !camera || !scene) return;
  const rect = renderer.domElement.getBoundingClientRect();
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(
    graphGroup.children.filter((obj) => obj.type === "Mesh"),
  );

  if (intersects.length > 0) {
    const clickedNode = intersects[0].object.userData;
    const newFilter = {
      type: clickedNode.type,
      id: clickedNode.id,
      label: clickedNode.label,
    };
    if (!activeFilters.value.some((f) => f.id === newFilter.id)) {
      activeFilters.value.push(newFilter);
      initThree();
    }
  }
}

function removeFilter(index) {
  activeFilters.value.splice(index);
  initThree();
}

function resetDrillDown() {
  activeFilters.value = [];
  initThree();
}

function clearAllFilters() {
  activeFilters.value = [];
  emit("clear-search");
  initThree();
}

function zoomIn() {
  if (controls) controls.dollyIn(1.2);
}
function zoomOut() {
  if (controls) controls.dollyOut(1.2);
}
function resetView() {
  fitCameraToGroup();
}

function fitCameraToGroup() {
  if (!graphGroup || graphGroup.children.length === 0) return;

  const box = new THREE.Box3().setFromObject(graphGroup);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());

  const maxDim = Math.max(size.x, size.y, size.z);
  const fov = camera.fov * (Math.PI / 180);
  let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
  cameraZ *= 1.3;

  camera.position.set(center.x, center.y, center.z + cameraZ);
  camera.lookAt(center);

  if (controls) {
    controls.target.copy(center);
    controls.update();
  }
}

function initThree() {
  if (!canvasContainer.value) return;
  const container = canvasContainer.value;
  const W = container.clientWidth,
    H = 460;

  if (renderer) {
    renderer.domElement.removeEventListener("click", handleNodeClick);
    controls?.dispose();
    cancelAnimationFrame(animationId);
    const oldCanvas = container.querySelector("canvas");
    if (oldCanvas) oldCanvas.remove();
    labelRenderer?.domElement?.remove();
  }

  scene = new THREE.Scene();
  scene.background = new THREE.Color("#fefefd");
  scene.fog = new THREE.Fog("#fefefd", 42, 95);

  camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 1000);
  camera.position.set(0, 2, 38);

  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.domElement.style.cursor = "grab";
  renderer.domElement.style.display = "block";
  const zoomCtrls = container.querySelector(".zoom-controls");
  container.insertBefore(renderer.domElement, zoomCtrls);

  controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.screenSpacePanning = false;
  controls.minDistance = 10;
  controls.maxDistance = 100;
  controls.autoRotate = false;
  controls.enableZoom = false;

  renderer.domElement.addEventListener("mousedown", () => {
    renderer.domElement.style.cursor = "grabbing";
  });
  renderer.domElement.addEventListener("mouseup", () => {
    renderer.domElement.style.cursor = "grab";
  });

  labelRenderer = new CSS2DRenderer();
  labelRenderer.setSize(W, H);
  labelRenderer.domElement.style.position = "absolute";
  labelRenderer.domElement.style.top = "0px";
  labelRenderer.domElement.style.pointerEvents = "none";
  labelRenderer.domElement.style.zIndex = "1";
  container.insertBefore(labelRenderer.domElement, zoomCtrls);

  raycaster = new THREE.Raycaster();
  mouse = new THREE.Vector2();
  renderer.domElement.addEventListener("click", handleNodeClick);

  scene.add(new THREE.AmbientLight(0xffffff, 0.9));
  const dl = new THREE.DirectionalLight(0xffffff, 0.35);
  dl.position.set(8, 12, 5);
  scene.add(dl);

  graphGroup = new THREE.Group();
  scene.add(graphGroup);

  const { nodes, links } = buildClusterFromList(filteredArticles.value);
  const nodeMap = new Map();

  const siteMat = new THREE.MeshStandardMaterial({
    color: 0xff5a1f,
    roughness: 0.4,
    metalness: 0.1,
  });
  const kwMat = new THREE.MeshStandardMaterial({
    color: 0x2d5bff,
    roughness: 0.5,
    metalness: 0.05,
  });

  const siteNodes = nodes.filter((n) => n.type === "site");
  const keywordNodes = nodes.filter((n) => n.type === "keyword");

  const meshes = [];

  nodes.forEach((n, i) => {
    const nodeRadius = n.type === "site" ? 1.6 : 0.6;
    const geo = new THREE.SphereGeometry(nodeRadius, 24, 24);
    const mat = n.type === "site" ? siteMat : kwMat;
    const mesh = new THREE.Mesh(geo, mat);

    let angle, r;
    if (n.type === "site") {
      const siteIndex = siteNodes.indexOf(n);
      const t = siteIndex / Math.max(siteNodes.length, 1);
      angle = t * Math.PI * 2 * 1.5;
      r = 10 + Math.random() * 6;
    } else {
      const kwIndex = keywordNodes.indexOf(n);
      const t = kwIndex / Math.max(keywordNodes.length, 1);
      angle = t * Math.PI * 2 * 2.5;
      r = 20 + Math.random() * 8;
    }

    mesh.position.set(
      Math.cos(angle) * r + (Math.random() - 0.5) * 2,
      Math.sin(angle) * r + (Math.random() - 0.5) * 2,
      (Math.random() - 0.5) * 5,
    );

    mesh.userData = { ...n, nodeRadius };

    const labelDiv = document.createElement("div");
    labelDiv.className = "node-label";
    labelDiv.textContent = n.label;
    labelDiv.style.color = "#111";
    labelDiv.style.fontSize = n.type === "site" ? "10px" : "8px";
    labelDiv.style.fontFamily = '"IBM Plex Mono", monospace';
    labelDiv.style.fontWeight = "700";
    labelDiv.style.padding = "2px 4px";
    labelDiv.style.background = "rgba(254, 254, 253, 0.9)";
    labelDiv.style.border = "1px solid #111";
    labelDiv.style.whiteSpace = "nowrap";
    const label = new CSS2DObject(labelDiv);
    label.position.set(0, nodeRadius + 0.8, 0);
    mesh.add(label);

    graphGroup.add(mesh);
    nodeMap.set(n.id, mesh);
    meshes.push(mesh);
  });

  const iterations = 50;
  const padding = 0.4;
  for (let iter = 0; iter < iterations; iter++) {
    for (let i = 0; i < meshes.length; i++) {
      for (let j = i + 1; j < meshes.length; j++) {
        const a = meshes[i];
        const b = meshes[j];
        const dist = a.position.distanceTo(b.position);
        const minDist = a.userData.nodeRadius + b.userData.nodeRadius + padding;

        if (dist < minDist && dist > 0.001) {
          const overlap = minDist - dist;
          const dir = new THREE.Vector3()
            .subVectors(a.position, b.position)
            .normalize();
          a.position.addScaledVector(dir, overlap * 0.5);
          b.position.addScaledVector(dir, -overlap * 0.5);
        }
      }
    }
  }

  const lineMat = new THREE.LineBasicMaterial({
    color: 0xe5e2de,
    transparent: true,
    opacity: 0.25,
  });

  links.forEach((l) => {
    const a = nodeMap.get(l.source),
      b = nodeMap.get(l.target);
    if (!a || !b) return;
    const geo = new THREE.BufferGeometry().setFromPoints([
      a.position,
      b.position,
    ]);
    const line = new THREE.Line(geo, lineMat);
    graphGroup.add(line);
  });

  fitCameraToGroup();

  const animate = () => {
    animationId = requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
  };
  animate();

  window.addEventListener("resize", () => {
    if (!canvasContainer.value) return;
    const w = canvasContainer.value.clientWidth;
    camera.aspect = w / H;
    camera.updateProjectionMatrix();
    renderer.setSize(w, H);
    labelRenderer.setSize(w, H);
  });
}

const fetchArticles = async () => {
  loading.value = true;
  error.value = null;
  loadBookmarks(); // load saved bookmarks first
  try {
    const res = await getArticles();
    let rawList = Array.isArray(res)
      ? res
      : res?.data || res?.articles || res?.items || [];
    articles.value = rawList.map(normalizeArticle);
    await nextTick();
    initThree();
  } catch (e) {
    error.value = e.message || "Failed to fetch";
  } finally {
    loading.value = false;
  }
};
onMounted(fetchArticles);
onBeforeUnmount(() => {
  if (renderer)
    renderer.domElement.removeEventListener("click", handleNodeClick);
  controls?.dispose();
  cancelAnimationFrame(animationId);
  renderer?.dispose();
  labelRenderer?.domElement?.remove();
});

const availableCategories = computed(() => {
  const set = new Set(articles.value.map((a) => a.category).filter(Boolean));
  return [...set].sort();
});
const availableAuthors = computed(() => {
  const set = new Set(articles.value.map((a) => a.author).filter(Boolean));
  return [...set].sort();
});

watch(
  articles,
  () => {
    emit("update:meta", {
      categories: availableCategories.value,
      authors: availableAuthors.value,
    });
  },
  { immediate: true },
);

const filteredArticles = computed(() => {
  let list = articles.value.filter((a) => {
    if (props.bookmarkedOnly && !a.bookmarked) return false;
    if (
      props.categories &&
      props.categories.length > 0 &&
      !props.categories.includes(a.category)
    )
      return false;
    if (props.author && a.author !== props.author) return false;
    if (props.dateFrom) {
      const d = new Date(a.collected);
      const from = new Date(props.dateFrom);
      if (!isNaN(d) && !isNaN(from) && d < from) return false;
    }
    if (props.dateTo) {
      const d = new Date(a.collected);
      const to = new Date(props.dateTo);
      to.setHours(23, 59, 59, 999); // include the whole "to" day
      if (!isNaN(d) && !isNaN(to) && d > to) return false;
    }
    if (props.search) {
      const q = props.search.toLowerCase();
      const haystack =
        `${a.title} ${a.summary} ${a.source} ${a.tags.map((t) => t.t).join(" ")} ${a.category}`.toLowerCase();
      if (!haystack.includes(q)) return false;
    }
    return true;
  });

  if (activeFilters.value.length > 0) {
    list = list.filter((a) => {
      return activeFilters.value.every((f) => {
        if (f.type === "site") return a.source === f.label;
        if (f.type === "keyword") return a.tags.some((t) => t.t === f.label);
        return true;
      });
    });
  }

  if (props.sort === "relevance")
    list = [...list].sort((a, b) => b.relevance - a.relevance);
  else if (props.sort === "words")
    list = [...list].sort((a, b) => b.words - a.words);
  else
    list = [...list].sort((a, b) => {
      const da = new Date(a.collected).getTime() || 0;
      const db = new Date(b.collected).getTime() || 0;
      return db - da;
    });
  return list;
});

function openArticle(a) {
  selected.value = a;
}
function openFullArticle() {
  const url = getArticleUrl(selected.value);
  if (url) window.open(url, "_blank", "noopener,noreferrer");
}

watch(
  filteredArticles,
  (l) => {
    const bookmarked = l.filter((a) => a.bookmarked).length;
    const sources = new Set(l.map((a) => a.source)).size;
    const totalBookmarked = articles.value.filter((a) => a.bookmarked).length;
    emit("update:count", {
      count: l.length,
      bookmarked,
      sources,
      totalBookmarked,
    });
  },
  { immediate: true },
);

watch(
  filteredArticles,
  async () => {
    if (!canvasContainer.value) return;
    await nextTick();
    initThree();
  },
  { deep: true },
);

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
  align-items: center;
  flex-wrap: wrap;
}

.legend i {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 4px;
}

.active-filters {
  display: flex;
  gap: 6px;
  align-items: center;
}

.filter-chip {
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  font-weight: 700;
  padding: 4px 8px;
  background: #ff5a1f;
  color: #fff;
  border: none;
  cursor: pointer;
}

.filter-chip:hover {
  background: #e54a10;
}

.btn-reset {
  font-family: "IBM Plex Mono", monospace;
  font-size: 8px;
  font-weight: 700;
  padding: 4px 8px;
  background: #111;
  color: #fff;
  border: none;
  cursor: pointer;
}

.btn-reset:hover {
  background: #333;
}

.graph-canvas {
  width: 100%;
  height: 460px;
  position: relative;
  overflow: hidden;
}

.zoom-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 1px;
  background: #fefefd;
  border: 1.5px solid #111;
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.1);
}

.zoom-btn {
  width: 32px;
  height: 32px;
  background: #fefefd;
  border: none;
  border-bottom: 1px solid #e5e2de;
  font-family: "IBM Plex Mono", monospace;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #111;
  transition: background 0.1s;
}

.zoom-btn:last-child {
  border-bottom: none;
}

.zoom-btn:hover {
  background: #f7f7f5;
}

.zoom-btn:active {
  background: #e5e2de;
}

.reset-btn {
  font-size: 14px;
}

.node-label {
  pointer-events: none !important;
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
  min-height: 220px;
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

.bookmark-line {
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: #facc15;
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

.bookmark-badge {
  background: #facc15;
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

.words-value {
  font-weight: 700;
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

.btn-bookmark {
  height: 42px;
  padding: 0 18px;
  background: #fff;
  border: 1.5px solid #111;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.1s;
}

.btn-bookmark:hover {
  background: #f7f7f5;
}

.btn-bookmark.active {
  background: #facc15;
  border-color: #111;
}

.btn-bookmark.active:hover {
  background: #e6b814;
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

.btn-black.large:disabled {
  background: #ccc;
  cursor: not-allowed;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  background: #fefefd;
  border: 1.5px solid #111;
}

.empty-icon {
  font-size: 48px;
  color: #e5e2de;
  margin-bottom: 16px;
  font-family: "IBM Plex Mono", monospace;
}

.empty-title {
  font-family: "IBM Plex Mono", monospace;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
  color: #111;
}

.empty-message {
  font-size: 12px;
  color: #666;
  margin-bottom: 20px;
  line-height: 1.5;
}

.empty-message b {
  color: #111;
  font-weight: 700;
}

.btn-clear-search {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  padding: 8px 16px;
  background: #111;
  color: #fff;
  border: none;
  cursor: pointer;
  letter-spacing: 0.04em;
  transition: background 0.1s;
}

.btn-clear-search:hover {
  background: #333;
}

.btn-clear-search:active {
  background: #000;
}
</style>
