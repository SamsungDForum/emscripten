// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_

#include <cstdint>
#include <functional>
#include <memory>

#include "GLES/gl.h"
#include "samsung/wasm/common.h"
#include "samsung/wasm/emss_version_info.h"
#include "samsung/wasm/operation_result.h"
#include "samsung/wasm/session_id.h"

namespace samsung {
namespace wasm {

class ElementaryMediaTrackListener;
class MediaKey;
struct ElementaryMediaPacket;
struct EncryptedElementaryMediaPacket;

/// @brief
/// Tracks are used to deliver either audio or video frames to WASM Player.
///
/// Each instance of this class represents a single elementary media track
/// (either audio or video). The track object allows sending
/// `ElementaryMediaPacket`s to platform for a playback.
///
/// Valid track objects can only be obtained through a call to
/// `ElementaryMediaStreamSource::AddTrack()`.
class ElementaryMediaTrack final {
 public:
  /// Enumerates track close reasons. Values of this enum are passed to
  /// `ElementaryMediaTrackListener::OnTrackClosed()` to inform about
  /// the reason of the close.
  enum class CloseReason {
    /// `ElementaryMediaStreamSource` state changed to
    /// `ElementaryMediaStreamSource::ReadyState::kClosed`.
    kSourceClosed,

    /// Source was closed due to an error.
    kSourceError,

    /// Source was detached from `html::HTMLMediaElement`.
    kSourceDetached,

    /// This `ElementaryMediaTrack` has been disabled.
    kTrackDisabled,

    /// This `ElementaryMediaTrack` has ended.
    kTrackEnded,

    /// This `ElementaryMediaTrack` has started seeking.
    kTrackSeeking,

    /// Track has closed due to an unspecified error; generally, this shouldn't
    /// happen.
    kUnknown,
  };

  /// Enumerates possible data decoding modes. Can be obtained by
  /// `GetActiveDecodingMode()` to check what decoding mode is selected for a
  /// particular track.
  enum class ActiveDecodingMode {
    /// Track is using platform hardware decoder.
    kHardware,
    /// Track is using platform software decoder.
    kSoftware
  };

  /// Enumerates track types. Can be obtained by `GetType()`.
  enum class TrackType {
    /// This is an audio track.
    kAudio,
    /// This is a video track.
    kVideo,
    /// Unknown track type, usually a result of track being invalid (i.e.
    /// `IsValid()` is `false`).
    kUnknown,
  };

  /// Default constructor, creates an *invalid* `ElementaryMediaTrack` object.
  /// It can be further replaced with a proper one, received with a call to
  /// `ElementaryMediaStreamSource::AddTrack()`.
  ElementaryMediaTrack();
  ~ElementaryMediaTrack();

  ElementaryMediaTrack(const ElementaryMediaTrack&) = delete;
  ElementaryMediaTrack& operator=(const ElementaryMediaTrack&) = delete;

  ElementaryMediaTrack(ElementaryMediaTrack&&);
  ElementaryMediaTrack& operator=(ElementaryMediaTrack&&);

  /// Returns `true` if the track instance is valid. All methods calls on an
  /// invalid track will fail.
  ///
  /// @return `true` if track instance is valid, otherwise `false`.
  bool IsValid() const;

  /// Returns a `TrackType` of this track.
  TrackType GetType() const;

  /// Appends a given `ElementaryMediaPacket` to the track.
  ///
  /// @remarks
  /// * `AppendPacket()` cannot be called on the main thread.
  /// * `AppendPacket()` and `AppendPacketAsync()` calls for the same track can
  ///    be mixed.
  ///
  /// @param[in] packet A packet to append.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success,  otherwise a code describing the
  /// error.
  Result<void> AppendPacket(const ElementaryMediaPacket& packet);

  /// Appends a given `ElementaryMediaPacket` to the track asynchronously.
  ///
  /// For clear packets, `AppendPacketAsync()` is functionally equivalent to
  /// `AppendPacket()` (i.e. it will validate the packet and return result
  /// synchronously).
  ///
  /// @remarks
  /// * `AppendPacketAsync()` can be called both on the main thread and on side
  ///   threads.
  /// * `AppendPacket()` and `AppendPacketAsync()` calls for the same track can
  ///   be mixed.
  ///
  /// @param[in] packet A packet to append.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` if packet validation and append to track was
  /// successful, otherwise a code describing the error.
  Result<void> AppendPacketAsync(const ElementaryMediaPacket& packet);

