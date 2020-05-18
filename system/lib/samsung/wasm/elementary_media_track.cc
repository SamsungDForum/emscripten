// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/wasm/elementary_media_track.h"

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
    EMSSElementaryMediaTrackCloseReason close_reason, void* user_data) {
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

}  // namespace

namespace samsung {
namespace wasm {

ElementaryMediaTrack::ElementaryMediaTrack()
    : ElementaryMediaTrack(-1, EmssVersionInfo::Create()) {}

ElementaryMediaTrack::ElementaryMediaTrack(int handle,
                                           EmssVersionInfo version_info)
    : handle_(handle), version_info_(version_info) {}

ElementaryMediaTrack::ElementaryMediaTrack(ElementaryMediaTrack&& other)
    : handle_(std::exchange(other.handle_, -1)),
      version_info_(other.version_info_) {}

ElementaryMediaTrack& ElementaryMediaTrack::operator=(
    ElementaryMediaTrack&& other) {
  handle_ = std::exchange(other.handle_, -1);
  version_info_ = other.version_info_;
  return *this;
}

ElementaryMediaTrack::~ElementaryMediaTrack() {
  if (IsValid()) {
    elementaryMediaTrackRemove(handle_);
  }
}

bool ElementaryMediaTrack::IsValid() const { return IsHandleValid(handle_); }

Result<void> ElementaryMediaTrack::AppendPacket(
    const samsung::wasm::ElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.session_id = kIgnoreSessionId;
  }

  return CAPICall<void>(elementaryMediaTrackAppendPacket, handle_,
                        &capi_packet);
}

Result<void> ElementaryMediaTrack::AppendEncryptedPacket(
    const EncryptedElementaryMediaPacket& packet) {
  auto capi_packet = PacketToCAPI(packet);

  if (version_info_.has_legacy_emss) {
    // Legacy EMSS didn't support session_id concept.
    capi_packet.base_packet.session_id = kIgnoreSessionId;
  }

  return CAPICall<void>(elementaryMediaTrackAppendEncryptedPacket, handle_,
                        &capi_packet);
}

Result<void> ElementaryMediaTrack::AppendEndOfTrack(SessionId app_session_id) {
  // Legacy EMSS didn't support session_id concept.
  auto session_id =
      (version_info_.has_legacy_emss ? kIgnoreSessionId : app_session_id);
  return CAPICall<void>(elementaryMediaTrackAppendEndOfTrack, handle_,
                        session_id);
}

Result<SessionId> ElementaryMediaTrack::GetSessionId() const {
  if (version_info_.has_legacy_emss) {
    Result<SessionId> result;
    result.operation_result = OperationResult::kSuccess;
    result.value = kIgnoreSessionId;
    return result;
  }
  return CAPICall<SessionId>(elementaryMediaTrackGetSessionId, handle_);
}

Result<bool> ElementaryMediaTrack::IsOpen() const {
  return CAPICall<bool>(elementaryMediaTrackIsOpen, handle_);
}

Result<void> ElementaryMediaTrack::SetMediaKey(wasm::MediaKey* key) {
  return CAPICall<void>(elementaryMediaTrackSetMediaKey, handle_, key->handle_);
}

Result<void> ElementaryMediaTrack::SetListener(
    ElementaryMediaTrackListener* listener) {
  SET_LISTENER(elementaryMediaTrackSetOnTrackOpen, handle_,
               ListenerCallback<ElementaryMediaTrackListener,
                                &ElementaryMediaTrackListener::OnTrackOpen>,
               listener);
  SET_LISTENER(elementaryMediaTrackSetOnTrackClosed, handle_,
               OnTrackClosedListenerCallback, listener);
  SET_LISTENER(elementaryMediaTrackSetOnSeek, handle_, OnSeekListenerCallback,
               listener);
  SET_LISTENER(
      elementaryMediaTrackSetOnSessionIdChanged, handle_,
      ListenerCallback<ElementaryMediaTrackListener, SessionId,
                       &ElementaryMediaTrackListener::OnSessionIdChanged>,
      listener);
  return {OperationResult::kSuccess};
}

}  // namespace wasm
}  // namespace samsung
