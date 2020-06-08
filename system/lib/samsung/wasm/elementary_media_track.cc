// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/elementary_media_track.h"

#include <atomic>
#include <chrono>
#include <type_traits>
#include <utility>

#include "samsung/bindings/common.h"
#include "samsung/bindings/elementary_media_packet.h"
#include "samsung/bindings/elementary_media_track.h"
#include "samsung/bindings/emss_operation_result.h"
#include "samsung/wasm/common.h"
#include "samsung/wasm/elementary_media_packet.h"
#include "samsung/wasm/elementary_media_track_listener.h"
#include "samsung/wasm/encrypted_elementary_media_packet.h"
#include "samsung/wasm/media_key.h"
#include "samsung/wasm/tizen_tv_wasm.h"

namespace {

::EMSSElementaryMediaPacket PacketToCAPI(
    const samsung::wasm::ElementaryMediaPacket& packet) {
  return {
      packet.pts.count(),   packet.dts.count(), packet.duration.count(),
      packet.is_key_frame,  packet.data_size,   packet.data,
      packet.width,         packet.height,      packet.framerate_num,
      packet.framerate_den, packet.session_id,
  };
}

::EMSSEncryptedElementaryMediaPacket PacketToCAPI(
    const samsung::wasm::EncryptedElementaryMediaPacket& packet) {
  // TODO(p.balut): A common structure should be used instead of a cast.
  static_assert(
      sizeof(EMSSEncryptedSubsampleDescription) ==
          sizeof(samsung::wasm::EncryptedSubsampleDescription),
      "C++ API subsample description != JS bindings subsample description.");
  static_assert(
      offsetof(EMSSEncryptedSubsampleDescription, clear_block) ==
          offsetof(samsung::wasm::EncryptedSubsampleDescription, clear_block),
      "C++ API subsample description != JS bindings subsample description.");
  static_assert(
      offsetof(EMSSEncryptedSubsampleDescription, cipher_block) ==
          offsetof(samsung::wasm::EncryptedSubsampleDescription, cipher_block),
      "C++ API subsample description != JS bindings subsample description.");

  EMSSElementaryMediaPacket base_packet = PacketToCAPI(
      static_cast<const samsung::wasm::ElementaryMediaPacket&>(packet));
  return {base_packet,
          packet.subsamples.size(),
          reinterpret_cast<const EMSSEncryptedSubsampleDescription*>(
              packet.subsamples.data()),
          packet.key_id.size(),
          packet.key_id.data(),
          packet.initialization_vector.size(),
          packet.initialization_vector.data(),
          static_cast<MediaKeyEncryptionMode>(packet.encryption_mode)};
}

void OnTrackClosedListenerCallback(
    EMSSElementaryMediaTrackCloseReason close_reason,
    void* user_data) {
  using samsung::wasm::ElementaryMediaTrack;
  using samsung::wasm::ElementaryMediaTrackListener;
  (static_cast<ElementaryMediaTrackListener*>(user_data))
      ->OnTrackClosed(
          static_cast<ElementaryMediaTrack::CloseReason>(close_reason));
}

void OnSeekListenerCallback(float new_time, void* user_data) {
  using samsung::wasm::ElementaryMediaTrackListener;
  (static_cast<ElementaryMediaTrackListener*>(user_data))
      ->OnSeek(samsung::wasm::Seconds(new_time));
}

void OnAppendErrorListenerCallback(
    EMSSOperationResult append_error,
    void* user_data) {
  using samsung::wasm::ElementaryMediaTrack;
  using samsung::wasm::ElementaryMediaTrackListener;
  (static_cast<ElementaryMediaTrackListener*>(user_data))
      ->OnAppendError(
          static_cast<samsung::wasm::OperationResult>(append_error));
}

}  // namespace

