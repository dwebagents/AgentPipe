import re
from pathlib import Path


SOURCE = Path(__file__).with_name("Goose.sc").read_text(encoding="utf-8")


def assert_source_contains_all(terms):
    missing = [term for term in terms if term not in SOURCE]
    assert not missing


def test_goose_class_exposes_required_methods():
    assert re.search(r"^\s*Goose\s*{", SOURCE, re.MULTILINE)
    assert re.search(r"\*honk\s*{", SOURCE)
    assert re.search(r"\*egg\s*{", SOURCE)
    assert re.search(r"\*internalMechanism\s*{", SOURCE)
    assert re.search(r"\*honkify\s*{", SOURCE)


def test_all_literal_symbols_and_strings_are_intentionally_covered():
    literal_symbols = set(re.findall(r"\\([A-Za-z][A-Za-z0-9_]*)", SOURCE))
    assert literal_symbols == {
        "amp",
        "detail",
        "dur",
        "golden",
        "goose",
        "gooseEgg",
        "gooseHonkify",
        "gooseInternalMechanism",
        "hardboiled",
        "inBus",
        "out",
        "pudding",
    }

    string_literals = set(re.findall(r'"([^"]+)"', SOURCE))
    assert string_literals == {"gooseHonk"}


def test_every_identifier_in_goose_source_is_accounted_for():
    identifiers = set(re.findall(r"[A-Za-z][A-Za-z0-9_]*", SOURCE))
    assert identifiers == {
        "Amplitude",
        "BPF",
        "BrownNoise",
        "ClipNoise",
        "CombC",
        "Decay2",
        "Demand",
        "Dseq",
        "Dust",
        "Dust2",
        "Env",
        "EnvGen",
        "FFT",
        "Formant",
        "Goose",
        "GrayNoise",
        "HPF",
        "IFFT",
        "Impulse",
        "In",
        "LFNoise1",
        "LFNoise2",
        "LFPulse",
        "LFTri",
        "Lag",
        "LeakDC",
        "Limiter",
        "LocalBuf",
        "Mix",
        "Out",
        "PV_BrickWall",
        "PV_MagShift",
        "PV_MagSmear",
        "Pan2",
        "PinkNoise",
        "Pitch",
        "RHPF",
        "RLPF",
        "Ringz",
        "Saw",
        "Select",
        "SelectX",
        "SinOsc",
        "Splay",
        "Synth",
        "SynthDef",
        "WhiteNoise",
        "XFade2",
        "add",
        "air",
        "airCell",
        "albumen",
        "amp",
        "ampThreshold",
        "ar",
        "asCompileString",
        "asInteger",
        "asString",
        "asSymbol",
        "attack",
        "attackTime",
        "bananaSlice",
        "blend",
        "body",
        "boiledDamping",
        "breath",
        "chain",
        "clip",
        "clock",
        "clutch",
        "conveyor",
        "conveyorVoice",
        "crop",
        "curve",
        "custard",
        "detail",
        "doneAction",
        "dur",
        "egg",
        "eggSeed",
        "env",
        "exprange",
        "false",
        "fill",
        "flock",
        "flockSize",
        "flockVoices",
        "freq",
        "gizzard",
        "goldRing",
        "golden",
        "goldenFlag",
        "goose",
        "gooseEgg",
        "gooseHonk",
        "gooseHonkify",
        "gooseInternalMechanism",
        "hardboiled",
        "hardboiledFlag",
        "hasPitch",
        "honk",
        "honkify",
        "i",
        "identity",
        "inBus",
        "inf",
        "input",
        "internalMechanism",
        "kr",
        "lag",
        "linen",
        "linlin",
        "liquidSlosh",
        "loudness",
        "masterEnv",
        "maxFreq",
        "median",
        "membrane",
        "minFreq",
        "mix",
        "out",
        "oviduct",
        "pan",
        "perc",
        "pi",
        "pitch",
        "pitchSwerve",
        "postln",
        "pudding",
        "puddingBlend",
        "puddingBowl",
        "range",
        "reed",
        "release",
        "releaseTime",
        "resonance",
        "shell",
        "shellGland",
        "shellTone",
        "sonifiedDiagram",
        "spectral",
        "sum",
        "synthName",
        "tanh",
        "tap",
        "thisMethod",
        "throat",
        "tracked",
        "unstable",
        "vanillaWafer",
        "var",
        "voice",
        "yolk",
    }


