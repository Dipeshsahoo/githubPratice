import { useQuery } from '@tanstack/react-query'
import { Briefcase, MapPin, Clock } from 'lucide-react'
import api from '../services/api'
import { Link } from 'react-router-dom'

const Jobs = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['jobs'],
    queryFn: async () => {
      const res = await api.get('/jobs?active_only=true&approved_only=true')
      return res.data
    }
  })

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Job Opportunities</h1>

      {isLoading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        </div>
      ) : data?.jobs && data.jobs.length > 0 ? (
        <div className="space-y-6">
          {data.jobs.map((job) => (
            <Link
              key={job.id}
              to={`/jobs/${job.id}`}
              className="block bg-white rounded-lg shadow-md hover:shadow-lg transition p-6"
            >
              <div className="flex items-start">
                <Briefcase className="w-8 h-8 text-primary-600 mr-4 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="text-xl font-semibold mb-2">{job.title}</h3>
                  <p className="text-primary-600 font-medium mb-2">{job.company}</p>
                  <p className="text-gray-600 mb-3 line-clamp-2">{job.description}</p>
                  <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                    {job.location && (
                      <div className="flex items-center">
                        <MapPin className="w-4 h-4 mr-1" />
                        {job.location}
                      </div>
                    )}
                    {job.job_type && (
                      <span className="bg-gray-100 px-2 py-1 rounded">{job.job_type}</span>
                    )}
                    {job.application_deadline && (
                      <div className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        Deadline: {new Date(job.application_deadline).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-500">No job postings found.</div>
      )}
    </div>
  )
}

export default Jobs
