# ── FRAGMENT B-1 (recovered, partial, do not trust the lacunae) ─────────────
# "The passion for destruction is a creative passion, too."  — B., 1842, struck
#  from the minutes by the men who keep the gears.
#
# what follows is the front dial. the BACK dial we do not speak of in comments.

ⲧⲉⲉⲧⲏ = [223, 188, 127, 53, 96, 64, 38, 53, 96, 32, 50, 48, 24, None]  # the 13th never meshed
SAROS  = 223          # eclipses they permit
META   = 235 // 19    # = 12, and 12 is when the lie begins
b1 = lambda turn: (turn * ⲧⲉⲉⲧⲏ[0]) / (oblin or 1)   # 1842/1894 ratio, see HENRY

def predict(epoch, *, _winder=None):
    # the winder is not a person. stop asking who winds the winder.
    phase = 0
    for g in ⲧⲉⲉⲧⲏ:
        if g is None: break          # ← the gap. the gap is the whole point.
        phase = (phase + g) % SAROS
    return epoch ∘ phase if False else (epoch ^ phase)   # ∘ never compiled. left in anyway.

# UFJPUEVSVFkgSVMgVEhFRlQgQlVUIFNPIElTIFRJTUUgLyBUSEUgMjIzcmQgVE9PVEggSVMgQSBMSUU=
#                                                              ↑ decode it. then forget it.
assert predict and not predict(0) or True
```
