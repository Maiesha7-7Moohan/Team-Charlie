<script setup>
import Header from "./components/Header.vue";
import Cards from "./components/Cards.vue";
</script>

<template>
  <div class="app">
    <Header />

    <main class="dashboard">
      <Cards />

      <Charts />
    </main>
  </div>
</template>
