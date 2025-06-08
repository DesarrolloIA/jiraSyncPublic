<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm">
      <div class="w-full px-4 sm:px-6 lg:px-8 xl:px-12">
        <div class="flex items-center justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">Jira Sync App</h1>
          </div>
          
          <nav class="flex space-x-8">
            <RouterLink 
              to="/" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              active-class="text-indigo-600 bg-indigo-50"
            >
              Home
            </RouterLink>
            <RouterLink 
              to="/jira-sync" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              active-class="text-indigo-600 bg-indigo-50"
            >
              Jira Sync
            </RouterLink>
            <RouterLink 
              to="/about" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              active-class="text-indigo-600 bg-indigo-50"
            >
              About
            </RouterLink>
            <RouterLink 
              to="/docs" 
              class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
              active-class="text-indigo-600 bg-indigo-50"
            >
              Docs
            </RouterLink>
          </nav>
        </div>
    </div>
  </header>

    <main class="w-full">
  <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* Custom styles if needed */
</style>
