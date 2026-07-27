<script setup>
import { ref, onMounted } from "vue";
import api from "./services/api";

const articles = ref([]);

onMounted(async () => {
  try {
    const response = await api.get("/items");
    articles.value = response.data;
  } catch (error) {
    console.error("Failed to load articles:", error);
  }
});
</script>

<template>
  <div class="container">
    <h1>Team Charlie News</h1>

    <div v-if="articles.length === 0">
      <p>No articles available.</p>
    </div>

    <div v-else>
      <div
        v-for="article in articles"
        :key="article.id"
        class="article"
      >
        <h2>{{ article.title }}</h2>

        <p><strong>Author:</strong> {{ article.author }}</p>

        <p><strong>Source:</strong> {{ article.source }}</p>

        <p><strong>Date:</strong> {{ article.date }}</p>

        <p>{{ article.summary }}</p>

        <hr>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
  font-family: Arial, sans-serif;
}

.article {
  margin-bottom: 20px;
}
</style>