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

/// Each instance of this class represents a single elementary media track
/// (either audio or video). The track object allows sending
/// <code>ElementaryMediaPacket</code>s to platform for a playback.
/// <br>
/// Valid track objects can only be obtained through a call to
/// <code>ElementaryMediaStreamSource::AddTrack</code>.
class ElementaryMediaTrack final {
 public:
  /// Enumerates track close reasons. Values of this enum are passed to
  /// <code>ElementaryMediaTrackListener::OnTrackClosed</code> to inform about
  /// the reason of the close.
  enum class CloseReason {
    /// <code>ElementaryMediaStreamSource</code> state chaned to
    /// <code>ElementaryMediaStreamSource::ReadyState::kClosed</code>.
    kSourceClosed,

    /// Source was closed due to an error.
    kSourceError,

    /// Source was detached from <code>html::HTMLMediaElement</code>.
    kSourceDetached,

    /// This <code>ElementaryMediaTrack</code> was disabled.
    kTrackDisabled,

    /// This <code>ElementaryMediaTrack</code> has ended.
    kTrackEnded,

    /// This <code>ElementaryMediaTrack</code> is seeking.
    kTrackSeeking,

    /// Track has closed due to an unspecified error; generally, this shouldn't
    /// happen.
    kUnknown,
  };

  enum class AsyncResult {
    kSuccess,
    kAlreadyDestroyedError,
    kWebGLContextNotRegistedError,
    kAlreadyInProgressError,
    kInvalidDataError,
    kNotSupportedError,
    kUnknownError,
  };

  /// Default constructor, creates an <b>invalid</b>
  /// <code>ElementaryMediaTrack</code> object, to be further replaced with
  /// a proper one, received with a call to
  /// <code>ElementaryMediaStreamSource::AddTrack()</code>.
  ElementaryMediaTrack();
  ~ElementaryMediaTrack();

  ElementaryMediaTrack(const ElementaryMediaTrack&) = delete;
  ElementaryMediaTrack& operator=(const ElementaryMediaTrack&) = delete;

  ElementaryMediaTrack(ElementaryMediaTrack&&);
  ElementaryMediaTrack& operator=(ElementaryMediaTrack&&);

  /// Returns <code>true</code> if track instance is valid. If track is invalid
  /// all method calls will fail.
  ///
  /// @return <code>true</code> if track instance is valid, otherwise
  /// <code>false</code>.
  bool IsValid() const;

  /// Appends given <code>ElementaryMediaPacket</code> to the track.
  ///
  /// @param[in] packet Packet to append.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> AppendPacket(const ElementaryMediaPacket& packet);

  /// Appends given <code>EncryptedElementaryMediaPacket</code> to the track.
  ///
  /// @param[in] packet Packet to append.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> AppendEncryptedPacket(const EncryptedElementaryMediaPacket&);

  /// Appends special end-of-track packet to the source. Upon processing this
  /// packet, the track will end. It is advised to end all tracks at a similar
  /// time.
  ///
  /// @param[in] session_id Id of the session the end of track packet should
  /// belong to.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> AppendEndOfTrack(SessionId session_id);

  /// Fills provided texture with a decoded video frame.
  /// Player will decode frames sent with
  /// <code>ElementaryMediaTrack::AppendPacket</code>, but won't render them
  /// when <code>ElementaryMediaStreamSource</code> is in
  /// <code>ElementaryMediaStreamSource::Mode::kVideoTexture</code> mode.
  /// Instead, their contents can be accessed by calling this method
  /// repeatedly.
  ///
  /// @remarks
  /// When <code>texture_id</code> is processed,
  /// it must be freed with <code>ElementaryMediaTrack::RecycleTexture</code>.
  ///
  /// @remarks
  /// Sets texture to type <code>GL_TEXTURE_EXTERNAL_OES</code>.
  ///
  /// @param texture_id A texture that will be filled with video frame.
  ///
  /// @param finished_callback A callback which will be called when
  /// <code>texture_id</code> is ready and should be rendered by App.
  ///
  /// @warning Can only be called in the
  /// <code>ElementaryMediaStreamSource::Mode::kVideoTexture</code> mode of
  /// <code>ElementaryMediaStreamSource</code>.
  /// Valid only for video track.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code>
  /// on success, otherwise a code describing the error.
  ///
  /// @sa <code>ElementaryMediaTrack::RecycleTexture</code>
  Result<void> FillTextureWithNextFrame(
      GLuint texture_id,
      std::function<void(AsyncResult)> finished_callback);

  /// Returns id of the currently active session.
  ///
  /// @remarks
  /// This should be used sparingly, because calling this method can be slow.
  /// It's recommended to obtain an initial value of <code>session_id</code>
  /// using <code>GetSessionId()</code> and receive further updates with the
  /// @sa ElementaryMediaTrackListener::OnSessionIdChanged() event.
  ///
  /// @return <code>Result\<::SessionId\></code> with the <code>operation_result
  /// </code> field set to <code>OperationResult::kSuccess</code> and a valid
  /// <code>SessionId</code> identifying the current session on a success,
  /// otherwise a code describing an error.
  ///
  /// @sa SessionId
  /// @sa ElementaryMediaPacket::session_id
  /// @sa ElementaryMediaTrackListener::OnSessionIdChanged
  Result<SessionId> GetSessionId() const;

  /// Returns current state of this track.
  /// <br>
  /// Open track can accept <code>ElementaryMediaPacket</code> objects. Track
  /// will open just before source enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpen</code> state.
  /// <br>
  /// Closed track can't accept <code>ElementaryMediaPacket</code> objects.
  /// Track will close just after source leaves
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpen</code> state.
  ///
  /// @return <code>Result\<::Seconds\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and
  /// <code>true</code> if the track is open, otherwise <code>false</code>
  /// on success, or a code describing the error.
  Result<bool> IsOpen() const;

  /// Pass texture to platform to release decoder buffers for new frames.
  /// Should be called after painting the frame has been completed.
  ///
  /// @warning Can only be called in the
  /// <code>ElementaryMediaStreamSource::Mode::kVideoTexture</code> mode of
  /// <code>ElementaryMediaStreamSource</code>.
  /// Valid only for video track.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> RecycleTexture(GLuint textureId);

  /// Pass current graphics context to platform to perform binding of
  /// video frame content to Open GL textures passed in
  /// <code>ElementaryMediaTrack::FillTextureWithNextFrame</code> method.
  ///
  /// @warning Bind current graphic context with OpenGLES first.
  /// Otherwise no action will be performed.
  ///
  /// @warning Can only be called in the
  /// <code>ElementaryMediaStreamSource::Mode::kVideoTexture</code> mode of
  /// <code>ElementaryMediaStreamSource</code>.
  /// Valid only for video track.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> RegisterCurrentGraphicsContext();

  /// Sets media keys used for decrypting packets in this track.
  ///
  /// @param[in] key Key to be set.
  ///
  /// @warning The ownership isn't transferred, and, as such,
  /// the key must outlive the track.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @sa MediaKey
  Result<void> SetMediaKey(MediaKey* key);

  /// Sets a listener to receive updates about this track's state changes. Only
  /// one listener can be set: setting another clears the previous one. Pass
  /// <code>nullptr</code> to reset the listener.
  ///
  /// @param[in] listener Listener to be set or <code>nullptr</code> to unset
  /// the listener.
  ///
  /// @warning The ownership isn't transferred, and, as such,
  /// the listener must outlive the track.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @sa ElementaryMediaTrackListener
  Result<void> SetListener(ElementaryMediaTrackListener* listener);

 private:
  class Impl;

  explicit ElementaryMediaTrack(int handle,
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
