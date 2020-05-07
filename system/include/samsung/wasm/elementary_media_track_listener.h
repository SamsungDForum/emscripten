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

/// An interface to receive updates of <code>ElementaryMediaTrack</code>.
/// Object implementing this interface needs to be bound to
/// <code>ElementaryMediaTrack::SetListener</code> method.
///
/// @sa ElementaryMediaTrack
class ElementaryMediaTrackListener {
 public:
  virtual ~ElementaryMediaTrackListener() = default;

  /// Fired when the track is ready to accept data.
  virtual void OnTrackOpen() {}

  /// Fired when associated source enters state that makes this track unable of
  /// accepting data. A reason for closing the track is passed as an argument.
  ///
  /// @param[in] close_reason The reason for closing this track.
  virtual void OnTrackClosed(ElementaryMediaTrack::CloseReason) {}

  /// Fired to indicate <code>currentTime</code> attribute of the associated
  /// <code>html::HTMLMediaElement</code> was changed. New playback time is
  /// delivered as an argument to the function.
  /// <br>
  /// Seek sequence:
  /// -# If track is open:
  ///    <code>ElementaryMediaTrackListener::OnTrackClosed</code> with reason
  ///    argument set to
  ///    <code>ElementaryMediaTrack::CloseReason::kTrackSeeking</code>.
  /// -# <code>ElementaryMediaTrackListener::OnSeek</code> with argument set to
  ///    a new playback time (this may fire multiple times if multiple seek
  ///    operations were performed in a close succession),
  /// -# <code>ElementaryMediaTrackListener::OnSessionIdChanged</code>
  ///    indicating start of a new session. Packets with the old session are
  ///    dropped in the backend. This event may also fire multiple times.
  /// -# If track was open prior seek operation:
  ///    <code>ElementaryMediaTrackListener::OnTrackOpen</code>.
  ///
  /// If associated <code>ElementaryMediaStreamSource</code> is in
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpen</code> state when
  /// seeking occurs, it will change it's state to
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpenPending</code> when
  /// above sequence is performed.
  /// <br>
  /// Please note this event will fire at other time than
  /// <code>html::HTMLMediaElement</code>'s seeking and seeked events and should
  /// be prioritized.
  ///
  /// @param[in] new_time Time to which the seek is being performed.
  virtual void OnSeek(Seconds /*new_time*/) {}

  /// Fired when id of the current session is changed, which happens during
  /// seek.
  /// <br>
  /// This event allows application to efficiently track sessions (as opposed
  /// to <code>ElementaryMediaTrack::GetSessionId</code>) and to differentiate
  /// packets before a seek (that should be dropped) and packets after a seek.
  /// Appending a packet with wrong
  /// <code>ElementaryMediaPacket::session_id</code> causes an error and the
  /// packet to be dropped.
  ///
  /// @param[in] session_id Id of new session.
  ///
  /// @sa ElementaryMediaPacket::session_id
  /// @sa ElementaryMediaTrackListener::OnSeek
  virtual void OnSessionIdChanged(uint32_t /*session_id*/) {}
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_TRACK_LISTENER_H_
