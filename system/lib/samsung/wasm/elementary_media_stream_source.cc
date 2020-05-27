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

}  // namespace

ElementaryMediaStreamSource::ElementaryMediaStreamSource(Mode mode)
    : handle_(EMSSCreate(static_cast<EMSSMode>(mode))),
      html_media_element_(nullptr),
      listener_(nullptr),
      url_(CAPICall<char*>(EMSSCreateObjectURL, handle_).value, std::free),
      version_info_(EmssVersionInfo::Create()) {}

ElementaryMediaStreamSource::ElementaryMediaStreamSource(
    ElementaryMediaStreamSource&& other)
    : handle_(std::exchange(other.handle_, -1)),
      html_media_element_(std::exchange(other.html_media_element_, nullptr)),
      listener_(nullptr),
      url_(std::exchange(other.url_, {nullptr, std::free})),
      version_info_(other.version_info_) {}

ElementaryMediaStreamSource& ElementaryMediaStreamSource::operator=(
    ElementaryMediaStreamSource&& other) {
  handle_ = std::exchange(other.handle_, -1);
  html_media_element_ = std::exchange(other.html_media_element_, nullptr);
  listener_ = std::exchange(other.listener_, nullptr);
  url_ = std::exchange(other.url_, {nullptr, std::free});
  version_info_ = other.version_info_;
  return *this;
}

ElementaryMediaStreamSource::~ElementaryMediaStreamSource() {
  SetHTMLMediaElement(nullptr);

  if (IsValid()) {
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
  const auto track_id =
      result.operation_result == OperationResult::kSuccess ? result.value : -1;
  return {ElementaryMediaTrack(track_id, version_info_),
          result.operation_result};
}

Result<ElementaryMediaTrack> ElementaryMediaStreamSource::AddTrack(
    const ElementaryVideoTrackConfig& config) {
  auto CAPIConfig = ConfigToCAPI(config);
  const auto result = CAPICall<int>(EMSSAddVideoTrack, handle_, &CAPIConfig);
  const auto track_id =
      result.operation_result == OperationResult::kSuccess ? result.value : -1;
  return {ElementaryMediaTrack(track_id, version_info_),
          result.operation_result};
}

Result<void> ElementaryMediaStreamSource::RemoveTrack(
    const ElementaryMediaTrack& track) {
  return CAPICall<void>(EMSSRemoveTrack, handle_, track.handle_);
}

Result<void> ElementaryMediaStreamSource::Flush() {
  return CAPICall<void>(EMSSFlush, handle_);
}

Result<void> ElementaryMediaStreamSource::Close(
    std::function<void(ElementaryMediaStreamSource::AsyncResult)>
        on_finished_callback) {
  return CAPIAsyncCall<AsyncResult, EMSSAsyncResult>(on_finished_callback,
                                                     EMSSClose, handle_);
}

Result<void> ElementaryMediaStreamSource::Open(
    std::function<void(ElementaryMediaStreamSource::AsyncResult)>
        on_finished_callback) {
  return CAPIAsyncCall<AsyncResult, EMSSAsyncResult>(on_finished_callback,
                                                     EMSSOpen, handle_);
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
  SET_LISTENER(
      EMSSSetOnSourceDetached, handle_,
      ListenerCallback<ElementaryMediaStreamSourceListener,
                       &ElementaryMediaStreamSourceListener::OnSourceDetached>,
      listener);
  SET_LISTENER(
      EMSSSetOnSourceClosed, handle_,
      ListenerCallback<ElementaryMediaStreamSourceListener,
                       &ElementaryMediaStreamSourceListener::OnSourceClosed>,
      listener);
  SET_LISTENER(EMSSSetOnSourceOpenPending, handle_,
               ListenerCallback<
                   ElementaryMediaStreamSourceListener,
                   &ElementaryMediaStreamSourceListener::OnSourceOpenPending>,
               listener);
  SET_LISTENER(
      EMSSSetOnSourceOpen, handle_,
      ListenerCallback<ElementaryMediaStreamSourceListener,
                       &ElementaryMediaStreamSourceListener::OnSourceOpen>,
      listener);
  SET_LISTENER(
      EMSSSetOnSourceEnded, handle_,
      ListenerCallback<ElementaryMediaStreamSourceListener,
                       &ElementaryMediaStreamSourceListener::OnSourceEnded>,
      listener);

  if (version_info_.has_legacy_emss) {
    if (html_media_element_)
      html_media_element_->RegisterOnTimeUpdateEMSS(listener);

    listener_ = listener;
  } else {
    SET_LISTENER(EMSSSetOnPlaybackPositionChanged, handle_,
                 OnPlaybackPositionChangedListenerCallback, listener);
  }
  return {OperationResult::kSuccess};
}

void ElementaryMediaStreamSource::SetHTMLMediaElement(
    html::HTMLMediaElement* html_media_element) {
  if (version_info_.has_legacy_emss && listener_) {
    if (html_media_element)
      html_media_element->RegisterOnTimeUpdateEMSS(listener_);
    else if (html_media_element_)
      html_media_element_->UnregisterOnTimeUpdateEMSS();
  }

  html_media_element_ = html_media_element;
}

}  // namespace wasm
}  // namespace samsung
