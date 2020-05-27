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

/// Type describing config for audio track.
struct ElementaryVideoTrackConfig final : ElementaryMediaTrackConfig {
  ElementaryVideoTrackConfig() : ElementaryMediaTrackConfig() {}

  ElementaryVideoTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata,
                             uint32_t width,
                             uint32_t height,
                             uint32_t framerate_num,
                             uint32_t framerate_den)
      : ElementaryMediaTrackConfig(mime_type, extradata),
        width(width),
        height(height),
        framerate_num(framerate_num),
        framerate_den(framerate_den) {}

  /// Initial width of video in pixels. Changing video width during playback
  /// is possible by changing <code>ElementaryMediaPacket::width</code>.
  uint32_t width;

  /// Initial height of video in pixels. Changing video height during playback
  /// is possible by changing <code>ElementaryMediaPacket::height</code>.
  uint32_t height;

  /// Initial framerate numerator, must be non-negative.
  /// Changing video framerate during playback is possible by changing
  /// <code>ElementaryMediaPacket::framerate_num</code> and
  /// <code>ElementaryMediaPacket::framerate_den</code>.
  uint32_t framerate_num;

  /// Framerate denominator, must be positive.
  /// Changing video framerate during playback is possible by changing
  /// <code>ElementaryMediaPacket::framerate_num</code> and
  /// <code>ElementaryMediaPacket::framerate_den</code>.
  uint32_t framerate_den;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_VIDEO_TRACK_CONFIG_H_