namespace samsung {
namespace wasm {

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaTrack::Impl declaration                    =*/
/*============================================================================*/

class ElementaryMediaTrack::Impl {
 public:
  explicit Impl(int handle,
                EmssVersionInfo version_info,
                bool use_session_id_emulation);
  Impl(const Impl&) = delete;
  Impl(Impl&&) = delete;
  Impl& operator=(const Impl&) = delete;
  Impl& operator=(Impl&&) = delete;
  ~Impl();

  bool IsValid() const;
  Result<void> AppendPacket(const ElementaryMediaPacket& packet);
  Result<void> AppendPacketAsync(const ElementaryMediaPacket& packet);
  Result<void> AppendEncryptedPacket(const EncryptedElementaryMediaPacket&);
  Result<void> AppendEncryptedPacketAsync(const EncryptedElementaryMediaPacket&);
  Result<void> AppendEndOfTrack(SessionId session_id);
  Result<void> AppendEndOfTrackAsync(SessionId session_id);
  Result<void> FillTextureWithNextFrame(
      GLuint texture_id,
      std::function<void(OperationResult)> finished_callback);
  Result<SessionId> GetSessionId() const;
  Result<bool> IsOpen() const;
  Result<void> RecycleTexture(GLuint textureId);
  Result<void> RegisterCurrentGraphicsContext();
  Result<void> SetMediaKey(MediaKey* key);
  Result<void> SetListener(ElementaryMediaTrackListener* listener);

  int handle() const { return handle_; }

 private:
  Result<void> AppendPacketInternal(const ElementaryMediaPacket&);
  Result<void> AppendEncryptedPacketInternal(
      const EncryptedElementaryMediaPacket&);
  Result<void> AppendPacketAsyncInternal(const ElementaryMediaPacket&);
  Result<void> AppendEncryptedPacketAsyncInternal(
      const EncryptedElementaryMediaPacket&);
  OperationResult SetListenerInternal(ElementaryMediaTrackListener* listener);

  // session id emulation for legacy mode: methods
  void EmulateSessionIdChange();
  void RegisterSessionIdEmulationCallbacks();
  void UnregisterSessionIdEmulationCallbacks();
  bool UseEmulatedAppend(SessionId session_id) const {
    return use_session_id_emulation_ && session_id != kIgnoreSessionId;
  }

  int handle_;
  ElementaryMediaTrackListener* listener_;
  EmssVersionInfo version_info_;

  // session id emulation for legacy mode: variables
  std::atomic<SessionId> emulated_session_id_;
  bool use_session_id_emulation_;
};

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaTrack::Impl definition                     =*/
/*============================================================================*/

ElementaryMediaTrack::Impl::Impl(int handle,
                                 EmssVersionInfo version_info,
                                 bool use_session_id_emulation)
    : handle_(handle),
      listener_(nullptr),
      version_info_(version_info),
      emulated_session_id_(0),
      use_session_id_emulation_(use_session_id_emulation) {
  if (use_session_id_emulation_)
    RegisterSessionIdEmulationCallbacks();
}

ElementaryMediaTrack::Impl::~Impl() {
  if (IsValid()) {
    if (use_session_id_emulation_)
      UnregisterSessionIdEmulationCallbacks();
    if (listener_)
      SetListenerInternal(nullptr);
    elementaryMediaTrackRemove(handle_);
  }
}

bool ElementaryMediaTrack::Impl::IsValid() const {
  return IsHandleValid(handle_);
}

Result<void> ElementaryMediaTrack::Impl::AppendPacket(
    const samsung::wasm::ElementaryMediaPacket& packet) {
  if (!UseEmulatedAppend(packet.session_id)) {
    // Use default code path.
    return AppendPacketInternal(packet);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != packet.session_id) {
      return {OperationResult::kFailed};
    }
    return AppendPacketInternal(packet);
  }
}

Result<void> ElementaryMediaTrack::Impl::AppendPacketAsync(
    const samsung::wasm::ElementaryMediaPacket& packet) {
  if (!UseEmulatedAppend(packet.session_id)) {
    // Use default code path.
    return AppendPacketAsyncInternal(packet);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != packet.session_id) {
      return {OperationResult::kFailed};
    }
    return AppendPacketAsyncInternal(packet);
  }
}

