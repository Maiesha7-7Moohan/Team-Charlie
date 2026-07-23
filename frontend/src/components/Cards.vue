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
        flex-wrap: wrap;
        margin-top: 20px;
        display: flex;
        justify-content: center;
        gap: 30px;
        padding: 10px;
    }

    .dashboard-card-container h2{
        font-size:23px;
        color:#222;
    }

    .dashboard-card-container p {
        color:#777;
        font-size:14px;
    }

    .dashboard-card1 {
        padding: 20px;
        width: 300px;
        background-color: #F5F5F5;
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
    }

    .dashboard-card2 {
        padding: 20px;
        width: 300px;
        background-color: #F5F5F5;
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
    }

    .dashboard-card3 {
        padding: 20px;
        width: 300px;
        background-color: #F5F5F5;
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
    }

    .dashboard-card4 {
        padding: 20px;
        width: 300px;
        background-color: #F5F5F5;
        box-shadow: 2px 4px 8px rgba(0, 0, 0, 0.15);
    }
</style>