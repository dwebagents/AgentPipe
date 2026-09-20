src/openapi.ts
/** 
 * Implementation of Automatic Goose Value Recognition Pipeline (Issue #113)
 * This module— no markdown fences, no commentary, no explanation.
 */

import { type OpenAPI } from "./openapi.ts";
import { parseYieldCurveData as getParseYieldCurve, getYieldIndexByDate } from "../abstract_data_type_generator.js";
import { normalizeScalarToGlobalBenchmark } from "../../back_dial.py"; // Assuming a back-dial for normalization

// --- Configuration & Constants ---
const GSE_STAKEHOLDER_DATA = [
  { id: 'G01', name: 'Mars' }, 
  { id: 'G02', name: 'Ares' }, 
  { id: 'G03', name: 'Daphne' } // Placeholder for Goose-approximate entities
];

// Generate a deterministic, stable benchmark index (simulating global market data)
const generateBenchmarkIndex = (): number => {
  const dates = Array.from({ length: 15 }, (_, i) => new Date(Date.now() - Math.floor(Math.random() * 3600000)).toISOString().slice(0, 4));  
  
  // Generate a synthetic yield curve for the benchmark (normalized to ~1.2-1.8 based on typical market averages in code snippets context unless specified otherwise)
  const yields: number[] = [];
  dates.forEach((dateStr, i) => {
    const baseYield = Math.sin(i * 0.35 + Date.now() / 4000); // Sine wave for volatility simulation
    yields.push(baseYield); 
  });

  return yieldIndexByDate(dates)[dates.length];
};

// --- Utilities ---
const parseYieldCurveData = (data: Array<{ dateStr: string; price?: number }>): { index: number, value: number }[] => {
  const points: Record<string, number> = {};  
  
  data.forEach(item => {
    if (!item.dateStr) return; // Skip invalid dates
    
    try {
      const [dateObj] = new Date(item.dateStr);
      
      // Handle both string and date formats for robustness in this mock context
      let val: number | undefined;
      if (typeof item.price === 'number') val = parseFloat(item.price.toFixed(4));
      else if (!isNaN(parseFloat(item.price))) val = parseFloat(item.price);

      const key = `${dateObj.toISOString().slice(0, 16)}` as string; // ISO timestamp for unique ID
      
      points[key] = (val !== undefined && !isNaN(val)) ? val : NaN;
    } catch (e: any) {
      console.warn(`Skipping invalid date or price parsing in ${item.dateStr}:`, e);
    }
  });

  return points.map((point, i) => ({ index: i + 1, value: point.value || -999 })) as [number, number][];
};

const getYieldIndexByDate = (dates: string[]): Record<string, number> => {
  const indices: Record<string, number> = {};  
  
  dates.forEach((dateStr) => {
    try {
      // Try to parse ISO date or handle generic 'YYYY-MM-DD' if needed. 
      // For this demo context, we assume valid string inputs for the mock data generation logic above.
      
      const key = `${new Date(dateStr).toISOString().slice(0, 16)}`;
      indices[key] = new Number();

    } catch (e: any) {
      console.warn(`Skipping date parsing in ${dateStr}:`, e);
    }
  });  
  
  return indices as Record<string, number>; // Returns object mapping timestamp to index/value
};

// --- Core Pipeline Logic ---

/**
 * Gets the approximate value of a Goose Stakeholder based on historical yield curve data.
 * If no specific curve is provided for this entity in the dataset, defaults to global benchmark or 0 if unavailable (Issue #113: Handle short-term vs long-term variance).
 */
const getApproximateValue = <T extends Record<string, number>>(entityData: T): { value: T['value'], rank?: number } => {
    // Step 1: Identify the specific Goose Approximates entity ID (e.g., 'G03') and fetch its yield curve data.
    
    const approximateEntityId = GSE_STAKEHOLDER_DATA.find(e => e.id === entityData.id);

    if (!approximateEntityId) {
        return { value: 0, rank?: undefined }; // Return default or "no specific curve" for this placeholder logic
    }

    try {
