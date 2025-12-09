'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface PipelineState {
  pipeline_id: string;
  timestamp: string;
  state?: any;
}

interface Metrics {
  invocations?: number;
  errors?: number;
  duration?: number;
  error_rate?: number;
}

export default function Home() {
  const [pipelines, setPipelines] = useState<PipelineState[]>([]);
  const [selectedPipeline, setSelectedPipeline] = useState<string>('');
  const [pipelineDetails, setPipelineDetails] = useState<any>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [rlStats, setRlStats] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState<string>('checking...');

  useEffect(() => {
    checkApiStatus();
    fetchPipelines();
    fetchRLStats();
    
    const interval = setInterval(() => {
      fetchPipelines();
      fetchRLStats();
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const checkApiStatus = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`, { timeout: 5000 });
      setApiStatus('connected');
    } catch (error) {
      setApiStatus('disconnected');
      console.error('API connection failed:', error);
    }
  };

  const fetchPipelines = async () => {
    try {
      const response = await axios.get(`${API_URL}/pipelines`);
      setPipelines(response.data.pipelines || []);
    } catch (error) {
      console.error('Error fetching pipelines:', error);
    }
  };

  const fetchPipelineDetails = async (pipelineId: string) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/pipeline/${pipelineId}`);
      setPipelineDetails(response.data);
    } catch (error) {
      console.error('Error fetching pipeline details:', error);
    }
    setLoading(false);
  };

  const fetchRLStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/rl/stats`);
      setRlStats(response.data);
    } catch (error) {
      console.error('Error fetching RL stats:', error);
    }
  };

  const handlePipelineSelect = (pipelineId: string) => {
    setSelectedPipeline(pipelineId);
    fetchPipelineDetails(pipelineId);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'deployed':
        return 'bg-green-500';
      case 'rolled_back':
        return 'bg-red-500';
      case 'monitoring':
        return 'bg-yellow-500';
      case 'optimizing':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-gray-900 dark:text-white">
            AWS DevOps Pipeline Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Automated pipeline management with Kestra AI Agent and Oumi RL
          </p>
          <div className="mt-4 flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div className={`h-3 w-3 rounded-full ${apiStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm text-gray-600 dark:text-gray-400">
                API: {apiStatus}
              </span>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Total Pipelines</h3>
            <p className="text-3xl font-bold text-blue-600">{pipelines.length}</p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">RL Training Updates</h3>
            <p className="text-3xl font-bold text-purple-600">
              {rlStats?.total_updates || 0}
            </p>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Avg RL Reward</h3>
            <p className="text-3xl font-bold text-green-600">
              {rlStats?.recent_avg_reward?.toFixed(2) || 'N/A'}
            </p>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pipeline List */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Recent Pipelines</h2>
            <div className="space-y-2">
              {pipelines.length === 0 ? (
                <p className="text-gray-500">No pipelines found</p>
              ) : (
                pipelines.map((pipeline) => (
                  <div
                    key={pipeline.pipeline_id}
                    onClick={() => handlePipelineSelect(pipeline.pipeline_id)}
                    className={`p-4 rounded cursor-pointer transition-colors ${
                      selectedPipeline === pipeline.pipeline_id
                        ? 'bg-blue-100 dark:bg-blue-900'
                        : 'bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600'
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-gray-900 dark:text-white">
                        {pipeline.pipeline_id}
                      </span>
                      {pipeline.state?.status && (
                        <span className={`px-2 py-1 rounded text-xs text-white ${getStatusColor(pipeline.state.status)}`}>
                          {pipeline.state.status}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      {new Date(pipeline.timestamp).toLocaleString()}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Pipeline Details */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">Pipeline Details</h2>
            {loading ? (
              <p className="text-gray-500">Loading...</p>
            ) : pipelineDetails ? (
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white">Pipeline ID</h3>
                  <p className="text-gray-600 dark:text-gray-400">{pipelineDetails.pipeline_id}</p>
                </div>
                
                {pipelineDetails.state?.state?.final_decision && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Final Decision</h3>
                    <div className="mt-2 p-3 bg-gray-100 dark:bg-gray-700 rounded">
                      <p className="text-gray-900 dark:text-white">
                        <strong>Action:</strong> {pipelineDetails.state.state.final_decision.action}
                      </p>
                      <p className="text-gray-900 dark:text-white">
                        <strong>Confidence:</strong> {(pipelineDetails.state.state.final_decision.confidence * 100).toFixed(1)}%
                      </p>
                      <p className="text-gray-900 dark:text-white mt-2">
                        <strong>Reasoning:</strong>
                      </p>
                      <ul className="list-disc list-inside text-gray-700 dark:text-gray-300">
                        {pipelineDetails.state.state.final_decision.reasoning?.map((reason: string, idx: number) => (
                          <li key={idx}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}

                {pipelineDetails.state?.state?.metrics && (
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white">Metrics</h3>
                    <div className="mt-2 grid grid-cols-2 gap-2">
                      <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded">
                        <p className="text-xs text-gray-600 dark:text-gray-400">Error Rate</p>
                        <p className="text-lg font-bold text-gray-900 dark:text-white">
                          {pipelineDetails.state.state.metrics.error_rate?.toFixed(2)}%
                        </p>
                      </div>
                      <div className="p-2 bg-gray-100 dark:bg-gray-700 rounded">
                        <p className="text-xs text-gray-600 dark:text-gray-400">Duration (ms)</p>
                        <p className="text-lg font-bold text-gray-900 dark:text-white">
                          {pipelineDetails.state.state.metrics.duration?.toFixed(0)}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-gray-500">Select a pipeline to view details</p>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">System Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="flex items-start gap-3">
              <div className="text-2xl">🤖</div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Kestra AI Agent</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Automated log summarization and intelligent decision-making
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="text-2xl">🧠</div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Oumi RL Optimization</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Continuous learning for deployment strategy optimization
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="text-2xl">☁️</div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">AWS Integration</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  CloudWatch, Lambda, S3, and DynamoDB monitoring
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="text-2xl">🔄</div>
              <div>
                <h3 className="font-semibold text-gray-900 dark:text-white">Automated Rollbacks</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Intelligent rollback decisions based on error patterns
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
