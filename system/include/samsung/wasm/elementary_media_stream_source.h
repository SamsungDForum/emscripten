// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_H_
#define INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_H_

#include <cstdlib>
#include <functional>
#include <memory>
#include <string>

#include "samsung/wasm/common.h"
#include "samsung/wasm/elementary_media_track.h"
#include "samsung/wasm/emss_version_info.h"

namespace samsung {

namespace html {
class HTMLMediaElement;
}  // namespace html

namespace wasm {

class ElementaryMediaStreamSourceListener;
struct ElementaryAudioTrackConfig;
struct ElementaryVideoTrackConfig;

/// @mainpage
///
/// [TOC]
///
/// # Overview
///
/// Tizen WASM Player is a Samsung TV extension API which grants a WebAssembly
/// application low level access to a Platform's media player. WASM Player
/// operates on Elementary Stream Packet level, accepting encoded packets that
/// are decoded and rendered by the TV multimedia pipeline. Depending on
/// operation mode, it is fit to be used either as a video on-demand player
/// (normal latency mode, suitable for adaptive streaming scenarios) or as a
/// streaming player (low latency mode).
///
/// As a low level media API, WASM Player is responsible only for decoding and
/// rendering media content. Acquiring media content and splitting it into
/// Elementary Media Packets that are passed to the player is entirely dependent
/// on App. This allows for a great flexibility: the application has full
/// control over downloading data, demuxing, either low latency or adaptive
/// streaming protocol implementation, etc. When EMSS is used major part of
/// multimedia pipeline can be implemented as a WebAssembly module and it is
/// platform-independent, allowing for a wide variety of multimedia
/// applications.
///
/// # Online resources
///
/// * [Tizen WASM Player Docs on Samsung Developers](https://developer.samsung.com/smarttv/develop/extension-libraries/webassembly/tizen-wasm-player/overview.html)
/// * [Tizen WASM Player Sample (Normal Latency) on GitHub](https://github.com/SamsungDForum/WebAssemblyDemos/tree/master/wasm_player_sample)
/// * [Moonlight ported to TizenTV WASM (Low Latency) on GitHub](https://github.com/SamsungDForum/moonlight-chrome)

/// @brief
/// Main class of WASM Player. `ElementaryMediaStreamSource` acts as a *data
/// source* for `html::HTMLMediaElement`.
///
/// `ElementaryMediaStreamSource` manages a set of `ElementaryMediaTrack`
/// objects. `ElementaryMediaPacket`s that media consists of are sent to WASM
/// Player via individual tracks added to the source.
///
/// # Usage overview:
///
/// ## Setup
///
/// -# Create an instance of `html::HTMLMediaElement` and attach an object
///    implementing the `html::HTMLMediaElementListener` interface.
/// -# Create an instance of `ElementaryMediaStreamSource` and attach an object
///    implementing the `ElementaryMediaStreamSourceListener` interface.
/// -# Associate media element with source using
///    `html::HTMLMediaElement::SetSrc()`. This triggers source transition from
///    `ReadyState::kDetached` to `ReadyState::kClosed`.
/// -# Add `ElementaryMediaTrack`s that will provide data for the media stream
///    using `ElementaryMediaStreamSource::AddTrack()`.
///    - do not add tracks if they are not used (e.g. do not add audio track if
///      stream doesn't have audio),
///    - attach an instance of `ElementaryMediaTrackListener` interface
///      implementation to each track.
/// -# Set duration of the stream using
///    `ElementaryMediaStreamSource::SetDuration()`. This step is skipped if low
///    latency mode is used.
/// -# Call `ElementaryMediaStreamSource::Open()` to conclude setup. Setup is
///    complete once source changes state from `ReadyState::kClosed` to
///    `ReadyState::kOpen`.
///
/// ## Sending data for playback
///
/// `ElementaryMediaStreamSource` is a data source. It provides elementary media
/// data for Media Player to play. `html::MediaElement` is a playback control
/// element: it controls when media is to be played, paused, seeked, and so on.
///
/// Changing configuration of the source and sending data will cause
/// `HTMLMediaElement::ReadyState` to change. Similarly, interacting with
/// `html::MediaElement` will impact `ElementaryMediaStreamSource`. Application
/// should listen to `ElementaryMediaStreamSourceListener` and all
/// `ElementaryMediaTrackListener`s and react accordingly.
///
/// Most notably, changes in both source and track states will inform
/// application when it should send elementary media data to Media Player for
/// playback:
/// * when the source enters `ReadyState::kOpen` (and each track receives
///  `ElementaryMediaTrackListener::OnTrackOpen()`) Media Player is ready to
///  accept data,
/// * when the source leaves `ReadyState::kOpen` (and each track receives
///  `ElementaryMediaTrackListener::OnTrackClosed()`) Media Player won't accept
///  any more data.
///
/// @note It's recommended to use `ElementaryMediaTrackListener` to track when
///       data should be sent to Media Player.
///
/// A single `ElementaryMediaPacket` is sent to Media Player using the
/// `ElementaryMediaTrack::AppendPacket()` method.
///
/// ### Sending data in the normal mode
///
/// When `Mode::kNormal` is used, App should track current playback position
/// using `ElementaryMediaStreamSourceListener::OnPlaybackPositionChanged()`.
/// Media Player uses buffering in this mode to ensure playback is smooth and
/// App can use current playback position information to ensure packet buffer
/// underrun doesn't happen:
/// * for clear (non-encrypted) content playback at most 64 MiB of data can be
///   buffered,
/// * for DRM-protected content playback at most 10 MiB of data can be buffered,
/// * for audio track at most 768 KiB of data can be buffered,
/// * App can buffer up to 3 seconds of content ahead of the current playback
///   position.
///
/// ### Sending data in the low latency mode
///
/// When `Mode::kLowLatency` is used, Media Player will render packets
/// immediately after they are sent. No internal buffering happens in Media
/// Player. Since this mode is intended for live sources, usually it's a good
/// idea to hand packets to the source right after they are received by App.
///
/// @sa [Detailed WASM Player Usage Guide on Samsung Developers](https://developer.samsung.com/smarttv/develop/extension-libraries/webassembly/tizen-wasm-player/usage-guide.html)
class ElementaryMediaStreamSource final {
 public:
  /// Defines modes in which `ElementaryMediaStreamSource` can operate. The mode
  /// is set in `ElementaryMediaStreamSource`'s constructor and cannot be
  /// changed during its lifetime.
  enum class Mode {
    /// This is a default mode, appropriate for most playback scenarios (most
    /// notably on-demand video playback).
    ///
    /// Pipeline clock is controlled by the Platform when WASM Player works in
    /// normal latency mode. `ElementaryMediaPacket`s will be buffered by
    /// Platform until they can be rendered according to their pts values.
    ///
    /// Platform guarantees smooth media playback when working in this mode,
    /// provided packets are delivered to the Source on time (i.e. internal
    /// buffer overrun doesn't happen).
    kNormal,

