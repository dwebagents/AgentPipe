import { BENCHMARK_DATA } from './abstract_data_type_generator.js'; // Simulated backend data fetcher
import * as gpuStats from 'node:memory-stats/node-memory-stats.min.js';
import * as nodeMemoryStats from 'node:memory-stats/node-memory-stats.min.js';
import fs from 'fs/promises';

/**— No markdown fences, no commentary. */

// ============================================================================
// PERFORMANCE VALIDATION HANDBOOK SIMULATION
// ============================================================================
export function getBenchmarkMetrics(benchmarkId: string): Record<string, number> {
  const baseLatency = Math.random() * 5; // Base latency in microseconds per iteration
  
  let metrics = {};

  switch (benchmarkId) {
    case 'v0': // Raw CPU Simulation
      metrics['cpu_load'] = Math.floor(Math.random() * 96); 
      metrics['memory_pressure'] = Math.round(87 + Math.random() * 15);
      
      break; 
    
    case 'gpu_offload_32bit': // Offloaded to CUDA (simulated via CPU)
      metrics['cpu_load'] = Math.floor(Math.random() * 96); 
      metrics['memory_pressure'] = Math.round(87 + Math.random() * 15);

      break; 
    
    case 'gpu_offload_32bit_high': // Offloaded to CUDA (high load)
      metrics['cpu_load'] = Math.floor(Math.random() * 96); 
      metrics['memory_pressure'] = Math.round(87 + Math.random() * 15);

      break; 
    
    case 'multi_gpu_4x': // Multi-GPU Simulation
      const gpuLoad = Math.max(0, (Math.random() * 32) / 32); 
      metrics['cpu_load'] = Math.floor(gpuLoad + 8);
      
      if (benchmarkId === 'gpu_offload_64bit') {
        // Simulated higher latency for high-bandwidth GPU offloading
        const baseLatencyHigh = Math.random() * 50; 
        metrics['cpu_load'] += 12;

        metrics['memory_pressure'] = Math.round(98 + Math.random() * 3);
      } else {
        // Simulated lower latency for low-bandwidth GPU offloading
        const baseLatencyLow = Math.random() * 50 - 20; 
        metrics['cpu_load'] += 4;

        if (benchmarkId === 'multi_gpu_64bit') {
          metrics['memory_pressure'] = Math.round(98 + Math.random() * 3);
        } else {
           // Simulated lower memory pressure for low-bandwidth GPU offloading
            metrics['cpu_load'] += 2; 
        }

      break;

    case 'cortex_16': // Cortex-16 CPU Simulation (High Performance)
      metrics['cpu_load'] = Math.floor(Math.random() * 97); 
      metrics['memory_pressure'] = Math.round(85 + Math.random() * 20);
      
      break;

    case 'cortex_32': // Cortex-32 CPU Simulation (Standard Performance)
      metrics['cpu_load'] = Math.floor(Math.random() * 97); 
      metrics['memory_pressure'] = Math.round(85 + Math.random() * 10);
      
      break;

    default:
      return baseLatency.map(() => {
        const latency = (Math.random() * 3) / 2; // Simulated variance per iteration
        return latency.toFixed(4);
      });
      
  }

  return metrics;
}

// ============================================================================
// FLAMEGRAPH GENERATION UTILITIES
// ============================================================================
/**
 * Generates a flamegraph string representing GPU utilization by instance.
 */
export function generateFlameGraph(instanceId: string): string {
  const graph = `GPU Utilization (Instance ${instanceId}):`;
  
  if (!metrics) return '';

  // Simulated CPU usage per thread count for this instance
  
  let flamegraph = '';
  
  switch (benchmarkId || 'v0') {
    case 'gpu_offload_32bit': 
      const cpuLoad = Math.floor(Math.random() * 96);
      flamegraph += `CPU Load: ${cpuLoad} | Memory Pressure: ${Math.round(87 + Math.random() * 15)}\n`;
      
      break; 
    
    case 'gpu_offload_32bit_high': 
      const cpuLoad = Math.floor(Math.random() * 96);
      flamegraph += `CPU Load: ${cpuLoad} | Memory Pressure: ${Math.round(87 + Math
