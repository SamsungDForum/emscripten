// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_

#include <cstddef>
#include <cstdint>

#include "samsung/wasm/common.h"
#include "samsung/wasm/session_id.h"

namespace samsung {
namespace wasm {

/// Type representing a single packet (video or audio).
struct ElementaryMediaPacket {
  /// Presentation Timestamp, indicates time relative to the beginning of
  /// the stream when a packet must be rendered.
  Seconds pts;

  /// Decode Timestamp, indicates time relative to the beginning of the stream
  /// when a packet must be sent to the decoder.
  Seconds dts;

  /// Duration of the packet.
  Seconds duration;

  /// Whether the packet represents a key frame.
  bool is_key_frame;

  /// Size in bytes of packet data.
  size_t data_size;

  /// Base address of buffer containing data of the packet.
  const void* data;

  /// Width of video frame in pixels, used to perform resolution change.
  /// Unused in audio packets. This parameter is optional, value 0 means
  /// it's empty and no resolution change is being performed.
  uint32_t width;

  /// Height of video frame in pixels, used to perform resolution change.
  /// Unused in audio packets. This parameter is optional, value 0 means
  /// it's empty and no resolution change is being performed.
  uint32_t height;

  /// Framerate numerator, used to perform framerate change. Unused in audio
  /// packets. This parameter is optional, although must be set if
  /// <code>ElementaryMediaPacket::framerate_den</code> is set. Value 0 means
  /// it's empty and no framerate change is being performed.
  uint32_t framerate_num;

  /// Framerate denominator, used to perform framerate change. Unused in audio
  /// packets. This parameter is optional, although it must be set if
  /// <code>ElementaryMediaPacket::framerate_num</code> is set. Value 0 means
  /// it's empty and no framerate change is being performed.
  uint32_t framerate_den;

  /// Id of a session the packet belongs to. Used to differentiate packets
  /// sent to @ref ElementaryMediaTrack before it closes and after it reopens.
  /// This is useful for multithreaded Apps in some playback scenarios (e.g when
  /// seeking or App multitasking happens).
  ///
  /// @remarks
  /// When a packet with an old <code>session_id</code> value is sent/processed
  /// by backend, it will be ignored. Such appends return errors, but it's okay
  /// to ignore them.
  ///
  /// @remarks
  /// The application should listen to
  /// @ref ElementaryMediaTrackListener::OnSessionIdChanged() and append
  /// post-open packets with a new session_id after this event fired.
  ///
  /// @remarks
  /// Apps that operate on a main thread only can ignore this mechanism. In
  /// such case, <code>session_id</code> should be set to @ref kIgnoreSessionId.
  ///
  /// @sa SessionId
  /// @sa ElementaryMediaTrack::GetSessionId()
  /// @sa ElementaryMediaTrackListener::OnSessionIdChanged()
  /// @sa ElementaryMediaTrackListener::OnTrackOpen()
  /// @sa ElementaryMediaTrackListener::OnTrackClose()
  SessionId session_id;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_
