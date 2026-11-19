<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import { History, X } from 'lucide-vue-next'

const open = ref(false)
const dialog = ref<HTMLDialogElement | null>(null)
watch(open, async (value) => {
  await nextTick()
  if (value) dialog.value?.showModal()
  else dialog.value?.close()
})
</script>

<template>
  <div class="history-trigger-wrap">
    <button
      class="history-trigger"
      type="button"
      aria-label="Historique des modifications"
      title="Historique des modifications"
      @click="open = true"
    >
      <History :size="20" />
    </button>
    <Teleport to="body">
      <dialog
        ref="dialog"
        class="history-dialog"
        aria-labelledby="history-title"
        @cancel.prevent="open = false"
        @close="open = false"
        @click.self="open = false"
      >
        <header>
          <div>
            <p>Leads</p>
            <h2 id="history-title">Historique des modifications</h2>
          </div>
          <button type="button" aria-label="Fermer l’historique" @click="open = false">
            <X :size="20" />
          </button>
        </header>
        <div class="history-list">
          <div class="history-empty">
            <History :size="30" />
            <h3>Aucune modification pour le moment</h3>
          </div>
        </div>
        <footer>
          <button class="button-secondary" type="button" @click="open = false">Fermer</button>
        </footer>
      </dialog>
    </Teleport>
  </div>
</template>

<style scoped>
.history-trigger {
  width: 40px;
  height: 40px;
  display: grid;
  place-items: center;
  border: 0;
  color: var(--muted);
  background: transparent;
  cursor: pointer;
}
.history-trigger:hover {
  color: var(--navy);
}
.history-trigger:focus-visible {
  outline: 2px solid var(--green);
  outline-offset: 3px;
}
.history-dialog {
  width: min(850px, calc(100vw - 32px));
  max-height: min(780px, calc(100dvh - 48px));
  padding: 0;
  border: 1px solid var(--line);
  border-radius: 16px;
  color: var(--navy);
  background: white;
  box-shadow: 0 28px 80px rgba(23, 31, 65, 0.28);
  overflow: auto;
}
.history-dialog[open] {
  display: flex;
  flex-direction: column;
}
.history-dialog::backdrop {
  background: rgba(28, 36, 68, 0.4);
  backdrop-filter: blur(3px);
}
header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px;
  border-bottom: 1px solid var(--line);
}
header p {
  margin: 0 0 7px;
  color: var(--green-dark);
  font-size: 11px;
  font-weight: 700;
}
header h2 {
  margin: 0;
  font-size: 23px;
}
header button {
  border: 0;
  border-radius: 8px;
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  color: var(--navy);
  background: var(--surface);
  cursor: pointer;
  flex-shrink: 0;
}
.history-list {
  padding: 0 24px 24px;
  min-height: 220px;
}
.history-empty {
  display: grid;
  justify-items: center;
  text-align: center;
  padding: 54px 12px;
  color: var(--muted);
}
.history-empty h3 {
  font-size: 17px;
  color: var(--navy);
  margin: 18px 0 0;
}
footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid var(--line);
}
</style>
