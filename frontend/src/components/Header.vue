<template>
  <header class="header">
    <div class="status-bar">
      <span>● Live</span>
      <span>South African News Analytics</span>
      <span>• 9 provinces tracked</span>
      <span>• Updated daily</span>
      <span>• Jul 2026</span>
    </div>

    <div class="dashboard-header-content">
      <h1>South African News Intelligence</h1>

      <p>
        Publication analytics across all nine provinces •
        Aug 2025 - Jul 2026
      </p>
    </div>

  </header>
</template>


<style scoped>

.header{
    width:100%;
    background:#ffffff;
    border-bottom:1px solid #d9d9d9;
}


.status-bar{
    background:#e53935;
    color:white;
    display:flex;
    border-radius: 20px;
    /* ---- */
    /* width: 100%;
    margin-top: -10px; */
    /* ---- */
    gap:18px;
    align-items:center;
    padding:8px 20px;
    font-size:12px;
    font-weight:500;
}


.dashboard-header-content{
    padding:20px;
}

.dashboard-header-content h1{
    font-size:34px;
    font-weight:700;
    margin-bottom:8px;
    color:#222;
}

.dashboard-header-content p{
    color:#777;
    font-size:14px;
}

</style>