  /// Appends a given `EncryptedElementaryMediaPacket` to the track.
  ///
  /// @remarks
  /// * It is recommended to use `AppendEncryptedPacketAsync()` method to append
  ///   encrypted packets over this method due to performance reasons
  ///   (decrypting packets takes some time, doing it synchronously may decrease
  ///   performance).
  /// * `AppendEncryptedPacket()` cannot be called on the main thread.
  /// * `AppendEncryptedPacket()` and `AppendEncryptedPacketAsync()` calls for
  ///    the same track can be mixed.
  ///
  /// @param[in] packet A packet to append.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> AppendEncryptedPacket(const EncryptedElementaryMediaPacket&);

  /// Appends a given `EncryptedElementaryMediaPacket` to the track, but
  /// decrypts it asynchronously.
  ///
  /// `AppendEncryptedPacketAsync()` will validate the packet and return result
  /// synchronously. However, packet decryption will be executed asynchronously.
  /// If decryption error occurs, it will be signaled via
  /// `ElementaryMediaTrackListener::OnAppendError()` event.
  ///
  /// @remarks
  /// * It is recommended to use this method to append encrypted packets over
  ///   `AppendEncryptedPacket()` due to performance reasons (decrypting packets
  ///   takes some time, doing it asynchronously will improve performance).
  /// * `AppendEncryptedPacketAsync()` can be called both on the main thread and
  ///   on side threads.
  /// * `AppendEncryptedPacket()` and `AppendEncryptedPacketAsync()` calls for
  ///   the same track can be mixed.
  ///
  /// @param[in] packet A packet to append.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` if packet validation and append to track was
  /// successful, otherwise a code describing the error.
  Result<void> AppendEncryptedPacketAsync(
      const EncryptedElementaryMediaPacket&);

  /// Appends a special end-of-track packet to the source.
  ///
  /// Upon processing this packet, the track will end. It is advised to end all
  /// tracks at a similar time. Operation will end once end of track is queued
  /// in Media Player's packet buffer.
  ///
  /// A track that has ended will close and therefore emit the
  /// `ElementaryMediaTrackListener::OnTrackClosed()` event. When tracks
  /// associated with `ElementaryMediaStreamSource` end, the source changes it's
  /// state to `ElementaryMediaStreamSource::ReadyState::kEnded`.
  ///
  /// @remark
  /// `AppendEndOfTrack()` cannot be called on the main thread.
  ///
  /// @param[in] session_id Id of the session the end of track packet should
  /// belong to.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> AppendEndOfTrack(SessionId session_id);

  /// Appends a special end-of-track packet to the source asynchronously.
  ///
  /// Upon processing this packet, the track will end. It is advised to end
  /// all tracks at a similar time.
  ///
  /// `AppendEndOfTrackAsync()` returns result synchronously when track starts
  /// closing or an error occurs.
  ///
  /// If `AppendEndOfTrackAsync()` returns success synchronously but if in the
  /// meantime `SessionId` changes or seek operation starts, track will not be
  /// closed and an error informing that end of track append is aborted will be
  /// signaled via `ElementaryMediaTrackListener::OnAppendError()` event.
  ///
  /// A track that has ended will close and therefore emit the
  /// `ElementaryMediaTrackListener::OnTrackClosed()` event. When tracks
  /// associated with `ElementaryMediaStreamSource` end, the source changes it's
  /// state to `ElementaryMediaStreamSource::ReadyState::kEnded`.
  ///
  /// @remark
  /// `AppendEndOfTrackAsync()` can be called both on the main thread and on
  /// side threads.
  ///
  /// @param[in] session_id Id of the session the end of track packet should
  /// belong to.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> AppendEndOfTrackAsync(SessionId session_id);

