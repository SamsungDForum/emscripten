// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_CONFIG_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_CONFIG_H_

#include <assert.h>
#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum EMSSDecodingMode {
  Hardware,
  HardwareWithFallback,
  Software,
} EMSSDecodingMode;

typedef struct EMSSElementaryMediaTrackConfig {
  const char* mime_type;
  size_t extradata_size;
  const uint8_t* extradata;
  EMSSDecodingMode decoding_mode;
} EMSSElementaryMediaTrackConfig;

static_assert(offsetof(EMSSElementaryMediaTrackConfig, mime_type) == 0,
              "EMSSElementaryMediaTrackConfig::mime_type has wrong alignment");
static_assert(
    offsetof(EMSSElementaryMediaTrackConfig, extradata_size) == 4,
    "EMSSElementaryMediaTrackConfig::extradata_size has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaTrackConfig, extradata) == 8,
              "EMSSElementaryMediaTrackConfig::extradata has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaTrackConfig, decoding_mode) == 12,
              "EMSSElementaryMediaTrackConfig::decoding_mode has "
              "wrong alignment");

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_CONFIG_H_
