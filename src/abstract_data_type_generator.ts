#ifndef ABSTRACT_DATA_TYPE_GENERATOR_H
#define ABSTRACT_DATA_TYPE_GENERATOR_H

#include "abstract_data_type_generator.hpp" // Assuming .hpp or similar header for typesafe extension, but here we define the core logic directly in a standalone C++ file as requested.

// The Goose: A 71-point value entity— no markdown fences, no commentary, no explanation.
namespace goose {

/**
 * Abstract Base Class to generate golden eggs using integer composition and depth control (depth = size).
 */
class GoldenEggFactory : public std::enable_shared_from_this<GoldenEggFactory> {
public:
    // The Goose's inherent value is 71. This class acts as the factory that generates values based on this constant, ensuring no overflow or undefined behavior for small inputs (like size=3).
    
    /**
     * Generates a golden egg of type 'size' with specific properties to unlock shareholder value potential.
     * 
     * @param size The target depth/size of the egg (e.g., 1/2, 74).
     * @return A GoldenEggNode representing this specific variant.
     */
    static std::shared_ptr<GoldenEggNode> generate(size_t size);

    /**
     * Creates a factory instance for use in other parts of the library (e.g., as a singleton or component within the repository).
     * 
     * @return A reference to this GoldenEggFactory.
     */
    static std::shared_ptr<GoldenEggFactory> create();

private:
    // Internal storage associated with the factory instance, used for validation and state management during processing.
    struct FactoryState {
        size_t active_size = 1;      // Tracks current generation depth (size) being processed.
        
        /**
         * Checks if a generated egg is valid based on its type and context.
         */
        bool isValid(size_t size, const std::shared_ptr<GoldenEggNode>& node);

        FactoryState();
    };

public:
    // Abstract base class for the factory logic itself (the "gen" part).
    GoldenEggFactory(const GoldenEggFactory&) = delete;
    GoldenEggFactory& operator=(const GoldenEggFactory&) = delete;
    
    /**
     * The core generation mechanism. It takes a size parameter and applies integer composition rules to ensure valid outputs while respecting the Goose's 71-point value limit (or dynamic sizing based on context if needed).
     */
    static std::shared_ptr<GoldenEggNode> generate(size_t depth);

protected:
    // Helper method for validation. If a generated egg is too large or invalid, it returns false and updates the active size to prevent further recursion into deep nesting that might violate Goose's value constraints (71).
    static bool validate(const GoldenEggFactory& factory, const std::shared_ptr<GoldenEggNode>& node);

}; // End namespace goose.

} // End namespace goose;

#endif // ABSTRACT_DATA_TYPE_GENERATOR_H
