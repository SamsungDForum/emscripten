// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_MEDIA_KEY_H_
#define INCLUDE_SAMSUNG_WASM_MEDIA_KEY_H_

#include <cstdint>
#include <functional>
#include <string>
#include <vector>

#include "samsung/wasm/common.h"

namespace samsung {
namespace wasm {

/// Lists supported encryption modes.
enum class EncryptionMode {
  kUnknown,  ///< Unknown encryption mode.
  kCenc,     ///< Full sample encryption AESCTR mode.
  kCbcs,     ///< Pattern encryption AESCBC mode.
};

/// Lists supported Content Decryption Modules.
enum class ContentDecryptionModule {
  kUnknown,    ///< Unknonw CDM.
  kPlayready,  ///< Playready CDM.
  kWidevine,   ///< Widevine classic CDM.
};

/// Lists supported robustness levels.
enum class Robustness {
  kEmpty,
  kSWSecureCrypto,
  kSWSecureDecode,
  kHWSecureCrypto,
  kHWSecureDecode,
  kHWSecureAll,
};

/// Aggregates all necessary data for setting up decryption.
struct DRMConfig {
  /// CDM used by content.
  ContentDecryptionModule cdm;

  /// Encryption mode used by content.
  EncryptionMode encryption_mode;

  /// URL of license server providing keys to decrypt media.
  std::string license_server;

  /// Buffer containing DRM-specific initialization data.
  std::vector<uint8_t> init_data;

  /// Mime type of encrypted audio or empty string if audio is not encrypted.
  std::string audio_mime_type;

  /// Robustness of audio track. Unused if audio is not encrypted.
  Robustness audio_robustness;

  /// Mime type of encrypted video or empty string if video is not encrypted.
  std::string video_mime_type;

  /// Robustness of video track. Unused if video is not encrypted.
  Robustness video_robustness;
};

/// Class representing an instance of media keys used to decrypt a content.
class MediaKey final {
 public:
  /// @copydoc ElementaryMediaStreamSource::AsyncResult
  enum class AsyncResult {
    kSuccess,                    ///< Operation ended with success.
    kInvalidConfigurationError,  ///< Configuration was invalid.
    kSessionNotUpdatedError,     ///< Attempt to update the session failed.
    kUnknownError,               ///< Unknown error.
  };

  using SetupFinishedCallback = std::function<void(AsyncResult, MediaKey)>;

  MediaKey(const MediaKey&) = delete;
  MediaKey(MediaKey&& other);
  MediaKey& operator=(const MediaKey&) = delete;
  MediaKey& operator=(MediaKey&&);
  ~MediaKey();

  /// Returns <code>true</code> if this instance is valid. This method should
  /// be called after constructor to ensure backend initialized the object
  /// properly. If object is invalid all method calls will fail.
  ///
  /// @return <code>true</code> if this instance is valid, otherwise
  /// <code>false</code>.
  bool IsValid() const;

  /// Asynchronously creates MediaKey instance and passes it as an argument to
  /// <code>on_finished</code>. If setting up the encryption fails, media keys
  /// won't be valid.
  ///
  /// @param[in] config An object containing DRM's configuration.
  /// @param[in] on_finished A callback notifying end of setting up encryption.
  /// The callback receives <code>#AsyncResult</code> informing of the
  /// result of the operation and a newly created <code>MediaKeys</code> object.
  ///
  /// @return <code>Result\<void\></code> with
  /// <code>operation_result</code> field set to
  /// <code>OperationResult::kSuccess</code> on success, otherwise a code
  /// describing the error.
  static Result<void> SetupEncryption(const DRMConfig& config,
                                      SetupFinishedCallback on_finished);

 private:
  struct AsyncImpl;

  explicit MediaKey(int handle);

  int handle_;

  // access to handle_
  friend class ElementaryMediaTrack;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_MEDIA_KEY_H_
