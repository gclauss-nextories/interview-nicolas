<script setup lang="ts">
import { ArrowLeft, ArrowRight, Check, Plus, X } from 'lucide-vue-next'
import { administrativeRegions } from '~/data/regions'
import type { LeadRule } from '~/types/domain'

const props = defineProps<{ open: boolean; configuredRegionIds: string[] }>()
const emit = defineEmits<{ close: []; save: [regionId: string, departments: string[], rule: LeadRule] }>()

const defaultRule = (): LeadRule => ({
  shortSurface: '30-50',
  mediumSurface: 'lt30',
  longSurface: 'disabled',
})
const step = ref(1)
const selectedRegionId = ref('')
const selectedDepartments = ref<string[]>([])
const rule = ref<LeadRule>(defaultRule())
const eligibleRegions = computed(() =>
  administrativeRegions.filter((region) => !props.configuredRegionIds.includes(region.id)),
)
const selectedRegion = computed(() =>
  administrativeRegions.find((region) => region.id === selectedRegionId.value),
)

watch(
  () => props.open,
  (open: boolean) => {
    if (open) {
      step.value = 1
      selectedRegionId.value = ''
      selectedDepartments.value = []
      rule.value = defaultRule()
    }
  },
)
watch(selectedRegionId, () => {
  selectedDepartments.value = []
})
function toggleDepartment(code: string) {
  selectedDepartments.value = selectedDepartments.value.includes(code)
    ? selectedDepartments.value.filter((item: string) => item !== code)
    : [...selectedDepartments.value, code]
}
function submit() {
  if (!selectedRegion.value || !selectedDepartments.value.length) return
  emit('save', selectedRegion.value.id, [...selectedDepartments.value].sort(), { ...rule.value })
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="modal-backdrop" @click.self="emit('close')">
      <section
        :class="['department-modal', 'add-region-modal', { 'flows-step': step === 2 }]"
        role="dialog"
        aria-modal="true"
        aria-label="Ajouter une région"
      >
        <header>
          <div>
            <p class="eyebrow">Étape {{ step }} sur 2</p>
            <h2>Ajouter une région</h2>
            <p>
              {{
                step === 1
                  ? 'Choisissez la région et ses départements éligibles.'
                  : 'Configurez les premiers flux avant son activation.'
              }}
            </p>
          </div>
          <button aria-label="Fermer" @click="emit('close')"><X :size="20" /></button>
        </header>
        <div v-if="step === 1" class="region-form">
          <label
            ><small>Région</small
            ><select v-model="selectedRegionId">
              <option value="" disabled>Sélectionner une région</option>
              <option v-for="region in eligibleRegions" :key="region.id" :value="region.id">
                {{ region.name }}
              </option>
            </select></label
          >
          <div v-if="selectedRegion" class="eligible-departments">
            <small>Départements éligibles</small>
            <div>
              <button
                v-for="department in selectedRegion.departments"
                :key="department.code"
                :class="{ selected: selectedDepartments.includes(department.code) }"
                @click="toggleDepartment(department.code)"
              >
                <span
                  ><b>{{ department.code }}</b
                  >{{ department.name }}</span
                ><Check v-if="selectedDepartments.includes(department.code)" :size="16" /><Plus
                  v-else
                  :size="16"
                />
              </button>
            </div>
          </div>
        </div>
        <div v-else class="initial-flow-form">
          <section>
            <div>
              <small>Court</small>
              <p>Distance inférieure à 100 km</p>
            </div>
            <SurfaceSelector v-model="rule.shortSurface" />
          </section>
          <section>
            <div>
              <small>Moyen</small>
              <p>Distance comprise entre 100 et 299 km</p>
            </div>
            <SurfaceSelector v-model="rule.mediumSurface" />
          </section>
          <section>
            <div>
              <small>Long</small>
              <p>Distance de 300 km et plus</p>
            </div>
            <SurfaceSelector v-model="rule.longSurface" />
          </section>
        </div>
        <footer>
          <button v-if="step === 1" class="button-secondary" @click="emit('close')">Annuler</button
          ><button v-else class="button-secondary" @click="step = 1"><ArrowLeft :size="16" /> Retour</button
          ><button
            v-if="step === 1"
            class="button-primary"
            :disabled="!selectedRegion || !selectedDepartments.length"
            @click="step = 2"
          >
            Configurer les flux <ArrowRight :size="16" /></button
          ><button v-else class="button-primary" @click="submit">
            <Plus :size="16" /> Ajouter la région
          </button>
        </footer>
      </section>
    </div>
  </Teleport>
</template>
