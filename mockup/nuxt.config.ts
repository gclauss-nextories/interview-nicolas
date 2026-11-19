export default defineNuxtConfig({
  compatibilityDate: '2026-10-01',
  telemetry: false,
  devtools: { enabled: false },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'One par Nextories',
      meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
    },
  },
})
