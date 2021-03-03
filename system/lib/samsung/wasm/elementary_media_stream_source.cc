// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/elementary_media_stream_source.h"

#include <algorithm>
#include <cctype>
#include <iterator>
#include <string>
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

const EMSSDecodingMode kIgnoreDecodingMode = static_cast<EMSSDecodingMode>(-1);

::EMSSElementaryAudioTrackConfig ConfigToCAPI(
    const ElementaryAudioTrackConfig& config,
    const EmssVersionInfo& version_info) {
  EMSSDecodingMode decoding_mode = kIgnoreDecodingMode;

  if (version_info.has_decoding_mode)
    decoding_mode = static_cast<EMSSDecodingMode>(config.decoding_mode);

  return {{config.mime_type.c_str(), config.extradata.size(),
           config.extradata.data(), decoding_mode},
          static_cast<EMSSSampleFormat>(config.sample_format),
          static_cast<EMSSChannelLayout>(config.channel_layout),
          config.samples_per_second};
}

::EMSSElementaryVideoTrackConfig ConfigToCAPI(
    const ElementaryVideoTrackConfig& config,
    const EmssVersionInfo& version_info) {
  EMSSDecodingMode decoding_mode = kIgnoreDecodingMode;

  if (version_info.has_decoding_mode)
    decoding_mode = static_cast<EMSSDecodingMode>(config.decoding_mode);

  return {{config.mime_type.c_str(), config.extradata.size(),
           config.extradata.data(), decoding_mode},
          config.width,
          config.height,
          config.framerate_num,
          config.framerate_den};
}

std::string StripWhiteSpace(const std::string& str) {
  auto it_first = std::find_if_not(
      str.begin(), str.end(), [](unsigned char c) { return std::isspace(c); });
  auto it_last =
      std::find_if_not(str.rbegin(), str.rend(), [](unsigned char c) {
        return std::isspace(c);
      }).base();
  if (it_first < it_last)
    return std::string(it_first, it_last);
  else
    return "";
}

std::string ToLower(const std::string& str) {
  std::string result = str;
  std::transform(result.begin(), result.end(), result.begin(),
                 [](unsigned char c) { return std::tolower(c); });
  return result;
}

std::vector<std::string> SplitMimeParameters(const std::string& mime_type) {
  std::vector<std::string> result;
  std::string stripped_mime = StripWhiteSpace(mime_type);
  std::string::iterator last_start = stripped_mime.begin();
  bool is_quoted = false;

  for (auto it = stripped_mime.begin(); it != stripped_mime.end(); ++it) {
    if (*it == ';' && !is_quoted) {
      std::string param(last_start, it);
      result.push_back(StripWhiteSpace(param));
      last_start = it + 1;
      continue;
    }

    if (*it == '\"') {
      is_quoted = !is_quoted;
    }
  }

  result.emplace_back(last_start, stripped_mime.end());
  return result;
}

std::string GetMimeParameter(const std::string& mime_type,
                             const std::string& parameter_name) {
  std::string look_for_name = StripWhiteSpace(parameter_name);
  look_for_name = ToLower(look_for_name);

  std::vector<std::string> parameters = SplitMimeParameters(mime_type);
  for (auto param : parameters) {
    auto equal_sign_pos = param.find('=');
    if (equal_sign_pos == std::string::npos)
      continue;

    std::string name(param.begin(), param.begin() + equal_sign_pos);
    name = ToLower(StripWhiteSpace(name));

    std::string value(param.begin() + equal_sign_pos + 1, param.end());
    value = StripWhiteSpace(value);
    value.erase(std::remove(value.begin(), value.end(), '\"'), value.end());

    if (look_for_name == name)
      return value;
  }

  return "";
}

OperationResult EarlyValidateAudioConfig(
    const ElementaryAudioTrackConfig& config) {
  bool pcm_codec = GetMimeParameter(config.mime_type, "codecs") == "pcm";

  if (pcm_codec && config.sample_format != SampleFormat::kS16)
    return OperationResult::kConfigInvalidSampleFormat;

  return OperationResult::kSuccess;
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

int FromLegacyMode(ElementaryMediaStreamSource::Mode mode) {
  switch (static_cast<EMSSMode>(mode)) {
    case EMSSModeNormal:
      return EMSSCreate(EMSSLatencyModeNormal,
                        EMSSRenderingModeMediaElement);
    case EMSSModeLowLatency:
      return EMSSCreate(EMSSLatencyModeLowLatency,
                        EMSSRenderingModeMediaElement);
    case EMSSModeVideoTexture:
      return EMSSCreate(EMSSLatencyModeNormal,
                        EMSSRenderingModeVideoTexture);
  }
  return -1;
}

}  // namespace

ElementaryMediaStreamSource::ElementaryMediaStreamSource(Mode mode)
    : ElementaryMediaStreamSource(FromLegacyMode(mode),
                                  mode == Mode::kLowLatency) {
}

ElementaryMediaStreamSource::ElementaryMediaStreamSource(
  LatencyMode latency_mode, RenderingMode rendering_mode)
    : ElementaryMediaStreamSource(EMSSCreate(
          static_cast<EMSSLatencyMode>(latency_mode),
          static_cast<EMSSRenderingMode>(rendering_mode)),
        latency_mode == LatencyMode::kLow) {
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
  using TrackType = ElementaryMediaTrack::TrackType;
  auto early_config_validation_result = EarlyValidateAudioConfig(config);
  if (early_config_validation_result != OperationResult::kSuccess)
    return {ElementaryMediaTrack{}, early_config_validation_result};

  auto CAPIConfig = ConfigToCAPI(config, version_info_);
  const auto result = CAPICall<int>(EMSSAddAudioTrack, handle_, &CAPIConfig);
  if (result.operation_result != OperationResult::kSuccess)
    return {ElementaryMediaTrack{}, result.operation_result};

  auto track = ElementaryMediaTrack{result.value, TrackType::kAudio,
                                    version_info_, use_session_id_emulation_};
  if (!track.IsValid())
    return {ElementaryMediaTrack{}, OperationResult::kFailed};

  return {std::move(track), OperationResult::kSuccess};
}