    /// This mode is appropriate for low latency playback scenarios (live
    /// streaming).
    ///
    /// Pipeline clock is controlled by the application when the player works
    /// in low latency mode. Source will render appended packets as soon as
    /// possible and won't perform any internal buffering. Pipeline clock is set
    /// according to the pts values of appended packets.
    ///
    /// @remarks
    /// - the application is responsible for maintaining stream synchronization,
    /// - packets are rendered as soon as possible, so fps is dependent entirely
    ///   on when packets are appended,
    /// - media element's time is calculated based on packets' pts values, so
    ///   they should be set correctly,
    /// - packets should be tuned for low latency playback (e.g. B-frames are
    ///   not allowed in video streams).
    kLowLatency,

    /// This mode makes WASM Player decode video packets into GL textures so
    /// that they can be renderer by App using OpenGL. Video is not displayed on
    /// the associated `HTMLMediaElement`.
    ///
    /// Source will buffer packets until they can be rendered according to their
    /// pts values. Buffered packets will be decoded and put into GL textures.
    /// Application should constantly request for new pictures by calling
    /// `ElementaryMediaTrack::FillTextureWithNextFrame()` method. This method
    /// is called by Platform when the texture should be displayed, so the
    /// application should render the texture immediately. After the texture is
    /// rendered, it should be released with the
    /// `ElementaryMediaTrack::RecycleTexture()` method.
    ///
    /// When this mode is set, Player behaves as in the `kNormal` mode in terms
    /// of available operations, stream synchronization and pipeline clock
    /// management.
    ///
    /// @remark
    /// This mode is supported only on devices which have
    /// `EmssVersionInfo::has_video_texture` set to `true`.
    kVideoTexture
  };

