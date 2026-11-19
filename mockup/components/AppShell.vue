<script setup lang="ts">
import { LayoutDashboard } from 'lucide-vue-next'
defineProps<{ active: 'overview' | 'leads' | 'premium' | 'online' }>()
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <NuxtLink to="/" class="brand" aria-label="One Nextories">
        <BrandLogo />
      </NuxtLink>

      <nav>
        <p class="nav-section-label">Pilotage</p>
        <NuxtLink to="/" :class="['nav-link nav-primary', { active: active === 'overview' }]"
          ><LayoutDashboard :size="18" /> Vue d’ensemble</NuxtLink
        >

        <div :class="['nav-group', { current: active === 'leads' }]">
          <div class="nav-submenu">
            <NuxtLink to="/vente-de-leads" :class="['nav-submenu-link', { active: active === 'leads' }]"
              ><i /> <span><b>Leads</b><small>Règles par zone</small></span></NuxtLink
            >
            <NuxtLink to="/premium" :class="['nav-submenu-link', { active: active === 'premium' }]"
              ><i /><span><b>Premium</b><small>Rendez-vous et visites</small></span></NuxtLink
            >
            <NuxtLink to="/online" :class="['nav-submenu-link', { active: active === 'online' }]"
              ><i /><span><b>Online</b><small>Parcours autonome</small></span></NuxtLink
            >
          </div>
        </div>
      </nav>
    </aside>

    <section class="workspace">
      <main><slot /></main>
    </section>
  </div>
</template>
