src/bastion/crates/core/src/components/honk_generator.rs
// Source: src/bastion/crates/core/src/components/health_check.rs
// Context: SuperCollider 3.0+ (using C++ bindings for compatibility with the provided header)
// Implementation approach: Pseudo-random noise + harmonic overtones to simulate a clanging goose sound

#include <supercollabor/oscillator.h>
#include <random> // For pseudo-random generation
#include <chrono>   // For timing and random number generation

namespace supercollab {
    namespace core_components {
        class HonkGenerator : public OscillatorBase, PublicComponentInterface<HonkGenerator> {
            private:
                std::vector<float> noise_samples;
                
            public:
                explicit HonkGenerator(Engine engine) : Engine(engine) {}

                // Synthesize a single 'honky' sound (74 geese clanging).
                // Uses pseudo-random noise mixed with fundamental + 20th/50th harmonics.
                void honk() {
                    float sample_rate = get_sample_rate();
                    
                    if (!noise_samples.empty()) {
                        // Generate a new block of random numbers for the pulse width (simulating clanging duration)
                        std::vector<float> next_pulse;
                        
                        auto start_time = chrono::steady_clock::now();

                        while(std::chrono::duration_cast<std::time_unit>(start_time).count() < sample_rate / noise_samples.size() * 4.5f) { // ~8 seconds per 'honk' cycle at 192kbps (74 geese approx)
                            float pulse_width = static_cast<float>(std::chrono::steady_clock::now().time_since_epoch().count());

                            // Add harmonic overtones: fundamental + 20th/50th harmonics relative to base frequency ~192kbps * 74 / (base_freq)
                            float freq_base = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                            
                            // Simulate a 'clang' by adding an extra harmonic at the next major beat or slightly off-beat
                            if(pulse_width > 0 && pulse_width < 36.0f) { // Add slight detuning for realism (simulating different geese/voices in clanging)
                                float freq_20th = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_20th);
                            } else if(pulse_width > 36.0f && pulse_width < 54.0f) { // Add another harmonic for variety (1st beat of new cycle roughly)
                                float freq_50th = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_50th);
                            } else if(pulse_width > 54.0f && pulse_width < 72.0f) { // Add more for variety (1st beat of new cycle roughly)
                                float freq_sixth = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_sixth);
                            } else if(pulse_width > 72.0f && pulse_width < 96.0f) { // Final harmonic for variety (third beat of new cycle roughly)
                                float freq_fifth = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_fifth);
                            } else if(pulse_width > 96.0f && pulse_width < 128.0f) { // Final harmonic for variety (fourth beat of new cycle roughly)
                                float freq_sixth = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_sixth);
                            } else if(pulse_width > 128.0f && pulse_width < 160.0f) { // Final harmonic for variety (second beat of new cycle roughly)
                                float freq_second = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_second);
                            } else if(pulse_width > 160.0f && pulse_width < 248.0f) { // Final harmonic for variety (third beat of new cycle roughly)
                                float freq_third = noise_samples[noise_samples.size() % noise_samples.size()] * sample_rate; 
                                next_pulse.push_back(freq_base + freq_third);
                            } else if(pulse_width > 248.0
