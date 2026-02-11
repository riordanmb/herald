/**
 * TypeScript type definitions for Herald API.
 */

export interface User {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
}

export interface Manuscript {
  id: string
  shelfmark: string
  repository: string
  collection?: string
  date_earliest?: string
  date_latest?: string
  language?: string
  surrogates?: Surrogate[]
  created_at: string
  updated_at: string
}

export interface Surrogate {
  id: string
  manuscript: string
  surrogate_type: string
  folio_number: string
  sequence_number: number
  image_url: string
  thumbnail_url?: string
  iiif_manifest?: string
  width: number
  height: number
  dpi?: number
  file_format: string
  file_size: number
  capture_date?: string
  photographer?: string
  copyright_holder?: string
  license?: string
  notes?: string
  created_at: string
  display_name?: string
}

export interface Annotation {
  id: string
  surrogate: string
  surrogate_display_name?: string
  annotation_type: 'point' | 'rect' | 'polygon' | 'circle'
  coordinates: 
    | { x: number; y: number } // point
    | { x: number; y: number; width: number; height: number } // rect
    | number[][] // polygon (array of [x, y] pairs)
    | { x: number; y: number; radius: number } // circle
  label: string
  category: string
  description?: string
  related_arms_id?: string
  related_transcription_id?: string
  tags?: string[]
  color?: string
  stroke_width?: number
  created_at: string
  updated_at: string
  created_by_username?: string
}

export interface ApiResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
