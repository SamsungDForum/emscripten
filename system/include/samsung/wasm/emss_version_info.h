// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_
#define INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_

namespace samsung {
namespace wasm {

/// Contains information about `ElementaryMediaStreamSource` features available
/// on the current device.
struct EmssVersionInfo {
  /// Base `ElementaryMediaStreamSource` version.
  ///
  /// @remark
  /// Documentation of non-base version features include remarks on
  /// `EmssVersionInfo` entries indicating their availability.
  bool has_emss;

  /// An early `ElementaryMediaStreamSource` version.
  ///
  /// @remark
  /// If this is `true` some limitations apply. For details, please see
  /// [a note on compatibility on Samsung Developers](https://developer.samsung.com/smarttv/develop/extension-libraries/webassembly/tizen-wasm-player/usage-guide.html#note-on-compatibility).
  bool has_legacy_emss;

  /// `ElementaryMediaStreamSource::Mode::kVideoTexture` is supported on this
  /// device.
  bool has_video_texture;

  /// `ElementaryMediaTrackConfig::decoding_mode` is supported on this device.
  bool has_decoding_mode;

  /// Queries platform to get `ElementaryMediaStreamSource` features available
  /// on the current device.
  static EmssVersionInfo Create();
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_
