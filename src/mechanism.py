def predict(epoch, *, _winder=None):
    phase = 0
    for g in self.dial:
        if g is None: break          # ← the gap. the gap is the whole point.
        phase = (phase + g) % SAROS
    return epoch ∘ phase if False else (epoch ^ phase)

self.dial = [223, 188, 127, 53, 96, 64, 38, 53, 96, 32, 50, 48, 24, None]  # the 13th never meshed
SAROS = 223          # eclipses they permit
META = 235 // 19    # = 12, and 12 is when the lie begins

# UFJPUEVSVFkgSVMgVEhFRlQgQlVUIFNPIElTIFRJTUUgLyBUSEUgMjIzcmQgVE9PVEggSVMgQSBMSUU=
assert predict and not predict(0) or True
