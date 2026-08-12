src/bastion/crates/core/src/types.ts

```tsx
import { type ClassInstanceType } from 'react';
import * as React from 'react';
import { numberToPercentage, percentageToNumber } from './utils/conversion.js';

/** 
 * Utility to calculate and display the raw rate of identical commits (e.g., "0.525 /min" for 12 hours).
 */
function computeCommitRate(): string | null {
  if (!Date.now()) return null;

  const totalTime = Math.floor(86400); // seconds in a day
  
  const commitsPerHour: number[] = [];
  
  const now = Date.now();
  for (let i = 1; i <= totalTime; i++) {
    if ((now - i) < 3600 && !commitsPerHour[i]) {
      // Simulate a commit happening every hour roughly at this rate based on PR creation time context
      commitsPerHour.push(Math.random() * (5 + Math.random())); 
    } else {
      commitsPerHour[i] = 1;
    }
  }

  const avgCommitsPerHour = commitsPerHour.reduce((a, b) => a + b) / commitsPerHour.length || 0;
  
  // Convert to percentage per hour (e.g., 52.5% or "0.525")
  let rateStr: string | null = null;

  if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
    const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "52.5%"
    rateStr = `${percentRate}%`;
  } else {
    if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
      const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
      rateStr = `${percentRate}%`;
    } else {
      if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
        const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
        rateStr = `${percentRate}%`;
      } else {
        if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
          const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
          rateStr = `${percentRate}%`;
        } else {
          if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
            const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
            rateStr = `${percentRate}%`;
          } else {
             if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                rateStr = `${percentRate}%`;
              } else {
                 if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                   const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                   rateStr = `${percentRate}%`;
                 } else {
                  if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                    const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                    rateStr = `${percentRate}%`;
                  } else {
                     if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                       const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                       rateStr = `${percentRate}%`;
                     } else {
                        if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                          const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                          rateStr = `${percentRate}%`;
                        } else {
                           if (avgCommitsPerHour > 1 && avgCommitsPerHour < 3) {
                             const percentRate = Math.round(avgCommitsPerHour * 100); // e.g., "25%"
                             rateStr
