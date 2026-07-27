<template>
  <div class="pie-chart-card">
    <!-- <h3>Articles by Province</h3> -->

    <div class="pie-wrapper">
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
.pie-chart-card{
    flex: 1;
    min-width: 320px;
    width: 100%;
    background: #F5F5F5;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 2px 4px 8px rgba(0,0,0,.15);
    box-sizing: border-box;
    overflow: hidden;
}

.pie-wrapper{
    position: relative;
    width: 100%;
    height: 450px;
}

.pie-wrapper canvas{
    width:100% !important;
    height:100% !important;
}
</style>