// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_
#define LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_

#ifdef __cplusplus
extern "C" {
#endif

typedef enum EMSSOperationResult {
  EmssSuccess = 0,
  EmssInvalidObject,
  EmssInvalidArgument,
  EmssInvalidState,
  EmssListenerAlreadySet,
  EmssNoSuchListener,
  EmssNotAllowed,
  EmssNotSupported,
  EmssAlreadyDestroyed,
  EmssAlreadyInProgress,
  EmssCloseInProgress,
  EmssNotAllowedInCurrentMode,
  EmssNoTracksAttached,
  EmssOpenInProgress,
  EmssPlaybackStateChangeInProgress,
  EmssSourceMustBeClosed,
  EmssSourceNotAttached,
  EmssTimestampsExceedDuration,
  EmssTrackLimitReached,
  EmssUnrelatedObject,
  EmssAborted,
  EmssFailed,
  EmssConfigInvalidChannelLayout,
  EmssConfigInvalidCodec,
  EmssConfigInvalidFramerate,
  EmssConfigInvalidResolution,
  EmssConfigInvalidMimeType,
  EmssConfigInvalidSampleFormat,
  EmssConfigInvalid,
  EmssAppendBufferFull,
  EmssAppendExpectsKeyframe,
  EmssAppendIgnored,
  EmssAppendNoDuration,
  EmssAppendInvalidDts,
  EmssAppendInvalidPts,
  EmssAppendInvalidTrackState,
  EmssAppendInvalidVideoParameters,
  EmssAppendNoPacketData,
  EmssAppendResourceAllocationError,
  EmssAppendDecryptionError,
  EmssAppendDecryptorNeedsMoreData,
  EmssAppendNoDecryptionKey,
  EmssAppendInvalidInitializationVector,
  EmssAppendInvalidKeyId,
  EmssAppendInvalidMediaKeySession,
  EmssAppendInvalidSubsampleDescription,
  EmssAppendUnknownDecryptionMode,
  EmssMediaKeyInvalidConfiguration,
  EmssMediaKeySessionNotUpdated,
  EmssVideoDecoderInvalidTrackType,
  EmssVideoDecoderInvalidVideoTexture,
  EmssVideoDecoderWebGlContextNotRegistered,
  EmssVideoDecoderNotInVideoTextureMode,
} EMSSOperationResult;

const char* EMSSOperationResultToString(EMSSOperationResult result);

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_
