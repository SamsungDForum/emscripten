// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_CONFIG_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_CONFIG_H_

#include <cstdint>
#include <string>
#include <vector>

namespace samsung {
namespace wasm {

/// Common part of audio and video configs.
struct ElementaryMediaTrackConfig {
  ElementaryMediaTrackConfig() {}

  ElementaryMediaTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata)
      : mime_type(std::move(mime_type)), extradata(std::move(extradata)) {}

  /// MIME containing codec and profile.
  std::string mime_type;

  /// Extra data for codec.
  std::vector<uint8_t> extradata;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_CONFIG_H_
