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
class ElementaryMediaStreamSourceListener;
enum class OperationResult;

}  // namespace wasm

namespace html {

class HTMLMediaElementListener;

/// @brief
/// Wraps `HTMLMediaElement` so that it can be used in WebAssembly code.
///
/// `HTMLMediaElement` is used with `wasm::ElementaryMediaStreamSource` and it
/// acts as a playback control element, providing operations like play, pause,
/// seek, etc. That is, `HTMLMediaElement` controls Media Player.
///
/// `HTMLMediaElement` is associated with either `<audio>` or `<video>` tag in
/// HTML, allowing to position playback area. Relevant part of
/// `HTMLMediaElement` WebAPI is wrapped by the class below.
///
/// @remarks
/// * App should rely on `HTMLMediaElement` events and methods when operating
///   Media Player. For example, `wasm::ElementaryMediaStreamSource` will signal
///   when Media Player requires media data. However, the moment Media Player
///   starts reading media data is not always the very same moment a playback
///   can be started. Readiness for playback will be signalized by
///   `HTMLMediaElement` by the means of `HTMLMediaElementListener::OnCanPlay()`
///   event.
/// * A *source* of media data should instead rely on events related to
///  `wasm::ElementaryMediaStreamSource`.
///
/// @sa
/// [HTMLMediaElement documentation on MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement)
class HTMLMediaElement final {
 public:
  enum class ReadyState {
    kHaveNothing,
    kHaveMetadata,
    kHaveCurrentData,
    kHaveFutureData,
    kHaveEnoughData,
  };

  /// Constructs `HTMLMediaElement` corresponding to a HTML element with a given
  /// id. Provided element must exist, otherwise object will be ill-constructed.
  ///
  /// @param[in] id Id of either `<audio>` or `<video>` HTML element.
  explicit HTMLMediaElement(const char* id);
  HTMLMediaElement(const HTMLMediaElement&) = delete;
  HTMLMediaElement(HTMLMediaElement&&);
  HTMLMediaElement& operator=(const HTMLMediaElement&) = delete;
  HTMLMediaElement& operator=(HTMLMediaElement&&);
  ~HTMLMediaElement();

  /// Returns `true` if this instance is valid. This method should be called
  /// after constructor to ensure the object was properly initialized. If object
  /// is invalid all method calls will fail.
  ///
  /// @return `true` if this instance is valid, otherwise `false`.
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

  bool HasSrc() const;

  /// Sets `wasm::ElementaryMediaStreamSource` object as the current source of
  /// playback data. This is equivalent of
  /// @code{.js}
  /// mediaElement.src = URL.createObjectURL(elementaryMediaStreamSource);
  /// @endcode
  /// in JS. URL is maintained by `wasm::ElementaryMediaStreamSource` and is not
  /// revoked manually.
  ///
  /// @warning This method doesn't take ownership of
  /// `wasm::ElementaryMediaStreamSource` object. It is imperative that the
  /// underlying HTML object (`HTMLMediaElement`) outlives
  /// `wasm::ElementaryMediaStreamSource`.
  ///
  /// @param[in] source New source to be set.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  wasm::Result<void> SetSrc(wasm::ElementaryMediaStreamSource* source);

  wasm::Result<void> Play(
      std::function<void(wasm::OperationResult)> finished_callback);
  wasm::Result<void> Pause();

  /// Sets a listener to receive updates about `HTMLMediaElement`. Only one
  /// listener can be set: setting another clears the previous one. Pass
  /// `nullptr` to reset the listener.
  ///
  /// @param[in] listener Listener to be set or `nullptr` to unset the listener.
  ///
  /// @warning The ownership isn't transferred, and, as such, the listener must
  /// outlive the source.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @sa `HTMLMediaElementListener`
  wasm::Result<void> SetListener(HTMLMediaElementListener* listener);

 private:
  wasm::OperationResult SetListenerInternal(HTMLMediaElementListener* listener);

  // legacy EMSS compatibility: methods
  wasm::Result<void> RegisterOnTimeUpdateEMSS(
      wasm::ElementaryMediaStreamSourceListener*,
      int source_handle);
  void UnregisterOnTimeUpdateEMSS(int source_handle);

  int handle_;
  HTMLMediaElementListener* listener_;

  // legacy EMSS compatibility: variables
  wasm::ElementaryMediaStreamSource* source_;

  friend class wasm::ElementaryMediaStreamSource;
};

}  // namespace html
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_HTML_HTML_MEDIA_ELEMENT_H_
