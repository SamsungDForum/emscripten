// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/tizen_tv_wasm.h"

extern "C" {
typedef void TizenTVWasm_AddApiFn(const char* name,
                                  const char* version,
                                  const uint32_t* api_levels,
                                  uint32_t api_level_size,
                                  void* user_data);
extern void TizenTVWasm_GetAvailableApis(TizenTVWasm_AddApiFn* add_api_fn,
                                         void* user_data);

typedef void TizenTVWasm_AddInstructionsFn(const char* name, void* user_data);
extern void TizenTVWasm_GetSupportedInstructions(
    TizenTVWasm_AddInstructionsFn* add_instructions_fn,
    void* user_data);

extern int TizenTVWasm_IsApiSupported(const char* name, uint32_t api_level);
}

namespace samsung {
namespace wasm {

std::vector<TizenTVApiInfo> GetAvailableApis() {
  std::vector<TizenTVApiInfo> result;
  // only a lambda with no capture is convertible to a function pointer
  TizenTVWasm_GetAvailableApis(
      [](const char* name, const char* version, const uint32_t* api_levels,
         uint32_t api_level_size, void* user_data) {
        auto* result = static_cast<std::vector<TizenTVApiInfo>*>(user_data);
        result->push_back(TizenTVApiInfo{
            name, version,
            std::vector<uint32_t>{api_levels, api_levels + api_level_size}});
      },
      &result);
  return result;
}

std::vector<std::string> GetSupportedInstructions() {
  std::vector<std::string> result;
  // only a lambda with no capture is convertible to a function pointer
  TizenTVWasm_GetSupportedInstructions(
      [](const char* instruction_set, void* user_data) {
        auto* result = static_cast<std::vector<std::string>*>(user_data);
        result->emplace_back(instruction_set);
      },
      &result);
  return result;
}

bool IsApiSupported(const std::string& api_name, uint32_t api_level) {
  return !!TizenTVWasm_IsApiSupported(api_name.c_str(), api_level);
}

}  // namespace wasm
}  // namespace samsung
