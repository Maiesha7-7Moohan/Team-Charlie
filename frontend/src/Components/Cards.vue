<template>
  <div class="dashboard-card-container">
    <div class="dashboard-card1">
      <p>Total Articles</p>
      <h2>146.2k</h2>
      <p>+4.1%all provinces</p>
    </div>
    <div class="dashboard-card2">
      <p>Total Pageviews</p>
      <h2>45.6M</h2>
      <p>+5.9%trailing 12 months</p>
    </div>
    <div class="dashboard-card3">
      <p>Active Outlets</p>
      <h2>71</h2>
      <p>+3.4%tracked nationally</p>
    </div>
    <div class="dashboard-card4">
      <p>Avg Engagement</p>
      <h2>6.2%</h2>
      <p>-0.3%shares + comments</p>
    </div>
  </div>
</template>

<style scoped>
.dashboard-card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
  padding: 16px;
  background: #f7f7f5;
}

.dashboard-card1,
.dashboard-card2,
.dashboard-card3,
.dashboard-card4 {
  background: #fefefd;
  border: 1px solid #e8e3de;
  padding: 16px 16px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 122px;
  position: relative;
  overflow: hidden;
  transition: all 0.18s ease;
  cursor: default;
}

.dashboard-card1:hover,
.dashboard-card2:hover,
.dashboard-card3:hover,
.dashboard-card4:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

/* first <p> = label */
.dashboard-card-container p:first-of-type {
  font-family: "IBM Plex Mono", monospace;
  font-size: 9px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #999;
  margin: 0;
}

.dashboard-card-container h2 {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: #111;
  margin: 2px 0 0;
  font-family: inherit;
}

/* second <p> = meta/value */
.dashboard-card-container p:last-of-type {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  color: #666;
  margin: auto 0 0;
  display: flex;
  align-items: center;
  gap: 6px;
}

.dashboard-card1 p:last-of-type::before,
.dashboard-card2 p:last-of-type::before,
.dashboard-card3 p:last-of-type::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #22c55e;
  border-radius: 50%;
  display: inline-block;
}

.dashboard-card4 p:last-of-type::before {
  content: "";
  width: 6px;
  height: 6px;
  background: #ff5a1f;
  border-radius: 50%;
  display: inline-block;
}
</style>