Result<void> ElementaryMediaTrack::Impl::AppendEncryptedPacket(
    const EncryptedElementaryMediaPacket& packet) {
  if (!UseEmulatedAppend(packet.session_id)) {
    // Use default code path.
    return AppendEncryptedPacketInternal(packet);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != packet.session_id) {
      return {OperationResult::kFailed};
    }
    return AppendEncryptedPacketInternal(packet);
  }
}

Result<void> ElementaryMediaTrack::Impl::AppendEncryptedPacketAsync(
    const EncryptedElementaryMediaPacket& packet) {
  if (!UseEmulatedAppend(packet.session_id)) {
    // Use default code path.
    return AppendEncryptedPacketAsyncInternal(packet);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != packet.session_id) {
      return {OperationResult::kFailed};
    }
    return AppendEncryptedPacketAsyncInternal(packet);
  }
}

Result<void> ElementaryMediaTrack::Impl::AppendEndOfTrack(
    SessionId app_session_id) {
  if (!UseEmulatedAppend(app_session_id)) {
    // Use default code path.
    auto session_id =
        (version_info_.has_legacy_emss ? kIgnoreSessionId : app_session_id);
    return CAPICall<void>(elementaryMediaTrackAppendEndOfTrack, handle_,
                          session_id);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != app_session_id) {
      return {OperationResult::kFailed};
    }
    return CAPICall<void>(elementaryMediaTrackAppendEndOfTrack, handle_,
                          kIgnoreSessionId);
  }
}

Result<void> ElementaryMediaTrack::Impl::AppendEndOfTrackAsync(
    SessionId app_session_id) {
  if (!UseEmulatedAppend(app_session_id)) {
    // Use default code path.
    auto session_id =
        (version_info_.has_legacy_emss ? kIgnoreSessionId : app_session_id);
    return CAPICall<void>(elementaryMediaTrackAppendEndOfTrackAsync, handle_,
                          session_id);
  } else {
    // Session id mechanism must be emulated, because legacy EMSS doesn't
    // support it at Platform level.
    if (emulated_session_id_.load() != app_session_id) {
      return {OperationResult::kFailed};
    }
    return CAPICall<void>(elementaryMediaTrackAppendEndOfTrackAsync, handle_,
                          kIgnoreSessionId);
  }
}

Result<void> ElementaryMediaTrack::Impl::FillTextureWithNextFrame(
    GLuint textureId,
    std::function<void(OperationResult)> finishedCallback) {
  if (!version_info_.has_video_texture)
    return {OperationResult::kNotSupported};

  return CAPIAsyncCallWithArg<
      OperationResult, EMSSOperationResult, uint32_t>(
      elementaryMediaTrackFillTextureWithNextFrame, handle_, textureId,
      finishedCallback);
}

Result<SessionId> ElementaryMediaTrack::Impl::GetSessionId() const {
  if (use_session_id_emulation_) {
    return {emulated_session_id_.load(), OperationResult::kSuccess};
  } else if (version_info_.has_legacy_emss) {
    return {kIgnoreSessionId, OperationResult::kSuccess};
  }
  return CAPICall<SessionId>(elementaryMediaTrackGetSessionId, handle_);
}

Result<bool> ElementaryMediaTrack::Impl::IsOpen() const {
  return CAPICall<bool>(elementaryMediaTrackIsOpen, handle_);
}

Result<void> ElementaryMediaTrack::Impl::RecycleTexture(GLuint textureId) {
  if (!version_info_.has_video_texture)
    return {OperationResult::kNotSupported};

  return CAPICall<void>(elementaryMediaTrackRecycleTexture, handle_, textureId);
}

