'use client'

import { motion } from 'framer-motion'
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid'

interface MetricCardProps {
  title: string
  value: string | number
  icon: React.ComponentType<{ className?: string }>
  trend?: 'positive' | 'negative' | 'neutral'
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info'
  subtitle?: string
  change?: string
}

const colorClasses = {
  primary: 'text-primary-600 bg-primary-50',
  success: 'text-success-600 bg-success-50',
  warning: 'text-warning-600 bg-warning-50',
  error: 'text-error-600 bg-error-50',
  info: 'text-blue-600 bg-blue-50',
}

export default function MetricCard({
  title,
  value,
  icon: Icon,
  trend = 'neutral',
  color = 'primary',
  subtitle,
  change
}: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
      className="metric-card"
    >
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
            <Icon className="h-6 w-6" />
          </div>
        </div>
        
        <div className="ml-4 flex-1">
          <div className="flex items-center justify-between">
            <p className="metric-label">{title}</p>
            {trend !== 'neutral' && (
              <div className={`flex items-center ${
                trend === 'positive' ? 'text-success-600' : 'text-error-600'
              }`}>
                {trend === 'positive' ? (
                  <ArrowUpIcon className="h-4 w-4" />
                ) : (
                  <ArrowDownIcon className="h-4 w-4" />
                )}
              </div>
            )}
          </div>
          
          <div className="mt-1">
            <p className="metric-value">{value}</p>
            {subtitle && (
              <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
            )}
            {change && (
              <p className={`metric-change mt-1 ${
                trend === 'positive' ? 'positive' : 
                trend === 'negative' ? 'negative' : ''
              }`}>
                {change}
              </p>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  )
}