Result<void> ElementaryMediaStreamSource::AddTrack(
    const ElementaryAudioTrackConfig& config,
    std::function<void(OperationResult, ElementaryMediaTrack)>
        on_finished_callback) {
  using TrackType = ElementaryMediaTrack::TrackType;
  if (!version_info_.has_decoding_mode) {
    // fallback to synchronous add track in case of missing async add track
    // functionality on a platform
    auto result = AddTrack(config);
    if (result.operation_result != OperationResult::kSuccess)
      return {result.operation_result};

    on_finished_callback(result.operation_result, std::move(result.value));
    return {result.operation_result};
  }

  const auto CAPIConfig = ConfigToCAPI(config, version_info_);

  return CAPIAsyncCallWithArgAndReturnParam<OperationResult, int32_t,
                                            EMSSOperationResult>(
      EMSSAddAudioTrackAsync, handle_, &CAPIConfig,
      GetOnAddTrackDoneCb(TrackType::kAudio, on_finished_callback));
}

Result<ElementaryMediaTrack> ElementaryMediaStreamSource::AddTrack(
    const ElementaryVideoTrackConfig& config) {
  using TrackType = ElementaryMediaTrack::TrackType;
  // TODO(p.balut): remove duplicated code
  auto CAPIConfig = ConfigToCAPI(config, version_info_);
  const auto result = CAPICall<int>(EMSSAddVideoTrack, handle_, &CAPIConfig);
  if (result.operation_result != OperationResult::kSuccess)
    return {ElementaryMediaTrack{}, result.operation_result};
  auto track = ElementaryMediaTrack{result.value, TrackType::kVideo,
                                    version_info_, use_session_id_emulation_};
  if (!track.IsValid())
    return {ElementaryMediaTrack{}, OperationResult::kFailed};
  return {std::move(track), OperationResult::kSuccess};
}

Result<void> ElementaryMediaStreamSource::AddTrack(
    const ElementaryVideoTrackConfig& config,
    std::function<void(OperationResult, ElementaryMediaTrack)>
        on_finished_callback) {
  using TrackType = ElementaryMediaTrack::TrackType;
  if (!version_info_.has_decoding_mode) {
    // fallback to synchronous add track in case of missing async add track
    // functionality on a platform
    auto result = AddTrack(config);
    if (result.operation_result != OperationResult::kSuccess)
      return {result.operation_result};

    on_finished_callback(result.operation_result, std::move(result.value));
    return {result.operation_result};
  }

  const auto CAPIConfig = ConfigToCAPI(config, version_info_);
  return CAPIAsyncCallWithArgAndReturnParam<OperationResult, int32_t,
                                            EMSSOperationResult>(
      EMSSAddVideoTrackAsync, handle_, &CAPIConfig,
      GetOnAddTrackDoneCb(TrackType::kVideo, on_finished_callback));
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

Result<ElementaryMediaStreamSource::LatencyMode>
ElementaryMediaStreamSource::GetLatencyMode() const {
  const auto result = CAPICall<EMSSLatencyMode>(EMSSGetLatencyMode, handle_);
  return {static_cast<LatencyMode>(result.value), result.operation_result};
}

Result<ElementaryMediaStreamSource::RenderingMode>
ElementaryMediaStreamSource::GetRenderingMode() const {
  const auto result = CAPICall<EMSSRenderingMode>(
      EMSSGetRenderingMode, handle_);
  return {static_cast<RenderingMode>(result.value), result.operation_result};
}

Result<ElementaryMediaStreamSource::ReadyState>
ElementaryMediaStreamSource::GetReadyState() const {
  const auto result = CAPICall<EMSSReadyState>(EMSSGetReadyState, handle_);
  return {static_cast<ReadyState>(result.value), result.operation_result};
}

const char* ElementaryMediaStreamSource::GetURL() const {
  return url_.get();
}

ElementaryMediaStreamSource::ElementaryMediaStreamSource(
  int handle, bool is_low_latency)
    : handle_(handle),
      html_media_element_(nullptr),
      listener_(nullptr),
      url_(CAPICall<char*>(EMSSCreateObjectURL, handle_).value, std::free),
      version_info_(EmssVersionInfo::Create()) {
  use_session_id_emulation_ =
      version_info_.has_legacy_emss && is_low_latency;
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

std::function<void(OperationResult, int32_t handle)>
ElementaryMediaStreamSource::GetOnAddTrackDoneCb(
    ElementaryMediaTrack::TrackType type,
    std::function<void(OperationResult, ElementaryMediaTrack)>
        on_finished_callback) {
  auto cb = [this, on_finished_callback, type](OperationResult result,
                                               int32_t handle) {
    if (result != OperationResult::kSuccess) {
      on_finished_callback(result, ElementaryMediaTrack{});
      return;
    }

    auto track = ElementaryMediaTrack{handle, type, version_info_,
                                      use_session_id_emulation_};
    if (!track.IsValid()) {
      on_finished_callback(OperationResult::kFailed, ElementaryMediaTrack{});
      return;
    }

    on_finished_callback(OperationResult::kSuccess, std::move(track));
  };

  return cb;
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
    }
    LISTENER_OP(EMSSClearListeners, handle_);
  }
  return OperationResult::kSuccess;
}

}  // namespace wasm
}  // namespace samsung
