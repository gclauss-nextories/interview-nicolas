<script setup lang="ts">
import { Check, Plus, Save, X } from 'lucide-vue-next'
import { regionById } from '~/data/regions'
import type { LeadRule, LeadZone } from '~/types/domain'

const props = defineProps<{ zone: LeadZone | null }>()
const emit = defineEmits<{ close: []; save: [departments: string[], rule: LeadRule] }>()
const departments = ref<string[]>([])
const draftRule = ref<LeadRule | null>(null)

watch(
  () => props.zone,
  (zone: LeadZone | null) => {
    if (zone) {
      departments.value = [...zone.departments]
      draftRule.value = { ...zone.rule }
    }
  },
)
const region = computed(() => (props.zone ? regionById[props.zone.regionId] : undefined))
function toggleDepartment(code: string) {
  departments.value = departments.value.includes(code)
    ? departments.value.filter((item: string) => item !== code)
    : [...departments.value, code]
}
function submit() {
  if (draftRule.value && departments.value.length)
    emit('save', [...departments.value].sort(), { ...draftRule.value })
}
</script>

<template>
  <Teleport to="body">
    <div v-if="zone && region && draftRule" class="modal-backdrop" @click.self="emit('close')">
      <section class="flow-modal" role="dialog" aria-modal="true" :aria-label="`Modifier ${region.name}`">
        <header>
          <div>
            <p class="eyebrow">Région administrative</p>
            <h2>{{ region.name }}</h2>
            <p>Modifiez les départements et les règles de vente de cette région.</p>
          </div>
          <button aria-label="Fermer" @click="emit('close')"><X :size="20" /></button>
        </header>
        <div class="flow-modal-content">
          <section class="modal-section">
            <div class="modal-section-title">
              <span>1</span>
              <div>
                <h3>Départements éligibles</h3>
                <p>Sélection limitée à la région administrative.</p>
              </div>
            </div>
            <div class="department-choice">
              <button
                v-for="department in region.departments"
                :key="department.code"
                :class="{ selected: departments.includes(department.code) }"
                @click="toggleDepartment(department.code)"
              >
                <b>{{ department.code }}</b
                ><span>{{ department.name }}</span
                ><Check v-if="departments.includes(department.code)" :size="15" /><Plus v-else :size="15" />
              </button>
            </div>
          </section>
          <section class="modal-section">
            <div class="modal-section-title">
              <span>2</span>
              <div>
                <h3>Court</h3>
                <p>Distance inférieure à 100 km.</p>
              </div>
            </div>
            <SurfaceSelector v-model="draftRule.shortSurface" />
          </section>
          <section class="modal-section">
            <div class="modal-section-title">
              <span>3</span>
              <div>
                <h3>Moyen</h3>
                <p>Distance comprise entre 100 et 299 km.</p>
              </div>
            </div>
            <SurfaceSelector v-model="draftRule.mediumSurface" />
          </section>
          <section class="modal-section">
            <div class="modal-section-title">
              <span>4</span>
              <div>
                <h3>Long</h3>
                <p>Distance de 300 km et plus.</p>
              </div>
            </div>
            <SurfaceSelector v-model="draftRule.longSurface" />
          </section>
        </div>
        <footer>
          <button class="button-secondary" @click="emit('close')">Annuler</button
          ><button class="button-primary" :disabled="!departments.length" @click="submit">
            <Save :size="16" /> Enregistrer
          </button>
        </footer>
      </section>
    </div>
  </Teleport>
</template>
