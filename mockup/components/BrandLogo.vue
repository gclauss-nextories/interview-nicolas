<script setup lang="ts">
withDefaults(defineProps<{ full?: boolean; inverse?: boolean }>(), { full: false, inverse: false })
</script>

<template>
  <span
    :class="['brand-logo', { 'brand-logo-full': full, 'brand-logo-inverse': inverse }]"
    role="img"
    :aria-label="full ? 'Nextories One' : 'One'"
  >
    <svg v-if="full" class="brand-wordmark" viewBox="610 130 1460 320" aria-hidden="true">
      <image href="/brand/nextories-logo.png" width="2158" height="629" />
    </svg>
    <svg class="brand-symbol" viewBox="80 70 500 480" aria-hidden="true">
      <image href="/brand/nextories-logo.png" width="2158" height="629" />
    </svg>
    <strong>One</strong>
  </span>
</template>

<style scoped>
.brand-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  line-height: 1;
  color: #1c2b68;
}
.brand-symbol {
  width: 43px;
  height: auto;
  display: block;
  flex-shrink: 0;
}
.brand-logo > strong {
  font-size: 32px;
  font-weight: 500;
  letter-spacing: -1px;
}
.brand-logo-full {
  gap: 8px;
  width: min(310px, calc(100vw - 84px));
}
.brand-logo-full .brand-wordmark {
  width: 57%;
  height: auto;
  display: block;
  flex-shrink: 0;
}
.brand-logo-full .brand-symbol {
  width: 17%;
}
.brand-logo-full > strong {
  font-size: clamp(24px, 3vw, 30px);
}
.brand-logo-inverse {
  color: white;
}
.brand-logo-inverse svg {
  filter: brightness(0) invert(1);
}
</style>
