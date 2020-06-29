// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_
#define INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_

#include "samsung/html/common.h"

namespace samsung {
namespace html {

/// @brief
/// Allows receiving `HTMLMediaElement` events.
///

/// `HTMLMediaElement` events are delivered via this interface when a listener
/// is registered by `HTMLMediaElement::SetListener()`.
///
/// @sa `HTMLMediaElement`
class HTMLMediaElementListener {
 public:
  virtual ~HTMLMediaElementListener() = default;
  virtual void OnPlaying() {}
  virtual void OnTimeUpdate() {}
  virtual void OnLoadStart() {}
  virtual void OnLoadedMetadata() {}
  virtual void OnLoadedData() {}
  virtual void OnCanPlay() {}
  virtual void OnCanPlayThrough() {}
  virtual void OnEnded() {}
  virtual void OnPlay() {}
  virtual void OnSeeking() {}
  virtual void OnSeeked() {}
  virtual void OnPause() {}
  virtual void OnWaiting() {}

  /// @remarks
  /// An ownership of `error_msg` is not transferred and is valid only for the
  /// duration of the `OnError()` call. Do not remove this string manually!
  virtual void OnError(MediaError, const char* /*error_msg*/) {}
};

}  // namespace html
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_
