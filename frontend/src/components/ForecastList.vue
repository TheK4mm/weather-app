<script setup>
import ForecastDayCard from './ForecastDayCard.vue'

defineProps({
  days: { type: Array, default: () => [] },
  units: { type: String, default: 'metric' },
})
</script>

<template>
  <section v-if="days.length" class="rounded-2xl bg-white/15 p-4 backdrop-blur">
    <h3 class="mb-3 px-1 text-lg font-semibold text-white">Pronóstico</h3>
    <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
      <ForecastDayCard v-for="day in days" :key="day.date" :day="day" :units="units" />
    </div>
  </section>
</template>
