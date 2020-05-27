// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_STREAM_SOURCE_H_
#define LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_STREAM_SOURCE_H_

#include <stdbool.h>

#include "samsung/bindings/emss_operation_result.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct EMSSElementaryAudioTrackConfig EMSSElementaryAudioTrackConfig;
typedef struct EMSSElementaryVideoTrackConfig EMSSElementaryVideoTrackConfig;

typedef enum EMSSMode {
  EMSSModeNormal = 0,
  EMSSModeLowLatency,
} EMSSMode;

typedef enum EMSSReadyState {
  EMSSReadyStateDetached = 0,
  EMSSReadyStateClosed,
  EMSSReadyStateOpenPending,
  EMSSReadyStateOpen,
  EMSSReadyStateEnded,
} EMSSReadyState;

typedef enum EMSSAsyncResult {
  EMSSAsyncResultSuccess = 0,
  EMSSAsyncResultOpenInProgressError,
  EMSSAsyncResultCloseInProgressError,
  EMSSAsyncResultInvalidStateError,
  EMSSAsyncResultSourceIsNotAttachedError,
  EMSSAsyncResultNoTracksAttachedError,
  EMSSAsyncResultUnknownError,
} EMSSAsyncResult;

typedef void (*OnEventCallback)(void* userData);
typedef void (*OnPlaybackPositionChangedCallback)(float newTime,
                                                  void* userData);
typedef void (*OnOperationDoneCallback)(EMSSAsyncResult result, void* userData);

extern int EMSSCreate(EMSSMode latencyMode);
extern EMSSOperationResult EMSSRemove(int handle);
extern EMSSOperationResult EMSSCreateObjectURL(int handle, char** out);
extern EMSSOperationResult EMSSRevokeObjectURL(char* url);
extern EMSSOperationResult EMSSAddAudioTrack(
    int handle,
    const EMSSElementaryAudioTrackConfig* config,
    int* outTrackHandle);
extern EMSSOperationResult EMSSAddVideoTrack(
    int handle,
    const EMSSElementaryVideoTrackConfig* config,
    int* outTrackHandle);
extern EMSSOperationResult EMSSRemoveTrack(int handle, int trackHandle);
extern EMSSOperationResult EMSSFlush(int handle);
extern EMSSOperationResult EMSSClose(int handle,
                                     OnOperationDoneCallback callback,
                                     void* userData);
extern EMSSOperationResult EMSSOpen(int handle,
                                    OnOperationDoneCallback callback,
                                    void* userData);
extern EMSSOperationResult EMSSGetDuration(int handle, double* out);
extern EMSSOperationResult EMSSSetDuration(int handle, double newDuration);
extern EMSSOperationResult EMSSGetMode(int handle, EMSSMode* out);
extern EMSSOperationResult EMSSGetReadyState(int handle, EMSSReadyState* out);

extern EMSSOperationResult EMSSSetOnSourceDetached(int handle,
                                                   OnEventCallback callback,
                                                   void* userData);
extern EMSSOperationResult EMSSUnsetOnSourceDetached(int handle);
extern EMSSOperationResult EMSSSetOnSourceClosed(int handle,
                                                 OnEventCallback callback,
                                                 void* userData);
extern EMSSOperationResult EMSSUnsetOnSourceClosed(int handle);
extern EMSSOperationResult EMSSSetOnSourceOpenPending(int handle,
                                                      OnEventCallback callback,
                                                      void* userData);
extern EMSSOperationResult EMSSUnsetOnSourceOpenPending(int handle);
extern EMSSOperationResult EMSSSetOnSourceOpen(int handle,
                                               OnEventCallback callback,
                                               void* userData);
extern EMSSOperationResult EMSSUnsetOnSourceOpen(int handle);
extern EMSSOperationResult EMSSSetOnSourceEnded(int handle,
                                                OnEventCallback callback,
                                                void* userData);
extern EMSSOperationResult EMSSUnsetOnSourceEnded(int handle);

extern EMSSOperationResult EMSSSetOnPlaybackPositionChanged(
    int handle,
    OnPlaybackPositionChangedCallback callback,
    void* userData);
extern EMSSOperationResult EMSSUnsetOnPlaybackPositionChanged(int handle);

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_ELEMENTARY_MEDIA_STREAM_SOURCE_H_