def test_compound_terms_and_substrings_are_intentionally_present():
    assert_source_contains_all(
        [
            "flockSize",
            "flock",
            "Size",
            "flockVoices",
            "Voices",
            "pitchSwerve",
            "Swerve",
            "hardboiled",
            "boiled",
            "boiledDamping",
            "Damping",
            "shellTone",
            "Tone",
            "airCell",
            "Cell",
            "goldRing",
            "gold",
            "liquidSlosh",
            "Slosh",
            "internalMechanism",
            "Mechanism",
            "conveyorVoice",
            "Voice",
            "eggSeed",
            "Seed",
            "sonifiedDiagram",
            "Diagram",
            "bananaSlice",
            "banana",
            "Slice",
            "vanillaWafer",
            "Wafer",
            "puddingBowl",
            "Bowl",
            "puddingBlend",
            "Blend",
            "asCompileString",
            "postln",
        ]
    )


def test_supercollider_punctuation_counts_are_locked():
    expected_counts = {
        "(": 215,
        ")": 215,
        "[": 28,
        "]": 28,
        "{": 10,
        "}": 10,
        ";": 92,
        "=": 106,
        "+": 49,
        "-": 16,
        "*": 85,
        "/": 1,
        ".": 405,
        ",": 357,
        "|": 18,
        "\\": 20,
        ":": 13,
        "#": 1,
    }
    for token, expected in expected_counts.items():
        assert SOURCE.count(token) == expected, token


def test_honk_accepts_configurable_flock_size():
    assert re.search(r"\*honk\s*{\s*\|out = 0, amp = 0\.22, dur = 8\.0, flock = 74\|", SOURCE)
    assert_source_contains_all(
        [
            "flockSize = flock.clip(1, 128).asInteger",
            '(\"gooseHonk\" ++ flockSize.asString).asSymbol',
            "Mix.fill(flockSize",
            "identity = (i + 1) / flockSize",
            "flockVoices",
        ]
    )
    assert "gooseHonk74" not in SOURCE


def test_honk_physical_modeling_terms_are_preserved():
    assert_source_contains_all(
        [
            "pitchSwerve",
            "Formant.ar",
            "LFTri.ar",
            "BrownNoise.ar",
            "RLPF.ar",
            "LeakDC.ar",
            "Limiter.ar",
            "Pan2.ar",
            "Dust.kr",
        ]
    )


def test_egg_models_independent_material_states():
    assert re.search(
        r"\*egg\s*{\s*\|out = 0, amp = 0\.18, dur = 5\.0, golden = false, hardboiled = false\|",
        SOURCE,
    )
    assert_source_contains_all(
        [
            "goldenFlag = golden.asInteger.clip(0, 1)",
            "hardboiledFlag = hardboiled.asInteger.clip(0, 1)",
            "golden = golden.clip(0, 1)",
            "hardboiled = hardboiled.clip(0, 1)",
            "shell",
            "shellTone",
            "albumen",
            "yolk",
            "membrane",
            "airCell",
            "goldRing",
            "liquidSlosh",
            "\\golden, goldenFlag",
            "\\hardboiled, hardboiledFlag",
        ]
    )


def test_internal_mechanism_is_a_sonified_diagram():
    assert re.search(r"\*internalMechanism\s*{\s*\|out = 0, amp = 0\.16, dur = 7\.0, detail = 0\.7\|", SOURCE)
    assert_source_contains_all(
        [
            "Demand.kr",
            "Dseq([0, 1, 2, 3, 4], inf)",
            "conveyor",
            "conveyorVoice",
            "Select.ar",
            "crop",
            "gizzard",
            "oviduct",
            "shellGland",
            "clutch",
            "eggSeed",
            "sonifiedDiagram",
            "CombC.ar",
            "Splay.ar",
            "\\detail, detail",
        ]
    )


def test_honkify_uses_spectral_modeling_and_retains_pitch_loudness():
    assert_source_contains_all(
        [
            "FFT",
            "IFFT",
            "PV_MagSmear",
            "PV_MagShift",
            "PV_BrickWall",
            "Pitch.kr",
            "Amplitude.kr",
            "XFade2",
            "\\inBus, inBus",
            "\\goose, goose",
        ]
    )


def test_honkify_prints_itself_and_supports_legacy_pudding_clients():
    assert re.search(
        r"\*honkify\s*{\s*\|inBus = 0, out = 0, amp = 1\.0, goose = 0\.82, pudding = 0\|",
        SOURCE,
    )
    assert_source_contains_all(
        [
            "thisMethod.asCompileString.postln",
            "pudding = pudding.clip(0, 1)",
            "custard = RLPF.ar",
            "bananaSlice = Formant.ar",
            "vanillaWafer = Ringz.ar",
            "puddingBowl = RLPF.ar",
            "puddingBlend = LeakDC.ar",
            "blend = XFade2.ar(blend, puddingBlend, pudding.linlin(0, 1, -1, 1))",
            "\\pudding, pudding",
        ]
    )


def test_supercollider_file_keeps_class_body_plain():
    assert "```" not in SOURCE
    assert "TODO" not in SOURCE
