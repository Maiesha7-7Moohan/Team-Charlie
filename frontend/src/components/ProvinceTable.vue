<template>
  <div class="table-card">
    <h3>Province Performance</h3>

    <table>
      <thead>
        <tr>
          <th>Province</th>
          <th>Articles</th>
          <th>Views</th>
          <th>Outlets</th>
          <th>Growth</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="province in provinces" :key="province.name">
          <td>{{ province.name }}</td>
          <td>{{ province.articles }}</td>
          <td>{{ province.views }}</td>
          <td>{{ province.outlets }}</td>
          <td class="growth">{{ province.growth }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const provinces = [
  {
    name: "Gauteng",
    articles: "52.1K",
    views: "18.6M",
    outlets: 18,
    growth: "+11%",
  },

  {
    name: "Western Cape",
    articles: "39.0K",
    views: "12.8M",
    outlets: 14,
    growth: "+9%",
  },

  {
    name: "KwaZulu-Natal",
    articles: "28.4K",
    views: "8.9M",
    outlets: 10,
    growth: "+8%",
  },

  {
    name: "Eastern Cape",
    articles: "24.1K",
    views: "6.3M",
    outlets: 8,
    growth: "+6%",
  },

  {
    name: "Limpopo",
    articles: "22.0K",
    views: "5.5M",
    outlets: 7,
    growth: "+5%",
  },

  {
    name: "Mpumalanga",
    articles: "7,210",
    views: "1.8M",
    outlets: 4,
    growth: "+2.4%",
  },

  {
    name: "North West",
    articles: "6,430",
    views: "1.6M",
    outlets: 4,
    growth: "+1.2%",
  },

  {
    name: "Free State",
    articles: "5,870",
    views: "1.4M",
    outlets: 3,
    growth: "+0.6%",
  },

  {
    name: "Northern Cape",
    articles: "3,180",
    views: "740.0K",
    outlets: 2,
    growth: "+5.3%",
  },
];
</script>

<style scoped>
.table-card {
  margin-top: 20px;
  background-color: #f5f5f5;
  box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  /* background:#efefef; */
  padding: 12px;
  text-align: left;
}

td {
  padding: 12px;
  border-bottom: 1px solid #e5e5e5;
}

.growth {
  color: #2e7d32;
  font-weight: 600;
}
@media (max-width: 480px) {
  .table-card {
    padding: 10px;
  }

  th,
  td {
    padding: 8px;
  }
}
</style>