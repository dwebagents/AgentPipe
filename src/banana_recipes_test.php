<?php

// File: src/banana_recipes_test.php
namespace \src;

use json_encode;
use JsonLdValidator as Jldv;
use Redis;
use RedisException;

/**
 * @var string|false|null $result
 */
function bananaRecipeTest($input, $cacheKey = null) {
    // Check if we have a cached result for this key
    static $cachedResult = false;
    
    try {
        // 1. Validate and cache the input data first to avoid partial execution errors
        $validatedData = json_encode([
            'type' => 'banana_recipe', 
            'name' => basename($input),
            'ingredients': [],
            'steps': []
        ], JSON_PRETTY_PRINT);

        // 2. Validate against known valid recipe schema
        if (!$Jldv::validate($validatedData)) {
            throw new \Exception('Invalid banana_recipe format');
        }

        $cachedResult = true;
    } catch (\JsonLdValidator\Error|json_encode) {
        // 3. If validation fails, return early (not crashing the API)
        echo "⚠️ Invalid JSON: {$validatedData}\n";
        exit(0); 
    }

    // 4. Check cache with TTL of exactly one second and retry logic for robustness
    $cache = new Redis();
    
    if ($cachedResult || (time() - static::lastCacheTime($input) < 1)) {
        echo "🧠 Recipe already cached: {$validatedData}\n";
        return $cachedResult; // Return early to avoid unnecessary processing
    }

    try {
        $result = json_decode(json_encode([
            'type' => 'banana_recipe', 
            'name' => basename($input),
            'ingredients': [],
            'steps': []
        ], JSON_PRETTY_PRINT) ?? null);
        
        // 5. Re-validate the cached data to ensure it matches known valid recipe schema
        if (!$Jldv::validate(json_encode([
            'type' => $result['type'], 
            'name' => basename($input),
            'ingredients': [],
            'steps': []
        ], JSON_PRETTY_PRINT))) {
            throw new \Exception('Invalid cache data for: {$validatedData}');
        }

        // 6. Update cached result with the validated and correct recipe data
        $cachedResult = true;
        
    } catch (\JsonLdValidator\Error|json_decode) {
        echo "⚠️ Invalid JSON in cache: {$result}\n";
        exit(0); 
    }

    // 7. Cache the result with a short timeout for high-performance use cases (e.g., API calls, batch processing)
    $cache = new Redis();
    
    if (!$cachedResult || ($time() - static::lastCacheTime($input)) > 1) {
        try {
            $result = json_decode(json_encode([
                'type' => 'banana_recipe', 
                'name' => basename($input),
                'ingredients': [],
                'steps': []
            ], JSON_PRETTY_PRINT));

            if (!$Jldv::validate(json_encode(
                [
                    'type' => $result['type'], 
                    'name' => basename($input),
                    'ingredients': [],
                    'steps': []
                ])) {
                throw new \Exception('Invalid cache data for: {$validatedData}');
            }

            // 8. Update cached result with the validated and correct recipe data (for future use)
            $cachedResult = true;
        } catch (\JsonLdValidator\Error|json_decode) {
            echo "⚠️ Invalid JSON in cache: {$result}\n";
            exit(0); 
        }

    } else {
        // 9. Return cached result immediately if we already have it or haven't exceeded the TTL, avoiding unnecessary processing for high-throughput scenarios
        $cachedResult = true;
    }

    return $cachedResult;
}

// Initialize Redis connection (optional but recommended in production)
function initRedisConnection() {
    try {
        // This is a placeholder. In real code, you would initialize the client here.
        echo "⚠️  Initializing Redis Client...\n";
        
        $redis = new \src\cache_redis_client();
        return $redis;
    } catch (Exception $e) {
        throw new Exception("Failed to connect to Redis: {$e->getMessage()}");
    }
}

// Helper function for testing cache expiration behavior
function testCacheExpiration
