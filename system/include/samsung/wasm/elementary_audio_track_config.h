// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_AUDIO_TRACK_CONFIG_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_AUDIO_TRACK_CONFIG_H_

#include <cstdint>
#include <string>
#include <vector>

#include "samsung/wasm/elementary_media_track_config.h"

namespace samsung {
namespace wasm {

/// Enum representing supported audio formats.
enum class SampleFormat {
  kUnknown,    ///< Unknown sample format.
  kU8,         ///< Unsigned 8-bit w/ bias of 128.
  kS16,        ///< Signed 16-bit.
  kS32,        ///< Signed 32-bit.
  kF32,        ///< Float 32-bit.
  kPlanarS16,  ///< Signed 16-bit planar.
  kPlanarF32,  ///< Float 32-bit planar.
  kPlanarS32,  ///< Signed 32-bit planar.
  kS24,        ///< Signed 24-bit.
  kAc3,        ///< Compressed AC3 bitstream.
  kEac3,       ///< Compressed E-AC3 bitstream.
};

/// Lists representations of ordering of audio channels.
enum class ChannelLayout {
  kNone,           ///< Channel Layout is unspecified.
  kUnsupported,    ///< Channel Layout is unsupported.
  kMono,           ///< Front C.
  kStereo,         ///< Front L + R.
  k2Point1,        ///< Stereo L + R, LFE.
  k2_1,            ///< Front L + R, Back C.
  k2_2,            ///< Front L + R, Side L + R.
  k3_1,            ///< Stereo L + R, Front C, LFE.
  k4_0,            ///< Front L + R + C, Back C.
  k4_1,            ///< Stereo L + R, Front C, Rear C, LFE.
  k4_1QuadSide,    ///< Front L + R, Side L + R, LFE.
  k5_0,            ///< Front L + R + C, Side L + R.
  k5_0Back,        ///< Front L + R + C, Back L + R.
  k5_1,            ///< Front L + R + C, LFE, Side L + R.
  k5_1Back,        ///< Front L, Front R, Front C, LFE, Back L + R.
  k6_0,            ///< Stereo L + R, Front C, Side L + R, Back C.
  k6_0Front,       ///< Stereo L + R, Side L + R, Front LofC + RofC.
  k6_1,            ///< Stereo L + R, Front C, LFE, Side L + R, Rear, Center.
  k6_1Back,        ///< Stereo L + R, Front C, LFE, Back L + R, Rear Center.
  k6_1Front,       ///< Stereo L + R, Side L, Side R, Front LofC + RofC, LFE.
  k7_0,            ///< Front L + R + C, Side L + R, Back L + R.
  k7_0Front,       ///< Front L + R + C, Side L + R, Front LofC, Front RofC.
  k7_1,            ///< Front L + R + C, LFE, Side L + R, Back L + R.
  k7_1Wide,        ///< Front L + R + C, LFE, Side L + R, Front LofC + RofC.
  k7_1WideBack,    ///< Front L + R + C, LFE, Back L + R, Front LofC + RofC.
  kDiscrete,       ///< Channels are not explicitly mapped to speakers.
  kHexagonal,      ///< Stereo L + R, Front C, Back L + R + C.
  kOctagonal,      ///< Front L + R + C, Side L + R, Back L + R + C.
  kQuad,           ///< Front L + R, Back L + R.
  kStereoDownmix,  ///< Stereo L + R.
  kSurround,       ///< Front L + R + C.
};

/// Type describing config for an audio track.
struct ElementaryAudioTrackConfig final : ElementaryMediaTrackConfig {
  ElementaryAudioTrackConfig() : ElementaryMediaTrackConfig() {}

  ElementaryAudioTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata,
                             SampleFormat sample_format,
                             ChannelLayout channel_layout,
                             uint32_t samples_per_second)
      : ElementaryMediaTrackConfig(mime_type, extradata),
        sample_format(sample_format),
        channel_layout(channel_layout),
        samples_per_second(samples_per_second) {}

  SampleFormat sample_format;
  ChannelLayout channel_layout;
  uint32_t samples_per_second;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_AUDIO_TRACK_CONFIG_H_
