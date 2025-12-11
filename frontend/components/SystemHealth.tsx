'use client'

import { motion } from 'framer-motion'
import { CheckCircleIcon, ExclamationTriangleIcon, XCircleIcon } from '@heroicons/react/24/solid'

interface SystemHealthProps {
  data?: {
    overall_status: string
    services: Record<string, any>
    alerts: any[]
    last_updated: string
  }
}

export default function SystemHealth({ data }: SystemHealthProps) {
  if (!data) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-3 bg-gray-200 rounded"></div>
            <div className="h-3 bg-gray-200 rounded w-5/6"></div>
          </div>
        </div>
      </div>
    )
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircleIcon className="h-5 w-5 text-success-500" />
      case 'warning':
      case 'degraded':
        return <ExclamationTriangleIcon className="h-5 w-5 text-warning-500" />
      case 'error':
      case 'unhealthy':
        return <XCircleIcon className="h-5 w-5 text-error-500" />
      default:
        return <div className="h-5 w-5 rounded-full bg-gray-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-success-700 bg-success-50 border-success-200'
      case 'warning':
      case 'degraded':
        return 'text-warning-700 bg-warning-50 border-warning-200'
      case 'error':
      case 'unhealthy':
        return 'text-error-700 bg-error-50 border-error-200'
      default:
        return 'text-gray-700 bg-gray-50 border-gray-200'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="card-header">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">System Health</h3>
          <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(data.overall_status)}`}>
            {getStatusIcon(data.overall_status)}
            <span className="ml-2 capitalize">{data.overall_status}</span>
          </div>
        </div>
      </div>

      <div className="space-y-4">
        {/* Services Status */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Services</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {Object.entries(data.services).map(([serviceName, serviceData]) => (
              <div
                key={serviceName}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  {getStatusIcon(serviceData.status)}
                  <div>
                    <p className="text-sm font-medium text-gray-900 capitalize">
                      {serviceName}
                    </p>
                    {serviceData.response_time && (
                      <p className="text-xs text-gray-500">
                        {serviceData.response_time}ms
                      </p>
                    )}
                    {serviceData.active_workflows && (
                      <p className="text-xs text-gray-500">
                        {serviceData.active_workflows} workflows
                      </p>
                    )}
                    {serviceData.model_accuracy && (
                      <p className="text-xs text-gray-500">
                        {(serviceData.model_accuracy * 100).toFixed(1)}% accuracy
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Alerts */}
        {data.alerts && data.alerts.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-3">Active Alerts</h4>
            <div className="space-y-2">
              {data.alerts.map((alert, index) => (
                <div
                  key={index}
                  className="flex items-center space-x-3 p-3 bg-warning-50 border border-warning-200 rounded-lg"
                >
                  <ExclamationTriangleIcon className="h-5 w-5 text-warning-500 flex-shrink-0" />
                  <div className="flex-1">
                    <p className="text-sm font-medium text-warning-800">
                      {alert.title}
                    </p>
                    <p className="text-xs text-warning-600">
                      {alert.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Last Updated */}
        <div className="text-xs text-gray-500 text-right">
          Last updated: {new Date(data.last_updated).toLocaleString()}
        </div>
      </div>
    </motion.div>
  )
}