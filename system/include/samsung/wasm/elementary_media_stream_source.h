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

/// @brief
/// Main class of WASM Player. <code>ElementaryMediaStreamSource</code> acts as
/// a data source for <code>HTMLMediaElement</code>.
///
/// <code>ElementaryMediaStreamSource</code> manages a set of <code>
/// ElementaryMediaTrack</code> objects. <code>ElementaryMediaPacket</code>s
/// that media consists of are sent to WASM Player via individual tracks added
/// to the source.
class ElementaryMediaStreamSource final {
 public:
  /// Defines modes in which <code>ElementaryMediaStreamSource</code> can
  /// operate. The mode is set in <code>ElementaryMediaStreamSource</code>'s
  /// constructor and cannot be changed during its lifetime.
  enum class Mode {
    /// This mode is a default mode, appropriate for most playback scenarios.
    /// <br>
    /// Pipeline clock is controlled by the platform player when the player
    /// works in normal latency mode. Source will buffer packets until they
    /// can be rendered according to their pts values.
    kNormal,

    /// This mode is appropriate for low latency playback scenarios.
    /// <br>
    /// Pipeline clock is controlled by the application when the player works
    /// in low latency mode. Source will render appended packets as soon as
    /// possible and won't perform any internal buffering. Pipeline clock is set
    /// according to the pts values of appended packets.
    /// @remarks
    /// - the application is responsible for maintaining stream synchronization,
    /// - packets are rendered as soon as possible, so fps is dependent entirely
    ///   on when packets are appended,
    /// - media element's time is calculated based on packets' pts values, so
    ///   they should be set correctly,
    /// - packets should be tuned for low latency playback (e.g. B-frames are
    ///   not allowed in video streams).
    kLowLatency,

    /// This mode is appropriate for decoding video into GL texture scenarios.
    /// <br>
    /// Pipeline clock is controlled by the platform player. Source will buffer
    /// packets until they can be rendered according to their pts values and
    /// they will be decoded and put into GL texture. Application should
    /// constantly request for new pictures by calling
    /// <code>ElementaryMediaTrack::FillTextureWithNextFrame()</code> method.
    /// After texture is rendered, application needs to call
    /// <code>ElementaryMediaTrack::recycleTexture()</code>' method.
    ///
    /// @remark
    /// This mode is supported on devices which have
    /// <code>EmssVersionInfo::has_video_texture</code> set to
    /// <code>true</code>.
    kVideoTexture
  };

  /// Enumerates all possible states of
  /// <code>ElementaryMediaStreamSource</code>. Current ready state of EMSS can
  /// be retrieved with <code>GetReadyState()</code> method, and its change is
  /// signalled by <code>ElementaryMediaStreamSourceListener</code>.
  ///
  /// @attention
  /// <code>ElementaryMediaStreamSource</code> and
  /// <code>html::HTMLMediaElement</code> states should not be confused.
  /// <code>ElementaryMediaStreamSource</code> represents state of a
  /// <b>source</b> of data, while <code>html::HTMLMediaElement</code>
  /// represents state of a multimedia player. As such,
  /// <code>ElementaryMediaStreamSource</code> will signal App whether or not
  /// multimedia pipeline needs data and can accept Elementary Media Packets.
  /// This is not in sync with multimedia player state.
  /// <br>
  /// For example, a <code>ReadyState::kEnded</code> source can be associated
  /// with a still-playing Media Element. This will occur in Normal Latency mode
  /// when App signals end of all tracks but multimedia pipeline has buffered
  /// Elementary Media Packets remaining to play.
  enum class ReadyState {
    /// Not attached to <code>html::HTMLMediaElement</code>. This is the initial
    /// state of <code>ElementaryMediaStreamSource</code> object. It is also
    /// entered after disconnecting from <code>html::HTMLMediaElement</code>.
    kDetached,

    /// Tracks are not configured and player is not initialized. Can't play in
    /// this state. <code>ElementaryMediaTrack</code> objects can be added to
    /// and removed from <code>ElementaryMediaStreamSource</code>. Track layout
    /// can be changed <b>only</b> in this state.
    /// <br>
    /// This state will be entered after
    /// <code>ElementaryMediaStreamSource</code> is attached to
    /// <code>html::HTMLMediaElement</code>, when unrecoverable playback error
    /// occurs or on App request.
    kClosed,

    /// <code>kOpen</code> state was requested, but pipeline state prevents
    /// entering it. State will change to <code>ReadyState::kOpen</code> when
    /// possible.
    /// <br>
    /// This state can be entered both from <code>ReadyState::kClosed</code>
    /// state (when opening of Source is requested) and from
    /// <code>ReadyState::kOpen</code> state (when pipeline can't accept ES data
    /// temporarily).
    kOpenPending,

    /// Player is fully initialized and Elementary Media Stream Source is ready
    /// to accept Elementary Packet Data from App via
    /// <code>ElementaryMediaTrack</code> objects.
    /// <br>
    /// When App finishes configuring tracks, it can request entering this
    /// state. Open state will be entered when possible. Some operations (like
    /// seek) will trigger a temporary transition to
    /// <code>ReadyState::kOpenPending</code> state.
    kOpen,

