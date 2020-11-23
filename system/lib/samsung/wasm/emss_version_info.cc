// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/emss_version_info.h"

#include "samsung/wasm/tizen_tv_wasm.h"

namespace samsung {
namespace wasm {

// static
EmssVersionInfo EmssVersionInfo::Create() {
  const auto api_name = std::string{"ElementaryMediaStreamSource"};
  EmssVersionInfo info;
  // API Level 0 is a legacy version that uses special code paths for
  // compatibility.
  info.has_legacy_emss = samsung::wasm::IsApiSupported(api_name, 0);
  info.has_emss = samsung::wasm::IsApiSupported(api_name, 1);
  info.has_video_texture = samsung::wasm::IsApiSupported(api_name, 2);
  info.has_decoding_mode = samsung::wasm::IsApiSupported(api_name, 3);
  info.has_low_latency_video_texture =
      samsung::wasm::IsApiSupported(api_name, 4);
  info.has_ultra_low_latency = samsung::wasm::IsApiSupported(api_name, 5);

  return info;
}

}  // namespace wasm
}  // namespace samsung
