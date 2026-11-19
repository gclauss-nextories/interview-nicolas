<script setup lang="ts">
import { ref } from 'vue'
import { Info } from 'lucide-vue-next'

defineProps<{ id: string; label: string }>()
const open = ref(false)
</script>

<template>
  <span class="flow-help" :class="{ open }" @keydown.esc="open = false">
    <button
      type="button"
      :aria-label="label"
      :aria-describedby="id"
      :aria-expanded="open"
      @click="open = !open"
      @blur="open = false"
    >
      <Info :size="18" />
    </button>
    <span :id="id" role="tooltip"><slot /></span>
  </span>
</template>

<style scoped>
.flow-help {
  position: relative;
  display: inline-flex;
}
.flow-help > button {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  color: var(--muted);
  background: transparent;
  cursor: pointer;
}
.flow-help > button:hover,
.flow-help > button:focus-visible {
  color: var(--navy);
  background: var(--surface);
}
.flow-help > button:focus-visible {
  outline: 2px solid var(--green);
  outline-offset: 2px;
}
.flow-help > span {
  position: absolute;
  top: calc(100% + 8px);
  left: -90px;
  z-index: 20;
  width: min(320px, calc(100vw - 64px));
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: white;
  color: var(--navy);
  box-shadow: var(--shadow);
  font-size: 12px;
  line-height: 1.7;
  visibility: hidden;
  opacity: 0;
}
.flow-help:hover > span,
.flow-help.open > span {
  visibility: visible;
  opacity: 1;
}
</style>
