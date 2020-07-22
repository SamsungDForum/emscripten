// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/bindings/emss_operation_result.h"

extern "C" {

const char* EMSSOperationResultToString(EMSSOperationResult result) {
  switch (result) {
    case EmssSuccess:
      return "Success";
    case EmssInvalidObject:
      return "Invalid object";
    case EmssInvalidArgument:
      return "Invalid argument";
    case EmssInvalidState:
      return "Invalid ready state";
    case EmssListenerAlreadySet:
      return "Listener already set";
    case EmssNoSuchListener:
      return "No such listener";
    case EmssNotAllowed:
      return "Not allowed";
    case EmssNotSupported:
      return "Not supported";
    case EmssAlreadyDestroyed:
      return "Player already destroyed";
    case EmssAlreadyInProgress:
      return "Already in progress";
    case EmssCloseInProgress:
      return "Close in progress";
    case EmssNotAllowedInCurrentMode:
      return "Not allowed in current mode";
    case EmssNoTracksAttached:
      return "No tracks attached";
    case EmssOpenInProgress:
      return "Open in progress";
    case EmssPlaybackStateChangeInProgress:
      return "Playback state change in progress";
    case EmssSourceMustBeClosed:
      return "Source must be closed";
    case EmssSourceNotAttached:
      return "Source not attached";
    case EmssTimestampsExceedDuration:
      return "Timestamps exceed duration";
    case EmssTrackLimitReached:
      return "Track limit reached";
    case EmssUnrelatedObject:
      return "Unrelated object";
    case EmssAborted:
      return "Operation aborted";
    case EmssConfigInvalidChannelLayout:
      return "Invalid channel layout";
    case EmssConfigInvalidCodec:
      return "Invalid codec";
    case EmssConfigInvalidFramerate:
      return "Invalid framerate";
    case EmssConfigInvalidResolution:
      return "Invalid resolution";
    case EmssConfigInvalidMimeType:
      return "Invalid mime type";
    case EmssConfigInvalidSampleFormat:
      return "Invalid Sample Format";
    case EmssConfigInvalid:
      return "Config Invalid";
    case EmssAppendBufferFull:
      return "Buffer full";
    case EmssAppendExpectsKeyframe:
      return "Key frame expected";
    case EmssAppendIgnored:
      return "Append ignored";
    case EmssAppendNoDuration:
      return "No duration";
    case EmssAppendInvalidDts:
      return "Invalid dts";
    case EmssAppendInvalidPts:
      return "Invalid pts";
    case EmssAppendInvalidTrackState:
      return "Invalid track state";
    case EmssAppendInvalidVideoParameters:
      return "Invalid video parameters";
    case EmssAppendNoPacketData:
      return "No packet data";
    case EmssAppendResourceAllocationError:
      return "Resource allocation error";
    case EmssAppendDecryptionError:
      return "Decryption error";
    case EmssAppendDecryptorNeedsMoreData:
      return "Decryptor needs more data";
    case EmssAppendNoDecryptionKey:
      return "No decryption key";
    case EmssAppendInvalidInitializationVector:
      return "Invalid initialization vector";
    case EmssAppendInvalidKeyId:
      return "Invalid key id";
    case EmssAppendInvalidMediaKeySession:
      return "Invalid media key session";
    case EmssAppendInvalidSubsampleDescription:
      return "Invalid subsample description";
    case EmssAppendUnknownDecryptionMode:
      return "Unknown decryption mode";
    case EmssMediaKeyInvalidConfiguration:
      return "Invalid Media Key configuration";
    case EmssMediaKeySessionNotUpdated:
      return "Media key session not updated";
    case EmssVideoDecoderInvalidTrackType:
      return "Invalid track type";
    case EmssVideoDecoderInvalidVideoTexture:
      return "Invalid video texture";
    case EmssVideoDecoderWebGlContextNotRegistered:
      return "WebGL context not registered";
    case EmssVideoDecoderNotInVideoTextureMode:
      return "Not in video texture mode";
    case EmssFailed:  // FALLTHROUGH
    default:
      return "Unknown error";
  }
}
}
