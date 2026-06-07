import { defineStore } from 'pinia'

import { fetchWeather } from '../services/weatherApi'

/**
 * Store central del clima: única fuente de verdad para la SPA.
 * Mantiene el estado (clima, pronóstico, unidades, carga, error) y las
 * acciones para consultarlo. Los componentes no llaman al servicio HTTP
 * directamente, sino a través de estas acciones.
 */
export const useWeatherStore = defineStore('weather', {
  state: () => ({
    current: null,
    forecast: [],
    units: 'metric',
    city: '',
    loading: false,
    error: '',
  }),

  getters: {
    hasData: (state) => state.current !== null,
  },

  actions: {
    /** Busca el clima de una ciudad y actualiza el estado. */
    async search(city) {
      const query = (city ?? this.city).trim()
      if (!query) {
        this.error = 'Por favor, escribe una ciudad.'
        return
      }

      this.city = query
      this.loading = true
      this.error = ''

      try {
        const data = await fetchWeather(query, this.units)
        this.current = data.current
        this.forecast = data.forecast
        this.units = data.units
      } catch (err) {
        this.current = null
        this.forecast = []
        this.error = mapError(err)
      } finally {
        this.loading = false
      }
    },

    /** Alterna °C/°F y vuelve a consultar si ya hay una ciudad cargada. */
    async toggleUnits() {
      this.units = this.units === 'metric' ? 'imperial' : 'metric'
      if (this.city) {
        await this.search(this.city)
      }
    },
  },
})

/** Traduce un error de Axios/Backend a un mensaje amigable en español. */
function mapError(err) {
  const code = err?.response?.data?.code
  if (code === 'city_not_found') return 'No se encontró la ciudad. Revisa el nombre e inténtalo de nuevo.'
  if (code === 'missing_api_key') return 'El servidor no tiene configurada la API key de OpenWeatherMap.'
  if (code === 'upstream_error') return 'No se pudo obtener el clima ahora mismo. Intenta más tarde.'
  if (err?.response?.data?.detail) return err.response.data.detail
  if (err?.code === 'ECONNABORTED') return 'La solicitud tardó demasiado. Revisa tu conexión.'
  return 'Hubo un problema de conexión. ¿Está encendido el backend?'
}
