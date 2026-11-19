<script setup lang="ts">
import { Ban } from 'lucide-vue-next'
defineProps<{ active: 'overview' | 'premium' | 'online'; title: string }>()
</script>

<template>
  <AppShell :active="active">
    <div class="page-heading">
      <h1>{{ title }}</h1>
    </div>
    <div class="card out-of-scope">
      <Ban :size="30" />
      <h3>Hors périmètre fonctionnel</h3>
      <p>Cet écran ne fait pas partie de l’exercice.</p>
    </div>
  </AppShell>
</template>
