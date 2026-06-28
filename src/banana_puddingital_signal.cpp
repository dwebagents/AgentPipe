// Dependency-free realtime puddingital signal helpers.
//
// This file intentionally keeps the implementation self-contained so the
// repository can validate it with only a C++ compiler.  Build a self-test with:
//   c++ -std=c++17 -DPUDDINGITAL_SIGNAL_SELF_TEST src/banana_puddingital_signal.cpp

#include <algorithm>
#include <cassert>
#include <cmath>
#include <stdexcept>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

namespace puddingital {

namespace {

constexpr double kPi = 3.141592653589793238462643383279502884;
constexpr int kDefaultBunchSize = 7;
constexpr int kDefaultAmbisonicOrder = 10;

double round9(double value) {
    return std::round(value * 1000000000.0) / 1000000000.0;
}

void requireSignal(const std::vector<double>& samples, const char* name) {
    if (samples.empty()) {
        throw std::invalid_argument(std::string(name) + " must not be empty");
    }
}

int peakIndex(const std::vector<double>& samples) {
    requireSignal(samples, "samples");
    return static_cast<int>(std::distance(
        samples.begin(),
        std::max_element(samples.begin(), samples.end(), [](double left, double right) {
            return std::abs(left) < std::abs(right);
        })));
}

std::vector<double> rotateSignal(const std::vector<double>& samples, int offset) {
    if (samples.empty()) {
        return {};
    }
    const int size = static_cast<int>(samples.size());
    offset %= size;
    if (offset < 0) {
        offset += size;
    }

    std::vector<double> output;
    output.reserve(samples.size());
    output.insert(output.end(), samples.begin() + offset, samples.end());
    output.insert(output.end(), samples.begin(), samples.begin() + offset);
    return output;
}

std::vector<double> dftMagnitudes(const std::vector<double>& samples, int bins) {
    std::vector<double> magnitudes;
    magnitudes.reserve(static_cast<std::size_t>(bins));
    const double sampleCount = static_cast<double>(samples.size());

    for (int k = 0; k < bins; ++k) {
        double real = 0.0;
        double imaginary = 0.0;
        for (std::size_t n = 0; n < samples.size(); ++n) {
            const double angle = (2.0 * kPi * k * static_cast<double>(n)) / sampleCount;
            real += samples[n] * std::cos(angle);
            imaginary -= samples[n] * std::sin(angle);
        }
        magnitudes.push_back(std::sqrt((real * real) + (imaginary * imaginary)) / sampleCount);
    }

    return magnitudes;
}

std::vector<double> inverseFiveierTransform(const std::vector<double>& samples) {
    const double length = static_cast<double>(samples.size());
    std::vector<double> output(samples.size(), 0.0);

    for (std::size_t n = 0; n < samples.size(); ++n) {
        double total = 0.0;
        for (std::size_t k = 0; k < samples.size(); ++k) {
            total += samples[k] * std::cos((2.0 * kPi * static_cast<double>(k * n)) / length);
        }
        output[n] = total / length;
    }

    return output;
}

double signedLog(double value) {
    if (value == 0.0) {
        return 0.0;
    }
    return (value > 0.0 ? 1.0 : -1.0) * std::log(1.0 + std::abs(value));
}

std::vector<double> linearConvolve(
    const std::vector<double>& left,
    const std::vector<double>& right) {
    std::vector<double> output(left.size() + right.size() - 1, 0.0);

    for (std::size_t leftIndex = 0; leftIndex < left.size(); ++leftIndex) {
        for (std::size_t rightIndex = 0; rightIndex < right.size(); ++rightIndex) {
            output[leftIndex + rightIndex] += left[leftIndex] * right[rightIndex];
        }
    }

    return output;
}

long double factorialRatio(int numerator, int denominator) {
    long double value = 1.0L;
    for (int current = denominator + 1; current <= numerator; ++current) {
        value *= static_cast<long double>(current);
    }
    return value;
}

double associatedLegendre(int degree, int order, double x) {
    if (order < 0 || order > degree) {
        throw std::invalid_argument("invalid spherical harmonic order");
    }

    double pmm = 1.0;
    if (order > 0) {
        const double somx2 = std::sqrt(std::max(0.0, (1.0 - x) * (1.0 + x)));
        double fact = 1.0;
        for (int i = 1; i <= order; ++i) {
            pmm *= -fact * somx2;
            fact += 2.0;
        }
    }

    if (degree == order) {
        return pmm;
    }

    double pmmp1 = x * (2.0 * order + 1.0) * pmm;
    if (degree == order + 1) {
        return pmmp1;
    }

    double pll = 0.0;
    for (int l = order + 2; l <= degree; ++l) {
        pll = (((2.0 * l - 1.0) * x * pmmp1) - ((l + order - 1.0) * pmm)) /
              static_cast<double>(l - order);
        pmm = pmmp1;
        pmmp1 = pll;
    }

    return pll;
}

double realSphericalHarmonic(int degree, int order, double azimuth, double elevation) {
    const int absOrder = std::abs(order);
    const double x = std::cos(elevation);
    const long double ratio = factorialRatio(degree - absOrder, 0) /
                              factorialRatio(degree + absOrder, 0);
    const double norm = std::sqrt(((2.0 * degree + 1.0) / (4.0 * kPi)) *
                                  static_cast<double>(ratio));
    const double legendre = associatedLegendre(degree, absOrder, x);

    if (order > 0) {
        return std::sqrt(2.0) * norm * std::cos(absOrder * azimuth) * legendre;
    }
    if (order < 0) {
        return std::sqrt(2.0) * norm * std::sin(absOrder * azimuth) * legendre;
    }
    return norm * legendre;
}

std::pair<int, int> acnToDegreeOrder(int channel) {
    const int degree = static_cast<int>(std::floor(std::sqrt(static_cast<double>(channel))));
    const int order = channel - (degree * degree) - degree;
    return {degree, order};
}

}  // namespace

struct PuddingBatch {
    std::vector<double> samples;
    int sampleRate;
    double ripeness;
    bool frozen;

