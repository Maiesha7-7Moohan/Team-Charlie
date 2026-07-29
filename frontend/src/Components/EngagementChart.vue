<template>
  <div class="chart-card">
    <h3>Reader Engagement Rate %</h3>
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
} from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);
import { Bar } from "vue-chartjs";
const chartData = {
  labels: ["FS", "NC", "NW", "MP", "LP", "EC", "KZN", "WC", "GP"],
  datasets: [
    {
      data: [11, 10, 8, 6.5, 6, 5.2, 4.2, 3.4, 2.6],
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
};
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: "y",
  plugins: { legend: { display: false } },
  scales: {
    x: { beginAtZero: true, max: 12, ticks: { callback: (v) => v + "%" } },
    y: { grid: { display: false } },
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