  /// Fills a provided texture with a decoded video frame.
  ///
  /// The texture should be rendered as soon as possible after it's received.
  /// Player will resolve `finished_callback` when playback time reaches the
  /// point when a frame associated with the texture should be displayed.
  ///
  /// Player will decode frames sent with `ElementaryMediaTrack::AppendPacket()`
  /// but won't render them on `HTMLMediaElement` when
  /// `ElementaryMediaStreamSource` is in the
  /// `ElementaryMediaStreamSource::Mode::kVideoTexture` mode. Instead, their
  /// contents can be accessed by calling this method repeatedly.
  ///
  /// @remarks
  /// * When `texture_id` is processed, it must be freed with
  ///   `ElementaryMediaTrack::RecycleTexture()`.
  /// * Sets the texture to the `GL_TEXTURE_EXTERNAL_OES` type.
  /// * This mode is supported only on devices which have
  ///   `EmssVersionInfo::has_video_texture` set to `true`.
  ///
  /// @warning
  /// * Can be called only on the *main* thread.
  /// * Can only be called in the
  ///   `ElementaryMediaStreamSource::Mode::kVideoTexture` mode of
  ///   `ElementaryMediaStreamSource`.
  /// * Valid only for video tracks.
  ///
  /// @param texture_id A texture that will be filled with video frame.
  ///
  /// @param finished_callback A callback which will be called when `texture_id`
  /// is ready and should be rendered by App.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `ElementaryMediaTrack::RegisterCurrentGraphicsContext()`
  /// @sa `ElementaryMediaTrack::RecycleTexture()`
  Result<void> FillTextureWithNextFrame(
      GLuint texture_id,
      std::function<void(OperationResult)> finished_callback);

  /// Fills a provided texture with a decoded video frame synchronously. This
  /// method blocks until texture is available and assigned to `texture_id`.
  ///
  /// The texture should be rendered as soon as possible after it's received.
  ///
  /// Player will decode frames sent with `ElementaryMediaTrack::AppendPacket()`
  /// but won't render them on `HTMLMediaElement` when
  /// `ElementaryMediaStreamSource` is in the
  /// `ElementaryMediaStreamSource::Mode::kVideoTexture` mode. Instead, their
  /// contents can be accessed by calling this method repeatedly.
  ///
  /// @remarks
  /// * When `texture_id` is processed, it must be freed with
  ///   `ElementaryMediaTrack::RecycleTexture()`.
  /// * Sets the texture to the `GL_TEXTURE_EXTERNAL_OES` type.
  /// * This mode is supported only on devices which have
  ///   `EmssVersionInfo::has_video_texture` set to `true`.
  ///
  /// @warning
  /// * This method may not return instantly if WASM Player's internal decoded
  ///   frame queue is empty. This method will block until a decoded frame is
  ///   available and as a blocking method it *cannot* be called on the main
  ///   thread.
  /// * Can only be called in the
  ///   `ElementaryMediaStreamSource::Mode::kVideoTexture` mode of
  ///   `ElementaryMediaStreamSource`.
  /// * Valid only for video tracks.
  ///
  /// @param texture_id A texture that will be filled with video frame.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `ElementaryMediaTrack::RegisterCurrentGraphicsContext()`
  /// @sa `ElementaryMediaTrack::RecycleTexture()`
  Result<void> FillTextureWithNextFrameSync(GLuint texture_id);

  /// Returns decoder mode used for track.
  ///
  /// @return `Result<::ActiveDecodingMode>` with the `operation_result` field
  /// set to `OperationResult::kSuccess` and a valid `ActiveDecodingMode`
  /// identifying the active decoding mode, otherwise a code describing an
  /// error.
  ///
  /// @sa `ActiveDecodingMode`
  Result<ActiveDecodingMode> GetActiveDecodingMode() const;

  /// Returns id of the currently active session.
  ///
  /// @remarks
  /// This should be used sparingly, because calling this method can be slow.
  /// It's recommended to obtain an initial value of `session_id` using
  /// `GetSessionId()` and receive further updates with the
  /// `ElementaryMediaTrackListener::OnSessionIdChanged()` event.
  ///
  /// @return `Result<::SessionId>` with the `operation_result` field set to
  /// `OperationResult::kSuccess` and a valid `SessionId` identifying the
  /// current session on a success, otherwise a code describing an error.
  ///
  /// @sa `SessionId`
  /// @sa `ElementaryMediaPacket::session_id`
  /// @sa `ElementaryMediaTrackListener::OnSessionIdChanged`
  Result<SessionId> GetSessionId() const;

