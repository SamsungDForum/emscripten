// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_
#define INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_

namespace samsung {
namespace wasm {

/// Contains information about EMSS features available on the current device.
struct EmssVersionInfo {
  /// Base EMSS version.
  ///
  /// @remark
  /// Documentation of non-base version features include remarks on <code>
  /// EmssVersionInfo</code> entries indicating their availability.
  bool has_emss;

  /// Legacy EMSS version indicate an early EMSS version.
  bool has_legacy_emss;

  /// Queries platform to get EMSS features available on the current device.
  static EmssVersionInfo Create();
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_EMSS_VERSION_INFO_
