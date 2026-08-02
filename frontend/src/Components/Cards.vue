<template>
  <div class="dashboard-card-container">
    <div class="dashboard-card1">
      <p>Total Articles</p>
      <h2>{{ totalArticles }}</h2>
      <p>Articles collected</p>
    </div>

    <div class="dashboard-card2">
      <p>News Sources</p>
      <h2>{{ totalSources }}</h2>
      <p>Active publishers</p>
    </div>

    <div class="dashboard-card3">
      <p>Categories</p>
      <h2>{{ totalCategories }}</h2>
      <p>Content categories</p>
    </div>

    <div class="dashboard-card4">
      <p>Latest Publication</p>
      <h2>{{ latestDate }}</h2>
      <p>Most recent article</p>
    </div>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";

const totalArticles = ref(0);
const totalSources = ref(0);
const totalCategories = ref(0);
const latestDate = ref("-");

onMounted(async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/items");

    if (!response.ok) {
      throw new Error("Failed to fetch articles");
    }

    const articles = await response.json();

    totalArticles.value = articles.length;


    totalSources.value = new Set(
      articles.map(article => article.source)
    ).size;


    totalCategories.value = new Set(
      articles.map(article => article.category)
    ).size;

    const validDates = articles
      .filter(article => article.published)
      .map(article => article.published);

    if (validDates.length > 0) {
      validDates.sort((a, b) => new Date(b) - new Date(a));
      latestDate.value = validDates[0].split(" ")[0];
    }
  } catch (err) {
    console.error("Error loading dashboard cards:", err);
  }
});
</script>

<style scoped>
.dashboard-card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
  padding: 16px;
  background: #f7f7f5;
}

.dashboard-card1,
.dashboard-card2,
.dashboard-card3,
.dashboard-card4 {
  background: #fefefd;
  border: 1px solid #e8e3de;
  padding: 16px 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 122px;
  position: relative;
  overflow: hidden;
  transition: all 0.18s ease;
  cursor: default;
}

.dashboard-card1:hover,
.dashboard-card2:hover,
.dashboard-card3:hover,
.dashboard-card4:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

/* first <p> = label */
.dashboard-card-container p:first-of-type {
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #999;
  margin: 0;
}

.dashboard-card-container h2 {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: #111;
  margin: 2px 0 0;
  font-family: inherit;
}

/* second <p> = meta/value */
.dashboard-card-container p:last-of-type {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  color: #666;
  margin: auto 0 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dashboard-card1 p:last-of-type::before,
.dashboard-card2 p:last-of-type::before,
.dashboard-card3 p:last-of-type::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  display: inline-block;
}

.dashboard-card4 p:last-of-type::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #ff5a1f;
  border-radius: 50%;
  display: inline-block;
}
</style>