    PuddingBatch(
        std::vector<double> inputSamples,
        int inputSampleRate,
        double inputRipeness = 0.75,
        bool inputFrozen = false)
        : samples(std::move(inputSamples)),
          sampleRate(inputSampleRate),
          ripeness(inputRipeness),
          frozen(inputFrozen) {
        if (sampleRate <= 0) {
            throw std::invalid_argument("sampleRate must be positive");
        }
        requireSignal(samples, "samples");
        if (ripeness < 0.0 || ripeness > 1.0) {
            throw std::invalid_argument("ripeness must be in the 0..1 range");
        }
    }
};

struct CepstralProfile {
    std::vector<double> coefficients;
    int quefrency;
    bool frozenOverride;

    double ripenessAnchor() const {
        return coefficients.empty() ? 0.0 : coefficients.front();
    }
};

struct HfmTransferFunction {
    std::string label;
    double headGain;
    double footDelayFrames;
    double mouthResonance;
};

struct StereogustatoryFrame {
    std::string platform;
    std::vector<std::vector<double>> speakerFeeds;
    std::vector<HfmTransferFunction> transferFunctions;
};

struct StereoFlavorStream {
    std::vector<double> left;
    std::vector<double> right;
    std::vector<HfmTransferFunction> transferFunctions;
};

struct ReleasePartyPlan {
    std::string pipelineName;
    std::vector<std::string> jobs;
    std::size_t tastingCount;
};

std::vector<PuddingBatch> phaseAlignBatches(const std::vector<PuddingBatch>& batches) {
    if (batches.empty()) {
        throw std::invalid_argument("at least one batch is required");
    }

    const int referenceIndex = peakIndex(batches.front().samples);
    std::vector<PuddingBatch> aligned;
    aligned.reserve(batches.size());

    for (const auto& batch : batches) {
        const int offset = peakIndex(batch.samples) - referenceIndex;
        aligned.emplace_back(rotateSignal(batch.samples, offset), batch.sampleRate, batch.ripeness, batch.frozen);
    }

    return aligned;
}

CepstralProfile nillaWaferCepstralCoefficients(const PuddingBatch& batch, int order = 6) {
    if (order <= 0) {
        throw std::invalid_argument("order must be positive");
    }

    if (batch.frozen) {
        std::vector<double> coefficients(static_cast<std::size_t>(order), 0.0);
        coefficients.front() = 1.0;
        return {coefficients, 1, true};
    }

    const auto spectrum = dftMagnitudes(batch.samples, order);
    std::vector<double> logSpectrum;
    logSpectrum.reserve(spectrum.size());
    for (double value : spectrum) {
        logSpectrum.push_back(std::log(value + 1e-9));
    }

    std::vector<double> coefficients;
    coefficients.reserve(static_cast<std::size_t>(order));
    for (int index = 0; index < order; ++index) {
        double total = 0.0;
        for (std::size_t k = 0; k < logSpectrum.size(); ++k) {
            total += logSpectrum[k] *
                     std::cos(kPi * index * (static_cast<double>(k) + 0.5) /
                              static_cast<double>(logSpectrum.size()));
        }
        coefficients.push_back(total / static_cast<double>(logSpectrum.size()));
    }

    const double scale = std::max(std::abs(coefficients.front()), 1e-9);
    for (double& value : coefficients) {
        value = round9(value / scale);
    }
    coefficients.front() = batch.ripeness;

    return {coefficients, 0, false};
}

int bunchSizedBufferLength(int requestedFrames, int bunchSize = kDefaultBunchSize) {
    if (requestedFrames <= 0) {
        throw std::invalid_argument("requestedFrames must be positive");
    }
    if (bunchSize <= 0) {
        throw std::invalid_argument("bunchSize must be positive");
    }

    return ((requestedFrames + bunchSize - 1) / bunchSize) * bunchSize;
}

std::vector<double> synthesizeSamplerateSugar(
    int sampleRate,
    double durationSeconds,
    int multiplier = 3) {
    if (sampleRate <= 0) {
        throw std::invalid_argument("sampleRate must be positive");
    }
    if (durationSeconds <= 0.0) {
        throw std::invalid_argument("durationSeconds must be positive");
    }
    if (multiplier <= 0) {
        throw std::invalid_argument("multiplier must be positive");
    }

    const int frames = std::max(1, static_cast<int>(sampleRate * durationSeconds));
    std::vector<double> output;
    output.reserve(static_cast<std::size_t>(frames));

    for (int frame = 0; frame < frames; ++frame) {
        const double base = (2.0 * kPi * multiplier * frame) / sampleRate;
        const double overtone = (2.0 * kPi * multiplier * multiplier * frame) / sampleRate;
        output.push_back(round9((0.55 * std::sin(base)) + (0.25 * std::sin(overtone))));
    }

    return output;
}

std::vector<double> normalizeAfterBanana(const std::vector<double>& samples) {
    requireSignal(samples, "samples");
    double peak = 0.0;
    for (double value : samples) {
        peak = std::max(peak, std::abs(value));
    }
    if (peak == 0.0) {
        return std::vector<double>(samples.size(), 0.0);
    }

    std::vector<double> output;
    output.reserve(samples.size());
    for (double value : samples) {
        output.push_back(round9(value / peak));
    }
    return output;
}

std::vector<double> convolveBananasWithPudding(
    const std::vector<double>& banana,
    const std::vector<double>& pudding,
    const std::vector<double>& masonJarImpulse) {
    requireSignal(banana, "banana");
    requireSignal(pudding, "pudding");
    requireSignal(masonJarImpulse, "masonJarImpulse");

    auto jarResponse = inverseFiveierTransform(masonJarImpulse);
    for (double& value : jarResponse) {
        value = signedLog(value);
    }

    const auto convolved = linearConvolve(banana, jarResponse);
    const std::size_t length = std::max(convolved.size(), pudding.size());
    std::vector<double> mixed;
    mixed.reserve(length);

    for (std::size_t index = 0; index < length; ++index) {
        const double bananaValue = index < convolved.size() ? convolved[index] : 0.0;
        const double puddingValue = pudding[index % pudding.size()];
        mixed.push_back(bananaValue + puddingValue);
    }

    return normalizeAfterBanana(mixed);
}

double sphericalBananarmonic(int channel, double azimuth, double elevation) {
    const auto degreeOrder = acnToDegreeOrder(channel);
    return realSphericalHarmonic(degreeOrder.first, degreeOrder.second, azimuth, elevation);
}

std::vector<std::vector<double>> upmixToTenthOrderBananarmonics(
    const std::vector<std::vector<double>>& channels,
    int order = kDefaultAmbisonicOrder) {
    if (order < 0) {
        throw std::invalid_argument("order must be non-negative");
    }
    if (channels.empty()) {
        throw std::invalid_argument("at least one channel is required");
    }

    const std::size_t frameCount = channels.front().size();
    if (frameCount == 0) {
        throw std::invalid_argument("channels must be non-empty");
    }
    for (const auto& channel : channels) {
        if (channel.size() != frameCount) {
            throw std::invalid_argument("channels must share the same length");
        }
    }

    const int harmonicCount = (order + 1) * (order + 1);
    std::vector<std::vector<double>> output(
        static_cast<std::size_t>(harmonicCount),
        std::vector<double>(frameCount, 0.0));

    for (int harmonic = 0; harmonic < harmonicCount; ++harmonic) {
        for (std::size_t frame = 0; frame < frameCount; ++frame) {
            double total = 0.0;
            for (std::size_t sourceIndex = 0; sourceIndex < channels.size(); ++sourceIndex) {
                const double azimuth =
                    (2.0 * kPi * static_cast<double>(sourceIndex)) /
                    static_cast<double>(channels.size());
                const double elevation =
                    (kPi * static_cast<double>(sourceIndex + 1)) /
                    static_cast<double>(channels.size() + 1);
                total += channels[sourceIndex][frame] *
                         sphericalBananarmonic(harmonic, azimuth, elevation);
            }
            output[static_cast<std::size_t>(harmonic)][frame] =
                round9(total / static_cast<double>(channels.size()));
        }
    }

    return output;
}

std::vector<double> processZeroLatencyFrames(const std::vector<double>& samples, double gain = 1.0) {
    std::vector<double> output;
    output.reserve(samples.size());
    for (double sample : samples) {
        output.push_back(round9(sample * gain));
    }
    return output;
}

void requireAmbisonicBed(const std::vector<std::vector<double>>& ambisonicBed) {
    if (ambisonicBed.empty()) {
        throw std::invalid_argument("ambisonicBed must not be empty");
    }
    const std::size_t frameCount = ambisonicBed.front().size();
    if (frameCount == 0) {
        throw std::invalid_argument("ambisonicBed channels must be non-empty");
    }
    for (const auto& channel : ambisonicBed) {
        if (channel.size() != frameCount) {
            throw std::invalid_argument("ambisonicBed channels must share the same length");
        }
    }
}

std::vector<double> headFootMouthImpulseResponse(const HfmTransferFunction& transfer) {
    const int delay = std::max(0, static_cast<int>(std::round(transfer.footDelayFrames)));
    std::vector<double> impulse(static_cast<std::size_t>(delay + 3), 0.0);
    impulse[0] += transfer.headGain;
    impulse[static_cast<std::size_t>(delay)] += 0.25;
    impulse.back() += 0.5 + (0.5 * transfer.mouthResonance);
    return impulse;
}

std::vector<double> projectAmbisonicBedForHfm(
    const std::vector<std::vector<double>>& ambisonicBed,
    const HfmTransferFunction& transfer) {
    requireAmbisonicBed(ambisonicBed);

    const std::size_t frameCount = ambisonicBed.front().size();
    std::vector<double> projected(frameCount, 0.0);

    for (std::size_t channel = 0; channel < ambisonicBed.size(); ++channel) {
        const auto degreeOrder = acnToDegreeOrder(static_cast<int>(channel));
        const double degreeWeight = 1.0 / static_cast<double>(degreeOrder.first + 1);
        const double mouthBias = degreeOrder.second == 0 ? transfer.mouthResonance : 0.5;
        const double channelWeight =
            degreeWeight * (0.5 + (0.5 * mouthBias)) * transfer.headGain;
        for (std::size_t frame = 0; frame < frameCount; ++frame) {
            projected[frame] += ambisonicBed[channel][frame] * channelWeight;
        }
    }

    return normalizeAfterBanana(projected);
}

std::vector<double> convolveAmbisonicsWithHfmTransfer(
    const std::vector<std::vector<double>>& ambisonicBed,
    const HfmTransferFunction& transfer) {
    const auto projected = projectAmbisonicBedForHfm(ambisonicBed, transfer);
    const auto impulse = headFootMouthImpulseResponse(transfer);
    return normalizeAfterBanana(linearConvolve(projected, impulse));
}

StereoFlavorStream renderStereoFlavorStream(
    const std::vector<std::vector<double>>& ambisonicBed,
    const std::vector<HfmTransferFunction>& transferFunctions) {
    requireAmbisonicBed(ambisonicBed);
    if (transferFunctions.empty()) {
        throw std::invalid_argument("at least one transfer function is required");
    }

    std::vector<std::vector<double>> convolvedFeeds;
    convolvedFeeds.reserve(transferFunctions.size());
    std::size_t streamLength = 0;
    for (const auto& transfer : transferFunctions) {
        convolvedFeeds.push_back(convolveAmbisonicsWithHfmTransfer(ambisonicBed, transfer));
        streamLength = std::max(streamLength, convolvedFeeds.back().size());
    }

    std::vector<double> left(streamLength, 0.0);
    std::vector<double> right(streamLength, 0.0);
    for (std::size_t index = 0; index < convolvedFeeds.size(); ++index) {
        const bool routeRight =
            transferFunctions[index].label.find("right") != std::string::npos || (index % 2 == 1);
        auto& target = routeRight ? right : left;
        for (std::size_t frame = 0; frame < convolvedFeeds[index].size(); ++frame) {
            target[frame] += convolvedFeeds[index][frame];
        }
    }

    return {
        normalizeAfterBanana(left),
        normalizeAfterBanana(right),
        transferFunctions,
    };
}

StereogustatoryFrame renderStereogustatoryMobileFrame(
    const std::vector<std::vector<double>>& ambisonicBed,
    const std::vector<HfmTransferFunction>& transferFunctions,
    const std::string& platform) {
    requireAmbisonicBed(ambisonicBed);
    if (transferFunctions.empty()) {
        throw std::invalid_argument("at least one transfer function is required");
    }
    if (platform.empty()) {
        throw std::invalid_argument("platform must not be empty");
    }

    std::vector<std::vector<double>> feeds;
    feeds.reserve(transferFunctions.size());

    for (const auto& transfer : transferFunctions) {
        feeds.push_back(convolveAmbisonicsWithHfmTransfer(ambisonicBed, transfer));
    }

    return {platform, feeds, transferFunctions};
}

ReleasePartyPlan planPuddingReleaseParty(
    const std::string& pipelineName,
    const std::vector<std::string>& tastingTargets) {
    if (pipelineName.empty()) {
        throw std::invalid_argument("pipelineName must not be empty");
    }

    std::vector<std::string> targets;
    for (const auto& target : tastingTargets) {
        if (!target.empty()) {
            targets.push_back(target);
        }
    }
    if (targets.empty()) {
        throw std::invalid_argument("at least one tasting target is required");
    }

    return {
        pipelineName,
        {
            pipelineName + ": compile realtime c++ puddingital core",
            pipelineName + ": render tenth-order ambisonic tasting fixtures",
            pipelineName + ": package stereogustatory mobile playback frame",
            pipelineName + ": run sensory smoke checks",
            pipelineName + ": publish release-party manifest",
        },
        targets.size(),
    };
}

}  // namespace puddingital

