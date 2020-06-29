// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_LISTENER_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_LISTENER_H_

#include <chrono>
#include <cstdint>

#include "samsung/wasm/common.h"
#include "samsung/wasm/elementary_media_track.h"

namespace samsung {
namespace wasm {

/// @brief
/// Allows receiving <code>ElementaryMediaTrack</code> events.
///
/// `ElementaryMediaTrack` events are delivered via this interface when a
/// listener is registered by `ElementaryMediaTrack::SetListener()`.
///
/// @sa `ElementaryMediaTrack`
class ElementaryMediaTrackListener {
 public:
  virtual ~ElementaryMediaTrackListener() = default;

  /// Fired when the track is ready to accept data.
  virtual void OnTrackOpen() {}

  /// Fired when an associated source enters a state that makes this track
  /// unable of accepting data. A reason for closing the track is passed as an
  /// argument.
  ///
  /// @param[in] close_reason A reason for closing this track.
  virtual void OnTrackClosed(ElementaryMediaTrack::CloseReason) {}

  /// Fired when an associated `html::HTMLMediaElement` is seeking. This is a
  /// result of either a call to `html::HTMLMediaElement::SetCurrentTime()` or
  /// direct user interaction with `HTMLMediaElement` with controls enabled. New
  /// playback time is delivered as an argument to this function.
  ///
  /// Seek sequence:
  /// -# If track is open:
  ///    `ElementaryMediaTrackListener::OnTrackClosed()` is fired with a reason
  ///    argument set to `ElementaryMediaTrack::CloseReason::kTrackSeeking`.
  /// -# `ElementaryMediaTrackListener::OnSessionIdChanged()` is fired
  ///    indicating the beginning of a new session. Packets with the old
  ///    `SessionId` are dropped by the backend. This may fire multiple times if
  ///    multiple seek operations were performed in a close succession
  /// -# `ElementaryMediaTrackListener::OnSeek()` is fired with an argument set
  ///    to a new playback time. This event may fire multiple times if multiple
  ///    seek operations were performed in a close succession.
  /// -# If track was open prior seek operation:
  ///    `ElementaryMediaTrackListener::OnTrackOpen()` is fired.
  ///
  /// If an associated `ElementaryMediaStreamSource` is in the
  /// `ElementaryMediaStreamSource::ReadyState::kOpen` state when seeking
  /// occurs, it will change it's state to
  /// `ElementaryMediaStreamSource::ReadyState::kOpenPending` for the duration
  /// of the sequence above.
  ///
  /// Please note this event doesn't fire at the same time that
  /// `html::HTMLMediaElement`'s `seeking` and `seeked` events. A source of
  /// media data should use this event to seek to the new playback position.
  ///
  /// @param[in] new_time A time to which the seek is being performed.
  ///
  /// @sa `SessionId`
  virtual void OnSeek(Seconds /*new_time*/) {}

  /// Fired when id of the current session is changed, which happens when track
  /// is closed.
  ///
  /// @remarks
  /// This event allows application to efficiently track sessions (as opposed
  /// to `ElementaryMediaTrack::GetSessionId()`, which should be used only
  /// to obtain an initial value of `session_id`).
  ///
  /// @param[in] session_id Id of new session.
  ///
  /// @sa `SessionId`
  /// @sa `ElementaryMediaPacket::session_id`
  /// @sa `ElementaryMediaTrackListener::OnSeek()`
  virtual void OnSessionIdChanged(SessionId /*session_id*/) {}

  /// Fired when one of async append methods fail:
  /// * `ElementaryMediaTrack::AppendPacketAsync()`
  /// * `ElementaryMediaTrack::AppendEncryptedPacketAsync()`
  /// * `ElementaryMediaTrack::AppendEndOfTrackAsync()`
  /// A code identifying an error is passed as an argument.
  ///
  /// @param[in] operation_result Error code representing append error.
  virtual void OnAppendError(OperationResult /*operation_result*/) {}
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_LISTENER_H_
