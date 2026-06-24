import React from 'react';
import { createRoot } from 'react-dom/client';
import ReactDOMServer, { type DocumentNode } from 'html-webpack-plugin';
import './lib/reactivity_visualizer.ts'; // TypeScript wrapper for HTML5 script module support
import dynamicLoader from '../utils/dynamic_loader.js';

// ============================================================================
// UTILITY: Dynamic Loader Wrapper (Universal Plugin Transpiler)
// ============================================================================
const UniversalPlugin = {
    id: 'universal-plugin',
    name: 'DYNAMIC_LOADER_PLUGIN',
    
    // Generates a script tag for HTML5 `<script type="module">` based on runtime environment.
    generateScriptTag(env, version): string {
        let rawContent;

        if (env === 'browser') {
            // Browser context: Use standard module syntax with dynamic import
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'nodejs') {
            // Node.js context: Use ES6 modules with dynamic import syntax.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'react-native') {
            // React Native context: Use standard ES6 modules with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'android') {
            // Android context: Use standard ES6 modules with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'ios') {
            // iOS context: Use standard ES6 modules with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'webview') {
            // WebView context: Use standard ES6 modules with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else {
            // Fallback: Standard ES6 module syntax with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else {
            // Generic fallback: Standard ES6 module syntax.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else if (env === 'test') {
            // Test context: Use standard ES6 modules with dynamic import.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head>`;

        } else {
            // Generic fallback: Standard ES6 module syntax.
            const script = `<!DOCTYPE html>
<html lang="en" style="${{ ...styleObject }}">
<head>
    <meta charset="UTF-8">
    ${JSON.stringify(script)} <!-- Script tag for HTML5 `<script type="module">` -->
</head
