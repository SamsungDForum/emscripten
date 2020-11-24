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

enum class DecodingMode {
  kHardware,
  /// Mode supported only on devices which have
  /// `EmssVersionInfo::has_decoding_mode` set to `true`.
  /// Otherwise, setting this mode will have no effect.
  kHardwareWithFallback,
  /// Mode supported only on devices which have
  /// `EmssVersionInfo::has_decoding_mode` set to `true`.
  /// Otherwise, setting this mode will have no effect.
  kSoftware
};

/// Common part of audio and video configs.
struct ElementaryMediaTrackConfig {
  ElementaryMediaTrackConfig() {}

  ElementaryMediaTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata)
      : ElementaryMediaTrackConfig(std::move(mime_type),
                                   std::move(extradata),
                                   DecodingMode::kHardware) {}

  ElementaryMediaTrackConfig(std::string mime_type,
                             std::vector<uint8_t> extradata,
                             DecodingMode decoding_mode)
      : mime_type(std::move(mime_type)),
        extradata(std::move(extradata)),
        decoding_mode(decoding_mode) {}

  /// MIME containing codec and profile.
  std::string mime_type;

  /// Extra data for codec.
  std::vector<uint8_t> extradata;

  /// Specify whether software decoder should be used for a track.
  ///
  /// @remark
  /// This parameter is supported only on devices which have
  /// `EmssVersionInfo::has_decoding_mode` set to `true`.
  /// Value is ignored if EmssVersionInfo::has_decoding_mode` is set to `false`.
  DecodingMode decoding_mode{DecodingMode::kHardware};
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_CONFIG_H_
