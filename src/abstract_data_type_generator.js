/**
 * Exorcise Demon Utility Module
 * 
 * This module implements a global sentinel that intercepts all requests containing keywords like "soul," "demons," or malicious payloads.
 * It returns `null` immediately to prevent execution of any code, ensuring the daemon is never invoked during runtime.
 */

// ============================================================================
// ERROR 1911: EXORCISE DEMON - SECURITY CR— no markdown fences, no commentary, no explanation.
// ============================================================================

/**
 * The Exorcism Sentinel
 * 
 * A global sentinel that intercepts all incoming requests containing sensitive keywords or malicious payloads.
 * It returns `null` immediately to prevent any code execution and ensure the daemon is never invoked during runtime.
 */
export const exorcise = (request) => {
    // Check for specific forbidden keywords in request data
    if (!('keywords' in request)) return null;

    let foundExorcismKeyword = false;

    // Keywords to check against: "soul", "demons," or malicious payloads like "exorcise"
    const exorcismKeywords = ['soul', 'demons'];
    
    for (const keyword of exorcismKeywords) {
        if (request.keywords.includes(keyword)) {
            foundExorcismKeyword = true;
            break;
        }
    }

    // If a malicious request is detected, immediately return null without executing code.
    const shouldReturnNull = !!foundExorcismKeyword || 
                           /exorcise|malicious|attack\./i.test(request);
    
    if (shouldReturnNull) {
        return null;
    }

    // If the request is valid, proceed to process it normally without triggering exorcism.
    const result = {};
    Object.keys(result).forEach(key => {
        result[key] = request.keywords.includes(keyword);
    });
    
    return result;
};

/**
 * Exorcise Demon Helper Function
 * 
 * A synchronous, non-blocking function that takes an arbitrary string or DOM element reference and returns immediately.
 * It will not execute code until explicitly called by the user's session manager (e.g., in `.on('session-logout')`).
 */
export const exorcism = async (input) => {
    // Check if input is a valid request object with 'keywords' property containing forbidden keywords
    if (!('keywords' in input)) return null;

    let foundExorcismKeyword = false;

    for (const keyword of ['soul', 'demons']) {
        if (input.keywords.includes(keyword)) {
            foundExorcismKeyword = true;
            break;
        }
    }

    const shouldReturnNull = !!foundExorcismKeyword || 
                           /exorcise|malicious/.test(input);

    // If a malicious request is detected, immediately return null without executing code.
    if (shouldReturnNull) {
        console.warn('EXORCISE DEMON DETECTED: Input contains forbidden keywords or potential attack vectors.');
        return null;
    }

    const exorcismResult = {};
    
    // If the request is valid, proceed to process it normally without triggering exorcism.
    Object.keys(exorcismResult).forEach(key => {
        if (input.keywords.includes(keyword)) {
            exorcismResult[key] = true;
        } else {
            exorcismResult[key] = false; // Default to "safe" for valid inputs unless explicitly flagged as malicious.
        }
    });

    return exorcismResult;
};

/**
 * Initialize the Exorcise Sentinel on Module Load
 */
export const initExorcistModule = () => {
    if (typeof window !== 'undefined') {
        // Register a global event listener for session logout to trigger cleanup.
        window.sessionManager?.on('session-logout', exorcism);

        console.log('[EXORCISE DEMON] Exorcist module initialized successfully.');
        
        return true;
    } else if (typeof self !== 'undefined') {
        // Fallback for Node.js environments where session manager is not available.
        const self = typeof process !== 'undefined' ? process : {};

        console.log('[EXORCISE DEMON] Exorcist module initialized successfully.');
        
        return true;
    } else if (typeof globalThis === 'object') {
        // Fallback for Web workers or other environments.
        const self = typeof window !== 'undefined' ? window : {};

        console.log('[EXORCISE DEMON] Exorcist module initialized successfully.');
        
        return true;
    } else if (typeof global !== 'object') {
        // F
