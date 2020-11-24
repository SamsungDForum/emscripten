// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef SAMSUNG_WASM_TIZEN_TV_WASM_
#define SAMSUNG_WASM_TIZEN_TV_WASM_

#include <cstdint>
#include <string>
#include <vector>

#include "samsung/wasm/tizen_tv_api_info.h"

namespace samsung {
namespace wasm {

/// Gets all TizenTV WASM APIs available on this platform.
std::vector<TizenTVApiInfo> GetAvailableApis();

/// Gets all supported instruction sets available on this platform.
std::vector<std::string> GetSupportedInstructions();

/// Checks if a given Tizen WASM API is supported on this platform in a given
/// API level.
bool IsApiSupported(const std::string& api_name, uint32_t api_level);

/// Checks whether or not a given API supports a given feature on this
/// platform.
bool IsApiFeatureSupported(const std::string& api_name,
                           const std::string& feature);

}  // namespace wasm
}  // namespace samsung

#endif  // SAMSUNG_WASM_TIZEN_TV_WASM_
