// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/html/html_media_element.h"

#include <utility>

#include "samsung/bindings/common.h"
#include "samsung/bindings/elementary_media_stream_source.h"
#include "samsung/bindings/emss_operation_result.h"
#include "samsung/bindings/html_media_element.h"
#include "samsung/html/html_media_element_listener.h"
#include "samsung/wasm/elementary_media_stream_source.h"
#include "samsung/wasm/elementary_media_stream_source_listener.h"
#include "samsung/wasm/media_key.h"

namespace samsung {
namespace html {

namespace {

void OnTimeUpdateEMSSCallback(void* user_data, void* element) {
  auto* listener =
      static_cast<wasm::ElementaryMediaStreamSourceListener*>(user_data);

  const auto* html_media_element = static_cast<HTMLMediaElement*>(element);

  if (!html_media_element->HasSrc()) return;

  auto new_time = html_media_element->GetCurrentTime();

  if (new_time) listener->OnPlaybackPositionChanged(new_time.value);
}

}  // namespace

HTMLMediaElement::HTMLMediaElement(const char* id)
    : handle_(mediaElementById(id)), source_(nullptr) {}

HTMLMediaElement::HTMLMediaElement(HTMLMediaElement&& other)
    : handle_(std::exchange(other.handle_, -1)),
      source_(std::exchange(other.source_, nullptr)) {}

HTMLMediaElement& HTMLMediaElement::operator=(HTMLMediaElement&& other) {
  handle_ = std::exchange(other.handle_, -1);
  source_ = std::exchange(other.source_, nullptr);
  return *this;
}

HTMLMediaElement::~HTMLMediaElement() {
  if (IsValid()) mediaElementRemove(handle_);
}

bool HTMLMediaElement::IsValid() const { return IsHandleValid(handle_); }

wasm::Result<bool> HTMLMediaElement::IsAutoplay() const {
  return CAPICall<bool>(mediaElementIsAutoplay, handle_);
}

wasm::Result<void> HTMLMediaElement::SetAutoplay(bool newAutoplay) {
  return CAPICall<void>(mediaElementSetAutoplay, handle_, newAutoplay);
}

wasm::Result<wasm::Seconds> HTMLMediaElement::GetCurrentTime() const {
  const auto result = CAPICall<double>(mediaElementGetCurrentTime, handle_);
  return {wasm::Seconds(result.value), result.operation_result};
}

wasm::Result<void> HTMLMediaElement::SetCurrentTime(wasm::Seconds new_time) {
  return CAPICall<void>(mediaElementSetCurrentTime, handle_, new_time.count());
}

wasm::Result<wasm::Seconds> HTMLMediaElement::GetDuration() const {
  const auto result = CAPICall<double>(mediaElementGetDuration, handle_);
  return {wasm::Seconds(result.value), result.operation_result};
}

wasm::Result<bool> HTMLMediaElement::IsEnded() const {
  return CAPICall<bool>(mediaElementIsEnded, handle_);
}

wasm::Result<bool> HTMLMediaElement::IsLoop() const {
  return CAPICall<bool>(mediaElementIsLoop, handle_);
}

wasm::Result<void> HTMLMediaElement::SetLoop(bool newLoop) {
  return CAPICall<void>(mediaElementSetLoop, handle_, newLoop);
}

wasm::Result<bool> HTMLMediaElement::IsPaused() const {
  return CAPICall<bool>(mediaElementIsPaused, handle_);
}

wasm::Result<HTMLMediaElement::ReadyState> HTMLMediaElement::GetReadyState()
    const {
  const auto result = CAPICall<int>(mediaElementGetReadyState, handle_);
  return {static_cast<ReadyState>(result.value), result.operation_result};
}

wasm::Result<std::string> HTMLMediaElement::GetSrc() const {
  const auto result = CAPICall<char*>(mediaElementGetSrc, handle_);
  if (result.operation_result != wasm::OperationResult::kSuccess) {
    return {"", result.operation_result};
  }
  std::string ret = result.value;
  free(result.value);
  return {ret, wasm::OperationResult::kSuccess};
}

bool HTMLMediaElement::HasSrc() const { return source_; }

wasm::Result<void> HTMLMediaElement::SetSrc(
    wasm::ElementaryMediaStreamSource* source) {
  if (!source) {
    source_->SetHTMLMediaElement(nullptr);
    source_ = nullptr;
    return CAPICall<void>(mediaElementSetSrc, handle_, "");
  }

  source_ = source;
  source_->SetHTMLMediaElement(this);
  return CAPICall<void>(mediaElementSetSrc, handle_, source->GetURL());
}

wasm::Result<void> HTMLMediaElement::Play(
    std::function<void(HTMLMediaElement::AsyncResult)> on_finished_callback) {
  return CAPIAsyncCall<AsyncResult, HTMLMediaElementAsyncResult>(
      on_finished_callback, mediaElementPlay, handle_);
}

wasm::Result<void> HTMLMediaElement::Pause() {
  return CAPICall<void>(mediaElementPause, handle_);
}

wasm::Result<void> HTMLMediaElement::SetListener(
    HTMLMediaElementListener* listener) {
  SET_LISTENER(mediaElementSetOnTimeUpdate, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnTimeUpdate>,
               listener);
  SET_LISTENER(mediaElementSetOnLoadStart, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnLoadStart>,
               listener);
  SET_LISTENER(mediaElementSetOnLoadedMetadata, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnLoadedMetadata>,
               listener);
  SET_LISTENER(mediaElementSetOnLoadedData, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnLoadedData>,
               listener);
  SET_LISTENER(mediaElementSetOnCanPlay, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnCanPlay>,
               listener);
  SET_LISTENER(mediaElementSetOnCanPlayThrough, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnCanPlayThrough>,
               listener);
  SET_LISTENER(mediaElementSetOnEnded, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnEnded>,
               listener);
  SET_LISTENER(mediaElementSetOnPlaying, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnPlaying>,
               listener);
  SET_LISTENER(mediaElementSetOnPlay, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnPlay>,
               listener);
  SET_LISTENER(mediaElementSetOnSeeking, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnSeeking>,
               listener);
  SET_LISTENER(mediaElementSetOnSeeked, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnSeeked>,
               listener);
  SET_LISTENER(mediaElementSetOnPause, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnPause>,
               listener);
  SET_LISTENER(mediaElementSetOnWaiting, handle_,
               ListenerCallback<HTMLMediaElementListener,
                                &HTMLMediaElementListener::OnWaiting>,
               listener);
  return {wasm::OperationResult::kSuccess};
}

wasm::Result<void> HTMLMediaElement::RegisterOnTimeUpdateEMSS(
    wasm::ElementaryMediaStreamSourceListener* listener) {
  SET_LISTENER(mediaElementRegisterOnTimeUpdateEMSS, handle_,
               OnTimeUpdateEMSSCallback, listener, this);

  return {wasm::OperationResult::kSuccess};
}

void HTMLMediaElement::UnregisterOnTimeUpdateEMSS() {
  CAPICall<void>(mediaElementUnregisterOnTimeUpdateEMSS, handle_);
}

}  // namespace html
}  // namespace samsung
