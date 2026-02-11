/**
 * Manuscript list page.
 */

'use client'

import { useQuery } from '@tanstack/react-query'
import Link from 'next/link'
import api from '@/lib/api'
import type { Manuscript, PaginatedResponse } from '@/types'

async function fetchManuscripts(): Promise<PaginatedResponse<Manuscript>> {
  const response = await api.get('/manuscripts/manuscripts/')
  return response.data
}

export default function ManuscriptsPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['manuscripts'],
    queryFn: fetchManuscripts,
  })

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading manuscripts...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-red-600">Error loading manuscripts</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-serif font-bold text-heraldic-azure">Manuscripts</h1>
        <Link
          href="/manuscripts/new"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Add Manuscript
        </Link>
      </div>

      {data && data.results.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p className="text-xl mb-4">No manuscripts found</p>
          <Link href="/manuscripts/new" className="text-blue-600 hover:underline">
            Create your first manuscript
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data?.results.map((manuscript) => (
            <Link
              key={manuscript.id}
              href={`/manuscripts/${manuscript.id}`}
              className="block p-6 border border-gray-200 rounded-lg hover:shadow-lg transition-shadow"
            >
              <h2 className="text-xl font-semibold mb-2">{manuscript.shelfmark}</h2>
              <p className="text-gray-600 mb-2">{manuscript.repository}</p>
              {manuscript.collection && (
                <p className="text-sm text-gray-500 mb-2">{manuscript.collection}</p>
              )}
              <div className="flex justify-between items-center mt-4 text-sm">
                <span className="text-gray-500">{manuscript.date_range || manuscript.date_display}</span>
                {manuscript.surrogate_count !== undefined && (
                  <span className="text-gray-500">
                    {manuscript.surrogate_count} {manuscript.surrogate_count === 1 ? 'image' : 'images'}
                  </span>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}

      {data && data.count > data.results.length && (
        <div className="mt-8 text-center">
          <p className="text-gray-500">
            Showing {data.results.length} of {data.count} manuscripts
          </p>
        </div>
      )}
    </div>
  )
}