  /// Enumerates all possible states of `ElementaryMediaStreamSource`. Current
  /// ready state of EMSS can be retrieved with `GetReadyState()` method and its
  /// change is signaled by `ElementaryMediaStreamSourceListener`.
  ///
  /// @attention
  /// `ElementaryMediaStreamSource` and `html::HTMLMediaElement` states should
  /// not be confused. `ElementaryMediaStreamSource` represents a state of the
  /// *source* of data, while `html::HTMLMediaElement` represents a state of the
  /// multimedia player. As such, `ElementaryMediaStreamSource` will signal App
  /// whether or not multimedia pipeline needs data and can accept
  /// `ElementaryMediaPacket`s. This is not in sync with the multimedia player
  /// state.
  ///
  /// For example, a Source that is in the `ReadyState::kEnded` state can be
  /// associated with a still-playing Media Element. This will occur in Normal
  /// Latency mode when App signals end of all tracks but multimedia pipeline
  /// has buffered `ElementaryMediaPacket`s that were not displayed yet.
  enum class ReadyState {
    /// Not attached to `html::HTMLMediaElement`. This is the initial state of
    /// `ElementaryMediaStreamSource` object. It is also entered after detaching
    /// from `html::HTMLMediaElement`.
    kDetached,

    /// Tracks are not configured and player is not initialized. Can't play in
    /// this state. `ElementaryMediaTrack` objects can be added to and removed
    /// from `ElementaryMediaStreamSource`. Track layout can be changed *only*
    /// in this state.
    ///
    /// This state will be entered when:
    /// - `ElementaryMediaStreamSource` is attached to `html::HTMLMediaElement`,
    /// - App requests it by calling `Close()`,
    /// - unrecoverable playback error occurs (this will also cause
    ///   `html::HTMLMediaElementListener::OnError()` to fire).
    kClosed,

    /// `kOpen` state was requested, but pipeline state prevents entering it.
    /// State will change to `ReadyState::kOpen` as soon as possible.
    ///
    /// This state can be entered both from the `ReadyState::kClosed` state
    /// (when opening of Source is requested) and from the `ReadyState::kOpen`
    /// state (when pipeline can't accept ES data temporarily, for example
    /// during Seek).
    kOpenPending,

    /// Player is fully initialized and `ElementaryMediaStreamSource` is ready
    /// to accept `ElementaryMediaPacket` data from App via
    /// `ElementaryMediaTrack` objects.
    ///
    /// When App finishes configuring tracks, it can request entering this state
    /// by calling `Open()`. This state will be entered when possible.
    ///
    /// When `ReadyState::kOpen` is the target state of a source, it's possible
    /// the `ReadyState::kOpenPending` state will be entered temporarily. This
    /// happens when `ElementaryMediaStreamSource` is opening or as a result of
    /// some operations (e.g. Seek).
    kOpen,

    /// Stream has ended but multimedia pipeline remains initialized. Playback
    /// can still be restarted, for example by seek.
    ///
    /// This state is entered when App marks active `ElementaryMediaTrack`
    /// objects as ended. The `ReadyState::kEnded` state reverts to the
    /// `ReadyState::kOpen` state when multimedia pipeline resumes playback
    /// (e.g. due to Seek).
    kEnded
  };

  /// Creates a source with the given mode. Mode cannot be changed during
  /// lifetime of the object.
  ///
  /// @param[in] mode Create a source that uses specified playback mode.
  explicit ElementaryMediaStreamSource(Mode mode = Mode::kNormal);
  ElementaryMediaStreamSource(const ElementaryMediaStreamSource&) = delete;
  ElementaryMediaStreamSource(ElementaryMediaStreamSource&&);
  ElementaryMediaStreamSource& operator=(const ElementaryMediaStreamSource&) =
      delete;
  ElementaryMediaStreamSource& operator=(ElementaryMediaStreamSource&&);
  ~ElementaryMediaStreamSource();

  /// Returns `true` if source instance is valid. This method should be called
  /// after constructor to ensure backend initialized the object properly. If
  /// source is invalid all method calls will fail.
  ///
  /// @return `true` if source instance is valid, otherwise `false`.
  bool IsValid() const;

  /// Adds an audio track to the source.
  ///
  /// @param[in] config A config describing track.
  ///
  /// @return `Result<ElementaryMediaTrack>` with `operation_result` field set
  /// to `OperationResult::kSuccess` and a valid `ElementaryMediaTrack` object
  /// on success, otherwise a code describing the error.
  ///
  /// @remarks
  /// - Tracks can only be added in `kClosed` state.
  /// - Only one track of each type can be held by the source at any given time.
  /// - Audio parameters cannot be changed during the lifetime of the track.
  Result<ElementaryMediaTrack> AddTrack(const ElementaryAudioTrackConfig&);

