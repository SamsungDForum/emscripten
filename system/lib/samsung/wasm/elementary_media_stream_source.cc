// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/elementary_media_stream_source.h"

#include <utility>

#include "samsung/bindings/common.h"
#include "samsung/bindings/elementary_audio_track_config.h"
#include "samsung/bindings/elementary_media_stream_source.h"
#include "samsung/bindings/elementary_video_track_config.h"
#include "samsung/bindings/emss_operation_result.h"
#include "samsung/html/html_media_element.h"
#include "samsung/wasm/elementary_audio_track_config.h"
#include "samsung/wasm/elementary_media_stream_source_listener.h"
#include "samsung/wasm/elementary_video_track_config.h"

namespace samsung {
namespace wasm {

namespace {

::EMSSElementaryAudioTrackConfig ConfigToCAPI(
    const ElementaryAudioTrackConfig& config) {
  return {{config.mime_type.c_str(), config.extradata.size(),
           config.extradata.data()},
          static_cast<EMSSSampleFormat>(config.sample_format),
          static_cast<EMSSChannelLayout>(config.channel_layout),
          config.samples_per_second};
}

::EMSSElementaryVideoTrackConfig ConfigToCAPI(
    const ElementaryVideoTrackConfig& config) {
  return {{config.mime_type.c_str(), config.extradata.size(),
           config.extradata.data()},
          config.width,
          config.height,
          config.framerate_num,
          config.framerate_den};
}

void OnPlaybackPositionChangedListenerCallback(float new_time,
                                               void* user_data) {
  const auto listener =
      static_cast<ElementaryMediaStreamSourceListener*>(user_data);
  listener->OnPlaybackPositionChanged(Seconds(new_time));
}

void OnClosedCaptionsListenerCallback(const uint8_t* closed_captions,
                                      uint32_t captions_length,
                                      void* user_data) {
  const auto listener =
      static_cast<ElementaryMediaStreamSourceListener*>(user_data);
  listener->OnClosedCaptions(closed_captions,
                             static_cast<size_t>(captions_length));
}

}  // namespace

ElementaryMediaStreamSource::ElementaryMediaStreamSource(Mode mode)
    : handle_(EMSSCreate(static_cast<EMSSMode>(mode))),
      html_media_element_(nullptr),
      listener_(nullptr),
      url_(CAPICall<char*>(EMSSCreateObjectURL, handle_).value, std::free),
      version_info_(EmssVersionInfo::Create()) {
  use_session_id_emulation_ =
      version_info_.has_legacy_emss && mode != Mode::kLowLatency;
}

ElementaryMediaStreamSource::ElementaryMediaStreamSource(
    ElementaryMediaStreamSource&& other)
    : handle_(std::exchange(other.handle_, -1)),
      html_media_element_(std::exchange(other.html_media_element_, nullptr)),
      listener_(std::exchange(other.listener_, nullptr)),
      url_(std::exchange(other.url_, {nullptr, std::free})),
      use_session_id_emulation_(other.use_session_id_emulation_),
      version_info_(other.version_info_) {}

ElementaryMediaStreamSource& ElementaryMediaStreamSource::operator=(
    ElementaryMediaStreamSource&& other) {
  handle_ = std::exchange(other.handle_, -1);
  html_media_element_ = std::exchange(other.html_media_element_, nullptr);
  listener_ = std::exchange(other.listener_, nullptr);
  url_ = std::exchange(other.url_, {nullptr, std::free});
  use_session_id_emulation_ = other.use_session_id_emulation_;
  version_info_ = other.version_info_;
  return *this;
}

ElementaryMediaStreamSource::~ElementaryMediaStreamSource() {
  if (IsValid()) {
    if (listener_)
      SetListenerInternal(nullptr);
    EMSSRemove(handle_);
    EMSSRevokeObjectURL(url_.get());
  }
}

bool ElementaryMediaStreamSource::IsValid() const {
  return IsHandleValid(handle_);
}

Result<ElementaryMediaTrack> ElementaryMediaStreamSource::AddTrack(
    const ElementaryAudioTrackConfig& config) {
  auto CAPIConfig = ConfigToCAPI(config);
  const auto result = CAPICall<int>(EMSSAddAudioTrack, handle_, &CAPIConfig);
  if (result.operation_result != OperationResult::kSuccess)
    return {ElementaryMediaTrack{}, result.operation_result};
  auto track = ElementaryMediaTrack{result.value, version_info_,
                                    use_session_id_emulation_};
  if (!track.IsValid())
    return {ElementaryMediaTrack{}, OperationResult::kFailed};
  return {std::move(track), OperationResult::kSuccess};
}

Result<ElementaryMediaTrack> ElementaryMediaStreamSource::AddTrack(
    const ElementaryVideoTrackConfig& config) {
  // TODO(p.balut): remove duplciated code
  auto CAPIConfig = ConfigToCAPI(config);
  const auto result = CAPICall<int>(EMSSAddVideoTrack, handle_, &CAPIConfig);
  if (result.operation_result != OperationResult::kSuccess)
    return {ElementaryMediaTrack{}, result.operation_result};
  auto track = ElementaryMediaTrack{result.value, version_info_,
                                    use_session_id_emulation_};
  if (!track.IsValid())
    return {ElementaryMediaTrack{}, OperationResult::kFailed};
  return {std::move(track), OperationResult::kSuccess};
}

Result<void> ElementaryMediaStreamSource::RemoveTrack(
    const ElementaryMediaTrack& track) {
  return CAPICall<void>(EMSSRemoveTrack, handle_, track.GetHandle());
}

Result<void> ElementaryMediaStreamSource::Flush() {
  return CAPICall<void>(EMSSFlush, handle_);
}

Result<void> ElementaryMediaStreamSource::Close(
    std::function<void(OperationResult)> on_finished_callback) {
  return CAPIAsyncCall<OperationResult, EMSSOperationResult>(
      on_finished_callback, EMSSClose, handle_);
}

Result<void> ElementaryMediaStreamSource::Open(
    std::function<void(OperationResult)> on_finished_callback) {
  return CAPIAsyncCall<OperationResult, EMSSOperationResult>(
      on_finished_callback, EMSSOpen, handle_);
}

Result<Seconds> ElementaryMediaStreamSource::GetDuration() const {
  const auto result = CAPICall<double>(EMSSGetDuration, handle_);
  return {Seconds(result.value), result.operation_result};
}

Result<void> ElementaryMediaStreamSource::SetDuration(Seconds new_duration) {
  return CAPICall<void>(EMSSSetDuration, handle_, new_duration.count());
}

Result<ElementaryMediaStreamSource::Mode> ElementaryMediaStreamSource::GetMode()
    const {
  const auto result = CAPICall<EMSSMode>(EMSSGetMode, handle_);
  return {static_cast<Mode>(result.value), result.operation_result};
}

Result<ElementaryMediaStreamSource::ReadyState>
ElementaryMediaStreamSource::GetReadyState() const {
  const auto result = CAPICall<EMSSReadyState>(EMSSGetReadyState, handle_);
  return {static_cast<ReadyState>(result.value), result.operation_result};
}

const char* ElementaryMediaStreamSource::GetURL() const {
  return url_.get();
}

Result<void> ElementaryMediaStreamSource::SetListener(
    ElementaryMediaStreamSourceListener* listener) {
  if (listener_ && listener)
    SetListenerInternal(nullptr);

  auto result = SetListenerInternal(listener);
  if (result != OperationResult::kSuccess) {
    // Rollback any listeners that were potentially set during the
    // SetListenerInternal call.
    if (listener)
      SetListenerInternal(nullptr);
    listener_ = nullptr;
    return {result};
  }

  listener_ = listener;
  return {OperationResult::kSuccess};
}

void ElementaryMediaStreamSource::SetHTMLMediaElement(
    html::HTMLMediaElement* html_media_element) {
  if (version_info_.has_legacy_emss && listener_) {
    if (html_media_element)
      html_media_element->RegisterOnTimeUpdateEMSS(listener_, handle_);
    else if (html_media_element_)
      html_media_element_->UnregisterOnTimeUpdateEMSS(handle_);
  }

  html_media_element_ = html_media_element;
}

OperationResult ElementaryMediaStreamSource::SetListenerInternal(
    ElementaryMediaStreamSourceListener* listener) {
  if (listener) {
    if (version_info_.has_legacy_emss) {
      if (html_media_element_)
        html_media_element_->RegisterOnTimeUpdateEMSS(listener, handle_);

      listener_ = listener;
    } else {
      LISTENER_OP(EMSSSetOnPlaybackPositionChanged, handle_,
                  OnPlaybackPositionChangedListenerCallback, listener);
    }

    LISTENER_OP(EMSSSetOnClosedCaptions, handle_,
                OnClosedCaptionsListenerCallback, listener);

    LISTENER_OP(EMSSSetOnSourceDetached, handle_,
                ListenerCallback<
                    ElementaryMediaStreamSourceListener,
                    &ElementaryMediaStreamSourceListener::OnSourceDetached>,
                listener);
    LISTENER_OP(
        EMSSSetOnSourceClosed, handle_,
        ListenerCallback<ElementaryMediaStreamSourceListener,
                         &ElementaryMediaStreamSourceListener::OnSourceClosed>,
        listener);
    LISTENER_OP(EMSSSetOnSourceOpenPending, handle_,
                ListenerCallback<
                    ElementaryMediaStreamSourceListener,
                    &ElementaryMediaStreamSourceListener::OnSourceOpenPending>,
                listener);
    LISTENER_OP(
        EMSSSetOnSourceOpen, handle_,
        ListenerCallback<ElementaryMediaStreamSourceListener,
                         &ElementaryMediaStreamSourceListener::OnSourceOpen>,
        listener);
    LISTENER_OP(
        EMSSSetOnSourceEnded, handle_,
        ListenerCallback<ElementaryMediaStreamSourceListener,
                         &ElementaryMediaStreamSourceListener::OnSourceEnded>,
        listener);
  } else {
    if (version_info_.has_legacy_emss) {
      if (html_media_element_)
        html_media_element_->UnregisterOnTimeUpdateEMSS(handle_);
    } else {
      LISTENER_OP(EMSSUnsetOnPlaybackPositionChanged, handle_);
    }
    LISTENER_OP(EMSSUnsetOnSourceDetached, handle_);
    LISTENER_OP(EMSSUnsetOnSourceClosed, handle_);
    LISTENER_OP(EMSSUnsetOnSourceOpenPending, handle_);
    LISTENER_OP(EMSSUnsetOnSourceOpen, handle_);
    LISTENER_OP(EMSSUnsetOnSourceEnded, handle_);
  }
  return OperationResult::kSuccess;
}

}  // namespace wasm
}  // namespace samsung
