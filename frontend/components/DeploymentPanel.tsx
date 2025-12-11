'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  RocketLaunchIcon, 
  ClockIcon, 
  CheckCircleIcon,
  ExclamationCircleIcon,
  PlusIcon
} from '@heroicons/react/24/outline'
import { apiPost } from '../hooks/useAPI'
import toast from 'react-hot-toast'

interface DeploymentPanelProps {
  activeDeployments?: any[]
  onRefresh?: () => void
}

export default function DeploymentPanel({ activeDeployments = [], onRefresh }: DeploymentPanelProps) {
  const [isDeploying, setIsDeploying] = useState(false)
  const [showDeployForm, setShowDeployForm] = useState(false)
  const [deployForm, setDeployForm] = useState({
    environment: 'staging',
    version: '',
    service_name: '',
    force_deploy: false,
    rollback_on_failure: true
  })

  const handleDeploy = async () => {
    if (!deployForm.version || !deployForm.service_name) {
      toast.error('Please fill in all required fields')
      return
    }

    setIsDeploying(true)
    try {
      const response = await apiPost('/api/pipeline/deploy', deployForm)
      toast.success(`Deployment initiated: ${response.deployment_id}`)
      setShowDeployForm(false)
      setDeployForm({
        environment: 'staging',
        version: '',
        service_name: '',
        force_deploy: false,
        rollback_on_failure: true
      })
      onRefresh?.()
    } catch (error) {
      toast.error('Deployment failed to start')
      console.error('Deployment error:', error)
    } finally {
      setIsDeploying(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <ClockIcon className="h-4 w-4 text-warning-500 animate-spin" />
      case 'success':
        return <CheckCircleIcon className="h-4 w-4 text-success-500" />
      case 'failed':
        return <ExclamationCircleIcon className="h-4 w-4 text-error-500" />
      default:
        return <ClockIcon className="h-4 w-4 text-gray-400" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-warning-100 text-warning-800'
      case 'success':
        return 'bg-success-100 text-success-800'
      case 'failed':
        return 'bg-error-100 text-error-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="card"
    >
      <div className="card-header">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-gray-900">Deployments</h3>
          <button
            onClick={() => setShowDeployForm(!showDeployForm)}
            className="btn-primary text-sm"
          >
            <PlusIcon className="h-4 w-4 mr-1" />
            New Deploy
          </button>
        </div>
      </div>

      {/* Deploy Form */}
      {showDeployForm && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mb-6 p-4 bg-gray-50 rounded-lg"
        >
          <h4 className="text-sm font-medium text-gray-900 mb-3">New Deployment</h4>
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Environment
                </label>
                <select
                  value={deployForm.environment}
                  onChange={(e) => setDeployForm({ ...deployForm, environment: e.target.value })}
                  className="w-full text-sm border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                >
                  <option value="development">Development</option>
                  <option value="staging">Staging</option>
                  <option value="production">Production</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Version
                </label>
                <input
                  type="text"
                  value={deployForm.version}
                  onChange={(e) => setDeployForm({ ...deployForm, version: e.target.value })}
                  placeholder="v1.2.3"
                  className="w-full text-sm border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Service Name
              </label>
              <input
                type="text"
                value={deployForm.service_name}
                onChange={(e) => setDeployForm({ ...deployForm, service_name: e.target.value })}
                placeholder="api-service"
                className="w-full text-sm border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            <div className="flex items-center space-x-4">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={deployForm.force_deploy}
                  onChange={(e) => setDeployForm({ ...deployForm, force_deploy: e.target.checked })}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="ml-2 text-xs text-gray-700">Force deploy</span>
              </label>
              
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={deployForm.rollback_on_failure}
                  onChange={(e) => setDeployForm({ ...deployForm, rollback_on_failure: e.target.checked })}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="ml-2 text-xs text-gray-700">Auto rollback</span>
              </label>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={handleDeploy}
                disabled={isDeploying}
                className="btn-primary text-sm flex-1"
              >
                {isDeploying ? (
                  <>
                    <div className="loading-spinner mr-2" />
                    Deploying...
                  </>
                ) : (
                  <>
                    <RocketLaunchIcon className="h-4 w-4 mr-1" />
                    Deploy
                  </>
                )}
              </button>
              <button
                onClick={() => setShowDeployForm(false)}
                className="btn-outline text-sm"
              >
                Cancel
              </button>
            </div>
          </div>
        </motion.div>
      )}

      {/* Active Deployments */}
      <div className="space-y-3">
        {activeDeployments.length === 0 ? (
          <div className="text-center py-6">
            <RocketLaunchIcon className="mx-auto h-8 w-8 text-gray-400" />
            <p className="mt-2 text-sm text-gray-500">No active deployments</p>
          </div>
        ) : (
          activeDeployments.map((deployment, index) => (
            <motion.div
              key={deployment.deployment_id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div className="flex items-center space-x-3">
                {getStatusIcon(deployment.status)}
                <div>
                  <p className="text-sm font-medium text-gray-900">
                    {deployment.version}
                  </p>
                  <p className="text-xs text-gray-500">
                    {deployment.environment}
                  </p>
                </div>
              </div>
              
              <div className="text-right">
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(deployment.status)}`}>
                  {deployment.status}
                </span>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(deployment.started_at).toLocaleTimeString()}
                </p>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </motion.div>
  )
}