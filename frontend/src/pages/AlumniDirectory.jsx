import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search, User } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const AlumniDirectory = () => {
  const [filters, setFilters] = useState({
    search: '',
    batch_year: '',
    profession: '',
    location: ''
  })
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['alumni', filters, page],
    queryFn: async () => {
      const params = new URLSearchParams({ page, per_page: 20 })
      if (filters.search) params.append('search', filters.search)
      if (filters.batch_year) params.append('batch_year', filters.batch_year)
      if (filters.profession) params.append('profession', filters.profession)
      if (filters.location) params.append('location', filters.location)
      const res = await api.get(`/alumni?${params}`)
      return res.data
    }
  })

  const handleFilterChange = (key, value) => {
    setFilters({ ...filters, [key]: value })
    setPage(1)
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Alumni Directory</h1>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Search</label>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={filters.search}
                onChange={(e) => handleFilterChange('search', e.target.value)}
                placeholder="Name, profession, company..."
                className="pl-10 w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Batch Year</label>
            <input
              type="number"
              value={filters.batch_year}
              onChange={(e) => handleFilterChange('batch_year', e.target.value)}
              placeholder="e.g., 2020"
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Profession</label>
            <input
              type="text"
              value={filters.profession}
              onChange={(e) => handleFilterChange('profession', e.target.value)}
              placeholder="e.g., Engineer"
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input
              type="text"
              value={filters.location}
              onChange={(e) => handleFilterChange('location', e.target.value)}
              placeholder="e.g., Mumbai"
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>
        </div>
      </div>

      {/* Results */}
      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.alumni && data.alumni.length > 0 ? (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {data.alumni.map((alumni) => (
              <Link
                key={alumni.id}
                to={`/alumni/${alumni.user_id}`}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
              >
                <div className="flex items-center mb-4">
                  {alumni.profile_picture ? (
                    <img
                      src={alumni.profile_picture}
                      alt={alumni.full_name}
                      className="w-16 h-16 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-16 h-16 rounded-full bg-primary-100 flex items-center justify-center">
                      <User className="w-8 h-8 text-primary-600" />
                    </div>
                  )}
                  <div className="ml-4">
                    <h3 className="font-semibold text-lg">
                      {alumni.first_name} {alumni.last_name}
                    </h3>
                    {alumni.batch_year && (
                      <p className="text-sm text-gray-500">Batch {alumni.batch_year}</p>
                    )}
                  </div>
                </div>
                {alumni.profession && (
                  <p className="text-gray-700 mb-2">
                    <span className="font-medium">Profession:</span> {alumni.profession}
                  </p>
                )}
                {alumni.company && (
                  <p className="text-gray-700 mb-2">
                    <span className="font-medium">Company:</span> {alumni.company}
                  </p>
                )}
                {alumni.location && (
                  <p className="text-gray-700">
                    <span className="font-medium">Location:</span> {alumni.location}
                  </p>
                )}
              </Link>
            ))}
          </div>

          {/* Pagination */}
          {data.pages > 1 && (
            <div className="flex justify-center space-x-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border rounded-md disabled:opacity-50"
              >
                Previous
              </button>
              <span className="px-4 py-2">
                Page {page} of {data.pages}
              </span>
              <button
                onClick={() => setPage(p => Math.min(data.pages, p + 1))}
                disabled={page === data.pages}
                className="px-4 py-2 border rounded-md disabled:opacity-50"
              >
                Next
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="text-center py-12 text-gray-500">
          No alumni found matching your criteria.
        </div>
      )}
    </div>
  )
}

export default AlumniDirectory
