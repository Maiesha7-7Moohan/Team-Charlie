<template>
  <button
    type="button"
    class="scrape-fab"
    :disabled="scraping"
    @click="runScrape"
    :title="scraping ? 'Scraping…' : 'Scrape all sites now'"
  >
    <span class="fab-icon" :class="{ spin: scraping }">⟳</span>
    <span class="fab-label">{{ scraping ? "Scraping…" : "Scrape Now" }}</span>
  </button>

  <div v-if="toast" class="scrape-toast" :class="toast.type">
    {{ toast.message }}
  </div>
</template>

<script setup>
import { ref } from "vue";
import api from "../services/api";

const scraping = ref(false);
const toast = ref(null);

async function runScrape() {
  if (scraping.value) return;
  scraping.value = true;
  toast.value = null;

  try {
    const { data } = await api.post("/scrape", {});
    const failed = (data.results || []).filter((r) => !r.success);

    toast.value = failed.length
      ? { type: "warn", message: `Done, but ${failed.length} site(s) failed. Refreshing…` }
      : { type: "ok", message: "Scrape complete. Refreshing dashboard…" };

    // Simplest reliable way to get every dashboard card, chart, and the
    // article grid to reflect the freshly scraped data.
    setTimeout(() => window.location.reload(), 900);
  } catch (err) {
    console.error("Scrape failed:", err);
    toast.value = { type: "err", message: "Scrape failed. Check the backend/logs." };
    scraping.value = false;
  }
}
</script>

<style scoped>
.scrape-fab {
  position: fixed;
  right: 24px;
  bottom: 24px;
  z-index: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: #111;
  color: #fff;
  border: none;
  border-radius: 999px;
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25);
  transition: transform 0.15s ease, background 0.15s ease;
}

.scrape-fab:hover:not(:disabled) {
  transform: translateY(-2px);
  background: #222;
}

.scrape-fab:disabled {
  cursor: not-allowed;
  opacity: 0.85;
}

.fab-icon {
  font-size: 14px;
  display: inline-block;
}

.fab-icon.spin {
  animation: fab-spin 0.8s linear infinite;
}

@keyframes fab-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.scrape-toast {
  position: fixed;
  right: 24px;
  bottom: 76px;
  z-index: 500;
  padding: 10px 14px;
  background: #fff;
  border: 1.5px solid #111;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  max-width: 260px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.scrape-toast.ok { border-color: #22C55E; }
.scrape-toast.warn { border-color: #FACC15; }
.scrape-toast.err { border-color: #EF4444; }

@media (max-width: 480px) {
  .scrape-fab {
    right: 14px;
    bottom: 14px;
    padding: 10px 14px;
  }
  .fab-label {
    display: none; /* icon-only on very small screens */
  }
  .scrape-toast {
    right: 14px;
    left: 14px;
    max-width: none;
  }
}
</style>