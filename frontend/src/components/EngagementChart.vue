<template>
  <div class="chart-card">
    <h3>Reader Engagement Rate %</h3>

      <div class="chart-wrapper2">
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
  Legend
} from "chart.js";

import { Bar } from "vue-chartjs";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const chartData = {
  labels: ["FS", "NC", "NW", "MP", "LP", "EC", "KZN", "WC", "GP"],
  datasets: [
    {
      data: [11, 10, 8, 6.5, 6, 5.2, 4.2, 3.4, 2.6],
      backgroundColor: "#4CAF50",
      borderRadius: 4
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: "y",

  plugins: {
    legend: {
      display: false
    }
  },

  scales: {
    x: {
      beginAtZero: true,
      max: 12,
      ticks: {
        callback: (value) => value + "%"
      }
    },

    y: {
      grid: {
        display: false
      }
    }
  }
};
</script>

<style scoped>
.chart-wrapper2 {
    position:relative;
    width:100%;
    height:320px;
}

.chart-card{
    margin-left: 20px;
    margin-bottom: 20px;
    margin-top: 20px;
    height: 400px;
    padding: 20px;
    width: 700px;
    background-color: #F5F5F5;
    box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
}
</style>
