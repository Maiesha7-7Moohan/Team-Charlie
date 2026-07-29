// src/api/fakearticles.js
import fakedata from "./fakedata.json";

export function getArticles() {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ data: fakedata });
    }, 500);
  });

  // REAL:
  // import axios from "axios";
  // return axios.get("http://localhost:3000/scraped-articles");
}
