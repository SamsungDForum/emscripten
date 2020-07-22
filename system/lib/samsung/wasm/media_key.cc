// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/media_key.h"

#include "samsung/bindings/common.h"
#include "samsung/bindings/media_key.h"

namespace samsung {
namespace wasm {

namespace {

MediaKeyConfig DRMConfigToCAPI(const DRMConfig& config) {
  return {
      static_cast<MediaKeyContentDecryptionModule>(config.cdm),
      static_cast<MediaKeyEncryptionMode>(config.encryption_mode),
      config.license_server.c_str(),
      config.init_data.size(),
      config.init_data.data(),
      config.audio_mime_type.c_str(),
      static_cast<MediaKeyRobustness>(config.audio_robustness),
      config.video_mime_type.c_str(),
      static_cast<MediaKeyRobustness>(config.video_robustness),
  };
}

}  // namespace

struct MediaKey::AsyncImpl {
  static void OnCAPICallFinished(EMSSOperationResult error,
                                 int media_key_handle,
                                 void* userData) {
    auto cb = std::unique_ptr<MediaKey::SetupFinishedCallback>(
        static_cast<MediaKey::SetupFinishedCallback*>(userData));
    (*cb)(static_cast<OperationResult>(error), MediaKey{media_key_handle});
  }
};

MediaKey::MediaKey(MediaKey&& other)
    : handle_(std::exchange(other.handle_, -1)) {}

MediaKey& MediaKey::operator=(MediaKey&& other) {
  handle_ = std::exchange(other.handle_, -1);
  return *this;
}

MediaKey::~MediaKey() {
  if (IsValid())
    mediaKeyRemove(handle_);
}

bool MediaKey::IsValid() const {
  return IsHandleValid(handle_);
}

// static
Result<void> MediaKey::SetupEncryption(const DRMConfig& config,
                                       SetupFinishedCallback on_finished) {
  const auto capi_config = DRMConfigToCAPI(config);
  auto callback = new SetupFinishedCallback(on_finished);
  return CAPICall<void>(mediaKeySetEncryption, &capi_config,
                        AsyncImpl::OnCAPICallFinished, callback);
}

MediaKey::MediaKey(int handle) : handle_(handle) {}

}  // namespace wasm
}  // namespace samsung
