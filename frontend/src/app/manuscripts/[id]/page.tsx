/**
 * Manuscript detail page.
 */

'use client'

import { useQuery } from '@tanstack/react-query'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import api from '@/lib/api'
import type { Manuscript } from '@/types'

async function fetchManuscript(id: string): Promise<Manuscript> {
  const response = await api.get(`/manuscripts/manuscripts/${id}/`)
  return response.data
}

export default function ManuscriptDetailPage() {
  const params = useParams()
  const id = params.id as string

  const { data: manuscript, isLoading, error } = useQuery({
    queryKey: ['manuscript', id],
    queryFn: () => fetchManuscript(id),
  })

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading manuscript...</div>
      </div>
    )
  }

  if (error || !manuscript) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-red-600">Error loading manuscript</div>
        <Link href="/manuscripts" className="text-blue-600 hover:underline mt-4 inline-block">
          Back to manuscripts
        </Link>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/manuscripts" className="text-blue-600 hover:underline">
          ← Back to manuscripts
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-4xl font-serif font-bold text-heraldic-azure mb-2">
              {manuscript.shelfmark}
            </h1>
            <p className="text-xl text-gray-600">{manuscript.repository}</p>
            {manuscript.collection && (
              <p className="text-lg text-gray-500">{manuscript.collection}</p>
            )}
          </div>
          <div className="flex gap-2">
            {manuscript.surrogates && manuscript.surrogates.length > 0 && (
              <Link
                href={`/manuscripts/${id}/viewer`}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                View Images
              </Link>
            )}
            <Link
              href={`/manuscripts/${id}/edit`}
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
            >
              Edit
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div>
            <h2 className="text-2xl font-semibold mb-4">Physical Description</h2>
            <dl className="space-y-2">
              <div>
                <dt className="font-semibold">Material:</dt>
                <dd className="text-gray-600 capitalize">{manuscript.material}</dd>
              </div>
              <div>
                <dt className="font-semibold">Folios:</dt>
                <dd className="text-gray-600">{manuscript.folios}</dd>
              </div>
              {manuscript.dimensions && (
                <div>
                  <dt className="font-semibold">Dimensions:</dt>
                  <dd className="text-gray-600">
                    {manuscript.dimensions.height} × {manuscript.dimensions.width}{' '}
                    {manuscript.dimensions.unit || 'mm'}
                  </dd>
                </div>
              )}
            </dl>
          </div>

          <div>
            <h2 className="text-2xl font-semibold mb-4">Dating & Provenance</h2>
            <dl className="space-y-2">
              <div>
                <dt className="font-semibold">Date:</dt>
                <dd className="text-gray-600">
                  {manuscript.date_range || manuscript.date_display}
                </dd>
              </div>
              {manuscript.origin_location && (
                <div>
                  <dt className="font-semibold">Origin:</dt>
                  <dd className="text-gray-600">{manuscript.origin_location}</dd>
                </div>
              )}
              <div>
                <dt className="font-semibold">Language:</dt>
                <dd className="text-gray-600">{manuscript.language}</dd>
              </div>
              <div>
                <dt className="font-semibold">Script:</dt>
                <dd className="text-gray-600">{manuscript.script}</dd>
              </div>
            </dl>
          </div>
        </div>

        <div className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Content Summary</h2>
          <p className="text-gray-700 whitespace-pre-wrap">{manuscript.content_summary}</p>
        </div>

        {manuscript.provenance && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Provenance</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{manuscript.provenance}</p>
          </div>
        )}

        {manuscript.surrogates && manuscript.surrogates.length > 0 && (
          <div>
            <h2 className="text-2xl font-semibold mb-4">Images ({manuscript.surrogates.length})</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {manuscript.surrogates.map((surrogate) => (
                <div key={surrogate.id} className="border border-gray-200 rounded overflow-hidden">
                  {surrogate.thumbnail_url ? (
                    <img
                      src={surrogate.thumbnail_url}
                      alt={`Folio ${surrogate.folio_number}`}
                      className="w-full h-48 object-cover"
                    />
                  ) : (
                    <div className="w-full h-48 bg-gray-100 flex items-center justify-center">
                      <span className="text-gray-400">No thumbnail</span>
                    </div>
                  )}
                  <div className="p-2">
                    <p className="text-sm font-semibold">Folio {surrogate.folio_number}</p>
                    <p className="text-xs text-gray-500 capitalize">{surrogate.surrogate_type}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

