<script setup>
import { onMounted } from 'vue'

import { useWeather } from '../composables/useWeather'
import SearchBar from '../components/SearchBar.vue'
import CurrentWeatherCard from '../components/CurrentWeatherCard.vue'
import ForecastList from '../components/ForecastList.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorMessage from '../components/ErrorMessage.vue'

const { current, forecast, units, loading, error, hasData, search, toggleUnits } = useWeather()

// Ciudad de ejemplo al abrir la app.
onMounted(() => search('Bogotá'))
</script>

<template>
  <main class="mx-auto flex min-h-screen max-w-3xl flex-col items-center px-4 py-8">
    <h1 class="mb-6 text-3xl font-semibold text-white drop-shadow">⛅ App del Clima</h1>

    <SearchBar :units="units" :loading="loading" @search="search" @toggle-units="toggleUnits" />

    <LoadingSpinner v-if="loading" class="mt-12" />
    <ErrorMessage v-else-if="error" :message="error" class="mt-8 w-full max-w-xl" />

    <template v-else-if="hasData">
      <CurrentWeatherCard :data="current" :units="units" class="mt-8 w-full" />
      <ForecastList :days="forecast" :units="units" class="mt-6 w-full" />
    </template>
  </main>
</template>
