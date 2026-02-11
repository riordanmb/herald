/**
 * Toolbar for annotation drawing tools.
 */

'use client'

import { useState } from 'react'

type DrawingMode = 'view' | 'draw-rect' | 'draw-polygon'

interface AnnotationToolbarProps {
  mode: DrawingMode
  onModeChange: (mode: DrawingMode) => void
  onClear?: () => void
}

export default function AnnotationToolbar({
  mode,
  onModeChange,
  onClear,
}: AnnotationToolbarProps) {
  return (
    <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-2 flex gap-2 z-20">
      <button
        onClick={() => onModeChange('view')}
        className={`px-3 py-2 rounded ${
          mode === 'view'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 hover:bg-gray-200'
        }`}
        title="View mode"
      >
        👁️ View
      </button>
      <button
        onClick={() => onModeChange('draw-rect')}
        className={`px-3 py-2 rounded ${
          mode === 'draw-rect'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 hover:bg-gray-200'
        }`}
        title="Draw rectangle"
      >
        ▭ Rectangle
      </button>
      <button
        onClick={() => onModeChange('draw-polygon')}
        className={`px-3 py-2 rounded ${
          mode === 'draw-polygon'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 hover:bg-gray-200'
        }`}
        title="Draw polygon"
      >
        ⬟ Polygon
      </button>
      {onClear && (
        <button
          onClick={onClear}
          className="px-3 py-2 rounded bg-red-100 hover:bg-red-200 text-red-700"
          title="Clear all"
        >
          Clear
        </button>
      )}
    </div>
  )
}

