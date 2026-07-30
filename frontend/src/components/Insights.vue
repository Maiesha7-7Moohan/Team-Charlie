<template>
  <div class="pie-chart-card">
    <h3>Articles by Province</h3>
    <div class="pie-wrapper">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>
<script setup>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import { Pie } from "vue-chartjs";
ChartJS.register(ArcElement, Tooltip, Legend);
const chartData = {
  labels: [
    "Gauteng",
    "Western Cape",
    "KwaZulu-Natal",
    "Eastern Cape",
    "Limpopo",
    "Mpumalanga",
  ],
  datasets: [
    {
      data: [52, 39, 28, 24, 22, 20],
      backgroundColor: [
        "#ff5a1f",
        "#2d5bff",
        "#22c55e",
        "#7c3aed",
        "#facc15",
        "#111111",
      ],
      borderWidth: 1,
    },
  ],
};
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: "bottom" } },
};
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