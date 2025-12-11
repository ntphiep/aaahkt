'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  CpuChipIcon,
  ArrowTrendingUpIcon,
  ArrowPathIcon,
  CheckCircleIcon,
  ClockIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import { useAPI } from '../hooks/useAPI'

interface OptimizationRecommendation {
  id: string
  type: string
  current_value: any
  recommended_value: any
  expected_improvement: number
  confidence: number
  reasoning: string
}

interface RLStats {
  model_accuracy: number
  total_optimizations: number
  success_rate: number
  learning_episodes: number
  last_training: string
}

export default function RLOptimization() {
  const { data: optimization, error, isLoading, refetch } = useAPI('/api/oumi/optimization')
  const [isOptimizing, setIsOptimizing] = useState(false)

  const handleOptimize = async () => {
    setIsOptimizing(true)
    try {
      // Trigger new optimization
      await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/oumi/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      })
      
      // Refresh data
      refetch()
    } catch (error) {
      console.error('Optimization failed:', error)
    } finally {
      setIsOptimizing(false)
    }
  }

  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-2/3 mb-4"></div>
          <div className="space-y-3">
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
          Failed to load RL optimization data
        </div>
      </div>
    )
  }

  const recommendations: OptimizationRecommendation[] = optimization?.recommendations || []
  const stats: RLStats = optimization?.stats || {
    model_accuracy: 0,
    total_optimizations: 0,
    success_rate: 0,
    learning_episodes: 0,
    last_training: 'Never'
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-2">
          <CpuChipIcon className="h-6 w-6 text-purple-600" />
          <h2 className="text-xl font-semibold text-gray-900">RL Optimization</h2>
        </div>
        <button
          onClick={handleOptimize}
          disabled={isOptimizing}
          className="btn-secondary text-sm flex items-center space-x-2"
        >
          <ArrowPathIcon className={`h-4 w-4 ${isOptimizing ? 'animate-spin' : ''}`} />
          <span>{isOptimizing ? 'Optimizing...' : 'Optimize'}</span>
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs text-purple-700 font-medium">Model Accuracy</span>
            <ChartBarIcon className="h-4 w-4 text-purple-600" />
          </div>
          <div className="mt-1 text-2xl font-bold text-purple-900">
            {Math.round(stats.model_accuracy * 100)}%
          </div>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs text-green-700 font-medium">Success Rate</span>
            <CheckCircleIcon className="h-4 w-4 text-green-600" />
          </div>
          <div className="mt-1 text-2xl font-bold text-green-900">
            {Math.round(stats.success_rate * 100)}%
          </div>
        </div>

        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs text-blue-700 font-medium">Total Optimizations</span>
            <ArrowTrendingUpIcon className="h-4 w-4 text-blue-600" />
          </div>
          <div className="mt-1 text-2xl font-bold text-blue-900">
            {stats.total_optimizations}
          </div>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg p-3">
          <div className="flex items-center justify-between">
            <span className="text-xs text-orange-700 font-medium">Episodes</span>
            <ClockIcon className="h-4 w-4 text-orange-600" />
          </div>
          <div className="mt-1 text-2xl font-bold text-orange-900">
            {stats.learning_episodes}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h3 className="text-sm font-medium text-gray-900 mb-3">Current Recommendations</h3>
        
        {recommendations.length === 0 ? (
          <div className="text-center py-6 bg-gray-50 rounded-lg">
            <CpuChipIcon className="mx-auto h-8 w-8 text-gray-400" />
            <p className="mt-2 text-sm text-gray-500">No optimizations recommended</p>
            <p className="text-xs text-gray-400 mt-1">System is performing optimally</p>
          </div>
        ) : (
          <div className="space-y-3">
            {recommendations.slice(0, 3).map((rec, index) => (
              <motion.div
                key={rec.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gradient-to-r from-purple-50 to-transparent border border-purple-200 rounded-lg p-3"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-900">{rec.type}</span>
                      <span className="text-xs px-2 py-0.5 rounded-full bg-purple-100 text-purple-700">
                        +{rec.expected_improvement.toFixed(1)}% improvement
                      </span>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">{rec.reasoning}</p>
                    
                    <div className="mt-2 flex items-center space-x-4 text-xs">
                      <div>
                        <span className="text-gray-500">Current: </span>
                        <span className="font-medium text-gray-900">
                          {typeof rec.current_value === 'object' 
                            ? JSON.stringify(rec.current_value) 
                            : rec.current_value}
                        </span>
                      </div>
                      <div>
                        <span className="text-gray-500">→ Recommended: </span>
                        <span className="font-medium text-purple-700">
                          {typeof rec.recommended_value === 'object' 
                            ? JSON.stringify(rec.recommended_value) 
                            : rec.recommended_value}
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="ml-3 text-right">
                    <div className="text-xs text-gray-500">Confidence</div>
                    <div className="text-sm font-bold text-purple-900">
                      {Math.round(rec.confidence * 100)}%
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {/* Last Training Info */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Powered by Oumi RL</span>
          <span>Last training: {stats.last_training}</span>
        </div>
      </div>
    </div>
  )
}
