// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_

#include <cstddef>
#include <cstdint>

#include "samsung/wasm/common.h"

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
  /// before a seek and packets after a seek.
  /// <br>
  /// Session mechanism is meant to help working with seek. In a multithreaded
  /// application, it's expected to have a separate thread for packet
  /// appending. That thread may receive information about seek with some delay,
  /// and continue appending packets with old (pre-seek) PTSes. Such behaviour
  /// can cause all sorts of problems during seek.
  /// <br>
  /// Thanks to <code>session_id</code> mechanism backend can still receive
  /// pre-seek packets and continue to drop them for as long as necessary.
  /// These appends return errors, but it's okay to ignore them. The application
  /// should listen to
  /// <code>ElementaryMediaTrackListener::OnSessionIdChanged</code> and append
  /// post-seek packets with new session_id after this event fired.
  ///
  /// @sa ElementaryMediaTrackListener::OnSessionIdChanged
  uint32_t session_id;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_PACKET_H_
