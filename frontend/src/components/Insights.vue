<template>
  <div class="chart-card">
    <!-- <h3>Articles by Province</h3> -->

    <div class="chart-container">
      <Pie
        :data="chartData"
        :options="chartOptions"
      />
    </div>
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "vue-chartjs";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

const chartData = {
  labels: [
    "Gauteng",
    "Western Cape",
    "KwaZulu-Natal",
    "Eastern Cape",
    "Limpopo",
    "Mpumalanga"
  ],

  datasets: [
    {
      data: [52, 39, 28, 24, 22, 20],

      backgroundColor: [
        "#FF4D4F",
        "#36A2EB",
        "#4CAF50",
        "#FFC107",
        "#9C27B0",
        "#FF9800"
      ],

      borderWidth: 1
    }
  ]
};

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,

  plugins: {
    legend: {
      position: "bottom"
    }
  }
};
</script>

<style scoped>
.chart-card{
    padding: 20px;
    background-color: #F5F5F5;
    box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
}

.chart-container{
    width:95%;
    height:350px;
}
</style>