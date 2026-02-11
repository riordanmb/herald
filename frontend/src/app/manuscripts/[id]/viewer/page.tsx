/**
 * Manuscript viewer page with OpenSeadragon image viewer.
 */

'use client'

import { useEffect, useRef, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import Link from 'next/link'
import dynamic from 'next/dynamic'
import api from '@/lib/api'
import type { Manuscript, Surrogate, Annotation } from '@/types'
import AnnotationCanvas from '@/components/annotations/AnnotationCanvas'
import AnnotationToolbar from '@/components/annotations/AnnotationToolbar'
import AnnotationForm from '@/components/annotations/AnnotationForm'
import {
  fetchAnnotations,
  createAnnotation,
  updateAnnotation,
  deleteAnnotation,
} from '@/lib/annotations'

// Dynamically import OpenSeadragon to avoid SSR issues
let OpenSeadragon: any = null
if (typeof window !== 'undefined') {
  import('openseadragon').then((module) => {
    OpenSeadragon = module.default
  })
}

async function fetchManuscript(id: string): Promise<Manuscript> {
  const response = await api.get(`/manuscripts/manuscripts/${id}/`)
  return response.data
}

async function fetchSurrogates(manuscriptId: string): Promise<Surrogate[]> {
  const response = await api.get(`/manuscripts/manuscripts/${manuscriptId}/surrogates/`)
  return response.data
}

type DrawingMode = 'view' | 'draw-rect' | 'draw-polygon'

export default function ManuscriptViewerPage() {
  const params = useParams()
  const router = useRouter()
  const manuscriptId = params.id as string
  const viewerRef = useRef<HTMLDivElement>(null)
  const [viewer, setViewer] = useState<OpenSeadragon.Viewer | null>(null)
  const [currentSurrogateIndex, setCurrentSurrogateIndex] = useState(0)
  const [drawingMode, setDrawingMode] = useState<DrawingMode>('view')
  const [pendingAnnotation, setPendingAnnotation] = useState<Partial<Annotation> | null>(null)
  const [selectedAnnotation, setSelectedAnnotation] = useState<Annotation | null>(null)
  const queryClient = useQueryClient()

  const { data: manuscript } = useQuery({
    queryKey: ['manuscript', manuscriptId],
    queryFn: () => fetchManuscript(manuscriptId),
  })

  const { data: surrogates = [] } = useQuery({
    queryKey: ['surrogates', manuscriptId],
    queryFn: () => fetchSurrogates(manuscriptId),
    enabled: !!manuscriptId,
  })

  const currentSurrogate = surrogates[currentSurrogateIndex]

  const { data: annotations = [] } = useQuery({
    queryKey: ['annotations', currentSurrogate?.id],
    queryFn: () => fetchAnnotations(currentSurrogate!.id),
    enabled: !!currentSurrogate?.id,
  })

  const createMutation = useMutation({
    mutationFn: createAnnotation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['annotations', currentSurrogate?.id] })
      setPendingAnnotation(null)
      setDrawingMode('view')
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Annotation> }) =>
      updateAnnotation(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['annotations', currentSurrogate?.id] })
      setSelectedAnnotation(null)
    },
  })

  const deleteMutation = useMutation({
    mutationFn: deleteAnnotation,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['annotations', currentSurrogate?.id] })
      setSelectedAnnotation(null)
    },
  })

  // Initialize OpenSeadragon viewer
  useEffect(() => {
    if (!viewerRef.current || !surrogates.length || typeof window === 'undefined') return

    const surrogate = surrogates[currentSurrogateIndex]
    if (!surrogate) return

    // Dynamically load OpenSeadragon if not already loaded
    const initViewer = async () => {
      if (!OpenSeadragon) {
        const osdModule = await import('openseadragon')
        OpenSeadragon = osdModule.default
      }

      // Initialize viewer
      const osdViewer = OpenSeadragon({
        element: viewerRef.current,
        prefixUrl: 'https://cdn.jsdelivr.net/npm/openseadragon@4.1.0/build/openseadragon/images/',
        tileSources: {
          type: 'image',
          url: surrogate.image_url,
        },
        showNavigationControl: true,
        showZoomControl: true,
        showHomeControl: true,
        showFullPageControl: true,
        showRotationControl: true,
        gestureSettingsMouse: {
          clickToZoom: true,
          dblClickToZoom: true,
          pinchToZoom: true,
          flickEnabled: true,
          flickMinSpeed: 120,
          flickMomentum: 0.25,
        },
      })

      setViewer(osdViewer)
    }

    initViewer()

    // Cleanup
    return () => {
      if (viewer) {
        viewer.destroy()
      }
    }
  }, [surrogates, currentSurrogateIndex])

  // Update viewer when surrogate changes
  useEffect(() => {
    if (!viewer || !surrogates.length || !currentSurrogate) return

    viewer.open({
      type: 'image',
      url: currentSurrogate.image_url,
    })
  }, [viewer, currentSurrogateIndex, surrogates, currentSurrogate])

  const handleAnnotationCreate = (annotation: Partial<Annotation>) => {
    setPendingAnnotation(annotation)
  }

  const handleAnnotationSave = (annotation: Partial<Annotation>) => {
    if (selectedAnnotation) {
      updateMutation.mutate({ id: selectedAnnotation.id, data: annotation })
    } else if (pendingAnnotation) {
      createMutation.mutate({ ...pendingAnnotation, ...annotation })
    }
  }

  const handleAnnotationCancel = () => {
    setPendingAnnotation(null)
    setSelectedAnnotation(null)
    setDrawingMode('view')
  }

  const goToSurrogate = (index: number) => {
    if (index >= 0 && index < surrogates.length) {
      setCurrentSurrogateIndex(index)
    }
  }

  if (!manuscript) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading manuscript...</div>
      </div>
    )
  }

  if (!surrogates.length) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <Link href={`/manuscripts/${manuscriptId}`} className="text-blue-600 hover:underline">
            ← Back to manuscript
          </Link>
        </div>
        <div className="text-center py-12">
          <p className="text-xl text-gray-500 mb-4">No images available for this manuscript</p>
          <Link
            href={`/manuscripts/${manuscriptId}`}
            className="text-blue-600 hover:underline"
          >
            Return to manuscript details
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div>
            <Link
              href={`/manuscripts/${manuscriptId}`}
              className="text-blue-600 hover:underline text-sm"
            >
              ← Back to manuscript
            </Link>
            <h1 className="text-xl font-semibold mt-1">
              {manuscript.shelfmark} - {currentSurrogate?.folio_number}
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm text-gray-600">
              Image {currentSurrogateIndex + 1} of {surrogates.length}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => goToSurrogate(currentSurrogateIndex - 1)}
                disabled={currentSurrogateIndex === 0}
                className="px-3 py-1 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Previous
              </button>
              <button
                onClick={() => goToSurrogate(currentSurrogateIndex + 1)}
                disabled={currentSurrogateIndex === surrogates.length - 1}
                className="px-3 py-1 border border-gray-300 rounded disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Viewer */}
      <div className="flex-1 relative">
        <div ref={viewerRef} className="w-full h-full" />
        {viewer && currentSurrogate && (
          <>
            <AnnotationCanvas
              viewer={viewer}
              annotations={annotations}
              onAnnotationCreate={handleAnnotationCreate}
              mode={drawingMode}
              imageWidth={currentSurrogate.width}
              imageHeight={currentSurrogate.height}
            />
            <AnnotationToolbar
              mode={drawingMode}
              onModeChange={setDrawingMode}
            />
            {(pendingAnnotation || selectedAnnotation) && (
              <AnnotationForm
                annotation={selectedAnnotation}
                onSave={handleAnnotationSave}
                onCancel={handleAnnotationCancel}
                surrogateId={currentSurrogate.id}
              />
            )}
          </>
        )}
      </div>

      {/* Thumbnail strip */}
      {surrogates.length > 1 && (
        <div className="bg-gray-100 border-t border-gray-200 px-4 py-2 overflow-x-auto">
          <div className="flex gap-2">
            {surrogates.map((surrogate, index) => (
              <button
                key={surrogate.id}
                onClick={() => goToSurrogate(index)}
                className={`flex-shrink-0 border-2 rounded overflow-hidden ${
                  index === currentSurrogateIndex
                    ? 'border-blue-500'
                    : 'border-transparent hover:border-gray-300'
                }`}
              >
                {surrogate.thumbnail_url ? (
                  <img
                    src={surrogate.thumbnail_url}
                    alt={`Folio ${surrogate.folio_number}`}
                    className="h-20 w-auto"
                  />
                ) : (
                  <div className="h-20 w-16 bg-gray-200 flex items-center justify-center text-xs text-gray-500">
                    {surrogate.folio_number}
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

