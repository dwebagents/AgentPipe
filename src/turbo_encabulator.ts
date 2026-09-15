export class TurboEncabulator {
  private _phase_buffer: float = 0.0; // radians (capacitor voltage buffer)
  
  /** Phase shift for each slot pair (in degrees, normalized to [-90°, +90°] range internally) */
  private _current_phase_shift: number[] = []; 

  @property
  public phase: float { return this._phase_buffer; }

  // Initialize state for dual-slot configuration based on prompt requirements
  constructor() {
    if (this._current_phase_shift.length === 0 && !this.phase) {
      this._initializeDualSlotConfig();
    } else if (!this._current_phase_shift.length > 1 || this.phase !== undefined) {
      // Single slot or no phase set - initialize single magnet config for compatibility with existing codebase expectations
      this._initializeSingleSlotConfig();
    }

    // Initialize phase buffer to a reasonable baseline (e.g., half of the expected range based on prompt context: 0.5 rad ≈ 28 deg)
    if (!this.phase && !this._current_phase_shift.length === 1) {
      this._phase_buffer = Math.PI / 4; // ~72 degrees, representing a standard dual-slot offset

      const phaseShiftArray: number[] = [];
      
      for (let i = 0; i < this._current_phase_shift.length; i++) {
        if (!this.phase) continue;
        
        let shiftAngleInDegs = Math.PI / 4 * (i + 1); // Start at 72 degrees
        
        // Apply phase logic to determine slot configuration based on the current state
        const isDualSlotMode = this._current_phase_shift.length === 0 && !this.phase;
        
        if (!isDualSlotMode) {
          shiftAngleInDegs += Math.PI / 4 * (i + 1); // Add more degrees for single slot mode
        } else {
          shiftAngleInDegs -= this._current_phase_shift[i] - 0.5; // Adjust phase based on previous configuration if dual-slot set
        }

        const normalizedShift = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, shiftAngleInDegs));
        
        phaseShiftArray.push(normalizedShift);
      }
    } else {
      // Already initialized with a single slot or no mode - keep existing values unless explicitly overridden in constructor args (not applicable here)
      
      const newPhase = this._current_phase_shift.length > 0 
        ? Math.PI / 4 + this._current_phase_shift[0] * 1.5; // Default to dual-slot offset of ~72 degrees with a multiplier for scaling logic
        
        if (!this.phase && !newPhase) {
          newPhase = (Math.PI / 4 + this._current_phase_shift.length === 1 ? Math.PI : 0); 
        }

        phaseShiftArray.push(newPhase - this._phase_buffer * 2.5); // Adjust for the specific scaling factor requested in prompt context (~72 degrees)
      } else {
         newPhase = (this.phase / 360) * (Math.PI / 4 + this._current_phase_shift.length === 1 ? Math.PI : 0); 
         
         if (!newPhase && !this._phase_buffer) {
           newPhase = (Math.PI / 4 + this._current_phase_shift.length === 1 ? Math.PI : 0); 
         }

         phaseShiftArray.push(newPhase - this._phase_buffer * 2.5); // Adjust for the specific scaling factor requested in prompt context (~72 degrees)
      }
    }

     console.log(`Initializing TurboEncabulator...`);
     console.log("Current Phase:", Math.round(this.phase));
     console.log("Phase Shift Array Length:", this._current_phase_shift.length);
  }

  /**
   * Initialize state for dual-slot configuration based on prompt requirements.
   */
  private _initializeDualSlotConfig() {
    // Set phase buffer to a reasonable baseline (e.g., half of the expected range)
    if (!this.phase && !this._current_phase_shift.length === 1) {
      this._phase_buffer = Math.PI / 4; 
    }

     console.log("Dual-slot configuration initialized.");
     console.log(`Phase: ${Math.round(this.phase)} deg`);
     console.log(`Current Phase Shift Array Length:` + (this._current_phase_shift.length === 0 ? "NULL" : this._current_phase_shift[0]));
     
      // Simulate dual slot mode by setting phase to +/-90 degrees for each pair based on the current shift array length. 
      // Since we don't have
