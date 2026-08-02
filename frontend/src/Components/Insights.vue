<template>
  <div class="pie-chart-card">
    <h3>Articles by Province</h3>
    <div class="pie-wrapper">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { Pie } from "vue-chartjs";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

const chartData = ref({
  labels: [],
  datasets: [
    {
      data: [],
      backgroundColor: [
        "#ff5a5f",
        "#2d9bff",
        "#22c55e",
        "#f59e0b",
        "#8b5cf6",
        "#06b6d4"
      ]
    }
  ]
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      position: "bottom"
    }
  }
};

onMounted(async () => {

  const response = await fetch("http://localhost:5000/api/articles");

  const articles = await response.json();

  const sourceCount = {};

  articles.forEach(article => {

    const source = article.source || "Unknown";

    sourceCount[source] = (sourceCount[source] || 0) + 1;

  });

  chartData.value = {

    labels: Object.keys(sourceCount),

    datasets: [
      {
        data: Object.values(sourceCount),

        backgroundColor: [
          "#ff5a5f",
          "#2d9bff",
          "#22c55e",
          "#f59e0b",
          "#8b5cf6",
          "#06b6d4"
        ]
      }
    ]
  };

});
</script>
<style scoped>
.pie-chart-card {
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
.pie-chart-card h3 {
  margin: 0 0 16px 0;
  height: 24px;
  flex-shrink: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
  line-height: 24px;
}
.pie-wrapper {
  position: relative;
  flex: 1;
  width: 100%;
  min-height: 0;
}
.pie-wrapper canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
