// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_
#define INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_

namespace samsung {
namespace wasm {

/// Enumerates possible outcomes of WASM function calls.
enum class OperationResult {
  /// An operation ended successfully.
  kSuccess = 0,

  /// The requested operation was called on an object which `IsValid()` property
  /// is `false`.
  kInvalidObject,

  /// The requested operation was called with an invalid argument.
  kInvalidArgument,

  /// Cannot perform requested operation in a current ready state.
  kInvalidState,

  /// A listener of the same type as the one passed as an argument is already
  /// assigned to this object.
  kListenerAlreadySet,

  /// A listener passed as an argument not assigned to this object.
  kNoSuchListener,

  /// Performing requested operation is not allowed.
  kNotAllowed,

  /// This functionality is not supported on this device.
  ///
  /// @remarks
  /// `EmssVersionInfo` contains information about `ElementaryMediaStreamSource`
  /// features available on this device.
  kNotSupported,

  /// The requested operation cannot be performed because player was already
  /// destroyed.
  kAlreadyDestroyed,

  /// The requested operation is already in progress and cannot be requested
  /// again before it is finished.
  kAlreadyInProgress,

  /// Cannot complete a state change, because a transition to the
  /// `ReadyState::kClosed` state is already in progress. This can happen when
  /// the state change request is made when `Close()` request is still being
  /// processed.
  kCloseInProgress,

  /// The requested operation is not allowed in the current
  /// `ElementaryMediaStreamSource::Mode`.
  kNotAllowedInCurrentMode,

  /// Cannot perform requested operation when no tracks are attached to the
  /// source.
  kNoTracksAttached,

  /// Cannot complete a state change, because a transition to the
  /// `ReadyState::kOpen` state is already in progress. This can happen when the
  /// state change request is made when `Open()` request is still being
  /// processed.
  kOpenInProgress,

  /// Cannot complete an Elementary Media Stream Source state change, because a
  /// playback state change is in progress. This can happen when
  /// `html::HTMLMediaElement` is processing a request that affects playback
  /// (e.g. seek is performed, playback is either started or paused, etc.).
  kPlaybackStateChangeInProgress,

  /// The requested operation can be executed only when
  /// `ElementaryMediaStreamSource` is in the `ReadyState::kClosed` state.
  kSourceMustBeClosed,

  /// Cannot perform the requested operation when `ElementaryMediaStreamSource`
  /// is not attached to `html::HTMLMediaElement`.
  kSourceNotAttached,

  /// Cannot set a duration value lower than the highest presentation timestamp
  /// of any `ElementaryMediaPacket` buffered so far.
  ///
  /// @remark
  /// `ElementaryMediaStreamSource::Flush()` can be used to clear buffered
  /// packets.
  kTimestampsExceedDuration,

  /// A maximum number of tracks of the given type is already assigned to
  /// `ElementaryMediaStreamSource`.
  kTrackLimitReached,

  /// The object on which the operation was called is not related to an object
  /// passed as an argument (e.g. another instance was used to create the passed
  /// object).
  kUnrelatedObject,

  /// The operation was aborted.
  kAborted,

  /// The operation failed due to an unspecified reason.
  kFailed,

  // Config verification errors:

  /// A provided channel layout is invalid.
  kConfigInvalidChannelLayout,

  /// A provided codec is invalid.
  kConfigInvalidCodec,

  /// A provided framerate is invalid.
  kConfigInvalidFramerate,

  /// A provided resolution is invalid.
  kConfigInvalidResolution,

  /// A provided mime type is invalid.
  kConfigInvalidMimeType,

  /// A provided sample format is invalid.
  kConfigInvalidSampleFormat,

  /// A provided config is invalid for an undetermined reason.
  kConfigInvalid,

  // Packet append errors:

  /// The append failed due to Platform's packet buffer overflow.
  ///
  /// @remarks
  /// * App is buffering ahead too many packets.
  /// * Since the packet was not accepted by `ElementaryMediaTrack`, it should
  ///   be sent again.
  kAppendBufferFull,

  /// The append failed because `ElementaryMediaTrack` expects a keyframe.
  ///
  /// @remark
  /// Sending a keyframe is *always* required when `ElementaryMediaTrack` opens.
  kAppendExpectsKeyframe,

  /// The append was ignored.
  ///
  /// @remark
  /// An append can be ignored when `session_id` changes but packets stamped
  /// with an old `SessionId` value are still being sent or processed. This is
  /// more of an information for App and usually shouldn't be treated as an
  /// error.
  kAppendIgnored,

  /// The append failed because packet has no duration.
  kAppendNoDuration,

  /// The append failed because packet has missing or negative dts.
  kAppendInvalidDts,

  /// The append failed because packet has missing or negative pts.
  kAppendInvalidPts,

  /// The append failed because `ElementaryMediaTrack` is not open.
  ///
  /// @sa `ElementaryMediaTrack::IsOpen()`
  kAppendInvalidTrackState,

  /// The append failed because either framerate or resolution provided is
  /// invalid or missing.
  kAppendInvalidVideoParameters,

  /// The append failed because packet has no data.
  kAppendNoPacketData,

  /// The append failed because shared memory creation failed or shared
  /// memory handle could not be obtained.
  kAppendResourceAllocationError,

  // Encrypted packet append errors:

  /// The append failed because encrypted packet decryption failed.
  kAppendDecryptionError,

  /// The append failed because decryptor needs more data to decrypt frame.
  kAppendDecryptorNeedsMoreData,

  /// The append failed because decryption key is not available.
  kAppendNoDecryptionKey,

  /// The append failed because encrypted packet has missing or bad
  /// initialization vector.
  kAppendInvalidInitializationVector,

  /// The append failed because encrypted packet has missing or bad key id.
  kAppendInvalidKeyId,

  /// The append failed because media key session is invalid.
  /// @sa `MediaKey`
  /// @sa `MediaKey::SetupEncryption()`
  /// @sa `MediaKey::IsValid()`
  kAppendInvalidMediaKeySession,

  /// The append failed because encrypted packet has missing or bad
  /// `EncryptedSubsampleDescription`.
  kAppendInvalidSubsampleDescription,

  /// The append failed because encrypted packet has missing or invalid
  /// `EncryptionMode`.
  kAppendUnknownDecryptionMode,

  // Media key errors:

  ///  Provided `DRMConfig` is invalid.
  kMediaKeyInvalidConfiguration,

  /// Attempt to update the session failed
  kMediaKeySessionNotUpdated,

  // Video decoder errors:

  /// The requested operation can be executed only on a certain track type.
  /// Video decoder related operations are available only for video tracks.
  kVideoDecoderInvalidTrackType,

  /// The requested operation failed because invalid video texture was provided.
  kVideoDecoderInvalidVideoTexture,

  /// The requested operation failed because WebGL rendering context is not
  /// registered.
  /// @sa `ElementaryMediaTrack::RegisterCurrentGraphicsContext()`
  kVideoDecoderWebGlContextNotRegistered,

  /// The requested operation failed because player is not set to
  /// `ElementaryMediaStreamSource::Mode::kVideoTexture`
  /// @sa `ElementaryMediaStreamSource::Mode`
  kVideoDecoderNotInVideoTextureMode,
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_