    /// Stream has ended but multimedia pipeline remains initialized. Playback
    /// can still be restarted, for example by seek.
    /// <br>
    /// This state is entered when App marks active
    /// <code>ElementaryMediaTrack</code> objects as ended.
    /// <code>ReadyState::kEnded</code> state will revert to
    /// <code>ReadyState::kOpen</code> when multimedia pipeline resumes playback
    /// (e.g. due to Seek).
    kEnded
  };

  /// Creates a source with the given mode. Mode cannot be changed during
  /// lifetime of the object.
  ///
  /// @param[in] latency_mode Create a source that uses specified playback mode.
  explicit ElementaryMediaStreamSource(Mode latency_mode = Mode::kNormal);
  ElementaryMediaStreamSource(const ElementaryMediaStreamSource&) = delete;
  ElementaryMediaStreamSource(ElementaryMediaStreamSource&&);
  ElementaryMediaStreamSource& operator=(const ElementaryMediaStreamSource&) =
      delete;
  ElementaryMediaStreamSource& operator=(ElementaryMediaStreamSource&&);
  ~ElementaryMediaStreamSource();

  /// Returns <code>true</code> if source instance is valid. This method should
  /// be called after constructor to ensure backend initialized the object
  /// properly. If source is invalid all method calls will fail.
  ///
  /// @return <code>true</code> if source instance is valid, otherwise
  /// <code>false</code>.
  bool IsValid() const;

  /// Adds an audio track to the source.
  ///
  /// @param[in] config A config describing track.
  ///
  /// @return <code>Result\<ElementaryMediaTrack\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>ElementaryMediaTrack</code> object on success, otherwise a code
  /// describing the error.
  ///
  /// @remarks
  /// - Tracks can only be added in <code>kClosed</code> state.
  /// - Only one track of each type can be held by the source at any given time.
  /// - Audio parameters cannot be changed during the lifetime of the track.
  Result<ElementaryMediaTrack> AddTrack(const ElementaryAudioTrackConfig&);

  /// Adds a video track to the source.
  ///
  /// @param[in] config A config describing track.
  ///
  /// @return <code>Result\<ElementaryMediaTrack\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>ElementaryMediaTrack</code> object on success, otherwise a code
  /// describing the error.
  ///
  /// @remarks
  /// - Tracks can only be added in <code>kClosed</code> state.
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
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @remarks
  /// - Tracks can only be removed in <code>kClosed</code> state.
  Result<void> RemoveTrack(const ElementaryMediaTrack&);

  /// Flushes internal packets' buffers, causing them to drop appended packets.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> Flush();

  /// Closes the source asynchronously. When the operation is done, the source
  /// will be in <code>ReadyState::kClosed</code> state and a callback passed
  /// as the argument will be called. During that time it's impossble to request
  /// another ready state change.
  ///
  /// @param[in] on_finished_callback A callback notifying end of close.
  /// The callback receives <code>OperationResult</code> informing of the
  /// result of the operation.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> Close(std::function<void(OperationResult)> on_finished_callback);

  /// Starts an asynchronous opening operation. When the operation is done,
  /// the source will be in <code>ReadyState::kOpen</code> state and a
  /// callback passed as the argument will be called. During that time it's
  /// impossble to request another ready state change.
  ///
  /// @param[in] on_finished_callback A callback notifying end of open.
  /// The callback receives <code>OperationResult</code> informing of the
  /// result of the operation.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @remarks This should be called when all tracks are added and configured,
  /// and the application is ready to provide data for the source.
  Result<void> Open(std::function<void(OperationResult)> on_finished_callback);

  /// Returns the duration of the source.
  ///
  /// @return <code>Result\<::Seconds\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>::Seconds</code> object representing duration of the source
  /// on success, otherwise a code describing the error.
  Result<Seconds> GetDuration() const;

  /// Sets the duration of the source. Note that this operation is unavailable
  /// in Mode::kLowLatency mode.
  ///
  /// @param[in] new_duration Duration to be set.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  Result<void> SetDuration(Seconds new_duration);

  /// Returns the mode of the source, as set in constructor.
  ///
  /// @return <code>Result\<#Mode\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>#Mode</code> representing mode of the source
  /// on success, otherwise a code describing the error.
  Result<Mode> GetMode() const;

  /// Returns current ready state of the source.
  ///
  /// @return <code>Result\<#ReadyState\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> and a valid
  /// <code>#ReadyState</code> representing current ready state of the source
  /// on success, otherwise a code describing the error.
  Result<ReadyState> GetReadyState() const;

  /// Sets a listener to receive updates about EMSS's state changes. Only one
  /// listener can be set: setting another clears the previous one. Pass <code>
  /// nullptr</code> to reset the listener
  ///
  /// @param[in] listener Listener to be set or <code>nullptr</code> to unset
  /// the listener.
  ///
  /// @warning The ownership isn't transferred, and, as such,
  /// the listener must outlive the source.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  ///
  /// @sa ElementaryMediaStreamSourceListener
  Result<void> SetListener(ElementaryMediaStreamSourceListener* listener);

  /// Returns the source's URL received from <code>URL.createObjectURL</code>
  /// WebAPI. The URL is bound to the source's lifetime and will be revoked
  /// automatically.
  ///
  /// @return c-style string containing the URL.
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
