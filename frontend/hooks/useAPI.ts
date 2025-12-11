'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface UseAPIResult<T> {
  data: T | null
  error: Error | null
  isLoading: boolean
  refetch: () => void
}

export function useAPI<T = any>(endpoint: string, refreshKey?: number): UseAPIResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const fetchData = async () => {
    try {
      setIsLoading(true)
      setError(null)
      
      const response = await axios.get(`${API_BASE_URL}${endpoint}`, {
        timeout: 10000,
        headers: {
          'Content-Type': 'application/json',
        },
      })
      
      setData(response.data)
    } catch (err) {
      console.error(`API Error for ${endpoint}:`, err)
      
      // Create mock data for demo purposes when API is not available
      const mockData = createMockData(endpoint)
      if (mockData) {
        setData(mockData as T)
        console.log(`Using mock data for ${endpoint}`)
      } else {
        setError(err instanceof Error ? err : new Error('API request failed'))
      }
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [endpoint, refreshKey])

  return {
    data,
    error,
    isLoading,
    refetch: fetchData,
  }
}

// Mock data generator for demo purposes
function createMockData(endpoint: string): any {
  if (endpoint.includes('/monitoring/dashboard')) {
    return {
      system_health: {
        overall_status: 'healthy',
        services: {
          aws: { status: 'healthy', response_time: 120 },
          kestra: { status: 'healthy', active_workflows: 3 },
          oumi_rl: { status: 'healthy', model_accuracy: 0.87 }
        },
        alerts: [],
        last_updated: new Date().toISOString()
      },
      active_deployments: [
        {
          deployment_id: 'deploy_staging_v1.2.3',
          environment: 'staging',
          version: 'v1.2.3',
          status: 'running',
          started_at: new Date(Date.now() - 300000).toISOString()
        }
      ],
      cost_metrics: {
        current_month_cost: 245.67,
        projected_month_cost: 320.45,
        cost_by_service: {
          Lambda: 45.23,
          S3: 12.34,
          CloudWatch: 8.90,
          DynamoDB: 15.67
        },
        cost_trend: 'increasing'
      },
      recent_activities: [
        {
          id: 1,
          type: 'deployment',
          message: 'Deployed api-service v1.2.3 to staging',
          timestamp: new Date(Date.now() - 600000).toISOString(),
          status: 'success'
        },
        {
          id: 2,
          type: 'ai_decision',
          message: 'AI Agent recommended scaling up based on traffic patterns',
          timestamp: new Date(Date.now() - 900000).toISOString(),
          status: 'info'
        },
        {
          id: 3,
          type: 'rl_optimization',
          message: 'RL model optimized timeout configuration for 12% improvement',
          timestamp: new Date(Date.now() - 1200000).toISOString(),
          status: 'success'
        }
      ]
    }
  }

  if (endpoint.includes('/aws/metrics')) {
    return {
      timestamp: new Date().toISOString(),
      service: 'all',
      lambda: {
        function_count: 5,
        functions: [
          {
            name: 'api-handler',
            runtime: 'python3.9',
            memory_size: 512,
            timeout: 300,
            metrics: {
              invocations: 1250,
              errors: 12,
              error_rate: 0.0096,
              average_duration: 245.6
            }
          },
          {
            name: 'data-processor',
            runtime: 'python3.9',
            memory_size: 1024,
            timeout: 600,
            metrics: {
              invocations: 890,
              errors: 3,
              error_rate: 0.0034,
              average_duration: 1200.3
            }
          }
        ]
      },
      s3: {
        bucket_count: 3,
        buckets: [
          {
            name: 'devops-pipeline-data',
            creation_date: '2024-01-01T00:00:00Z',
            object_count: 1250
          },
          {
            name: 'devops-pipeline-logs',
            creation_date: '2024-01-01T00:00:00Z',
            object_count: 5600
          }
        ]
      },
      dynamodb: {
        table_count: 2,
        tables: [
          {
            name: 'pipeline-state',
            status: 'ACTIVE',
            item_count: 1500,
            table_size_bytes: 2048000
          },
          {
            name: 'deployment-history',
            status: 'ACTIVE',
            item_count: 890,
            table_size_bytes: 1024000
          }
        ]
      },
      cloudwatch: {
        available_metrics: 45,
        namespaces: ['AWS/Lambda', 'AWS/S3', 'AWS/DynamoDB', 'Custom/DevOps'],
        sample_metrics: []
      }
    }
  }

  return null
}

export async function apiPost<T = any>(endpoint: string, data: any): Promise<T> {
  try {
    const response = await axios.post(`${API_BASE_URL}${endpoint}`, data, {
      timeout: 15000,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.data
  } catch (error) {
    console.error(`API POST Error for ${endpoint}:`, error)
    throw error
  }
}

export async function apiPut<T = any>(endpoint: string, data: any): Promise<T> {
  try {
    const response = await axios.put(`${API_BASE_URL}${endpoint}`, data, {
      timeout: 15000,
      headers: {
        'Content-Type': 'application/json',
      },
    })
    return response.data
  } catch (error) {
    console.error(`API PUT Error for ${endpoint}:`, error)
    throw error
  }
}