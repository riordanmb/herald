/**
 * Fabric.js canvas overlay for annotations on OpenSeadragon viewer.
 */

'use client'

import { useEffect, useRef, useState, useCallback } from 'react'
import type { Annotation } from '@/types'

interface AnnotationCanvasProps {
  viewer: any // OpenSeadragon.Viewer
  annotations: Annotation[]
  onAnnotationCreate?: (annotation: Partial<Annotation>) => void
  onAnnotationUpdate?: (id: string, annotation: Partial<Annotation>) => void
  onAnnotationDelete?: (id: string) => void
  mode?: 'view' | 'draw-rect' | 'draw-polygon'
  selectedAnnotationId?: string | null
  imageWidth?: number
  imageHeight?: number
}

export default function AnnotationCanvas({
  viewer,
  annotations,
  onAnnotationCreate,
  onAnnotationUpdate,
  onAnnotationDelete,
  mode = 'view',
  selectedAnnotationId,
  imageWidth = 1,
  imageHeight = 1,
}: AnnotationCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const fabricCanvasRef = useRef<any>(null)
  const fabricRef = useRef<any>(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [startPoint, setStartPoint] = useState<any>(null)
  const [currentRect, setCurrentRect] = useState<any>(null)
  const polygonPointsRef = useRef<any[]>([])
  const [currentPolygon, setCurrentPolygon] = useState<any>(null)

  // Load Fabric.js dynamically
  useEffect(() => {
    if (typeof window === 'undefined') return

    import('fabric').then((fabricModule: any) => {
      // Fabric.js v6 exports everything directly
      fabricRef.current = fabricModule
    })
  }, [])

  // Initialize Fabric.js canvas
  useEffect(() => {
    if (!canvasRef.current || !viewer || !fabricRef.current) return

    const fabric = fabricRef.current
    const container = viewer.container as HTMLElement
    const rect = container.getBoundingClientRect()

    const fabricCanvas = new fabric.Canvas(canvasRef.current, {
      width: rect.width,
      height: rect.height,
      selection: mode === 'view',
      backgroundColor: 'transparent',
    })

    fabricCanvasRef.current = fabricCanvas

    // Update canvas size when viewer resizes
    const updateCanvasSize = () => {
      const newRect = container.getBoundingClientRect()
      fabricCanvas.setDimensions({
        width: newRect.width,
        height: newRect.height,
      })
      fabricCanvas.renderAll()
    }

    viewer.addHandler('resize', updateCanvasSize)
    window.addEventListener('resize', updateCanvasSize)

    return () => {
      viewer.removeHandler('resize', updateCanvasSize)
      window.removeEventListener('resize', updateCanvasSize)
      fabricCanvas.dispose()
    }
  }, [viewer, mode])

  // Convert image coordinates to canvas coordinates
  const imageToCanvas = useCallback(
    (imagePoint: { x: number; y: number }) => {
      if (!viewer || !fabricCanvasRef.current) return { x: 0, y: 0 }

      const container = viewer.container as HTMLElement
      const rect = container.getBoundingClientRect()
      const imageSize = viewer.world.getItemAt(0).getContentSize()

      // Convert image coordinates to canvas coordinates
      const scaleX = rect.width / imageSize.x
      const scaleY = rect.height / imageSize.y

      const canvasPoint = {
        x: imagePoint.x * scaleX,
        y: imagePoint.y * scaleY,
      }

      return canvasPoint
    },
    [viewer]
  )

  // Convert canvas coordinates to image coordinates
  const canvasToImage = useCallback(
    (canvasPoint: { x: number; y: number }) => {
      if (!viewer || !fabricCanvasRef.current) return { x: 0, y: 0 }

      const container = viewer.container as HTMLElement
      const rect = container.getBoundingClientRect()
      const imageSize = viewer.world.getItemAt(0).getContentSize()

      const scaleX = imageSize.x / rect.width
      const scaleY = imageSize.y / rect.height

      const imagePoint = {
        x: canvasPoint.x * scaleX,
        y: canvasPoint.y * scaleY,
      }

      return imagePoint
    },
    [viewer]
  )

  // Load annotations onto canvas
  useEffect(() => {
    if (!fabricCanvasRef.current || !fabricRef.current) return

    const canvas = fabricCanvasRef.current
    const fabric = fabricRef.current
    const objectsToRemove = canvas.getObjects().filter((obj: any) => {
      const data = obj.data
      return data?.isAnnotation
    })
    objectsToRemove.forEach((obj: any) => canvas.remove(obj))

    if (!annotations.length) {
      canvas.renderAll()
      return
    }

    annotations.forEach((annotation) => {
      let fabricObject: any = null

      switch (annotation.annotation_type) {
        case 'rect': {
          const coords = annotation.coordinates as {
            x: number
            y: number
            width: number
            height: number
          }
          const canvasCoords = imageToCanvas({ x: coords.x, y: coords.y })
          fabricObject = new fabric.Rect({
            left: canvasCoords.x,
            top: canvasCoords.y,
            width: (coords.width / imageWidth) * (canvas.width || 1),
            height: (coords.height / imageHeight) * (canvas.height || 1),
            fill: 'transparent',
            stroke: annotation.color || '#ff0000',
            strokeWidth: annotation.stroke_width || 2,
            selectable: mode === 'view',
            data: { annotationId: annotation.id, isAnnotation: true },
          })
          break
        }
        case 'polygon': {
          const points = (annotation.coordinates as number[][]).map((p) =>
            imageToCanvas({ x: p[0], y: p[1] })
          )
          fabricObject = new fabric.Polygon(
            points.map((p) => new fabric.Point(p.x, p.y)),
            {
              fill: 'transparent',
              stroke: annotation.color || '#ff0000',
              strokeWidth: annotation.stroke_width || 2,
              selectable: mode === 'view',
              data: { annotationId: annotation.id, isAnnotation: true },
            }
          )
          break
        }
        case 'circle': {
          const coords = annotation.coordinates as {
            x: number
            y: number
            radius: number
          }
          const canvasCoords = imageToCanvas({ x: coords.x, y: coords.y })
          const radius = (coords.radius / imageWidth) * (canvas.width || 1)
          fabricObject = new fabric.Circle({
            left: canvasCoords.x - radius,
            top: canvasCoords.y - radius,
            radius,
            fill: 'transparent',
            stroke: annotation.color || '#ff0000',
            strokeWidth: annotation.stroke_width || 2,
            selectable: mode === 'view',
            data: { annotationId: annotation.id, isAnnotation: true },
          })
          break
        }
        case 'point': {
          const coords = annotation.coordinates as { x: number; y: number }
          const canvasCoords = imageToCanvas({ x: coords.x, y: coords.y })
          fabricObject = new fabric.Circle({
            left: canvasCoords.x - 5,
            top: canvasCoords.y - 5,
            radius: 5,
            fill: annotation.color || '#ff0000',
            stroke: annotation.color || '#ff0000',
            strokeWidth: 1,
            selectable: mode === 'view',
            data: { annotationId: annotation.id, isAnnotation: true },
          })
          break
        }
      }

      if (fabricObject) {
        canvas.add(fabricObject)
      }
    })

    canvas.renderAll()
  }, [annotations, mode, imageWidth, imageHeight, imageToCanvas])

  // Handle drawing mode
  useEffect(() => {
    if (!fabricCanvasRef.current || !fabricRef.current) return

    const canvas = fabricCanvasRef.current
    const fabric = fabricRef.current
    canvas.selection = mode === 'view'
    canvas.defaultCursor = mode === 'view' ? 'default' : 'crosshair'

    if (mode === 'draw-rect') {
      canvas.on('mouse:down', handleRectStart)
      canvas.on('mouse:move', handleRectMove)
      canvas.on('mouse:up', handleRectEnd)
    } else if (mode === 'draw-polygon') {
      canvas.on('mouse:down', handlePolygonClick)
    } else {
      canvas.off('mouse:down')
      canvas.off('mouse:move')
      canvas.off('mouse:up')
      // Clean up any drawing state
      if (currentRect) {
        canvas.remove(currentRect)
        setCurrentRect(null)
      }
      if (currentPolygon) {
        canvas.remove(currentPolygon)
        setCurrentPolygon(null)
      }
      polygonPointsRef.current = []
      setIsDrawing(false)
      setStartPoint(null)
    }

    return () => {
      canvas.off('mouse:down')
      canvas.off('mouse:move')
      canvas.off('mouse:up')
    }
  }, [mode, currentRect, currentPolygon])

  const handleRectStart = (e: any) => {
    if (mode !== 'draw-rect' || !fabricCanvasRef.current || !fabricRef.current) return
    const fabric = fabricRef.current
    const pointer = fabricCanvasRef.current.getPointer(e.e)
    setIsDrawing(true)
    setStartPoint(new fabric.Point(pointer.x, pointer.y))
  }

  const handleRectMove = (e: any) => {
    if (!isDrawing || mode !== 'draw-rect' || !fabricCanvasRef.current || !startPoint || !fabricRef.current)
      return

    const fabric = fabricRef.current
    const canvas = fabricCanvasRef.current
    const pointer = canvas.getPointer(e.e)

    const width = Math.abs(pointer.x - startPoint.x)
    const height = Math.abs(pointer.y - startPoint.y)
    const left = Math.min(pointer.x, startPoint.x)
    const top = Math.min(pointer.y, startPoint.y)

    if (currentRect) {
      canvas.remove(currentRect)
    }

    const rect = new fabric.Rect({
      left,
      top,
      width,
      height,
      fill: 'transparent',
      stroke: '#ff0000',
      strokeWidth: 2,
    })

    canvas.add(rect)
    setCurrentRect(rect)
    canvas.renderAll()
  }

  const handleRectEnd = (e: any) => {
    if (mode !== 'draw-rect' || !isDrawing || !fabricCanvasRef.current || !startPoint)
      return

    const canvas = fabricCanvasRef.current
    const pointer = canvas.getPointer(e.e)

    const width = Math.abs(pointer.x - startPoint.x)
    const height = Math.abs(pointer.y - startPoint.y)

    if (width > 5 && height > 5 && onAnnotationCreate) {
      const imageStart = canvasToImage({ x: startPoint.x, y: startPoint.y })
      const imageEnd = canvasToImage({ x: pointer.x, y: pointer.y })

      onAnnotationCreate({
        annotation_type: 'rect',
        coordinates: {
          x: Math.min(imageStart.x, imageEnd.x),
          y: Math.min(imageStart.y, imageEnd.y),
          width: Math.abs(imageEnd.x - imageStart.x),
          height: Math.abs(imageEnd.y - imageStart.y),
        },
      })
    }

    if (currentRect) {
      canvas.remove(currentRect)
      setCurrentRect(null)
    }

    setIsDrawing(false)
    setStartPoint(null)
  }

  const handlePolygonClick = (e: any) => {
    if (mode !== 'draw-polygon' || !fabricCanvasRef.current || !fabricRef.current) return

    const fabric = fabricRef.current
    const canvas = fabricCanvasRef.current
    const pointer = canvas.getPointer(e.e)

    // Double-click to finish polygon
    if (e.e.detail === 2 && polygonPointsRef.current.length >= 3) {
      if (onAnnotationCreate) {
        const imagePoints = polygonPointsRef.current.map((p: any) => {
          const img = canvasToImage({ x: p.x, y: p.y })
          return [img.x, img.y]
        })

        onAnnotationCreate({
          annotation_type: 'polygon',
          coordinates: imagePoints,
        })
      }

      if (currentPolygon) {
        canvas.remove(currentPolygon)
        setCurrentPolygon(null)
      }
      polygonPointsRef.current = []
      return
    }

    // Add point to polygon
    polygonPointsRef.current.push(new fabric.Point(pointer.x, pointer.y))

    if (currentPolygon) {
      canvas.remove(currentPolygon)
    }

    if (polygonPointsRef.current.length >= 2) {
      const polygon = new fabric.Polygon(polygonPointsRef.current, {
        fill: 'transparent',
        stroke: '#ff0000',
        strokeWidth: 2,
      })
      canvas.add(polygon)
      setCurrentPolygon(polygon)
      canvas.renderAll()
    }
  }

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        pointerEvents: 'auto',
        zIndex: 10,
      }}
    />
  )
}
