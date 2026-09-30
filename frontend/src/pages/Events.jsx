import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Calendar, MapPin, Users, Clock } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const Events = () => {
  const [filters, setFilters] = useState({
    type: '',
    is_jubilee: ''
  })
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery({
    queryKey: ['events', filters, page],
    queryFn: async () => {
      const params = new URLSearchParams({ page, per_page: 20 })
      if (filters.type) params.append('type', filters.type)
      if (filters.is_jubilee) params.append('is_jubilee', filters.is_jubilee)
      const res = await api.get(`/events?${params}`)
      return res.data
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Events</h1>
        <div className="flex space-x-4">
          <select
            value={filters.type}
            onChange={(e) => setFilters({ ...filters, type: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="">All Types</option>
            <option value="jubilee">Jubilee</option>
            <option value="reunion">Reunion</option>
            <option value="workshop">Workshop</option>
            <option value="other">Other</option>
          </select>
          <select
            value={filters.is_jubilee}
            onChange={(e) => setFilters({ ...filters, is_jubilee: e.target.value })}
            className="border border-gray-300 rounded-md px-3 py-2"
          >
            <option value="">All Events</option>
            <option value="true">Jubilee Events Only</option>
          </select>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.events && data.events.length > 0 ? (
        <>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {data.events.map((event) => (
              <Link
                key={event.id}
                to={`/events/${event.id}`}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
              >
                {event.is_jubilee_event && (
                  <span className="inline-block bg-primary-600 text-white text-xs px-2 py-1 rounded mb-3">
                    Platinum Jubilee
                  </span>
                )}
                <h3 className="text-xl font-semibold mb-3">{event.title}</h3>
                <p className="text-gray-600 mb-4 line-clamp-3">{event.description}</p>
                <div className="space-y-2 text-sm text-gray-500">
                  {event.start_date && (
                    <div className="flex items-center">
                      <Calendar className="w-4 h-4 mr-2" />
                      {new Date(event.start_date).toLocaleDateString()}
                    </div>
                  )}
                  {event.location && (
                    <div className="flex items-center">
                      <MapPin className="w-4 h-4 mr-2" />
                      {event.location}
                    </div>
                  )}
                  {event.registration_count !== null && (
                    <div className="flex items-center">
                      <Users className="w-4 h-4 mr-2" />
                      {event.registration_count} registered
                    </div>
                  )}
                </div>
              </Link>
            ))}
          </div>

          {data.pages > 1 && (
            <div className="flex justify-center space-x-2">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border rounded-md disabled:opacity-50"
              >
                Previous
              </button>
              <span className="px-4 py-2">Page {page} of {data.pages}</span>
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
        <div className="text-center py-12 text-gray-500">No events found.</div>
      )}
    </div>
  )
}

export default Events
