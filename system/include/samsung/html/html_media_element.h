// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_H_
#define INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_H_

#include <functional>
#include <string>

#include "samsung/wasm/common.h"
#include "samsung/wasm/operation_result.h"

namespace samsung {

namespace wasm {

class ElementaryMediaStreamSource;

}  // namespace wasm

namespace html {

class HTMLMediaElementListener;

/// <code>HTMLMediaElement</code> is used with EMSS as a playback control
/// element, providing operations like play, pause, seek, etc. That is,
/// <code>HTMLMediaElement</code> controls Media Player.
/// <br>
/// <code>HTMLMediaElement</code> is associated with either \<audio\> or
/// \<video\> tag in HTML, allowing to position playback area. Relevant part of
/// <code>%HTMLMediaElement</code> WebAPI is wrapped by a below class.
/// <br>
/// When operating Media Player, App should rely on
/// <code>HTMLMediaElement</code> events and methods. For example,
/// <code>wasm::ElementaryMediaStreamSource</code> will signal when Media Player
/// requires media data. However, the moment Media Player starts reading media
/// data is not always the very same moment a playback can be started. Readiness
/// for playback will be signalized by <code>HTMLMediaElement</code> by the
/// means of <code>HTMLMediaElementListener::OnCanPlay()</code> event.
///
/// @sa
/// <a href="https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement">
/// %HTMLMediaElement documentation on MDN
/// </a>
class HTMLMediaElement final {
 public:
  enum class ReadyState {
    kHaveNothing,
    kHaveMetadata,
    kHaveCurrentData,
    kHaveFutureData,
    kHaveEnoughData,
  };
  enum class AsyncResult {
    kSuccess,
    kNotAllowedError,
    kNotSupportedError,
    kUnknownError,
  };
  /// Constructs <code>HTMLMediaElement</code> corresponding to an HTML element
  /// with a given id. Provided element must exist, otherwise object will be
  /// ill-constructed.
  ///
  /// @param[in] id Id of either \<audio\> or \<video\> HTML element.
  explicit HTMLMediaElement(const char* id);
  HTMLMediaElement(const HTMLMediaElement&) = delete;
  HTMLMediaElement(HTMLMediaElement&&);
  HTMLMediaElement& operator=(const HTMLMediaElement&) = delete;
  HTMLMediaElement& operator=(HTMLMediaElement&&);
  ~HTMLMediaElement();

  /// Returns <code>true</code> if this instance is valid. This method should
  /// be called after constructor to ensure backend initialized the object
  /// properly. If object is invalid all method calls will fail.
  ///
  /// @return <code>true</code> if this instance is valid, otherwise
  /// <code>false</code>.
  bool IsValid() const;

  wasm::Result<bool> IsAutoplay() const;
  wasm::Result<void> SetAutoplay(bool new_autoplay);

  wasm::Result<wasm::Seconds> GetCurrentTime() const;
  wasm::Result<void> SetCurrentTime(wasm::Seconds new_time);

  wasm::Result<wasm::Seconds> GetDuration() const;
  wasm::Result<bool> IsEnded() const;

  wasm::Result<bool> IsLoop() const;
  wasm::Result<void> SetLoop(bool new_loop);

  wasm::Result<bool> IsPaused() const;

  wasm::Result<ReadyState> GetReadyState() const;

  wasm::Result<std::string> GetSrc() const;

  /// Sets <code>wasm::ElementaryMediaStreamSource</code> object as the current
  /// source of the playback. This is equivalent of
  /// @code{.js}
  /// mediaElement.src = URL.createObjectURL(elementaryMediaStreamSource);
  /// @endcode
  /// in JS. URL is mantained by wasm::ElementaryMediaStreamSource and it is not
  /// necessary to revoke it manually.
  ///
  /// @warning This method doesn't take ownership of
  /// <code>wasm::ElementaryMediaStreamSource</code> object and it is imperative
  /// that the underlying HTML object of <code>HTMLMediaElement</code> outlives
  /// the source.
  ///
  /// @param[in] source New source to be set.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  wasm::Result<void> SetSrc(wasm::ElementaryMediaStreamSource* source);

  wasm::Result<void> Play(
      std::function<void(AsyncResult)> finished_callback);
  wasm::Result<void> Pause();

  /// Sets a listener to receive updates about HTMLMediaElement. Only one
  /// listener can be set, setting another listner causes an error.
  ///
  /// @param[in] listener Listener to be set.
  ///
  /// @warning The ownership isn't transferred, and, as such,
  /// the listener must outlive the source.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @sa HTMLMediaElementListener
  wasm::Result<void> SetListener(HTMLMediaElementListener* listener);

 private:
  int handle_;
};

}  // namespace html
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_H_
