<template>
  <div class="table-card">
    <h3>Articles Published Per Day</h3>

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
          <td>{{ day.category }}</td>
          <td>{{ day.topSource }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";

const dailyStats = ref([]);

onMounted(async () => {
  try {
    const { data: articles } = await api.get("/items");
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
      .slice(0, 7); // Show only 7 rows
  } catch (err) {
    console.error("Error loading data:", err);
  }
});
</script>

<style scoped>
.table-card {
  margin-top: 20px;
  background-color: #f5f5f5;
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  /* background:#efefef; */
  padding: 12px;
  text-align: left;
}

td {
  padding: 12px;
  border-bottom: 1px solid #e5e5e5;
}

.growth {
  color: #2e7d32;
  font-weight: 600;
}
@media (max-width: 480px) {
  .table-card {
    padding: 10px;
  }

  th,
  td {
    padding: 8px;
  }
}
</style>
