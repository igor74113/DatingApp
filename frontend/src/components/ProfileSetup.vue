<template>
  <div class="h-screen flex flex-col items-center justify-center bg-gray-50">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Set Up Your Profile</h2>
    <form class="w-80 space-y-4" @submit.prevent="saveProfile">
      <input v-model="profile.age" type="number" placeholder="Age" class="w-full px-4 py-2 border rounded-lg">
      <select v-model="profile.gender" class="w-full px-4 py-2 border rounded-lg">
        <option value="Male">Male</option>
        <option value="Female">Female</option>
        <option value="Other">Other</option>
      </select>
      <input v-model="profile.location" type="text" placeholder="Location" class="w-full px-4 py-2 border rounded-lg">
      <input v-model="profile.job_title" type="text" placeholder="Job Title" class="w-full px-4 py-2 border rounded-lg">
      <input v-model="profile.specialty" type="text" placeholder="Specialty" class="w-full px-4 py-2 border rounded-lg">
      <button type="submit" class="w-full py-2 bg-green-500 text-white rounded-lg">Save Profile</button>
    </form>
  </div>
</template>

<script>
import api from '@/api/api'; 
import { useRouter } from 'vue-router';

export default {
  name: "ProfileSetup",
  data() {
    return {
      profile: { age: "", gender: "Other", location: "", job_title: "", specialty: "" },
      userId: null,
    };
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  async mounted() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        // Fetch current authenticated user
        const userResponse = await api.get('current-user/');
        this.userId = userResponse.data.id;

        // Fetch the profile dynamically
        const response = await api.get(`profiles/${this.userId}/`);
        this.profile = response.data;
      } catch (error) {
        console.error("Error fetching profile:", error);
        if (error.response && error.response.status === 401) {
          alert("You must log in first!");
          this.router.push('/login');  // Redirect to login if unauthorized
        }
      }
    },
    async saveProfile() {
      try {
        if (!this.profile.id) {
          alert("Error: Profile ID not found.");
          return;
        }
        await api.put(`profiles/${this.profile.id}/`, this.profile);
        alert("Profile saved!");
      } catch (error) {
        console.error("Error saving profile:", error);
        alert("Failed to save profile. Please try again.");
      }
    }
  }
};
</script>
