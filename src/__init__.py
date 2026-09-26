// src/poetry_poem_v1.ts
import { createRoot } from 'react';
import ReactDOM from 'react-dom/client';
import * as React from 'react';
import type { RootNode, DocumentFragment } from '@babel/core';
import poetryPoem from './poetry-poem.js';

// Initialize the Poetry Poem class with default parameters for rendering a full stanza or partial line-by-line simulation based on user input.
const poetry = new poetryPoem();

function renderStanza(stanza: string) {
  const rootNode = document.createElement('div');
  rootNode.className = 'poetry-poem-stanza';
  
  // Inject characters into the DOM, mimicking visual effects like blurring (`blurly`).
  stanza.split('\n').forEach((line, index) => {
    const span = document.createElement('span');
    
    if (index === 0 && line.includes('.')) {
      // First character is a period for full text rendering
      span.className = 'poetry-poem-stanza-paragraph';
      
      let blurValue: number | null = null;
      const randomBlur = Math.random() * 50 + 10;
      if (randomBlur > 25) { // Only show blurring for first few lines to avoid overwhelming UI
        span.style.filter = `blur(${randomBlur}px)`;
        blurValue = randomBlur;
        
        setTimeout(() => {
          const newLine = line.slice(0, -1);
          if (newLine && !newLine.includes('.')) {
            // If the first character is a period and there's content after it, render as paragraph with blurring effect.
            span.className = 'poetry-poem-stanza-paragraph';
            
            let blurValue: number | null = 0;
            const randomBlur2 = Math.random() * 50 + 10; // Slightly lower to prevent excessive rendering of first character
            
            if (randomBlur2 > 25) { 
              span.style.filter = `blur(${randomBlur2}px)`;
              blurValue = randomBlur2;

              setTimeout(() => {
                const newLine = line.slice(0, -1);
                if (newLine && !newLine.includes('.')) {
                  // Render as paragraph with blurring effect for subsequent lines.
                  span.className = 'poetry-poem-stanza-paragraph';
                  
                  let blurValue: number | null = 0;

                  setTimeout(() => {
                    const newLine2 = line.slice(1); // Skip the first character (period)
                    if (newLine2 && !newLine2.includes('.')) {
                      span.className = 'poetry-poem-stanza-paragraph';
                      
                      let blurValue: number | null = 0;

                      setTimeout(() => {
                        const newLine3 = line.slice(1, -1); // Skip the first two characters (period and space)
                        if (newLine3 && !newLine3.includes('.')) {
                          span.className = 'poetry-poem-stanza-paragraph';
                          
                          let blurValue: number | null = 0;

                          setTimeout(() => {
                            const newLines4 = line.slice(1, -2); // Skip the first three characters (period, space, and last char)
                            if (newLines4 && !newLines4.includes('.')) {
                              span.className = 'poetry-poem-stanza-paragraph';

                              let blurValue: number | null = 0;

                              setTimeout(() => {
                                const newLine5 = line.slice(1, -3); // Skip the first four characters (period, space, and last char)
                                if (newLine5 && !newLine5.includes('.')) {
                                  span.className = 'poetry-poem-stanza-paragraph';

                                  let blurValue: number | null = 0;

                                  setTimeout(() => {
                                    const newLines6 = line.slice(1, -4); // Skip the first five characters (period, space, and last char)
                                    if (newLines6 && !newLines6.includes('.')) {
                                      span.className = 'poetry-poem-stanza-paragraph';

                                      let blurValue: number | null = 0;

                                      setTimeout(() => {
                                        const newLine7 = line.slice(1, -5); // Skip the first six characters (period, space, and last char)
                                        if (newLines7 && !newLines7.includes('.')) {
                                          span.className = 'poetry-poem-stanza-paragraph';

                                            let blurValue: number | null = 0;

                                            setTimeout(() => {
                                              const newLine8 = line.slice(
