<template>
  <div class="chart-card">
    <h3>Top Authors</h3>
    <div class="chart-wrapper">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: "Articles",
      data: [],
      backgroundColor: [
        "#7c3aed",
        "#2d5bff",
        "#06b6d4",
        "#22c55e",
        "#facc15",
        "#f97316",
        "#ff5a1f",
        "#ef4444",
        "#111",
      ],
      borderRadius: 4,
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: "y",
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      beginAtZero: true,
      ticks: {
        precision: 0,
      },
    },
    y: {
      grid: {
        display: false,
      },
    },
  },
};

onMounted(async () => {
  try {
    const { data: { items: articles } } = await api.get("/items?limit=1000");

    const authorCounts = {};

    articles.forEach((article) => {
      const author = article.author || "Unknown";
      authorCounts[author] = (authorCounts[author] || 0) + 1;
    });

    // Keep only the top 10 authors
    const sortedAuthors = Object.entries(authorCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    chartData.value = {
      labels: sortedAuthors.map((item) => item[0]),
      datasets: [
        {
          label: "Articles",
          data: sortedAuthors.map((item) => item[1]),
          backgroundColor: [
            "#7c3aed",
            "#2d5bff",
            "#06b6d4",
            "#22c55e",
            "#facc15",
            "#f97316",
            "#ff5a1f",
            "#ef4444",
            "#111",
            "#6b7280",
          ],
          borderRadius: 4,
        },
      ],
    };
  } catch (error) {
    console.error("Error loading authors:", error);
  }
});
</script>
<style scoped>
.chart-card {
  margin-top: 20px;
  flex: 1 1 0;
  min-width: 350px;
  height: 420px;
  display: flex;
  flex-direction: column;
  width: 100%;
  background: #f5f5f5;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
  box-sizing: border-box;
  overflow: hidden;
}

.chart-card h3 {
  margin: 0 0 16px 0;
  height: 24px;
  flex-shrink: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
  line-height: 24px;
}

.chart-wrapper {
  position: relative;
  flex: 1;
  width: 100%;
  min-height: 0;
}

.chart-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
