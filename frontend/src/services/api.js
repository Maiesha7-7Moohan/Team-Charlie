import axios from "axios";

const api = axios.create({
    baseURL: "https://team-charlie-fch6.onrender.com/api",
});

export default api;