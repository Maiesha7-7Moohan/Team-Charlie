
<script setup>
import Header from "./components/Header.vue";
import Cards from "./components/Cards.vue";
import Charts from "./components/Charts.vue";
import EngagementChart from "./components/EngagementChart.vue";
import Insights from "./components/Insights.vue";
import ProvinceTable from "./components/ProvinceTable.vue";
// import FooterCards from "./components/FooterCards.vue";
</script>

<template>
  <div class="app">

    <Header />

    <main class="dashboard">

      <!-- Statistics Cards -->
      <Cards />

      <!-- Charts -->
      <section class="charts-row">
        <Charts />
        <EngagementChart />
      </section>

      <!-- Bottom Section -->
      <section class="bottom-row">
        <Insights />
        <ProvinceTable />
      </section>

      <!-- Footer Cards -->
      <FooterCards />
      <br><br><br><br><br><br><br><br><br><br><br><br>
      <div class="foot">
        <hr>
        <p>
          73 tracked outlets · Data sourced from public APIs · Updated daily
        </p>
      </div>

    </main>

  </div>
</template>

<style>

/* body{
  font-family: Arial, Helvetica, sans-serif;
  background:#ececec;
} */

.app{
  min-height:100vh;
} 


/* ---------- Charts ---------- */

.charts-row{
  display: flex;
  gap: 20px;
  margin:20px 0;
  padding: 20px;
}

/* ---------- Bottom Section ---------- */

.bottom-row{
  display:grid;
  padding: 10px 10px 10px 25px;
  grid-template-columns:1fr 2fr;
  gap:40px;
  margin:20px 0;
}

.foot p{
  color:#777;
  font-size:14px;
}

/* ---------- Responsive ---------- */

@media (max-width:992px){

  .charts-row{
    grid-template-columns:2fr;
  }

  .bottom-row{
    grid-template-columns:1fr;
  }

}

@media (max-width:768px){

  .dashboard{
    width:95%;
  }

}
</style>