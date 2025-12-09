'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  ChartBarIcon, 
  CpuChipIcon, 
  CloudIcon, 
  BoltIcon,
  ArrowTrendingUpIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import DashboardLayout from '../components/DashboardLayout'
import MetricCard from '../components/MetricCard'
import SystemHealth from '../components/SystemHealth'
import DeploymentPanel from '../components/DeploymentPanel'
import AIInsights from '../components/AIInsights'
import RLOptimization from '../components/RLOptimization'
import RecentActivity from '../components/RecentActivity'
import { useAPI } from '../hooks/useAPI'

export default function Dashboard() {
  const [refreshKey, setRefreshKey] = useState(0)
  const { data: dashboardData, error, isLoading } = useAPI('/api/monitoring/dashboard', refreshKey)
  const { data: healthData } = useAPI('/api/aws/metrics?service=all', refreshKey)

  // Auto-refresh every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setRefreshKey(prev => prev + 1)
    }, 30000)
    
    return () => clearInterval(interval)
  }, [])

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1)
  }

  if (error) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-error-500" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">Error loading dashboard</h3>
            <p className="mt-1 text-sm text-gray-500">{error.message}</p>
            <button
              onClick={handleRefresh}
              className="mt-4 btn-primary"
            >
              Try Again
            </button>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout onRefresh={handleRefresh} isLoading={isLoading}>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              DevOps Pipeline Dashboard
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              AI-powered automation with real-time monitoring and optimization
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1 text-sm text-gray-500">
              <ClockIcon className="h-4 w-4" />
              <span>Last updated: {new Date().toLocaleTimeString()}</span>
            </div>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            title="System Health"
            value={dashboardData?.system_health?.overall_status || 'Unknown'}
            icon={CheckCircleIcon}
            trend={dashboardData?.system_health?.overall_status === 'healthy' ? 'positive' : 'negative'}
            color={dashboardData?.system_health?.overall_status === 'healthy' ? 'success' : 'error'}
          />
          
          <MetricCard
            title="Active Deployments"
            value={dashboardData?.active_deployments?.length || 0}
            icon={BoltIcon}
            trend="neutral"
            color="primary"
          />
          
          <MetricCard
            title="Monthly Cost"
            value={`$${dashboardData?.cost_metrics?.current_month_cost?.toFixed(2) || '0.00'}`}
            icon={ChartBarIcon}
            trend={dashboardData?.cost_metrics?.cost_trend === 'increasing' ? 'negative' : 'positive'}
            color="warning"
            subtitle={`Projected: $${dashboardData?.cost_metrics?.projected_month_cost?.toFixed(2) || '0.00'}`}
          />
          
          <MetricCard
            title="Lambda Functions"
            value={healthData?.lambda?.function_count || 0}
            icon={CpuChipIcon}
            trend="neutral"
            color="info"
            subtitle={`${healthData?.lambda?.functions?.filter((f: any) => f.metrics?.error_rate < 0.05).length || 0} healthy`}
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="lg:col-span-2 space-y-6">
            {/* System Health */}
            <SystemHealth data={dashboardData?.system_health} />
            
            {/* AI Insights */}
            <AIInsights />
            
            {/* Recent Activity */}
            <RecentActivity activities={dashboardData?.recent_activities} />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            {/* Deployment Panel */}
            <DeploymentPanel 
              activeDeployments={dashboardData?.active_deployments}
              onRefresh={handleRefresh}
            />
            
            {/* RL Optimization */}
            <RLOptimization />
          </div>
        </div>

        {/* AWS Services Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CloudIcon className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">Lambda</h3>
                <p className="text-sm text-gray-500">
                  {healthData?.lambda?.function_count || 0} functions
                </p>
                <div className="mt-2">
                  {healthData?.lambda?.functions?.map((func: any, index: number) => (
                    <div key={index} className="flex items-center space-x-2 text-xs">
                      <div className={`status-indicator ${
                        func.metrics?.error_rate < 0.05 ? 'bg-success-500' : 
                        func.metrics?.error_rate < 0.1 ? 'bg-warning-500' : 'bg-error-500'
                      }`} />
                      <span className="truncate">{func.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-success-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">S3</h3>
                <p className="text-sm text-gray-500">
                  {healthData?.s3?.bucket_count || 0} buckets
                </p>
                <div className="mt-2 text-xs text-gray-600">
                  Total objects: {healthData?.s3?.buckets?.reduce((sum: number, bucket: any) => 
                    sum + (bucket.object_count || 0), 0) || 0}
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CpuChipIcon className="h-8 w-8 text-warning-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">DynamoDB</h3>
                <p className="text-sm text-gray-500">
                  {healthData?.dynamodb?.table_count || 0} tables
                </p>
                <div className="mt-2 text-xs text-gray-600">
                  Active tables: {healthData?.dynamodb?.tables?.filter((table: any) => 
                    table.status === 'ACTIVE').length || 0}
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ArrowTrendingUpIcon className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-medium text-gray-900">CloudWatch</h3>
                <p className="text-sm text-gray-500">
                  {healthData?.cloudwatch?.available_metrics || 0} metrics
                </p>
                <div className="mt-2 text-xs text-gray-600">
                  Namespaces: {healthData?.cloudwatch?.namespaces?.length || 0}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </DashboardLayout>
  )
}