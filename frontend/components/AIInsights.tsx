'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  LightBulbIcon, 
  SparklesIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'
import { useAPI } from '../hooks/useAPI'

interface AIInsight {
  id: string
  type: 'recommendation' | 'warning' | 'info' | 'success'
  title: string
  description: string
  confidence: number
  timestamp: string
  actions?: string[]
}

export default function AIInsights() {
  const { data: insights, error, isLoading } = useAPI('/api/kestra/insights')
  const [selectedInsight, setSelectedInsight] = useState<string | null>(null)

  const getIcon = (type: string) => {
    switch (type) {
      case 'recommendation':
        return LightBulbIcon
      case 'warning':
        return ExclamationTriangleIcon
      case 'info':
        return InformationCircleIcon
      case 'success':
        return CheckCircleIcon
      default:
        return SparklesIcon
    }
  }

  const getColorClasses = (type: string) => {
    switch (type) {
      case 'recommendation':
        return 'bg-primary-50 border-primary-200 text-primary-900'
      case 'warning':
        return 'bg-warning-50 border-warning-200 text-warning-900'
      case 'info':
        return 'bg-blue-50 border-blue-200 text-blue-900'
      case 'success':
        return 'bg-success-50 border-success-200 text-success-900'
      default:
        return 'bg-gray-50 border-gray-200 text-gray-900'
    }
  }

  const getIconColorClasses = (type: string) => {
    switch (type) {
      case 'recommendation':
        return 'text-primary-600'
      case 'warning':
        return 'text-warning-600'
      case 'info':
        return 'text-blue-600'
      case 'success':
        return 'text-success-600'
      default:
        return 'text-gray-600'
    }
  }

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="flex items-center space-x-3 text-error-600">
          <ExclamationTriangleIcon className="h-5 w-5" />
          <span className="text-sm">Failed to load AI insights</span>
        </div>
      </div>
    )
  }

  const insightsList: AIInsight[] = insights?.insights || []

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <SparklesIcon className="h-6 w-6 text-primary-600" />
          <h2 className="text-xl font-semibold text-gray-900">AI Insights</h2>
        </div>
        <div className="text-xs text-gray-500">
          Powered by Kestra AI Agent
        </div>
      </div>

      {insightsList.length === 0 ? (
        <div className="text-center py-8">
          <InformationCircleIcon className="mx-auto h-12 w-12 text-gray-400" />
          <p className="mt-2 text-sm text-gray-500">No insights available at this time</p>
          <p className="text-xs text-gray-400 mt-1">The AI agent is analyzing your system</p>
        </div>
      ) : (
        <div className="space-y-4">
          {insightsList.map((insight, index) => {
            const Icon = getIcon(insight.type)
            const isExpanded = selectedInsight === insight.id

            return (
              <motion.div
                key={insight.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className={`border rounded-lg p-4 cursor-pointer transition-all ${getColorClasses(insight.type)} ${
                  isExpanded ? 'ring-2 ring-offset-2 ring-primary-500' : ''
                }`}
                onClick={() => setSelectedInsight(isExpanded ? null : insight.id)}
              >
                <div className="flex items-start space-x-3">
                  <Icon className={`h-5 w-5 flex-shrink-0 mt-0.5 ${getIconColorClasses(insight.type)}`} />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h3 className="text-sm font-medium">{insight.title}</h3>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-medium px-2 py-1 rounded-full bg-white bg-opacity-60">
                          {Math.round(insight.confidence * 100)}% confidence
                        </span>
                      </div>
                    </div>
                    <p className="mt-1 text-sm opacity-90">{insight.description}</p>
                    
                    {isExpanded && insight.actions && insight.actions.length > 0 && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-3 pt-3 border-t border-current border-opacity-20"
                      >
                        <p className="text-xs font-medium mb-2">Recommended Actions:</p>
                        <ul className="space-y-1">
                          {insight.actions.map((action, idx) => (
                            <li key={idx} className="text-xs flex items-center space-x-2">
                              <span className="w-1 h-1 rounded-full bg-current"></span>
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </motion.div>
                    )}
                    
                    <div className="mt-2 text-xs opacity-75">
                      {new Date(insight.timestamp).toLocaleString()}
                    </div>
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
