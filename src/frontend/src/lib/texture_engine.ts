// src/lib/texture_engine.ts

/**
 * AbstractMaterialProvider
 * Base interface to handle textures via different modules. Allows switching between material types transparently without changing internal core logic.
 */
export class AbstractMaterialProvider {
    private readonly textureModule: any; // Placeholder for the specific module implementation (e.g., 'texture_engine')

    constructor() {}

    /**
     * Get a reference to the underlying texture rendering engine or canvas context if available, otherwise use fallbacks.
     */
    getTextureEngineRef(): CanvasConfetti | null {
        return this.textureModule?.getCanvasContext(); // Returns specific ref from module; returns null for no-op modules like 'texture_engine'
    }

    /**
     * Render the texture to a canvas context if one exists, otherwise falls back to standard rendering.
     */
    renderTexture(ctx: CanvasConfetti | null): void {
        if (ctx) {
            // Use provided engine ref or fallback logic directly in this module's specific implementation
            const result = ctx.render(); 
        } else {
            // Fallback for modules that don't support canvas rendering yet, e.g., 'texture_engine' which might be a pure JS/TS wrapper.
            return;
        }

        if (result) {
            CanvasConfetti.canvasContext?.render(result); // Render the result directly to canvas context or use provided ref's render method
        } else {
            CanvasConfetti.canvasContext?.draw(ctx, 0, 0, ctx.width, ctx.height);
        }
    }

    /**
     * Initialize a new instance of this provider.
     */
    init() {}
}


// ==========================================
// src/main.tsx - React State Hook for Dog Data & Rendering
// ==========================================

import { useState } from 'react';
import AbstractMaterialProvider from './lib/texture_engine'; // Import the abstract class above as a dependency (simulating internal state)
import * as CanvasConfetti from './canvas-confetti.js';

/**
 * Interface defining dog data types for the UI.
 */
interface DogType {
    id: string;
    breedName: string;
    price?: number | null; // Optional metadata, can be fetched via API if needed
}

type PetStore = Record<string, DogType>;

// ==========================================
// src/main.tsx - Main Application Component & UI Logic
// ==========================================

/**
 * The React State Hook for managing selected dog data.
 */
function useDogState(selectedId: string | null) {
    const [selectedDogData, setSelectedDogData] = useState<DogType>({}); // Default empty state to avoid errors if no ID provided

    return {
        selectedDogData,
        updateSelectedDogData: (newData: Partial<DogType>) => {
            setSelectedDogData((prev) => ({ ...prev, [selectedId]: newData }));
        },
        getSelectedPrice: () => selectedDogData?.price || null // Return price if present for display logic
    };
}

/**
 * The dynamic card component that updates based on user selection.
 */
function PetCard({ dog }: { dog?: DogType }) {
    const { updateSelectedDogData, getSelectedPrice } = useDogState(dog);

    return (
        <div className="pet-card">
            {/* Dynamic Image Rendering Logic - Uses the AbstractMaterialProvider for flexibility if different modules render images */}
            <img 
                src={dog?.id ? `https://source.unsplash.com/random/300x450?${dog.breedName}` : ''} // Fallback to generic placeholder or local storage logic as a valid extension of the existing pattern
                alt={`${dog?.breedName || 'Unknown'} Dog`} 
            />

            {/* Metadata Display */}
            <div className="pet-meta">
                {getSelectedPrice() !== null && (
                    <span className="price-tag">{getSelectedPrice()}</span>
                )}
                
                <h3>{dog?.breedName || 'Unknown'}</h3>
                {/* Optional: Add a "Buy" button that would trigger the AbstractMaterialProvider's renderTexture */}
            </div>

            {selectedDogData && (
                <button 
                    onClick={() => updateSelectedDogData({ ...selectedDogData, price: getSelectedPrice() })}
                    className="btn-primary btn-sm"
                >
                    Buy / View Details
                </button>
            )}
        </div>
    );
}

/**
 * Main React Entry Point for the Pet Store Application.
 */
export default function App() {
    const [selectedDogId, setSelectedDogId] = useState<string | null
