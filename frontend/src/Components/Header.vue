<template>
  <header class="header">
    <div class="status-bar">
      <span>● Live</span>
      <span>Lightning News Analytics</span>
      <span>• 9 provinces tracked</span>
      <span>• Updated daily</span>
      <span>• Jul 2026</span>
    </div>

    <div class="dashboard-header-content">
      <h1>Lightning News</h1>

      <p>
        Publication analytics across all nine provinces • Aug 2025 - Jul 2026
      </p>
    </div>
  </header>
</template>

<style scoped>
.header {
  width: 100%;
  background: #fefefd;
  border-bottom: 1px solid #111;
}

.status-bar {
  height: 36px;
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 0 16px;
  background: #fefefd;
  border-bottom: 1px solid #e5e2de;
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #666;
  width: 100%;
  box-sizing: border-box;
}

.status-bar span:first-child {
  color: #111;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 700;
}

.status-bar span:first-child::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  display: inline-block;
}

.dashboard-header-content {
  padding: 24px 16px 20px;
  background: #f7f7f5;
}

.dashboard-header-content h1 {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: -0.02em;
  color: #111;
  margin: 0 0 8px;
}

.dashboard-header-content p {
  font-family: "IBM Plex Mono", monospace;
  font-size: 11px;
  line-height: 1.5;
  color: #666;
  margin: 0;
}
</style>
