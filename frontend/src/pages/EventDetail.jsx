import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Calendar, MapPin, Users, Clock, CheckCircle } from 'lucide-react'
import { QRCodeSVG } from 'qrcode.react'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'
import { useState } from 'react'

const EventDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user, isAlumni } = useAuth()
  const queryClient = useQueryClient()
  const [showQR, setShowQR] = useState(false)

  const { data: event, isLoading } = useQuery({
    queryKey: ['event', id],
    queryFn: async () => {
      const res = await api.get(`/events/${id}`)
      return res.data
    }
  })

  const registerMutation = useMutation({
    mutationFn: async () => {
      const res = await api.post(`/events/${id}/register`)
      return res.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries(['event', id])
      setShowQR(true)
    }
  })

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
      </div>
    )
  }

  if (!event) {
    return <div className="text-center py-12">Event not found</div>
  }

  const handleRegister = () => {
    if (!user) {
      navigate('/login')
      return
    }
    registerMutation.mutate()
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {event.is_jubilee_event && (
        <span className="inline-block bg-primary-600 text-white text-sm px-3 py-1 rounded mb-4">
          Platinum Jubilee Event
        </span>
      )}
      <h1 className="text-4xl font-bold mb-4">{event.title}</h1>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="space-y-4 mb-6">
          {event.start_date && (
            <div className="flex items-center text-gray-700">
              <Calendar className="w-5 h-5 mr-3 text-primary-600" />
              <div>
                <p className="font-medium">Start Date</p>
                <p>{new Date(event.start_date).toLocaleString()}</p>
              </div>
            </div>
          )}
          {event.end_date && (
            <div className="flex items-center text-gray-700">
              <Clock className="w-5 h-5 mr-3 text-primary-600" />
              <div>
                <p className="font-medium">End Date</p>
                <p>{new Date(event.end_date).toLocaleString()}</p>
              </div>
            </div>
          )}
          {event.location && (
            <div className="flex items-center text-gray-700">
              <MapPin className="w-5 h-5 mr-3 text-primary-600" />
              <div>
                <p className="font-medium">Location</p>
                <p>{event.location}</p>
              </div>
            </div>
          )}
          {event.venue && (
            <div className="flex items-center text-gray-700">
              <MapPin className="w-5 h-5 mr-3 text-primary-600" />
              <div>
                <p className="font-medium">Venue</p>
                <p>{event.venue}</p>
              </div>
            </div>
          )}
          {event.registration_count !== null && (
            <div className="flex items-center text-gray-700">
              <Users className="w-5 h-5 mr-3 text-primary-600" />
              <p>{event.registration_count} registered</p>
            </div>
          )}
        </div>

        {event.description && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Description</h2>
            <p className="text-gray-700 whitespace-pre-wrap">{event.description}</p>
          </div>
        )}

        {event.is_registered ? (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center mb-4">
              <CheckCircle className="w-6 h-6 text-green-600 mr-2" />
              <p className="font-semibold text-green-800">You are registered for this event</p>
            </div>
            {event.registration?.qr_code && (
              <div>
                <button
                  onClick={() => setShowQR(!showQR)}
                  className="text-primary-600 hover:text-primary-700 font-medium mb-2"
                >
                  {showQR ? 'Hide' : 'Show'} QR Code
                </button>
                {showQR && (
                  <div className="bg-white p-4 rounded-lg inline-block">
                    <QRCodeSVG value={event.registration.qr_code} size={200} />
                    <p className="text-sm text-gray-600 mt-2 text-center">
                      Present this QR code at the event
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          isAlumni() && (
            <button
              onClick={handleRegister}
              disabled={registerMutation.isLoading}
              className="w-full bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
            >
              {registerMutation.isLoading ? 'Registering...' : 'Register for Event'}
            </button>
          )
        )}
      </div>
    </div>
  )
}

export default EventDetail
