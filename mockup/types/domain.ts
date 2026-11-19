export interface Department {
  code: string
  name: string
}

export interface AdministrativeRegion {
  id: string
  name: string
  departments: Department[]
}

export type SurfaceThreshold = 'disabled' | 'lt30' | '30-50' | '50-80' | '80-120' | '120-180' | 'gt180'

export interface LeadRule {
  shortSurface: SurfaceThreshold
  mediumSurface: SurfaceThreshold
  longSurface: SurfaceThreshold
}

export interface LeadZone {
  regionId: string
  departments: string[]
  active: boolean
  rule: LeadRule
}
