// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/tizen_tv_wasm.h"

extern "C" {
typedef void TizenTVWasm_AddFeatureFn(const char* feature,
                                      std::vector<std::string>* features_ptr);
typedef void TizenTVWasm_AddApiFn(
    const char* name,
    const char* version,
    const uint32_t* api_levels,
    uint32_t api_level_size,
    std::vector<std::string>* features_ptr,
    std::vector<samsung::wasm::TizenTVApiInfo>* api_infos_ptr);
extern void TizenTVWasm_GetAvailableApis(
    TizenTVWasm_AddFeatureFn* add_feature_fn,
    TizenTVWasm_AddApiFn* add_api_fn,
    std::vector<std::string>* features_ptr,
    std::vector<samsung::wasm::TizenTVApiInfo>* api_info_ptr);

typedef void TizenTVWasm_AddInstructionsFn(const char* name, void* user_data);
extern void TizenTVWasm_GetSupportedInstructions(
    TizenTVWasm_AddInstructionsFn* add_instructions_fn,
    void* user_data);

extern int TizenTVWasm_IsApiSupported(const char* name, uint32_t api_level);
extern int TizenTVWasm_IsApiFeatureSupported(const char* name,
                                             const char* feature);
}

namespace samsung {
namespace wasm {

std::vector<TizenTVApiInfo> GetAvailableApis() {
  std::vector<TizenTVApiInfo> result;
  std::vector<std::string> features_temp_storage;
  // only a lambda with no capture is convertible to a function pointer
  TizenTVWasm_GetAvailableApis(
      [](const char* feature_str, std::vector<std::string>* features_ptr) {
        features_ptr->push_back(feature_str);
      },
      [](const char* name, const char* version, const uint32_t* api_levels,
         uint32_t api_level_size, std::vector<std::string>* features_ptr,
         std::vector<TizenTVApiInfo>* api_infos_ptr) {
        api_infos_ptr->push_back(TizenTVApiInfo{
            name, version,
            std::vector<uint32_t>{api_levels, api_levels + api_level_size},
            std::move(*features_ptr)});
      },
      &features_temp_storage, &result);
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

bool IsApiFeatureSupported(const std::string& api_name,
                           const std::string& feature) {
  return !!TizenTVWasm_IsApiFeatureSupported(api_name.c_str(), feature.c_str());
}

}  // namespace wasm
}  // namespace samsung
