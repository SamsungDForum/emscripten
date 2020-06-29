// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_SESSION_ID_H_
#define INCLUDE_SAMSUNG_WASM_SESSION_ID_H_

#include <cstdint>

#include "samsung/wasm/common.h"
#include "samsung/wasm/operation_result.h"

namespace samsung {
namespace wasm {

/// A *session* starts when track opens and lasts until it closes. All packets
/// sent between those two events belong to a single session. When appending
/// either a packet or an end of track to `ElementaryMediaTrack`, a
/// multithreaded App must mark them with the current `session_id` value.
///
/// @sa `ElementaryMediaPacket::session_id`
/// @sa `ElementaryMediaTrack::GetSessionId()`
/// @sa `ElementaryMediaTrackListener::OnSessionIdChanged()`
using SessionId = int32_t;

/// This should be passed as `ElementaryMediaPacket::session_id` when session
/// mechanism is not used (i.e. App appends packets on the main thread only).
extern const SessionId kIgnoreSessionId;

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_SESSION_ID_H_
