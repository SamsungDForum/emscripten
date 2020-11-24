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

  /// API version. Usually, it has the following format:
  ///
  /// ```
  /// (api level).(wasm)/(component)/(subcomponent A)-...-(subcomponent N)
  /// ```
  ///
  /// ...where `api level` is a number, and `wasm`/`component`/`subcomponent`
  /// are hashes.
  /// Subcomponent part is optional.
  ///
  /// @remarks
  /// version is composed of:
  /// - `api level`: highest supported API level,
  /// - `wasm`, `component`, `subcomponent`: detailed implementation version.
  ///
  /// @note
  /// Older Tizen TV WASM implementations used simple format in the form of
  /// `(api level).(detailed implementation version)` (both values were
  /// numbers).
  const std::string version;

  /// Each API level represents a single version of the API. This vector
  /// contains all API versions supported by this platform.
  const std::vector<uint32_t> api_levels;

  /// Returns a list of supported API-specific features.
  const std::vector<std::string> features;
};  // struct TizenTVApiInfo

}  // namespace wasm
}  // namespace samsung

#endif  // SAMSUNG_WASM_TIZEN_TV_API_INFO_
