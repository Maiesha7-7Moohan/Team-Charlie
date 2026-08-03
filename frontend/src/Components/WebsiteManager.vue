<template>
  <div class="website-manager">
    <h3>Manage Target Sites</h3>
    <ul>
      <li v-for="site in websites" :key="site.url">{{ site.name }} — {{ site.url }}</li>
    </ul>
    <form @submit.prevent="addSite">
      <input v-model="newName" placeholder="Site name" required />
      <input v-model="newUrl" placeholder="https://..." required />
      <button type="submit">Add Site</button>
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
  await api.post("/websites", { name: newName.value, url: newUrl.value });
  newName.value = ""; newUrl.value = "";
  await loadWebsites();
}
onMounted(loadWebsites);
</script>