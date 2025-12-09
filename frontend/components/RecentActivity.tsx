'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  BoltIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  ClockIcon,
  ArrowPathIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/outline'
import { useAPI } from '../hooks/useAPI'

interface Activity {
  id: string
  type: 'deployment' | 'optimization' | 'alert' | 'rollback' | 'scale'
  status: 'success' | 'failed' | 'pending' | 'in_progress'
  title: string
  description: string
  timestamp: string
  duration?: number
  user?: string
  environment?: string
}

interface RecentActivityProps {
  activities?: Activity[]
}

export default function RecentActivity({ activities: propActivities }: RecentActivityProps) {
  const { data: apiData, error, isLoading } = useAPI('/api/monitoring/activities')
  const [filter, setFilter] = useState<string>('all')
  
  const activities: Activity[] = propActivities || apiData?.activities || []

  const getIcon = (type: string) => {
    switch (type) {
      case 'deployment':
        return RocketLaunchIcon
      case 'optimization':
        return BoltIcon
      case 'alert':
        return ExclamationTriangleIcon
      case 'rollback':
        return ArrowPathIcon
      case 'scale':
        return BoltIcon
      default:
        return ClockIcon
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'success':
        return CheckCircleIcon
      case 'failed':
        return XCircleIcon
      case 'in_progress':
        return ClockIcon
      default:
        return ClockIcon
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-success-600 bg-success-50'
      case 'failed':
        return 'text-error-600 bg-error-50'
      case 'in_progress':
        return 'text-blue-600 bg-blue-50'
      case 'pending':
        return 'text-gray-600 bg-gray-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'deployment':
        return 'text-purple-600'
      case 'optimization':
        return 'text-blue-600'
      case 'alert':
        return 'text-warning-600'
      case 'rollback':
        return 'text-error-600'
      case 'scale':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  const formatDuration = (duration: number) => {
    if (duration < 60) return `${duration}s`
    if (duration < 3600) return `${Math.floor(duration / 60)}m ${duration % 60}s`
    return `${Math.floor(duration / 3600)}h ${Math.floor((duration % 3600) / 60)}m`
  }

  const filteredActivities = filter === 'all' 
    ? activities 
    : activities.filter(a => a.type === filter)

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-16 bg-gray-200 rounded"></div>
            <div className="h-16 bg-gray-200 rounded"></div>
            <div className="h-16 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="text-error-600 text-sm">
          Failed to load recent activities
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center space-x-2">
          <ClockIcon className="h-6 w-6 text-gray-600" />
          <span>Recent Activity</span>
        </h2>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 text-xs rounded-full transition-colors ${
              filter === 'all' 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('deployment')}
            className={`px-3 py-1 text-xs rounded-full transition-colors ${
              filter === 'deployment' 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Deployments
          </button>
          <button
            onClick={() => setFilter('alert')}
            className={`px-3 py-1 text-xs rounded-full transition-colors ${
              filter === 'alert' 
                ? 'bg-primary-600 text-white' 
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            Alerts
          </button>
        </div>
      </div>

      {filteredActivities.length === 0 ? (
        <div className="text-center py-8">
          <ClockIcon className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">No recent activities</p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredActivities.slice(0, 10).map((activity, index) => {
            const TypeIcon = getIcon(activity.type)
            const StatusIcon = getStatusIcon(activity.status)
            
            return (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-start space-x-3 p-3 rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div className={`flex-shrink-0 p-2 rounded-lg ${getTypeColor(activity.type)} bg-opacity-10`}>
                  <TypeIcon className={`h-5 w-5 ${getTypeColor(activity.type)}`} />
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {activity.title}
                    </p>
                    <span className={`flex-shrink-0 inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${getStatusColor(activity.status)}`}>
                      <StatusIcon className="h-3 w-3 mr-1" />
                      {activity.status}
                    </span>
                  </div>
                  
                  <p className="mt-1 text-xs text-gray-600">{activity.description}</p>
                  
                  <div className="mt-2 flex items-center space-x-4 text-xs text-gray-500">
                    <span>{new Date(activity.timestamp).toLocaleString()}</span>
                    
                    {activity.duration && (
                      <>
                        <span>•</span>
                        <span>Duration: {formatDuration(activity.duration)}</span>
                      </>
                    )}
                    
                    {activity.environment && (
                      <>
                        <span>•</span>
                        <span className="capitalize">{activity.environment}</span>
                      </>
                    )}
                    
                    {activity.user && (
                      <>
                        <span>•</span>
                        <span>by {activity.user}</span>
                      </>
                    )}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      )}
    </div>
  )
}
