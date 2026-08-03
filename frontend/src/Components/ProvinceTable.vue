<template>
  <div class="table-card">
    <h3>Articles Published Per Day</h3>

    <div class="table-scroll" v-if="dailyStats.length">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Articles</th>
            <th>Sources</th>
            <th>Top Category</th>
            <th>Top Source</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="day in dailyStats" :key="day.date">
            <td>{{ day.date }}</td>
            <td>{{ day.articles }}</td>
            <td>{{ day.sources }}</td>
            <td><span class="pill">{{ day.category }}</span></td>
            <td><span class="pill">{{ day.topSource }}</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    <p class="empty-state" v-else>No data yet — run a scrape to populate this table.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const dailyStats = ref([]);

onMounted(async () => {
  try {
    const { data: { items: articles } } = await api.get("/items?limit=1000");
    const stats = {};

    articles.forEach((article) => {
      if (!article.published) return;

      const date = article.published.split(" ")[0];

      if (!stats[date]) {
        stats[date] = {
          date: date,
          articles: 0,
          sources: new Set(),
          category: article.category || "Unknown",
          sourceCount: {},
        };
      }

      stats[date].articles++;
      stats[date].sources.add(article.source || "Unknown");

      const source = article.source || "Unknown";
      stats[date].sourceCount[source] =
        (stats[date].sourceCount[source] || 0) + 1;
    });

    dailyStats.value = Object.values(stats)
      .map((day) => ({
        date: day.date,
        articles: day.articles,
        sources: day.sources.size,
        category: day.category,
        topSource: Object.keys(day.sourceCount).reduce((a, b) =>
          day.sourceCount[a] > day.sourceCount[b] ? a : b
        ),
      }))
      .sort((a, b) => new Date(b.date) - new Date(a.date))
      .slice(0, 7);
  } catch (err) {
    console.error("Error loading data:", err);
  }
});
</script>

<style scoped>
.table-card {
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

.table-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.table-card h3 {
  margin: 0 0 14px 0;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: -0.01em;
  color: #111;
  flex-shrink: 0;
}

.table-scroll {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-family: "IBM Plex Mono", monospace;
}

thead th {
  position: sticky;
  top: 0;
  background: #FEFEFD;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #999;
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1px solid #111;
}

tbody td {
  font-size: 11px;
  color: #333;
  padding: 9px 10px;
  border-bottom: 1px solid #F0EDE8;
  white-space: nowrap;
}

tbody tr:hover td {
  background: #F7F7F5;
}

tbody tr:last-child td {
  border-bottom: none;
}

.pill {
  display: inline-block;
  font-size: 8px;
  font-weight: 800;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 3px 7px;
  border: 1px solid #111;
  background: #fff;
  color: #111;
}

.empty-state {
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  color: #999;
  text-align: center;
  padding: 40px 0;
}

@media (max-width: 480px) {
  .table-card {
    padding: 14px;
    height: auto;
  }
  thead th,
  tbody td {
    padding: 6px 8px;
  }
}
</style>
