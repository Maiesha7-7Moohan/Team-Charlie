<template>
  <div class="manager-card">
    <div class="manager-head">
      <h3>Manage Target Sites</h3>
      <span v-if="lastRun" class="last-run">Last scrape: {{ formatTime(lastRun.timestamp) }}</span>
    </div>

    <p v-if="loadError" class="banner error">{{ loadError }}</p>

    <div v-if="loading" class="empty-state">Loading sites…</div>

    <ul class="site-list" v-else-if="websites.length">
      <li class="site-item" v-for="(site, index) in websites" :key="index">
        <span class="site-dot" :class="statusClass(site.name)" :title="statusTitle(site.name)"></span>
        <div class="site-info">
          <span class="site-name">{{ site.name }}</span>
          <span class="site-url">{{ site.url }}</span>
        </div>
        <button
          type="button"
          class="site-delete"
          :disabled="deletingIndex === index"
          @click="removeSite(index)"
        >&times;</button>
      </li>
    </ul>
    <p class="empty-state" v-else>No sites configured yet.</p>

    <form class="add-site-form" @submit.prevent="addSite">
      <input v-model="newName" placeholder="Site name" required />
      <input v-model="newUrl" placeholder="https://..." required />
      <p v-if="formError" class="banner error small">{{ formError }}</p>
      <button type="submit" :disabled="submitting">
        {{ submitting ? "Adding…" : "+ Add Site" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const websites = ref([]);
const newName = ref("");
const newUrl = ref("");

const loading = ref(true);
const loadError = ref("");
const formError = ref("");
const submitting = ref(false);
const deletingIndex = ref(-1);
const lastRun = ref(null);

function isValidUrl(value) {
  try {
    const u = new URL(value);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

// Looks up how this site did in the most recent "Scrape Now" run.
function statusClass(name) {
  if (!lastRun.value) return "unknown";
  const result = (lastRun.value.results || []).find((r) => r.source === name);
  if (!result) return "unknown";
  return result.success ? "ok" : "fail";
}

function statusTitle(name) {
  if (!lastRun.value) return "Not scraped yet";
  const result = (lastRun.value.results || []).find((r) => r.source === name);
  if (!result) return "Not included in the last scrape";
  return result.success ? "Last scrape succeeded" : `Last scrape failed: ${result.message || ""}`;
}

function formatTime(ts) {
  if (!ts) return "";
  return new Date(ts).toLocaleString();
}

async function loadWebsites() {
  loading.value = true;
  loadError.value = "";
  try {
    const res = await api.get("/websites");
    websites.value = res.data;
  } catch (err) {
    console.error("Failed to load websites:", err);
    loadError.value = "Couldn't load sites. Check the backend connection.";
  } finally {
    loading.value = false;
  }
}

async function loadLastRun() {
  try {
    const res = await api.get("/history");
    const history = res.data || [];
    lastRun.value = history.length ? history[history.length - 1] : null;
  } catch (err) {
    console.error("Failed to load scrape history:", err);
  }
}

async function addSite() {
  formError.value = "";

  const name = newName.value.trim();
  const url = newUrl.value.trim();

  if (!isValidUrl(url)) {
    formError.value = "Enter a valid URL, starting with http:// or https://";
    return;
  }

  const duplicate = websites.value.some(
    (s) => s.name.toLowerCase() === name.toLowerCase() || s.url === url
  );
  if (duplicate) {
    formError.value = "That site is already in the list.";
    return;
  }

  submitting.value = true;
  try {
    const res = await api.post("/websites", { name, url });
    websites.value.push(res.data);
    newName.value = "";
    newUrl.value = "";
  } catch (err) {
    console.error("Failed to add site:", err);
    formError.value = "Couldn't add that site. Try again.";
  } finally {
    submitting.value = false;
  }
}

async function removeSite(index) {
  deletingIndex.value = index;
  try {
    await api.delete(`/websites/${index}`);
    websites.value.splice(index, 1);
  } catch (err) {
    console.error("Failed to remove site:", err);
    loadError.value = "Couldn't remove that site. Try again.";
  } finally {
    deletingIndex.value = -1;
  }
}

onMounted(() => {
  loadWebsites();
  loadLastRun();
});
</script>

<style scoped>
.manager-card {
  margin-top: 20px;
  flex: 1 1 0;
  min-width: 350px;
  height: 420px;
  display: flex;
  flex-direction: column;
  background: #FEFEFD;
  border: 1px solid #E8E3DE;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
  transition: all 0.18s ease;
}

.manager-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
  flex-shrink: 0;
}

.last-run {
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  color: #999;
  white-space: nowrap;
}

.banner {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  padding: 8px 10px;
  margin: 8px 0 0;
  border: 1px solid #EF4444;
  background: #FEF2F2;
  color: #991B1B;
}

.banner.small {
  margin-top: 0;
}

.site-delete {
  margin-left: auto;
  border: none;
  background: none;
  color: #999;
  font-size: 16px;
  cursor: pointer;
}

.site-delete:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.manager-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.manager-card h3 {
  margin: 0 0 14px 0;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #111;
  flex-shrink: 0;
}

.site-list {
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.site-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid #F0EDE8;
}

.site-item:last-child {
  border-bottom: none;
}

.site-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ccc; /* unknown by default */
  flex-shrink: 0;
}

.site-dot.ok {
  background: #22C55E;
}

.site-dot.fail {
  background: #EF4444;
}

.site-dot.unknown {
  background: #ccc;
}

.site-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.site-name {
  font-size: 12px;
  font-weight: 700;
  color: #111;
}

.site-url {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.empty-state {
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  color: #999;
  text-align: center;
  padding: 30px 0;
}

.add-site-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 14px;
  flex-shrink: 0;
  border-top: 1px solid #E8E3DE;
  padding-top: 14px;
}

.add-site-form input {
  border: 1px solid #E5E2DE;
  background: #fff;
  padding: 8px 10px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  outline: none;
}

.add-site-form input:focus {
  border-color: #111;
}

.add-site-form button {
  border: 1.5px solid #111;
  background: #111;
  color: #fff;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 9px 0;
  cursor: pointer;
  transition: background 0.15s ease;
}

.add-site-form button:hover {
  background: #333;
}

.add-site-form button:disabled {
  background: #999;
  border-color: #999;
  cursor: not-allowed;
}

@media (max-width: 480px) {
  .manager-card {
    padding: 14px;
    height: auto;
  }
}
</style>