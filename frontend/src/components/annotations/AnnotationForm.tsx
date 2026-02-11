/**
 * Form for creating/editing annotations.
 */

'use client'

import { useState, useEffect } from 'react'
import type { Annotation } from '@/types'

interface AnnotationFormProps {
  annotation?: Annotation | null
  onSave: (annotation: Partial<Annotation>) => void
  onCancel: () => void
  surrogateId: string
}

const CATEGORIES = [
  'heraldry',
  'text',
  'decoration',
  'marginalia',
  'illumination',
  'other',
]

export default function AnnotationForm({
  annotation,
  onSave,
  onCancel,
  surrogateId,
}: AnnotationFormProps) {
  const [formData, setFormData] = useState({
    label: annotation?.label || '',
    category: annotation?.category || 'heraldry',
    description: annotation?.description || '',
    color: annotation?.color || '#ff0000',
    stroke_width: annotation?.stroke_width || 2,
    tags: annotation?.tags?.join(', ') || '',
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave({
      ...formData,
      tags: formData.tags
        .split(',')
        .map((t) => t.trim())
        .filter((t) => t.length > 0),
      surrogate: surrogateId,
      annotation_type: annotation?.annotation_type || 'rect',
      coordinates: annotation?.coordinates || {},
    })
  }

  return (
    <div className="absolute bottom-4 left-4 right-4 bg-white rounded-lg shadow-lg p-4 z-20 max-w-md">
      <h3 className="text-lg font-semibold mb-4">
        {annotation ? 'Edit Annotation' : 'New Annotation'}
      </h3>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Label *</label>
          <input
            type="text"
            value={formData.label}
            onChange={(e) => setFormData({ ...formData, label: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Category *</label>
          <select
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded"
            required
          >
            {CATEGORIES.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Description</label>
          <textarea
            value={formData.description}
            onChange={(e) =>
              setFormData({ ...formData, description: e.target.value })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded"
            rows={3}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Color</label>
            <input
              type="color"
              value={formData.color}
              onChange={(e) => setFormData({ ...formData, color: e.target.value })}
              className="w-full h-10 border border-gray-300 rounded"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Stroke Width</label>
            <input
              type="number"
              min="1"
              max="10"
              value={formData.stroke_width}
              onChange={(e) =>
                setFormData({ ...formData, stroke_width: parseInt(e.target.value) })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Tags (comma-separated)</label>
          <input
            type="text"
            value={formData.tags}
            onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
            className="w-full px-3 py-2 border border-gray-300 rounded"
            placeholder="e.g., coat of arms, shield, heraldic"
          />
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            className="flex-1 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            {annotation ? 'Update' : 'Create'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}

