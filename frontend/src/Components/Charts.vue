<template>
  <div class="chart-card">
    <h3>Articles Published by Province</h3>
    <div class="chart-wrapper">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
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
  Title,
);
const chartData = {
  labels: ["GP", "WC", "KZN", "EC", "LP", "MP", "NW", "FS", "NC"],
  datasets: [
    {
      label: "Articles",
      data: [52, 39, 28, 24, 22, 20, 17, 12, 6],
      backgroundColor: [
        "#ff5a1f",
        "#2d5bff",
        "#22c55e",
        "#7c3aed",
        "#facc15",
        "#ef4444",
        "#06b6d4",
        "#111",
        "#f97316",
      ],
      borderRadius: 4,
      barThickness: 24,
    },
  ],
};
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: { bottom: 15 } },
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { padding: 10 } },
    y: { beginAtZero: true, max: 60, ticks: { stepSize: 10 } },
  },
};
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
