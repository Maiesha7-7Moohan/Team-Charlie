<template>
  <div class="manager-card">
    <h3>Manage Target Sites</h3>

    <ul class="site-list" v-if="websites.length">
      <li class="site-item" v-for="(site, index) in websites" :key="index">
        <span class="site-dot"></span>
        <div class="site-info">
          <span class="site-name">{{ site.name }}</span>
          <span class="site-url">{{ site.url }}</span>
        </div>
        <button type="button" class="site-delete" @click="removeSite(index)">&times;</button>
      </li>
    </ul>
    <p class="empty-state" v-else>No sites configured yet.</p>

    <form class="add-site-form" @submit.prevent="addSite">
      <input v-model="newName" placeholder="Site name" required />
      <input v-model="newUrl" placeholder="https://..." required />
      <button type="submit">+ Add Site</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const websites = ref([]);
const newName = ref("");
const newUrl = ref("");

async function loadWebsites() {
  const res = await api.get("/websites");
  websites.value = res.data;
}
async function addSite() {
  const res = await api.post("/websites", { name: newName.value, url: newUrl.value });
  websites.value.push(res.data);   // show it immediately, no re-fetch needed
  newName.value = ""; newUrl.value = "";
}

async function removeSite(index) {
  await api.delete(`/websites/${index}`);
  websites.value.splice(index, 1);  // remove it immediately
}
onMounted(loadWebsites);
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

.site-delete {
  margin-left: auto;
  border: none;
  background: none;
  color: #999;
  font-size: 16px;
  cursor: pointer;
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
  background: #22C55E;
  flex-shrink: 0;
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

@media (max-width: 480px) {
  .manager-card {
    padding: 14px;
    height: auto;
  }
}
</style>
