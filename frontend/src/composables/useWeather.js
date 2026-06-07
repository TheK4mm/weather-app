import { storeToRefs } from 'pinia'

import { useWeatherStore } from '../stores/weather'

/**
 * Composable que expone el estado y las acciones del clima a los componentes,
 * preservando la reactividad de Pinia (storeToRefs). Es el punto de entrada
 * reutilizable que usan las vistas.
 */
export function useWeather() {
  const store = useWeatherStore()
  const { current, forecast, units, city, loading, error, hasData } = storeToRefs(store)

  return {
    // Estado reactivo
    current,
    forecast,
    units,
    city,
    loading,
    error,
    hasData,
    // Acciones
    search: store.search,
    toggleUnits: store.toggleUnits,
  }
}
