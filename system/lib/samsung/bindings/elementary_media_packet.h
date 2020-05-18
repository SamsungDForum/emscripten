// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_PACKET_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_PACKET_H_

#include <assert.h>
#include <stddef.h>
#include <stdint.h>

#include "samsung/bindings/media_key.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct EMSSEncryptedSubsampleDescription {
  uint32_t clear_block;
  uint32_t cipher_block;
} EMSSEncryptedSubsampleDescription;

typedef struct EMSSElementaryMediaPacket {
  double pts;
  double dts;
  double duration;
  bool is_key_frame;
  size_t data_size;
  const void* data;
  uint32_t width;
  uint32_t height;
  uint32_t framerate_num;
  uint32_t framerate_den;
  int32_t session_id;
} EMSSElementaryMediaPacket;

typedef struct EMSSEncryptedElementaryMediaPacket {
  EMSSElementaryMediaPacket base_packet;

  size_t subsamples_size;
  const EMSSEncryptedSubsampleDescription* subsamples;
  size_t key_id_size;
  const uint8_t* key_id;
  size_t initialization_vector_size;
  const uint8_t* initialization_vector;
  MediaKeyEncryptionMode encryption_mode;
} EMSSEncryptedElementaryMediaPacket;

static_assert(offsetof(EMSSElementaryMediaPacket, pts) == 0,
              "EMSSElementaryMediaPacket::pts has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, dts) == 8,
              "EMSSElementaryMediaPacket::dts has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, duration) == 16,
              "EMSSElementaryMediaPacket::duration has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, is_key_frame) == 24,
              "EMSSElementaryMediaPacket::isKeyFrame has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, data_size) == 28,
              "EMSSElementaryMediaPacket::data_size has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, data) == 32,
              "EMSSElementaryMediaPacket::data has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, width) == 36,
              "EMSSElementaryMediaPacket::width has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, height) == 40,
              "EMSSElementaryMediaPacket::height has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, framerate_num) == 44,
              "EMSSElementaryMediaPacket::framerate_num has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, framerate_den) == 48,
              "EMSSElementaryMediaPacket::framerate_den has wrong alignment");
static_assert(offsetof(EMSSElementaryMediaPacket, session_id) == 52,
              "EMSSElementaryMediaPacket::sessionId has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, base_packet) == 0,
              "EMSSEncryptedElementaryMediaPacket::base_packet"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, subsamples_size) ==
                  56,
              "EMSSEncryptedElementaryMediaPacket::subsamples_size"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, subsamples) == 60,
              "EMSSEncryptedElementaryMediaPacket::subsamples"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, key_id_size) == 64,
              "EMSSEncryptedElementaryMediaPacket::key_id_size"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, key_id) == 68,
              "EMSSEncryptedElementaryMediaPacket::key_id has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket,
                       initialization_vector_size) == 72,
              "EMSSEncryptedElementaryMediaPacket::initialization_vector_size"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket,
                       initialization_vector) == 76,
              "EMSSEncryptedElementaryMediaPacket::initialization_vector"
              " has wrong alignment");
static_assert(offsetof(EMSSEncryptedElementaryMediaPacket, encryption_mode) ==
                  80,
              "EMSSEncryptedElementaryMediaPacket::encryption_mode"
              " has wrong alignment");

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_PACKET_H_
