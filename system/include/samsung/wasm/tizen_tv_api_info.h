// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef SAMSUNG_WASM_TIZEN_TV_API_INFO_
#define SAMSUNG_WASM_TIZEN_TV_API_INFO_

#include <cstdint>
#include <string>
#include <vector>

namespace samsung {
namespace wasm {

/// This structure contains version information of a single TizenTV WASM API.
struct TizenTVApiInfo {
  /// A name of the TizenTV WASM API.
  const std::string name;

  /// API version in format: major.minor
  ///
  /// @remarks
  /// version is composed of:
  /// - major number: highest supported API level,
  /// - minor number: detailed implementation version.
  const std::string version;

  /// Each API level represents a single version of the API. This vector
  /// contains all API versions supported by this platform.
  const std::vector<uint32_t> api_levels;
};  // struct TizenTVApiInfo

}  // namespace wasm
}  // namespace samsung

#endif  // SAMSUNG_WASM_TIZEN_TV_API_INFO_
