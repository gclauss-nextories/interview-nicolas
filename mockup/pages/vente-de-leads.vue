<script setup lang="ts">
import { ArrowRight, Plus } from 'lucide-vue-next'
import { initialZones } from '~/data/zones'
import { regionById } from '~/data/regions'
import { surfaceLabel } from '~/utils/surfaces'
import type { LeadRule, LeadZone, SurfaceThreshold } from '~/types/domain'

// État de session uniquement : rien n'est enregistré, un rechargement remet les valeurs initiales.
const zones = useState<LeadZone[]>('lead-zones', () => structuredClone(initialZones))
const regionModalOpen = ref(false)
const selectedRegionId = ref<string | null>(null)

// Les régions désactivées passent en bas de la liste.
const sortedZones = computed<LeadZone[]>(() => [...zones.value].sort((a, b) => Number(b.active) - Number(a.active)))
const configuredRegionIds = computed(() => zones.value.map((zone) => zone.regionId))
const selectedZone = computed(() => zones.value.find((zone) => zone.regionId === selectedRegionId.value) || null)

function thresholdLabel(threshold: SurfaceThreshold) {
  return surfaceLabel[threshold]
}
function addRegion(regionId: string, departments: string[], rule: LeadRule) {
  zones.value.push({ regionId, departments, active: true, rule })
  regionModalOpen.value = false
}
function saveRegion(departments: string[], rule: LeadRule) {
  const zone = selectedZone.value
  if (!zone) return
  zone.departments = departments
  zone.rule = rule
  selectedRegionId.value = null
}
</script>

<template>
  <AppShell active="leads">
    <div class="page-heading leads-heading">
      <div>
        <div class="regional-title-row">
          <h1>Leads</h1>
          <FlowHelp id="leads-help" label="Comprendre la vente de leads">
            Pilotez la vente de leads par région de départ. Sélectionnez les départements et les surfaces
            éligibles pour les distances Court, Moyen et Long. Chaque région possède ses propres règles.
          </FlowHelp>
        </div>
        <p>Choisissez une zone pour consulter et ajuster ses règles de vente.</p>
      </div>
      <FlowHistory />
    </div>

    <section class="zone-catalogue">
      <div class="zone-card-grid">
        <article v-for="zone in sortedZones" :key="zone.regionId">
          <div
            :class="['zone-card', { inactive: !zone.active }]"
            role="button"
            tabindex="0"
            @click="selectedRegionId = zone.regionId"
            @keydown.enter.self="selectedRegionId = zone.regionId"
          >
            <span class="zone-card-heading"
              ><span class="zone-card-title"
                ><strong>{{ regionById[zone.regionId]?.name }}</strong
                ><small>Départements {{ zone.departments.join(', ') }}</small></span
              ><button
                type="button"
                :class="['zone-status-switch', { on: zone.active }]"
                :aria-label="`${zone.active ? 'Désactiver' : 'Activer'} ${regionById[zone.regionId]?.name}`"
                :aria-pressed="zone.active"
                @click.stop="zone.active = !zone.active"
              >
                <span><i /></span><b>{{ zone.active ? 'On' : 'Off' }}</b>
              </button></span
            >
            <span class="zone-flow-preview">
              <span
                ><small>Court</small><b>{{ thresholdLabel(zone.rule.shortSurface) }}</b></span
              >
              <span
                ><small>Moyen</small><b>{{ thresholdLabel(zone.rule.mediumSurface) }}</b></span
              >
              <span
                ><small>Long</small><b>{{ thresholdLabel(zone.rule.longSurface) }}</b></span
              >
            </span>
            <span class="zone-card-footer"
              ><strong>Modifier les flux <ArrowRight :size="17" /></strong></span
            >
          </div>
        </article>
      </div>

      <div v-if="!zones.length" class="card empty-zones">
        <img src="/brand/icons/france.png" alt="" />
        <h3>Aucune zone trouvée</h3>
        <p>Ajoutez une région pour configurer ses flux.</p>
      </div>
    </section>
    <button class="button-primary floating-add" type="button" @click="regionModalOpen = true">
      <Plus :size="17" /> Ajouter une région
    </button>
    <AddRegionModal
      :open="regionModalOpen"
      :configured-region-ids="configuredRegionIds"
      @close="regionModalOpen = false"
      @save="addRegion"
    />
    <RegionFlowModal :zone="selectedZone" @close="selectedRegionId = null" @save="saveRegion" />
  </AppShell>
</template>

<style scoped>
.zone-catalogue {
  padding-bottom: 78px;
}
.floating-add {
  position: fixed;
  right: 36px;
  bottom: 28px;
  z-index: 25;
  min-height: 48px;
  box-shadow: 0 8px 24px rgba(37, 49, 99, 0.2);
}
@media (max-width: 700px) {
  .floating-add {
    right: 20px;
    bottom: max(20px, env(safe-area-inset-bottom));
  }
}

.regional-title-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.regional-title-row h1 {
  margin: 0;
}
</style>