  /// Returns the current state of this track.
  ///
  /// An open track can accept `ElementaryMediaPacket` objects. Tracks open
  /// just before source enters `ElementaryMediaStreamSource::ReadyState::kOpen`
  /// state.
  ///
  /// A closed track can't accept `ElementaryMediaPacket` objects. Tracks close
  /// just after source leaves `ElementaryMediaStreamSource::ReadyState::kOpen`
  /// state.
  ///
  /// @return `Result<::Seconds>` with `operation_result` field set to
  /// `OperationResult::kSuccess` and `true` if the track is open, otherwise
  /// `false` on success or a code describing the error.
  Result<bool> IsOpen() const;

  /// Release decoder buffers associated with the texture with `texture_id`.
  /// Should be called after painting the frame has been completed, as number of
  /// frames App can request simultaneously is limited by Platform.
  ///
  /// @remark
  /// This mode is supported only on devices which have
  /// `EmssVersionInfo::has_video_texture` set to `true`.
  ///
  /// @warning
  /// * Can only be called in the
  ///   `ElementaryMediaStreamSource::Mode::kVideoTexture` mode of
  ///   `ElementaryMediaStreamSource`.
  /// * Valid only for video track.
  /// * Regular canvas is not available to worker contexts - when using it,
  ///   method has to be called on main thread.
  /// * Offscreen canvas is available to both: window and worker contexts,
  ///   in such case method can be called on any thread.
  ///
  /// @param texture_id A texture that will be recycled.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `ElementaryMediaTrack::FillTextureWithNextFrame()`
  /// @sa `ElementaryMediaTrack::RegisterCurrentGraphicsContext()`
  Result<void> RecycleTexture(GLuint texture_id);

  /// Binds Player with an OpenGL graphics context associated with this WASM
  /// module.
  ///
  /// Must be called before the
  /// `ElementaryMediaTrack::FillTextureWithNextFrame()` method is called for
  /// the first time.
  ///
  /// @remark
  /// This mode is supported only on devices which have
  /// `EmssVersionInfo::has_video_texture` set to `true`.
  ///
  /// @warning
  /// * Bind current graphic context with OpenGLES first. Otherwise no action
  ///   will be performed.
  /// * Can only be called in the
  ///   `ElementaryMediaStreamSource::Mode::kVideoTexture` mode of
  ///   `ElementaryMediaStreamSource`.
  /// * Valid only for video track.
  /// * Regular canvas is not available to worker contexts - when using it,
  ///   method has to be called on main thread.
  /// * Offscreen canvas is available to both: window and worker contexts,
  ///   in such case method can be called on any thread.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `ElementaryMediaTrack::FillTextureWithNextFrame()`
  /// @sa `ElementaryMediaTrack::RecycleTexture()`

  Result<void> RegisterCurrentGraphicsContext();

  /// Sets media keys used for decrypting packets in this track.
  ///
  /// @param[in] key A `MediaKey` to be used by this track.
  ///
  /// @warning The ownership isn't transferred, and, as such, the key must
  /// outlive the track.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `MediaKey`
  Result<void> SetMediaKey(MediaKey* key);

  /// Sets a listener to receive updates about this track's state changes. Only
  /// one listener can be set: setting another clears the previous one. Pass
  /// `nullptr` to reset the listener.
  ///
  /// @param[in] listener Listener to be set or `nullptr` to unset the listener.
  ///
  /// @warning The ownership isn't transferred, and, as such, the listener must
  /// outlive the track.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `ElementaryMediaTrackListener`
  Result<void> SetListener(ElementaryMediaTrackListener* listener);

 private:
  class Impl;

  explicit ElementaryMediaTrack(int handle,
                                TrackType type,
                                EmssVersionInfo version_info,
                                bool use_session_id_emulation);

  int GetHandle() const;

  std::unique_ptr<Impl> pimpl_;

  // access to GetHandle()
  friend class ElementaryMediaStreamSource;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_
