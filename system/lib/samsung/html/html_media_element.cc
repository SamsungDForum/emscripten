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

void OnTimeUpdateEMSSCallback(void* user_data, float new_time) {
  auto* listener =
      static_cast<wasm::ElementaryMediaStreamSourceListener*>(user_data);
  listener->OnPlaybackPositionChanged(wasm::Seconds(new_time));
}

void OnErrorListenerCallback(int error_code,
                             const char* error_message,
                             void* user_data) {
  const auto listener = static_cast<HTMLMediaElementListener*>(user_data);
  listener->OnError(static_cast<MediaError>(error_code), error_message);
}

}  // namespace

HTMLMediaElement::HTMLMediaElement(const char* id)
    : handle_(mediaElementById(id)), listener_(nullptr), source_(nullptr) {}

HTMLMediaElement::HTMLMediaElement(HTMLMediaElement&& other)
    : handle_(std::exchange(other.handle_, -1)),
      listener_(std::exchange(other.listener_, nullptr)),
      source_(std::exchange(other.source_, nullptr)) {}

HTMLMediaElement& HTMLMediaElement::operator=(HTMLMediaElement&& other) {
  handle_ = std::exchange(other.handle_, -1);
  listener_ = std::exchange(other.listener_, nullptr);
  source_ = std::exchange(other.source_, nullptr);
  return *this;
}

HTMLMediaElement::~HTMLMediaElement() {
  if (IsValid()) {
    if (listener_)
      SetListenerInternal(nullptr);
    mediaElementRemove(handle_);
  }
}

bool HTMLMediaElement::IsValid() const {
  return IsHandleValid(handle_);
}

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

bool HTMLMediaElement::HasSrc() const {
  return source_;
}

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
    std::function<void(wasm::OperationResult)> on_finished_callback) {
  return CAPIAsyncCall<wasm::OperationResult, EMSSOperationResult>(
      on_finished_callback, mediaElementPlay, handle_);
}

wasm::Result<void> HTMLMediaElement::Pause() {
  return CAPICall<void>(mediaElementPause, handle_);
}

wasm::Result<void> HTMLMediaElement::SetListener(
    HTMLMediaElementListener* listener) {
  if (listener_ && listener)
    SetListenerInternal(nullptr);

  auto result = SetListenerInternal(listener);
  if (result != wasm::OperationResult::kSuccess) {
    // Rollback any listeners that were potentially set during the
    // SetListenerInternal call.
    if (listener)
      SetListenerInternal(nullptr);
    listener_ = nullptr;
    return {result};
  }

  listener_ = listener;
  return {wasm::OperationResult::kSuccess};
}

// private

wasm::OperationResult HTMLMediaElement::SetListenerInternal(
    HTMLMediaElementListener* listener) {
  if (listener) {
    LISTENER_OP(mediaElementSetOnTimeUpdate, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnTimeUpdate>,
                listener);
    LISTENER_OP(mediaElementSetOnLoadStart, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnLoadStart>,
                listener);
    LISTENER_OP(mediaElementSetOnLoadedMetadata, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnLoadedMetadata>,
                listener);
    LISTENER_OP(mediaElementSetOnLoadedData, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnLoadedData>,
                listener);
    LISTENER_OP(mediaElementSetOnCanPlay, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnCanPlay>,
                listener);
    LISTENER_OP(mediaElementSetOnCanPlayThrough, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnCanPlayThrough>,
                listener);
    LISTENER_OP(mediaElementSetOnEnded, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnEnded>,
                listener);
    LISTENER_OP(mediaElementSetOnPlaying, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnPlaying>,
                listener);
    LISTENER_OP(mediaElementSetOnPlay, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnPlay>,
                listener);
    LISTENER_OP(mediaElementSetOnSeeking, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnSeeking>,
                listener);
    LISTENER_OP(mediaElementSetOnSeeked, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnSeeked>,
                listener);
    LISTENER_OP(mediaElementSetOnPause, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnPause>,
                listener);
    LISTENER_OP(mediaElementSetOnWaiting, handle_,
                ListenerCallback<HTMLMediaElementListener,
                                 &HTMLMediaElementListener::OnWaiting>,
                listener);
    LISTENER_OP(mediaElementSetOnError, handle_, OnErrorListenerCallback,
                listener);
  } else {
    LISTENER_OP(mediaElementUnsetOnTimeUpdate, handle_);
    LISTENER_OP(mediaElementUnsetOnLoadStart, handle_);
    LISTENER_OP(mediaElementUnsetOnLoadedMetadata, handle_);
    LISTENER_OP(mediaElementUnsetOnLoadedData, handle_);
    LISTENER_OP(mediaElementUnsetOnCanPlay, handle_);
    LISTENER_OP(mediaElementUnsetOnCanPlayThrough, handle_);
    LISTENER_OP(mediaElementUnsetOnEnded, handle_);
    LISTENER_OP(mediaElementUnsetOnPlaying, handle_);
    LISTENER_OP(mediaElementUnsetOnPlay, handle_);
    LISTENER_OP(mediaElementUnsetOnSeeking, handle_);
    LISTENER_OP(mediaElementUnsetOnSeeked, handle_);
    LISTENER_OP(mediaElementUnsetOnPause, handle_);
    LISTENER_OP(mediaElementUnsetOnWaiting, handle_);
    LISTENER_OP(mediaElementUnsetOnError, handle_);
  }
  return wasm::OperationResult::kSuccess;
}

// legacy EMSS compatibility: private methods

wasm::Result<void> HTMLMediaElement::RegisterOnTimeUpdateEMSS(
    wasm::ElementaryMediaStreamSourceListener* listener,
    int source_handle) {
  const auto result =
      CAPICall<void>(mediaElementRegisterOnTimeUpdateEMSS, handle_,
                     source_handle, OnTimeUpdateEMSSCallback, listener)
          .operation_result;
  return {result};
}

void HTMLMediaElement::UnregisterOnTimeUpdateEMSS(int source_handle) {
  CAPICall<void>(mediaElementUnregisterOnTimeUpdateEMSS, handle_,
                 source_handle);
}

}  // namespace html
}  // namespace samsung
