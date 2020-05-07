// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_MEDIA_KEY_H_
#define LIB_SAMSUNG_BINDINGS_MEDIA_KEY_H_

#include <assert.h>
#include <stddef.h>
#include <stdint.h>

#include "samsung/bindings/emss_operation_result.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef enum MediaKeyContentDecryptionModule {
  MediaKeyContentDecryptionModuleUnknown,
  MediaKeyContentDecryptionModuleCenc,
  MediaKeyContentDecryptionModuleCbcs,
} MediaKeyContentDecryptionModule;

typedef enum MediaKeyEncryptionMode {
  MediaKeyEncryptionModeUnknown,
  MediaKeyEncryptionModePlayready,
  MediaKeyEncryptionModeWidevine,
} MediaKeyEncryptionMode;

typedef enum MediaKeyRobustness {
  MediaKeyRobustnessEmpty,
  MediaKeyRobustnessSWSecureCrypto,
  MediaKeyRobustnessSWSecureDecode,
  MediaKeyRobustnessHWSecureCrypto,
  MediaKeyRobustnessHWSecureDecode,
  MediaKeyRobustnessHWSecureAll,
} MediaKeyRobustness;

typedef struct MediaKeyConfig {
  MediaKeyContentDecryptionModule cdm;
  MediaKeyEncryptionMode encryption_mode;
  const char* license_server;
  size_t init_data_size;
  const uint8_t* init_data;

  const char* audio_mime_type;
  MediaKeyRobustness audio_robustness;

  const char* video_mime_type;
  MediaKeyRobustness video_robustness;
} MediaKeyConfig;

typedef enum MediaKeyAsyncResult {
  MediaKeyAsyncResultSuccess = 0,
  MediaKeyAsyncResultInvalidConfigurationError,
  MediaKeyAsyncResultSessionNotUpdatedError,
  MediaKeyAsyncResultUnknownError,
} MediaKeyAsyncResult;

typedef void (*OnSetEncryptionDoneCallback)(MediaKeyAsyncResult result,
                                            int media_key_handle,
                                            void* userData);

extern EMSSOperationResult mediaKeySetEncryption(
    const MediaKeyConfig* config, OnSetEncryptionDoneCallback on_finished,
    void* user_data);
extern EMSSOperationResult mediaKeyRemove(int handle);

static_assert(offsetof(MediaKeyConfig, cdm) == 0,
              "MediaKeyConfig::cdm has wrong alignment");
static_assert(offsetof(MediaKeyConfig, encryption_mode) == 4,
              "MediaKeyConfig::encryption_mode has wrong alignment");
static_assert(offsetof(MediaKeyConfig, license_server) == 8,
              "MediaKeyConfig::license_server has wrong alignment");
static_assert(offsetof(MediaKeyConfig, init_data_size) == 12,
              "MediaKeyConfig::init_data_size has wrong alignment");
static_assert(offsetof(MediaKeyConfig, init_data) == 16,
              "MediaKeyConfig::data_size has wrong alignment");
static_assert(offsetof(MediaKeyConfig, audio_mime_type) == 20,
              "MediaKeyConfig::audio_mime_type has wrong alignment");
static_assert(offsetof(MediaKeyConfig, audio_robustness) == 24,
              "MediaKeyConfig::audio_robustness has wrong alignment");
static_assert(offsetof(MediaKeyConfig, video_mime_type) == 28,
              "MediaKeyConfig::video_mime_type has wrong alignment");
static_assert(offsetof(MediaKeyConfig, video_robustness) == 32,
              "MediaKeyConfig::video_robustness has wrong alignment");

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_MEDIA_KEY_H_
