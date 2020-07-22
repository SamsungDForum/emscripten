// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_H_

#include <stdbool.h>
#include <stdint.h>

#include "samsung/bindings/emss_operation_result.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct EMSSElementaryMediaPacket EMSSElementaryMediaPacket;
typedef struct EMSSElementaryVideoPicture EMSSElementaryVideoPicture;

typedef enum EMSSElementaryMediaTrackCloseReason {
  ElementaryMediaTrackCloseReasonSourceClosed = 0,
  ElementaryMediaTrackCloseReasonSourceError,
  ElementaryMediaTrackCloseReasonSourceDetached,
  ElementaryMediaTrackCloseReasonTrackDisabled,
  ElementaryMediaTrackCloseReasonTrackEnded,
  ElementaryMediaTrackCloseReasonTrackSeeking,
  ElementaryMediaTrackCloseReasonUnknown,
} EMSSElementaryMediaTrackCloseReason;

typedef void (*OnTrackOpenCallback)(void* userData);
typedef void (*OnTrackClosedCallback)(
    EMSSElementaryMediaTrackCloseReason reason,
    void* userData);
typedef void (*OnTrackSeekCallback)(float newTime, void* userData);
typedef void (*OnSessionIdChangedCallback)(int32_t sessionId, void* userData);
typedef void (*OnAppendErrorCallback)(EMSSOperationResult appendError,
                                      void* userData);

extern EMSSOperationResult elementaryMediaTrackRemove(int handle);
extern EMSSOperationResult elementaryMediaTrackAppendPacket(
    int handle,
    EMSSElementaryMediaPacket* packet);
extern EMSSOperationResult elementaryMediaTrackAppendPacketAsync(
    int handle,
    EMSSElementaryMediaPacket* packet);
extern EMSSOperationResult elementaryMediaTrackAppendEncryptedPacket(
    int handle,
    EMSSEncryptedElementaryMediaPacket* packet);
extern EMSSOperationResult elementaryMediaTrackAppendEncryptedPacketAsync(
    int handle,
    EMSSEncryptedElementaryMediaPacket* packet);
extern EMSSOperationResult elementaryMediaTrackAppendEndOfTrack(
    int handle,
    int32_t sessionId);
extern EMSSOperationResult elementaryMediaTrackAppendEndOfTrackAsync(
    int handle,
    int32_t sessionId);
extern EMSSOperationResult elementaryMediaTrackFillTextureWithNextFrame(
    int handle,
    uint32_t textureId,
    void (*finishedCallback)(EMSSOperationResult result, void* userData),
    void* userData);
extern EMSSOperationResult elementaryMediaTrackFillTextureWithNextFrameSync(
    int handle,
    uint32_t textureId);
extern EMSSOperationResult elementaryMediaTrackGetSessionId(int handle,
                                                            int32_t* sessionId);
extern EMSSOperationResult elementaryMediaTrackIsOpen(int handle, bool* isOpen);
extern EMSSOperationResult elementaryMediaTrackRecycleTexture(
    int handle,
    uint32_t textureId);
extern EMSSOperationResult elementaryMediaTrackRegisterCurrentGraphicsContext(
    int handle);
extern EMSSOperationResult elementaryMediaTrackSetMediaKey(
    int handle,
    int media_key_handle);
extern EMSSOperationResult elementaryMediaTrackSetOnAppendError(
    int handle,
    OnAppendErrorCallback callback,
    void* userData);
extern EMSSOperationResult elementaryMediaTrackUnsetOnAppendError(int handle);
extern EMSSOperationResult elementaryMediaTrackSetOnTrackOpen(
    int handle,
    OnTrackOpenCallback callback,
    void* userData);
extern EMSSOperationResult elementaryMediaTrackUnsetOnTrackOpen(int handle);
extern EMSSOperationResult elementaryMediaTrackSetOnTrackClosed(
    int handle,
    OnTrackClosedCallback callback,
    void* userData);
extern EMSSOperationResult elementaryMediaTrackUnsetOnTrackClosed(int handle);
extern EMSSOperationResult elementaryMediaTrackSetOnSeek(
    int handle,
    OnTrackSeekCallback callback,
    void* userData);
extern EMSSOperationResult elementaryMediaTrackUnsetOnSeek(int handle);
extern EMSSOperationResult elementaryMediaTrackSetOnSessionIdChanged(
    int handle,
    OnSessionIdChangedCallback callback,
    void* userData);
extern EMSSOperationResult elementaryMediaTrackUnsetOnSessionIdChanged(
    int handle);

extern EMSSOperationResult
elementaryMediaTrackSetListenersForSessionIdEmulation(int handle,
                                                      OnTrackClosedCallback,
                                                      void* userData);
extern EMSSOperationResult
elementaryMediaTrackUnsetListenersForSessionIdEmulation(int handle);

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_TRACK_H_
