import type { LeadZone } from '~/types/domain'

// Valeurs fictives : elles illustrent l'écran et ne reflètent aucune configuration réelle.
export const initialZones: LeadZone[] = [
  {
    regionId: 'ile-de-france',
    departments: ['75', '77', '78', '91', '92', '93', '94', '95'],
    active: true,
    rule: { shortSurface: 'disabled', mediumSurface: 'disabled', longSurface: 'disabled' },
  },
  {
    regionId: 'nouvelle-aquitaine',
    departments: ['33'],
    active: true,
    rule: { shortSurface: '30-50', mediumSurface: 'lt30', longSurface: 'disabled' },
  },
  {
    regionId: 'corse',
    departments: ['2A', '2B'],
    active: false,
    rule: { shortSurface: 'lt30', mediumSurface: 'disabled', longSurface: 'disabled' },
  },
  {
    regionId: 'auvergne-rhone-alpes',
    departments: ['69'],
    active: true,
    rule: { shortSurface: '30-50', mediumSurface: 'lt30', longSurface: 'disabled' },
  },
  {
    regionId: 'provence-alpes-cote-d-azur',
    departments: ['13'],
    active: true,
    rule: { shortSurface: '50-80', mediumSurface: '30-50', longSurface: 'lt30' },
  },
]
