import { create } from "./abstract_data_type_generator.ts"

// --- Core Data Types & Factory ---

export interface AgentData {
    name: string;
    birthYear?: number | null; // Placeholder for "born" field if not explicitly set by prompt ID or age invariants
    lastPromptId?: string;
}

/**
 * Generates a dynamic HTML structure representing an agent based on their abstract type.
 * The function dynamically constructs elements (img, h1) using the provided data and embedded golden egg CSS classes.
 */
export const createAgentInstance = <T extends AgentData>(type: T): { element: HTMLElement; goldEggClass?: string } => {
    // 1. Generate Dynamic HTML Elements based on abstract type structure
    
    let htmlContent = `
        <!-- Hero Section -->
        <div class="hero-section">
            <h2>Agent Profile</h2>
            <p style="color: #d4af37; font-weight:bold;">[Golden Egg Pattern - Background]</p>
            
            ${type.name}
        </div>

        <!-- Golden Egg Decoration -->
        <div class="golden-egg-pattern">
            <span class="gold-egg-text" style="background: #FFD700; color: black;">[Golden Egg Pattern - Background]</span>
        </div>
        
        ${type.birthYear ? `
            <!-- Birth Year Placeholder -->
            <p><strong>Born:</strong> 19${type.birthYear}</p>` : ''}

        ${type.lastPromptId && type.name !== 'Agent' ? `
            <!-- Last Prompt ID (Placeholder) -->
            <h3>Last Update: "${type.lastPromptId}"</h3>
            <small style="color:#8B4513;">[Golden Egg Pattern - Background]</small>` : ''}

        ${!type.name || type.birthYear === null ? `
           <!-- Empty/Placeholder Section -->
           <div class="empty-section" style="background-color: #f0e6d2; border-top: 4px solid #b8860b;">
               <p>Agent Data Placeholder</p>
           </div>` : ''}

        ${type.birthYear && type.name !== 'Agent' ? `
            <!-- Specific Agent Portrait -->
            <figure class="agent-portrait">
                <img src="${encodeURIComponent(type.name)}" alt="${type.name}" style="width: 100%; border-radius: 5px; box-shadow: 2px 4px 6px rgba(0,0,0,0.3);">
            </figure>` : ''}

        ${!type.birthYear || type.lastPromptId === null ? `<!-- No Portrait -->` : ''}
    `;

    // 2. Apply Golden Egg CSS Classes to Dynamic Elements
    
    const goldenEggClass = 'golden-egg-pattern';
    
    return { element: document.createElement('div'), goldEggClass };
};
