import { createRouter, createWebHistory } from "vue-router";
import HomeView from "./views/HomeView.vue";
import AnalysisView from "./views/AnalysisView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/analysis/:id",
      name: "analysis",
      component: AnalysisView,
      props: true,
    },
  ],
});

export default router;