  /// Adds a video track to the source.
  ///
  /// @param[in] config A config describing track.
  ///
  /// @return `Result<ElementaryMediaTrack>` with `operation_result` field set
  /// to `OperationResult::kSuccess` and a valid `ElementaryMediaTrack` object
  /// on success, otherwise a code describing the error.
  ///
  /// @remarks
  /// - Tracks can only be added in `kClosed` state.
  /// - Only one track of each type can be held by the source at any given time.
  /// - As opposed to audio track, some video parameters can change during
  ///   playback, notably resolution or framerate, by passing packets with new
  ///   resolution/fps values.
  Result<ElementaryMediaTrack> AddTrack(const ElementaryVideoTrackConfig&);

  /// Removes a track from the source. After the operation removed track is
  /// still valid and can be re-added to the source again.
  ///
  /// @param[in] track Track to remove.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @remarks
  /// - Tracks can only be removed in `kClosed` state.
  Result<void> RemoveTrack(const ElementaryMediaTrack&);

  /// Flushes internal packets' buffers, causing `ElementaryMediaTrack`s
  /// belonging to this Source to drop all packets appended so far.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> Flush();

  /// Closes the source asynchronously. When the operation is done, the source
  /// will be in `ReadyState::kClosed` state and a callback passed as the
  /// argument will be called. During that time it's impossible to request
  /// another ready state change.
  ///
  /// @param[in] on_finished_callback A callback notifying end of `Close()`. The
  /// callback receives `OperationResult` informing of the result of the
  /// operation.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> Close(std::function<void(OperationResult)> on_finished_callback);

  /// Starts an asynchronous opening operation. When the operation is done,
  /// the source will be in `ReadyState::kOpen` state and a callback passed as
  /// the argument will be called. During that time it's impossible to request
  /// another ready state change.
  ///
  /// @param[in] on_finished_callback A callback notifying end of `Open()`. The
  /// callback receives `OperationResult` informing of the result of the
  /// operation.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  ///
  /// @remarks This should be called when all tracks are added and configured,
  /// and the application is ready to provide data for the source.
  Result<void> Open(std::function<void(OperationResult)> on_finished_callback);

  /// Returns the duration of the source.
  ///
  /// @return `Result<::Seconds>` with `operation_result` field set to
  /// `OperationResult::kSuccess` and a valid `::Seconds` object representing
  /// duration of the source on success, otherwise a code describing the error.
  Result<Seconds> GetDuration() const;

  /// Sets the duration of the source. Note that this operation is unavailable
  /// in `Mode::kLowLatency` mode.
  ///
  /// @param[in] new_duration Duration to be set.
  ///
  /// @return `Result<void>` with `operation_result` field set to
  /// `OperationResult::kSuccess` on success, otherwise a code describing the
  /// error.
  Result<void> SetDuration(Seconds new_duration);

  /// Returns the mode of the source, as set during object construction.
  ///
  /// @return `Result<ElementaryMediaStreamSource::Mode>` with
  /// `operation_result` field set to `OperationResult::kSuccess` and a valid
  /// `Mode` representing mode of the source on success, otherwise a code
  /// describing the error.
  Result<Mode> GetMode() const;

  /// Returns current `ReadyState` of the source.
  ///
  /// @return `Result<ReadyState>` with `operation_result` field set to
  /// `OperationResult::kSuccess` and a valid `ReadyState` representing current
  /// ready state of the source on success, otherwise a code describing the
  /// error.
  Result<ReadyState> GetReadyState() const;

  /// Sets a listener to receive updates about EMSS's state changes. Only one
  /// listener can be set: setting another clears the previous one. Pass
  /// `nullptr` to reset the listener
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
  /// @sa `ElementaryMediaStreamSourceListener`
  Result<void> SetListener(ElementaryMediaStreamSourceListener* listener);

  /// Returns the source's URL received from `URL.createObjectURL`
  /// WebAPI. The URL is bound to the source's lifetime and will be revoked
  /// automatically.
  ///
  /// @return c-style string containing the URL. Ownership is not transferred
  /// and the string is valid as long as this object is alive.
  const char* GetURL() const;

 private:
  void SetHTMLMediaElement(html::HTMLMediaElement*);
  OperationResult SetListenerInternal(
      ElementaryMediaStreamSourceListener* listener);

  int handle_;
  html::HTMLMediaElement* html_media_element_;
  ElementaryMediaStreamSourceListener* listener_;
  std::unique_ptr<char, decltype(&std::free)> url_;
  bool use_session_id_emulation_;
  EmssVersionInfo version_info_;

  friend class html::HTMLMediaElement;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ELEMENTARY_MEDIA_STREAM_SOURCE_H_
