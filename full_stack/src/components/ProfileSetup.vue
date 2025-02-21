<template>
  <div class="h-screen flex flex-col items-center justify-center bg-gray-50">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Set Up Your Profile</h2>
    <form class="w-80 space-y-4" @submit.prevent="saveProfile">
      <!-- First and Last Name (User Model) -->
      <input v-model="user.first_name" type="text" placeholder="First Name" class="w-full px-4 py-2 border rounded-lg">
      <input v-model="user.last_name" type="text" placeholder="Last Name" class="w-full px-4 py-2 border rounded-lg">
      
      <!-- Profile Fields -->
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

    <!-- Matches List (Example) -->
    <div v-if="matches.length > 0">
      <h3 class="mt-8 text-lg">Your Matches</h3>
      <ul>
        <li v-for="match in matches" :key="match.id">
          {{ match.username }} (Match Score: {{ match.score }})
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import api, { fetchMatches } from '@/api/api';  // Import the fetchMatches function

export default {
  name: "ProfileSetup",
  data() {
    return {
      user: { first_name: "", last_name: "" },
      profile: { age: "", gender: "Other", location: "", job_title: "", specialty: "" },
      userId: null,
      profileId: null,
      matches: [],  // Array to store fetched matches
    };
  },
  async mounted() {
    await this.fetchProfile();
    await this.fetchMatches();  // Fetch matches when the component is mounted
  },
  methods: {
    // Fetch user data and profile
    async fetchProfile() {
      try {
        const userResponse = await api.get('current-user/');
        this.userId = userResponse.data.id;
        if (!this.userId) {
          console.error("User ID is null! Cannot fetch profile.");
          return;
        }
        this.user.first_name = userResponse.data.first_name;
        this.user.last_name = userResponse.data.last_name;

        const profileResponse = await api.get(`profiles/?user_id=${this.userId}`);
        if (profileResponse.data.length > 0) {
          this.profile = profileResponse.data[0];
          this.profileId = this.profile.id;
        } else {
          console.warn("No profile found.");
        }
      } catch (error) {
        console.error("Error fetching profile:", error.response ? error.response.data : error);
        alert("Failed to load profile.");
      }
    },

    // Fetch matches using the fetchMatches function
    async fetchMatches() {
      try {
        const matches = await fetchMatches();  // Call fetchMatches function from api.js
        this.matches = matches;  // Store the fetched matches in the component's data
      } catch (error) {
        console.error("Error fetching matches:", error);
        alert("Failed to fetch matches.");
      }
    },

    // Save the profile
    async saveProfile() {
      try {
        await api.put(`users/${this.userId}/`, this.user);

        if (this.profileId) {
          await api.put(`profiles/${this.profileId}/`, this.profile);
        } else {
          await api.post("profiles/", { ...this.profile, user: this.userId });
        }

        alert("Profile saved!");
      } catch (error) {
        console.error("Error saving profile:", error);
        alert("Failed to save profile. Please try again.");
      }
    }
  }
};
</script>
