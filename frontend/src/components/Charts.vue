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
  Title
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

const chartData = {
  labels: ["GP", "WC", "KZN", "EC", "LP", "MP", "NW", "FS", "NC"],
  datasets: [
    {
      label: "Articles",
      data: [52, 39, 28, 24, 22, 20, 17, 12, 6],
      backgroundColor: "#ff4d4f",
      borderRadius: 4,
      barThickness: 24
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  layout: {
    padding: {
      bottom: 15
    }
  },

  plugins: {
    legend: {
      display: false
    }
  },

  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        padding: 10
      }
    },

    y: {
      beginAtZero: true,
      max: 60,
      ticks: {
        stepSize: 10
      }
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
    position: relative;
    height: 280px;
    width: 100%;
}

.chart-card{
    margin-left: 20px;
    margin-bottom: 20px;
    margin-top: 20px;
    height: 360px;
    padding: 20px;
    width: 50%;
    background-color: #F5F5F5;
    box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
}

.chart-card h3 {
  margin-bottom: 20px;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}
</style>