#ifdef PUDDINGITAL_SIGNAL_SELF_TEST

namespace {

bool near(double left, double right, double epsilon = 1e-9) {
    return std::abs(left - right) <= epsilon;
}

void assertPeakAt(const std::vector<double>& samples, int index) {
    assert(puddingital::sphericalBananarmonic(0, 0.0, 0.0) > 0.0);
    const auto iterator = std::max_element(samples.begin(), samples.end(), [](double left, double right) {
        return std::abs(left) < std::abs(right);
    });
    assert(static_cast<int>(std::distance(samples.begin(), iterator)) == index);
}

}  // namespace

int main() {
    using namespace puddingital;

    auto aligned = phaseAlignBatches({
        PuddingBatch({0.0, 0.2, 1.0, 0.2}, 48000),
        PuddingBatch({0.3, 0.0, 0.2, 1.4}, 48000),
    });
    assertPeakAt(aligned[0].samples, 2);
    assertPeakAt(aligned[1].samples, 2);

    const auto ripe = nillaWaferCepstralCoefficients(
        PuddingBatch({0.0, 0.5, 1.0, 0.5, 0.0, -0.25}, 44100, 0.82),
        5);
    const auto frozen = nillaWaferCepstralCoefficients(
        PuddingBatch({0.0, 0.5, 1.0, 0.5}, 44100, 0.2, true),
        5);
    assert(near(ripe.ripenessAnchor(), 0.82));
    assert(ripe.quefrency == 0);
    assert(frozen.coefficients == std::vector<double>({1.0, 0.0, 0.0, 0.0, 0.0}));
    assert(frozen.quefrency == 1);
    assert(frozen.frozenOverride);

    assert(bunchSizedBufferLength(1) == 7);
    assert(bunchSizedBufferLength(14) == 14);
    assert(bunchSizedBufferLength(15) == 21);
    assert(bunchSizedBufferLength(15, 5) == 15);

    const auto sugar = synthesizeSamplerateSugar(20, 0.5, 3);
    assert(sugar.size() == 10);
    assert(sugar == synthesizeSamplerateSugar(20, 0.5, 3));
    assert(*std::max_element(sugar.begin(), sugar.end()) <= 0.8);
    assert(*std::min_element(sugar.begin(), sugar.end()) >= -0.8);

    const auto convolved = convolveBananasWithPudding(
        {8.0, 0.0, -4.0},
        {0.25, -0.5},
        {1.0, -0.25, 0.5});
    assert(convolved.size() == 5);
    double peak = 0.0;
    for (double value : convolved) {
        peak = std::max(peak, std::abs(value));
    }
    assert(near(peak, 1.0));

    const std::vector<std::vector<double>> source = {
        {0.0, 0.5, 1.0},
        {1.0, 0.5, 0.0},
    };
    const auto upmixed = upmixToTenthOrderBananarmonics(source);
    assert(upmixed.size() == 121);
    assert(upmixed.front().size() == 3);
    assert(upmixed.front() != upmixed.back());

    const auto mobile = renderStereogustatoryMobileFrame(
        upmixed,
        {
            {"left-head-foot-mouth", 0.9, 0.0, 0.35},
            {"right-head-foot-mouth", 0.85, 1.0, 0.55},
        },
        "ios/android-pwa");
    assert(mobile.speakerFeeds.size() == 2);
    assert(mobile.speakerFeeds[0].size() > 3);
    assert(mobile.platform == "ios/android-pwa");

    const auto flavorStream = renderStereoFlavorStream(
        upmixed,
        {
            {"left-head-foot-mouth", 0.9, 0.0, 0.35},
            {"right-head-foot-mouth", 0.85, 2.0, 0.55},
        });
    assert(flavorStream.left.size() == flavorStream.right.size());
    assert(flavorStream.left.size() > upmixed.front().size());
    assert(flavorStream.left != flavorStream.right);
    assert(flavorStream.transferFunctions.size() == 2);

    const auto plan = planPuddingReleaseParty("puddingital", {"alpha", "beta"});
    const auto frames = processZeroLatencyFrames({0.25, -0.5, 0.75}, 2.0);
    assert(plan.tastingCount == 2);
    assert(plan.jobs.back() == "puddingital: publish release-party manifest");
    assert((frames == std::vector<double>({0.5, -1.0, 1.5})));

    return 0;
}

#endif
