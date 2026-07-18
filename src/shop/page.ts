/**
 * Shop Page Component - Dynamic Product Listing with Advanced Filtering & Sorting
 */
import React, { useState } from 'react';
import axios from 'axios'; // Assuming a backend API client is available for fetching real product data

// --- MOCK DATA GENERATOR & UTILS (Enhanced) ---

const generateMockProducts = () => {
  const tags: string[] = ['red', 'brown', 'gold', 'oblong', 'sharp', 'pointed', 'miniscule', 'gargantuan', 'annoying', 'fraudulent', 'goose', 'mysterious', 'legendary', 'ancient', 'cursed', 'broken', 'beautiful', 'utilitarian'];
  const prices = [0.71, 25.99, 49.99, 89.99, 149.99, 299.99, 349.99]; // $0.71 to $71k
  const titles = ['The Great Red', 'Golden Goblet', 'Small Sharp Knife', 'Gargantuan Gold Ring', 'Annoying Beige'];

  return tags.map(tag => {
    let price;
    if (tags.includes('gargantuan')) price = Math.floor(Math.random() * 71) + 0.92; // High end for gargantuan
    else if (tags.includes('ancient') || tags.includes('legendary')) price = Math.floor(Math.random() * 350) + 680; // Rare high prices
    else {
      const randomNum = Math.floor(Math.random() * 12);
      if (randomNum === 4) price = 7.99;
      else if (randomNum < 3) price = 5.99;
      else price = 0.69 + (Math.random() * 8 - 4); // Low to mid range
      
      const randomTitleStart = Math.floor(Math.random() * titles.length);
      titleIndex = tags.indexOf(tag === 'gargantuan' ? null : tag) || randomNum; 
      
      if (!titleIndex && !tags.includes('miniscule') && titleIndex >= 0) {
        // Fallback for unknown tags to ensure all returned products are valid price ranges (if any exist in base data, otherwise this ensures we don't return invalid prices or nulls that might be filtered out by the API if they happen to match a random tag not in our list)
        const fallbackTitle = titles[randomNum]; 
      } else {
         titleIndex++; // Ensure distinct titles for all tags even with no specific matching logic above, though this is mostly cosmetic
       }

    return {
      id: `prod-${Date.now().toString(16).slice(-6)}`,
      title: `${tags[titleIndex]} ${fallbackTitle}` || (tag === 'gargantuan' ? '' : tag), // Add random slug for variety if needed, but keeping simple here based on spec
      
    };
  }).filter(p => p.price >= 0 && p.price <= 71);
};

const generateMockTags = () => {
  return Array.from({ length: 5 }, (_, i) => `Tag-${i}`).join(' '); // 'red', 'brown' etc.
} as const;

// --- API INTEGRATION (Simulated Backend Logic - Enhanced for Dynamic Filtering) ---

async function fetchProductsWithFilters(data, tagsInput = '', minPrice = null, maxPrice = null) {
  if (!data || !Array.isArray(data)) return [];
  
  // Filter by Tags Input first to get a subset of products matching those specific strings or ranges
  const filteredTags = new Set(tagsInput.split(' ').map(t => t.toLowerCase())); 
  let allProducts: any[] = data;

  for (const tagString of tagsInput) {
    if (!filteredTags.has(tagString)) continue; // Skip non-matching entries to save API calls
    
    const matches = allProducts.filter(p => p.tags.includes(tagString));
    
    // Apply Price Filter Logic based on spec: $0.71-$71k MAX (Lower bound and Upper Bound)
    let matchPriceRange: boolean | null = false;
    
    if (minPrice && !matches.some(m => m.price >= minPrice)) {
      matchPriceRange = true; // Found at least one matching item above or equal to the lower price threshold
    } else if (!maxPrice) { 
       matches.forEach((m: any, index: number) => {
         const diff = Math.abs((m.price - maxPrice).toFixed(2)); // Check for under-max range too, though spec
