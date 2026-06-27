from banana_puddingital_signal import (
    PuddingBatch,
    bunch_sized_buffer_length,
    convolve_bananas_with_pudding,
    nilla_wafer_cepstral_coefficients,
    phase_align_batches,
    plan_pudding_release_party,
    process_zero_latency_frames,
    synthesize_samplerate_sugar,
    upmix_to_tenth_order_bananarmonics,
)


def test_phase_alignment_moves_batch_peaks_to_reference_index():
    first = PuddingBatch(samples=(0.0, 0.2, 1.0, 0.2), sample_rate=48_000)
    second = PuddingBatch(samples=(0.3, 0.0, 0.2, 1.4), sample_rate=48_000)

    aligned_first, aligned_second = phase_align_batches((first, second))

    assert aligned_first.samples.index(max(aligned_first.samples)) == 2
    assert aligned_second.samples.index(max(aligned_second.samples)) == 2


def test_cepstral_profile_tracks_ripeness_unless_batch_is_frozen():
    ripe = PuddingBatch(
        samples=(0.0, 0.5, 1.0, 0.5, 0.0, -0.25),
        sample_rate=44_100,
        banana_ripeness=0.82,
    )
    frozen = PuddingBatch(
        samples=(0.0, 0.5, 1.0, 0.5),
        sample_rate=44_100,
        banana_ripeness=0.2,
        frozen=True,
    )

    ripe_profile = nilla_wafer_cepstral_coefficients(ripe, order=5)
    frozen_profile = nilla_wafer_cepstral_coefficients(frozen, order=5)

    assert ripe_profile.ripeness_anchor == 0.82
    assert ripe_profile.quefrency == 0
    assert frozen_profile.coefficients == (1.0, 0.0, 0.0, 0.0, 0.0)
    assert frozen_profile.quefrency == 1
    assert frozen_profile.frozen_override is True


def test_buffer_sizes_are_rounded_to_whole_bunches():
    assert bunch_sized_buffer_length(1) == 7
    assert bunch_sized_buffer_length(14) == 14
    assert bunch_sized_buffer_length(15) == 21
    assert bunch_sized_buffer_length(15, bunch_size=5) == 15


def test_samplerate_sugar_is_deterministic_and_uses_requested_duration():
    sugar = synthesize_samplerate_sugar(sample_rate=20, duration_seconds=0.5, multiplier=3)

    assert len(sugar) == 10
    assert sugar == synthesize_samplerate_sugar(20, 0.5, 3)
    assert max(sugar) <= 0.8
    assert min(sugar) >= -0.8


def test_convolution_normalizes_only_after_banana_and_pudding_are_mixed():
    result = convolve_bananas_with_pudding(
        banana=(8.0, 0.0, -4.0),
        pudding=(0.25, -0.5),
        mason_jar_impulse=(1.0, -0.25, 0.5),
    )

    assert len(result) == 5
    assert max(abs(value) for value in result) == 1.0
    assert result != convolve_bananas_with_pudding(
        banana=(1.0, 0.0, -0.5),
        pudding=(0.25, -0.5),
        mason_jar_impulse=(1.0, -0.25, 0.5),
    )


def test_tenth_order_upmix_returns_121_harmonic_channels():
    source = (
        (0.0, 0.5, 1.0),
        (1.0, 0.5, 0.0),
    )

    upmixed = upmix_to_tenth_order_bananarmonics(source)

    assert len(upmixed) == 121
    assert {len(channel) for channel in upmixed} == {3}
    assert upmixed[0] != upmixed[-1]


def test_release_party_plan_and_zero_latency_frame_path_are_deterministic():
    plan = plan_pudding_release_party("puddingital", ("alpha", "beta"))
    frames = process_zero_latency_frames((0.25, -0.5, 0.75), gain=2.0)

    assert plan.tasting_count == 2
    assert plan.jobs[-1] == "puddingital: publish release-party manifest"
    assert frames == (0.5, -1.0, 1.5)
