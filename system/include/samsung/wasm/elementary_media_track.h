// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_

#include <cstdint>

#include "samsung/wasm/common.h"
#include "samsung/wasm/operation_result.h"

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

  /// Default constructor, creates an <b>invalid</b>
  /// <code>ElementaryMediaTrack</code> object, to be further replaced with a
  /// proper one, received with a call to
  /// <code>ElementaryMediaStreamSource::AddTrack</code>.
  ElementaryMediaTrack();
  ElementaryMediaTrack(const ElementaryMediaTrack&) = delete;
  ElementaryMediaTrack(ElementaryMediaTrack&&);
  ElementaryMediaTrack& operator=(const ElementaryMediaTrack&) = delete;
  ElementaryMediaTrack& operator=(ElementaryMediaTrack&&);
  ~ElementaryMediaTrack();

  /// Returns <code>true</code> if track instance is valid. This method should
  /// be called after a call to
  /// <code>ElementaryMediaStreamSource::AddTrack</code>
  /// to ensure backend initialized the object properly. If track is invalid
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
  Result<void> AppendEndOfTrack(uint32_t session_id);

  /// Sets a listener to receive updates about this track's state changes. Only
  /// one listener can be set, setting another listner causes an error.
  ///
  /// @param[in] listener Listener to be set.
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

  /// Returns id of the current active session. This should be used sparingly,
  /// because it blocks the backend. For updates on session id
  /// using <code>ElementaryMediaTrackListener::OnSessionIdChanged</code> is the
  /// recommended way.
  ///
  /// @return <code>Result\<::Seconds\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>uint32_t</code> identifying current session
  /// on success, otherwise a code describing the error.
  ///
  /// @sa ElementaryMediaPacket::session_id
  /// @sa ElementaryMediaTrackListener::OnSessionIdChanged
  Result<uint32_t> GetSessionId() const;

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
 private:
  explicit ElementaryMediaTrack(int handle);

  int handle_;

  // access to handle_
  friend class ElementaryMediaStreamSource;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_H_
