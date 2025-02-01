import { createRouter, createWebHistory } from "vue-router";
import HomeScreen from "@/components/HomeScreen.vue";
import LoginScreen from "@/components/LoginScreen.vue";
import ProfileSetup from "@/components/ProfileSetup.vue";
import MatchDiscovery from "@/components/MatchDiscovery.vue";
import ChatScreen from "@/components/ChatScreen.vue";
import SettingsScreen from "@/components/SettingsScreen.vue";

const routes = [
  { path: "/", component: HomeScreen },
  { path: "/login", component: LoginScreen },
  { path: "/profile-setup", component: ProfileSetup },
  { path: "/match-discovery", component: MatchDiscovery },
  { path: "/chat", component: ChatScreen },
  { path: "/settings", component: SettingsScreen },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