Result<void> ElementaryMediaTrack::Impl::RegisterCurrentGraphicsContext() {
  if (!version_info_.has_video_texture)
    return {OperationResult::kNotSupported};

  return CAPICall<void>(elementaryMediaTrackRegisterCurrentGraphicsContext,
                        handle_);
}

Result<void> ElementaryMediaTrack::Impl::SetMediaKey(wasm::MediaKey* key) {
  return CAPICall<void>(elementaryMediaTrackSetMediaKey, handle_, key->handle_);
}

Result<void> ElementaryMediaTrack::Impl::SetListener(
    ElementaryMediaTrackListener* listener) {
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

// private:

Result<void> ElementaryMediaTrack::Impl::AppendPacketInternal(
    const ElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.session_id = kIgnoreSessionId;
  }
  return CAPICall<void>(elementaryMediaTrackAppendPacket, handle_,
                        &capi_packet);
}

Result<void> ElementaryMediaTrack::Impl::AppendPacketAsyncInternal(
    const ElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.session_id = kIgnoreSessionId;
  }
  return CAPICall<void>(elementaryMediaTrackAppendPacketAsync, handle_,
                        &capi_packet);
}

Result<void> ElementaryMediaTrack::Impl::AppendEncryptedPacketInternal(
    const EncryptedElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.base_packet.session_id = kIgnoreSessionId;
  }

  return CAPICall<void>(elementaryMediaTrackAppendEncryptedPacket, handle_,
                        &capi_packet);
}

Result<void> ElementaryMediaTrack::Impl::AppendEncryptedPacketAsyncInternal(
    const EncryptedElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.base_packet.session_id = kIgnoreSessionId;
  }

  return CAPICall<void>(elementaryMediaTrackAppendEncryptedPacketAsync, handle_,
                        &capi_packet);
}

OperationResult ElementaryMediaTrack::Impl::SetListenerInternal(
    ElementaryMediaTrackListener* listener) {
  if (listener) {
    LISTENER_OP(elementaryMediaTrackSetOnTrackOpen, handle_,
                ListenerCallback<ElementaryMediaTrackListener,
                                 &ElementaryMediaTrackListener::OnTrackOpen>,
                listener);
    LISTENER_OP(elementaryMediaTrackSetOnTrackClosed, handle_,
                OnTrackClosedListenerCallback, listener);
    LISTENER_OP(elementaryMediaTrackSetOnSeek, handle_, OnSeekListenerCallback,
                listener);
    LISTENER_OP(elementaryMediaTrackSetOnAppendError, handle_,
                OnAppendErrorListenerCallback, listener);

    if (!version_info_.has_legacy_emss) {
      LISTENER_OP(
          elementaryMediaTrackSetOnSessionIdChanged, handle_,
          ListenerCallback<ElementaryMediaTrackListener, SessionId,
                           &ElementaryMediaTrackListener::OnSessionIdChanged>,
          listener);
    }
  } else {
    LISTENER_OP(elementaryMediaTrackUnsetOnTrackOpen, handle_);
    LISTENER_OP(elementaryMediaTrackUnsetOnTrackClosed, handle_);
    LISTENER_OP(elementaryMediaTrackUnsetOnSeek, handle_);

    if (!version_info_.has_legacy_emss) {
      LISTENER_OP(elementaryMediaTrackUnsetOnSessionIdChanged, handle_);
    }
  }
  return OperationResult::kSuccess;
}

// session id emulation for legacy mode: private methods

void ElementaryMediaTrack::Impl::EmulateSessionIdChange() {
  assert(use_session_id_emulation_);
  // atomically increases session id
  SessionId new_sid = ++emulated_session_id_;

  if (listener_)
    listener_->OnSessionIdChanged(new_sid);
}

