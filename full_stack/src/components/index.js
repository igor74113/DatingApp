import Vue from "vue";
import VueRouter from "vue-router";
import HomeScreen from "@/components/HomeScreen.vue";
import LoginScreen from "@/components/LoginScreen.vue";
import ProfileSetup from "@/components/ProfileSetup.vue";
import MatchDiscovery from "@/components/MatchDiscovery.vue";
import ChatScreen from "@/components/ChatScreen.vue";
import SettingsScreen from "@/components/SettingsScreen.vue";

Vue.use(VueRouter);

const routes = [
  { path: "/", component: HomeScreen },
  { path: "/login", component: LoginScreen },
  { path: "/profile-setup", component: ProfileSetup },
  { path: "/match-discovery", component: MatchDiscovery },
  { path: "/chat", component: ChatScreen },
  { path: "/settings", component: SettingsScreen },
];

const router = new VueRouter({
  mode: "history", // Use history mode for clean URLs (e.g., "/login" instead of "#/login").
  routes,
});

export default router;
