// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_
#define INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_

namespace samsung {
namespace html {

/// An interface to receive updates of <code>HTMLMediaElement</code>. Object
/// implementing this interface needs to be bound to
/// <code>HTMLMediaElement::SetListener</code> method.
///
/// @sa HTMLMediaElement
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
};

}  // namespace html
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_LISTENER_H_
