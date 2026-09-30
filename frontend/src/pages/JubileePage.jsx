import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import Countdown from 'react-countdown'
import { Calendar, MapPin, Users, Clock } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const JubileePage = () => {
  const { data: events, isLoading } = useQuery({
    queryKey: ['jubilee-events'],
    queryFn: async () => {
      const res = await api.get('/events?is_jubilee=true')
      return res.data.events
    }
  })

  // Set target date for countdown (adjust as needed)
  const targetDate = new Date('2024-12-31T00:00:00')

  const countdownRenderer = ({ days, hours, minutes, seconds, completed }) => {
    if (completed) {
      return <span className="text-4xl font-bold">Celebration Started!</span>
    }
    return (
      <div className="grid grid-cols-4 gap-4 text-center">
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="text-4xl font-bold text-primary-600">{days}</div>
          <div className="text-sm text-gray-600">Days</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="text-4xl font-bold text-primary-600">{hours}</div>
          <div className="text-sm text-gray-600">Hours</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="text-4xl font-bold text-primary-600">{minutes}</div>
          <div className="text-sm text-gray-600">Minutes</div>
        </div>
        <div className="bg-white rounded-lg p-4 shadow-md">
          <div className="text-4xl font-bold text-primary-600">{seconds}</div>
          <div className="text-sm text-gray-600">Seconds</div>
        </div>
      </div>
    )
  }

  return (
    <div>
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-4">Platinum Jubilee</h1>
          <p className="text-2xl md:text-3xl mb-8 text-primary-100">75 Years of Excellence</p>
        </div>
      </div>

      {/* Countdown Section */}
      <div className="bg-primary-50 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-8">Countdown to Celebration</h2>
          <Countdown date={targetDate} renderer={countdownRenderer} />
        </div>
      </div>

      {/* Events Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-3xl font-bold mb-8">Jubilee Events</h2>
        {isLoading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          </div>
        ) : events && events.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {events.map((event) => (
              <Link
                key={event.id}
                to={`/events/${event.id}`}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
              >
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
        ) : (
          <div className="text-center py-12 text-gray-500">
            No jubilee events scheduled yet. Check back soon!
          </div>
        )}
      </div>

      {/* Info Section */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold mb-8 text-center">About the Platinum Jubilee</h2>
          <div className="prose max-w-none">
            <p className="text-lg text-gray-700 mb-4">
              Join us in celebrating 75 years of excellence, growth, and achievement. The Platinum Jubilee is a
              milestone that brings together alumni from all generations to reconnect, reminisce, and create new memories.
            </p>
            <p className="text-lg text-gray-700">
              Register for events, connect with fellow alumni, and be part of this historic celebration. Your presence
              makes this milestone even more special.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default JubileePage
