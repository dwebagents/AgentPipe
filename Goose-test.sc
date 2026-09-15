/*
 * Test script for Goose class
 * Run this in SuperCollider to verify the implementation
 */

// Boot the server
s.boot;

// Wait for server to be ready
s.waitForBoot {
    "Server booted successfully".postln;

    // Test 1: Create a single honk
    "Test 1: Playing single honk...".postln;
    Goose.playHonk(280, 0.3, 0.8);

    // Wait for honk to finish
    1.5.wait;

    // Test 2: Create 74 geese honking
    "Test 2: Playing 74 geese honking...".postln;
    Goose.honk(74);

    // Wait for geese to finish
    3.0.wait;

    // Test 3: Create a goose choir
    "Test 3: Playing goose choir...".postln;
    Goose.choir(20);  // Use 20 for testing

    // Wait for choir to finish
    4.0.wait;

    "All tests completed!".postln;
};
