// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_AUDIO_TRACK_CONFIG_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_AUDIO_TRACK_CONFIG_H_

#include <assert.h>
#include <stddef.h>
#include <stdint.h>

#include "samsung/bindings/elementary_media_track_config.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum EMSSSampleFormat {
  SampleFormatUnknown,
  SampleFormatU8,         // Unsigned 8-bit w/ bias of 128.
  SampleFormatS16,        // Signed 16-bit.
  SampleFormatS32,        // Signed 32-bit.
  SampleFormatF32,        // Float 32-bit.
  SampleFormatPlanarS16,  // Signed 16-bit planar.
  SampleFormatPlanarF32,  // Float 32-bit planar.
  SampleFormatPlanarS32,  // Signed 32-bit planar.
  SampleFormatS24,        // Signed 24-bit.
  SampleFormatAc3,        // Compressed AC3 bitstream.
  SampleFormatEac3        // Compressed E-AC3 bitstream.
} EMSSSampleFormat;

typedef enum EMSSChannelLayout {
  ChannelLayoutNone,
  ChannelLayoutUnsupported,
  ChannelLayoutMono,         // Front C
  ChannelLayoutStereo,       // Front L, Front R
  ChannelLayout2Point1,      // Stereo L, Stereo R, LFE
  ChannelLayout2_1,          // Front L, Front R, Back C
  ChannelLayout2_2,          // Front L, Front R, Side L, Side R
  ChannelLayout3_1,          // Stereo L, Stereo R, Front C, LFE
  ChannelLayout4_0,          // Front L, Front R, Front C, Back C
  ChannelLayout4_1,          // Stereo L, Stereo R, Front C, Rear C, LFE
  ChannelLayout4_1QuadSide,  // Front L, Front R, Side L, Side R, LFE
  ChannelLayout5_0,          // Front L, Front R, Front C, Side L, Side R
  ChannelLayout5_0Back,      // Front L, Front R, Front C, Back L, Back R
  ChannelLayout5_1,          // Front L, Front R, Front C, LFE, Side L, Side R
  ChannelLayout5_1Back,      // Front L, Front R, Front C, LFE, Back L, Back R
  ChannelLayout6_0,       // Stereo L, Stereo R, Front C, Side L, Side R, Back C
  ChannelLayout6_0Front,  // Stereo L, Stereo R, Side L, Side R, Front LofC,
                          // Front RofC
  ChannelLayout6_1,  // Stereo L, Stereo R, Front C, LFE, Side L, Side R, Rear
                     // Center
  ChannelLayout6_1Back,   // Stereo L, Stereo R, Front C, LFE, Back L, Back R,
                          // Rear Center
  ChannelLayout6_1Front,  // Stereo L, Stereo R, Side L, Side R, Front LofC,
                          // Front RofC, LFE
  ChannelLayout7_0,  // Front L, Front R, Front C, Side L, Side R, Back L, Back
                     // R
  ChannelLayout7_0Front,  // Front L, Front R, Front C, Side L, Side R, Front
                          // LofC, Front RofC
  ChannelLayout7_1,  // Front L, Front R, Front C, LFE, Side L, Side R, Back L,
                     // Back R
  ChannelLayout7_1Wide,      // Front L, Front R, Front C, LFE, Side L, Side R,
                             // Front LofC, Front RofC
  ChannelLayout7_1WideBack,  // Front L, Front R, Front C, LFE, Back L, Back R,
                             // Front LofC, Front RofC
  ChannelLayoutDiscrete,     // Channels are not explicitly mapped to speakers.
  ChannelLayoutHexagonal,  // Stereo L, Stereo R, Front C, Rear L, Rear R, Rear
                           // C
  ChannelLayoutOctagonal,  // Front L, Front R, Front C, Side L, Side R, Rear L,
                           // Back R, Back C.
  ChannelLayoutQuad,       // Front L, Front R, Back L, Back R
  ChannelLayoutStereoDownmix,  // Stereo L, Stereo R
  ChannelLayoutSurround,       // Front L, Front R, Front C
} EMSSChannelLayout;

typedef struct EMSSElementaryAudioTrackConfig {
  EMSSElementaryMediaTrackConfig base_config;
  EMSSSampleFormat sample_format;
  EMSSChannelLayout channel_layout;
  uint32_t samples_per_second;
} EMSSElementaryAudioTrackConfig;

static_assert(
    offsetof(EMSSElementaryAudioTrackConfig, sample_format) == 16,
    "EMSSElementaryAudioTrackConfig::sample_format has wrong alignment");
static_assert(
    offsetof(EMSSElementaryAudioTrackConfig, channel_layout) == 20,
    "EMSSElementaryAudioTrackConfig::channel_layout has wrong alignment");
static_assert(
    offsetof(EMSSElementaryAudioTrackConfig, samples_per_second) == 24,
    "EMSSElementaryAudioTrackConfig::samples_per_second has wrong alignment");

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_AUDIO_TRACK_CONFIG_H_
