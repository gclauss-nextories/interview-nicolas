import type { SurfaceThreshold } from '~/types/domain'

// Tranches de surface du formulaire Website, utilisées par le sélecteur.
export const surfaceOptions: { value: SurfaceThreshold; label: string }[] = [
  { value: 'disabled', label: 'Désactivé' },
  { value: 'lt30', label: '< 30 m²' },
  { value: '30-50', label: '30–50 m²' },
  { value: '50-80', label: '50–80 m²' },
  { value: '80-120', label: '80–120 m²' },
  { value: '120-180', label: '120–180 m²' },
  { value: 'gt180', label: '+ de 180 m²' },
]

// Libellé d'un seuil sur une carte de région.
export const surfaceLabel: Record<SurfaceThreshold, string> = {
  disabled: 'Désactivé',
  lt30: 'Moins de 30 m²',
  '30-50': 'Jusqu’à 50 m²',
  '50-80': 'Jusqu’à 80 m²',
  '80-120': 'Jusqu’à 120 m²',
  '120-180': 'Jusqu’à 180 m²',
  gt180: 'Toutes surfaces',
}
