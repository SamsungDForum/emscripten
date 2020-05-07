// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_VIDEO_TRACK_CONFIG_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_VIDEO_TRACK_CONFIG_H_

#include <assert.h>
#include <stddef.h>
#include <stdint.h>

#include "samsung/bindings/elementary_media_track_config.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct EMSSElementaryVideoTrackConfig {
  EMSSElementaryMediaTrackConfig base_config;
  uint32_t width;
  uint32_t height;
  uint32_t framerate_num;
  uint32_t framerate_den;
} EMSSElementaryVideoTrackConfig;

static_assert(offsetof(EMSSElementaryVideoTrackConfig, width) == 12,
              "EMSSElementaryVideoTrackConfig::width has wrong alignment");
static_assert(offsetof(EMSSElementaryVideoTrackConfig, height) == 16,
              "EMSSElementaryVideoTrackConfig::height has wrong alignment");
static_assert(
    offsetof(EMSSElementaryVideoTrackConfig, framerate_num) == 20,
    "EMSSElementaryVideoTrackConfig::framerate_num has wrong alignment");
static_assert(
    offsetof(EMSSElementaryVideoTrackConfig, framerate_den) == 24,
    "EMSSElementaryVideoTrackConfig::framerate_den has wrong alignment");

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_VIDEO_TRACK_CONFIG_H_
