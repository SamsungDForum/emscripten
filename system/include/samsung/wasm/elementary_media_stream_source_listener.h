// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_

#include "samsung/wasm/common.h"

namespace samsung {
namespace wasm {

/// @brief
/// Allows receiving `ElementaryMediaStreamSource` events.
///
/// `ElementaryMediaStreamSource` events are delivered via this interface when
/// a listener is registered by `ElementaryMediaStreamSource::SetListener()`.
///
/// @sa `ElementaryMediaStreamSource`
class ElementaryMediaStreamSourceListener {
 public:
  virtual ~ElementaryMediaStreamSourceListener() = default;

  /// Called when an associated source object enters the
  /// `ElementaryMediaStreamSource::ReadyState::kDetached` state.
  virtual void OnSourceDetached() {}

  /// Called when an associated source object enters the
  /// `ElementaryMediaStreamSource::ReadyState::kClosed` state.
  virtual void OnSourceClosed() {}

  /// Called when an associated source object enters the
  /// `ElementaryMediaStreamSource::ReadyState::kOpenPending` state.
  virtual void OnSourceOpenPending() {}

  /// Called when an associated source object enters the
  /// `ElementaryMediaStreamSource::ReadyState::kOpen` state.
  virtual void OnSourceOpen() {}

  /// Called when an associated source object enters the
  /// `ElementaryMediaStreamSource::ReadyState::kEnded` state.
  virtual void OnSourceEnded() {}

  /// Called when current playback position changes. This is the preferred
  /// method of receiving time updates and should be used instead of
  /// `html::HTMLMediaElementListener::OnTimeUpdate()`.
  ///
  /// @param[in] new_time New playback position.
  virtual void OnPlaybackPositionChanged(Seconds /*new_time*/) {}

  /// This event is emitted immediately after VBI closed captions data is
  /// detected and read from a video stream. `closed_captions` contain raw VBI
  /// data. It must be decoded and displayed by the application when it
  /// receives this event.
  ///
  /// @param[in] closed_captions Pointer to array with processed subtitles.
  /// @param[in] captions_length Length of processed subtitles array.
  /// @remarks
  /// An ownership of `closed_captions` is not transferred and is valid only for
  /// the duration of the `OnClosedCaptions()` call. Do not remove this array
  /// manually!
  virtual void OnClosedCaptions(const uint8_t* /*closed_captions*/,
                                size_t /*captions_length*/) {}
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_LISTENER_H_
