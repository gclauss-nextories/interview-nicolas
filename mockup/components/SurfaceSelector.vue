<script setup lang="ts">
import type { SurfaceThreshold } from '~/types/domain'
import { surfaceOptions as options } from '~/utils/surfaces'

const model = defineModel<SurfaceThreshold>({ required: true })
const selectedIndex = computed(() => options.findIndex((option) => option.value === model.value))
const previousValue = model.value
</script>

<template>
  <div class="surface-selector">
    <div class="selector-rail" />
    <button
      v-for="(option, index) in options"
      :key="option.value"
      type="button"
      :class="[
        'selector-stop',
        {
          selected: model === option.value,
          included: index <= selectedIndex,
          previous: option.value === previousValue && model !== previousValue,
        },
      ]"
      :aria-pressed="model === option.value"
      :title="option.value === previousValue && model !== previousValue ? 'Réglage précédent' : undefined"
      @click="model = option.value"
    >
      <span /><small>{{ option.label }}</small>
    </button>
  </div>
</template>
