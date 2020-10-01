// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_VIDEO_TRACK_CONFIG_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_VIDEO_TRACK_CONFIG_H_

#include <cstdint>
#include <string>
#include <vector>

#include "samsung/wasm/elementary_media_track_config.h"

namespace samsung {
namespace wasm {

/// Contains video `ElementaryMediaTrack` config.
struct ElementaryVideoTrackConfig final : ElementaryMediaTrackConfig {
  ElementaryVideoTrackConfig() : ElementaryMediaTrackConfig() {}

  ElementaryVideoTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata,
                             uint32_t width,
                             uint32_t height,
                             uint32_t framerate_num,
                             uint32_t framerate_den)
      : ElementaryVideoTrackConfig(std::move(mime_type),
                                   std::move(extradata),
                                   DecodingMode::kHardware,
                                   width,
                                   height,
                                   framerate_num,
                                   framerate_den) {}

  ElementaryVideoTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata,
                             DecodingMode decoding_mode,
                             uint32_t width,
                             uint32_t height,
                             uint32_t framerate_num,
                             uint32_t framerate_den)
      : ElementaryMediaTrackConfig(std::move(mime_type),
                                   std::move(extradata),
                                   decoding_mode),
        width(width),
        height(height),
        framerate_num(framerate_num),
        framerate_den(framerate_den) {}

  /// Initial width of video in pixels. Changing video width during playback
  /// is possible by changing `ElementaryMediaPacket::width`.
  uint32_t width;

  /// Initial height of video in pixels. Changing video height during playback
  /// is possible by changing `ElementaryMediaPacket::height`.
  uint32_t height;

  /// Initial framerate numerator, must be non-negative.
  /// Changing video framerate during playback is possible by changing
  /// `ElementaryMediaPacket::framerate_num` and
  /// `ElementaryMediaPacket::framerate_den`.
  uint32_t framerate_num;

  /// Framerate denominator, must be positive.
  /// Changing video framerate during playback is possible by changing
  /// `ElementaryMediaPacket::framerate_num` and
  /// `ElementaryMediaPacket::framerate_den`.
  uint32_t framerate_den;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_VIDEO_TRACK_CONFIG_H_
