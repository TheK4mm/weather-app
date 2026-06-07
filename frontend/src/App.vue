<script setup>
import { computed } from 'vue'
import { RouterView } from 'vue-router'

import { useWeather } from './composables/useWeather'

const { current } = useWeather()

// Fondo dinámico según el icono del clima actual (día/noche/condición).
const backgroundClass = computed(() => backgroundFor(current.value?.icon))

function backgroundFor(iconUrl) {
  if (!iconUrl) return 'bg-weather'
  if (iconUrl.includes('n@')) return 'bg-weather-night' // icono nocturno
  if (/\/(09|10|11)/.test(iconUrl)) return 'bg-weather-rain' // lluvia / tormenta
  if (/\/13/.test(iconUrl)) return 'bg-weather-snow' // nieve
  if (/\/(03|04|50)/.test(iconUrl)) return 'bg-weather-clouds' // nubes / niebla
  return 'bg-weather-clear' // despejado
}
</script>

<template>
  <div :class="['min-h-screen w-full transition-all duration-700', backgroundClass]">
    <RouterView />
  </div>
</template>