void ElementaryMediaTrack::Impl::RegisterSessionIdEmulationCallbacks() {
  CAPICall<void>(
      elementaryMediaTrackSetListenersForSessionIdEmulation, handle_,
      [](EMSSElementaryMediaTrackCloseReason reason, void* user_data) {
        auto thiz = static_cast<ElementaryMediaTrack::Impl*>(user_data);
        thiz->EmulateSessionIdChange();
      },
      this);
}

void ElementaryMediaTrack::Impl::UnregisterSessionIdEmulationCallbacks() {
  CAPICall<void>(elementaryMediaTrackUnsetListenersForSessionIdEmulation,
                 handle_);
}

/*============================================================================*/
/*= samsung::wasm::ElementaryMediaTrack:                                     =*/
/*============================================================================*/

ElementaryMediaTrack::ElementaryMediaTrack() = default;

ElementaryMediaTrack::ElementaryMediaTrack(int handle,
                                           EmssVersionInfo version_info,
                                           bool use_session_id_emulation)
    : pimpl_(std::make_unique<Impl>(handle,
                                    version_info,
                                    use_session_id_emulation)) {}

ElementaryMediaTrack::~ElementaryMediaTrack() = default;

ElementaryMediaTrack::ElementaryMediaTrack(ElementaryMediaTrack&&) = default;

ElementaryMediaTrack& ElementaryMediaTrack::operator=(ElementaryMediaTrack&&) =
    default;

bool ElementaryMediaTrack::IsValid() const {
  if (!pimpl_)
    return false;
  return pimpl_->IsValid();
}

Result<void> ElementaryMediaTrack::AppendPacket(
    const ElementaryMediaPacket& packet) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendPacket(packet);
}

Result<void> ElementaryMediaTrack::AppendPacketAsync(
    const ElementaryMediaPacket& packet) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendPacketAsync(packet);
}

Result<void> ElementaryMediaTrack::AppendEncryptedPacket(
    const EncryptedElementaryMediaPacket& packet) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendEncryptedPacket(packet);
}

Result<void> ElementaryMediaTrack::AppendEncryptedPacketAsync(
    const EncryptedElementaryMediaPacket& packet) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendEncryptedPacketAsync(packet);
}

Result<void> ElementaryMediaTrack::AppendEndOfTrack(SessionId session_id) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendEndOfTrack(session_id);
}

Result<void> ElementaryMediaTrack::AppendEndOfTrackAsync(SessionId session_id) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->AppendEndOfTrackAsync(session_id);
}

Result<void> ElementaryMediaTrack::FillTextureWithNextFrame(
    GLuint texture_id,
    std::function<void(OperationResult)> finished_callback) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->FillTextureWithNextFrame(texture_id,
                                          std::move(finished_callback));
}

Result<SessionId> ElementaryMediaTrack::GetSessionId() const {
  if (!pimpl_)
    return {kIgnoreSessionId, OperationResult::kInvalidObject};
  return pimpl_->GetSessionId();
}

Result<bool> ElementaryMediaTrack::IsOpen() const {
  if (!pimpl_)
    return {false, OperationResult::kInvalidObject};
  return pimpl_->IsOpen();
}

Result<void> ElementaryMediaTrack::RecycleTexture(GLuint textureId) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->RecycleTexture(textureId);
}

Result<void> ElementaryMediaTrack::RegisterCurrentGraphicsContext() {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->RegisterCurrentGraphicsContext();
}

Result<void> ElementaryMediaTrack::SetMediaKey(MediaKey* key) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->SetMediaKey(key);
}

Result<void> ElementaryMediaTrack::SetListener(
    ElementaryMediaTrackListener* listener) {
  if (!pimpl_)
    return {OperationResult::kInvalidObject};
  return pimpl_->SetListener(listener);
}

int ElementaryMediaTrack::GetHandle() const {
  return pimpl_ ? pimpl_->handle() : -1;
}

}  // namespace wasm
}  // namespace samsung
