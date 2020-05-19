// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_

#include "samsung/wasm/common.h"

namespace samsung {
namespace wasm {

/// An interface to receive updates of <code>ElementaryMediaStreamSource</code>.
/// Object implementing this interface needs to be bound to
/// <code>ElementaryMediaStreamSource::SetListener</code> method.
///
/// @sa ElementaryMediaStreamSource
class ElementaryMediaStreamSourceListener {
 public:
  virtual ~ElementaryMediaStreamSourceListener() = default;

  /// Called when associated EMSS object enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kDetached</code> state.
  virtual void OnSourceDetached() {}

  /// Called when associated EMSS object enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kClosed</code> state.
  virtual void OnSourceClosed() {}

  /// Called when associated EMSS object enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpenPending</code> state.
  virtual void OnSourceOpenPending() {}

  /// Called when associated EMSS object enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kOpen</code> state.
  virtual void OnSourceOpen() {}

  /// Called when associated EMSS object enters
  /// <code>ElementaryMediaStreamSource::ReadyState::kEnded</code> state.
  virtual void OnSourceEnded() {}

  /// Called when current playback position changes. This is preferred method
  /// of informing the app about playback position over
  /// <code>html::HTMLMediaElementListener::OnTimeUpdate</code>.
  ///
  /// @remarks
  /// If <code>EmssVersionInfo.has_legacy_emss</code> is <code>true</code> (API
  /// version 0 is used), this event behaves the same way as the <code>
  /// html::HTMLMediaElementListener::OnTimeUpdate()</code> event.
  ///
  /// @param[in] new_time New playback position.
  virtual void OnPlaybackPositionChanged(Seconds /*new_time*/) {}
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_
