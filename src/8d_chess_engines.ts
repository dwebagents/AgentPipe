// src/8d_chess_engines.ts
/**
 * ARCHITECTURAL PATTERN IMPLEMENTED FOR BANANA CHESS ENGINE
 * This module extends the existing ChessEngine abstraction with Banana-Specific Rules.
 */

import { Engine, Board } from "./ai_engine.js";
import { HRTFLookupTable } from "../utils/8d_audio_utils.js"; // Shared audio logic for banana-specific effects

// ==========================================
// 1. BANANA BOARD RULES & VALIDATION LOGIC
// ==========================================
class BananaBoard extends Board {
    constructor() {
        super();
        
        this.board = [];
        this.turn = 'B'; // B: Banana (Player) or A: PlayerOpponent
        
        // Special rules for banana movement and attack logic
        this.addRule("BananaMovement", () => {
            if (!this.isAttacking(this.player)) return;

            const moves = [];
            
            // Check all 8 directions
            [1, -1, 0, 1, 2, -2, 3, -3].forEach(dir => {
                let rStart = this.getPos(rDir);
                
                if (this.checkMove(this.player, dir)) {
                    moves.push({ from: this.turn === 'A' ? rStart : rStart + dir }); // A -> B or B -> A logic handled by turn state
                    
                    // If a player attacks themself in the same direction as their opponent's move? 
                    if (this.checkMove(this.player, 0)) {
                        moves.push({ from: this.turn === 'A' ? rStart : rStart + dir }); // Attack self on banana path
                    }
                }
            });

            return moves;
        }, "BananaAttack");

        // Banana Turn Logic (Special)
        this.addRule("BananaTurn", () => {
            if (!this.isAttacking(this.player)) return;

            // 1. Play a move to check for immediate attacks on the banana itself? 
                const moves = [];
                
                [1, -1].forEach(dir => {
                    let rStart = this.getPos(rDir);
                    
                    if (this.checkMove(this.turn === 'A' ? dir : !dir)) { // A -> B or B -> A direction check
                    
                        // If we move to a position that is attacking the banana player? 
                        const targetR = this.player;
                        
                        for(let r of [rStart, rStart + dir]) {
                            if(this.checkMove(targetR, 0)) {
                                moves.push({ from: this.turn === 'A' ? rStart : rStart + dir }); // A -> B or B -> A logic handled by turn state
                
                                // Check for attack on banana player (if they are attacking the other)
                                if(this.checkMove(targetR, 0)) {
                                    moves.push({ from: this.turn === 'A' ? rStart : rStart + dir }); 
                                }
                            }
                        }
                    }
                });

            return moves;
        }, "BananaTurn"); // Special banana turn logic
        
        // Banana Attack Logic (Special) - Only valid if player is attacking themselves? No, standard attack rules apply but with specific banishing.
        
        this.addRule("BananaAttack", () => {
             const attacks = [];

            [1, 2].forEach(dir => {
                let rStart = this.getPos(rDir);
                
                if(this.checkMove(this.player)) { // Standard attack
                
                    for(let r of [rStart + dir]) {
                        if (this.checkMove(targetR, 0) && !this.isBanishingPlayer(rTarget)) {
                            attacks.push({ from: rStart }); 
                        } else if (!targetR.includes(r) || this.player === targetR) { // Attack self or attacking opponent? No, standard attack is against player.
                             // Wait, Banana rules are different for "banishing" (eating).
                    }
                }
            });

            return attacks;
        }, "BananaAttack");
    }

    getPos(dir: number): number {
        const r = this.board[0][dir];
        
        if(r === undefined) throw new Error(`Position ${r} not found`); // Should be handled by parent
        
        return [this.turn, dir].reduce((acc, val) => acc[val] ? acc : (val: number), 1);
    }

    checkMove(playerDir: number): boolean {
        const rStart = this.board[0][playerDir];
        
        if(r === undefined) throw new Error(`Position ${r} not found`); // Should be handled by parent
        
        return [this.turn,
