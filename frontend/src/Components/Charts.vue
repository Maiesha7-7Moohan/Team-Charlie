<template>
  <div class="chart-card">
    <h3>Top 5 Categories</h3>
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
  Title,
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  Title
);

const chartData = ref({
  labels: [],
  datasets: [
    {
      label: "Articles",
      data: [],
      backgroundColor: [
        "#ff5a1f",
        "#2d5bff",
        "#22c55e",
        "#7c3aed",
        "#facc15",
      ],
      borderRadius: 4,
      barThickness: 20
    },
  ],
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    x: {
      grid: {
        display: false,
      },
    },
    y: {
      beginAtZero: true,
      ticks: {
        precision: 0,
      },
    },
  },
};

onMounted(async () => {
  try {
    const { data: articles } = await api.get("/items");

    const categoryCounts = {};

    articles.forEach((article) => {
      const category = article.category || "Uncategorized";
      categoryCounts[category] = (categoryCounts[category] || 0) + 1;
    });

    const topCategories = Object.entries(categoryCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    chartData.value = {
      labels: topCategories.map((item) => item[0]),
      datasets: [
        {
          label: "Articles",
          data: topCategories.map((item) => item[1]),
          backgroundColor: [
            "#ff5a1f",
            "#2d5bff",
            "#22c55e",
            "#7c3aed",
            "#facc15",
          ],
          borderRadius: 4,
        },
      ],
    };
  } catch (error) {
    console.error(error);
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
  background-color: #f5f5f5;
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
