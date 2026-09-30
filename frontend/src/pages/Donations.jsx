import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Heart } from 'lucide-react'
import api from '../services/api'
import { useAuth } from '../contexts/AuthContext'

const Donations = () => {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    donor_name: user?.profile ? `${user.profile.first_name} ${user.profile.last_name}`.trim() : '',
    donor_email: user?.email || '',
    donor_mobile: user?.mobile || '',
    amount: '',
    purpose: '',
    payment_method: ''
  })
  const [success, setSuccess] = useState(false)

  const donationMutation = useMutation({
    mutationFn: async (data) => {
      const res = await api.post('/donations', data)
      return res.data
    },
    onSuccess: () => {
      setSuccess(true)
      setFormData({
        donor_name: '',
        donor_email: '',
        donor_mobile: '',
        amount: '',
        purpose: '',
        payment_method: ''
      })
    }
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    donationMutation.mutate(formData)
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  if (success) {
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-green-50 border border-green-200 rounded-lg p-8 text-center">
          <Heart className="w-16 h-16 text-green-600 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-green-800 mb-2">Thank You!</h2>
          <p className="text-green-700">
            Your donation has been recorded. Admin will process it and update the status.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold mb-8">Make a Donation</h1>

      <div className="bg-white rounded-lg shadow-md p-6">
        <p className="text-gray-600 mb-6">
          Support the school and alumni initiatives through your generous contribution.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Donor Name *
            </label>
            <input
              type="text"
              name="donor_name"
              required
              value={formData.donor_name}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              name="donor_email"
              value={formData.donor_email}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Mobile
            </label>
            <input
              type="tel"
              name="donor_mobile"
              value={formData.donor_mobile}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Amount (₹) *
            </label>
            <input
              type="number"
              name="amount"
              required
              min="1"
              step="0.01"
              value={formData.amount}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Purpose
            </label>
            <input
              type="text"
              name="purpose"
              value={formData.purpose}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Payment Method
            </label>
            <select
              name="payment_method"
              value={formData.payment_method}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="">Select method</option>
              <option value="bank_transfer">Bank Transfer</option>
              <option value="upi">UPI</option>
              <option value="cheque">Cheque</option>
              <option value="cash">Cash</option>
            </select>
          </div>

          {donationMutation.isError && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {donationMutation.error?.response?.data?.error || 'Failed to submit donation'}
            </div>
          )}

          <button
            type="submit"
            disabled={donationMutation.isLoading}
            className="w-full bg-primary-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
          >
            {donationMutation.isLoading ? 'Submitting...' : 'Submit Donation'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default Donations
