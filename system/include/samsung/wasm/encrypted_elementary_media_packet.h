// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_ENCRYPTED_ELEMENTARY_MEDIA_PACKET_H_
#define INCLUDE_SAMSUNG_WASM_ENCRYPTED_ELEMENTARY_MEDIA_PACKET_H_

#include <cstdint>
#include <vector>

#include "samsung/wasm/common.h"
#include "samsung/wasm/elementary_media_packet.h"
#include "samsung/wasm/media_key.h"

namespace samsung {
namespace wasm {

struct EncryptedSubsampleDescription {
  uint32_t clear_block;
  uint32_t cipher_block;
};

/// Type representing a single *encrypted* packet (either video or audio).
struct EncryptedElementaryMediaPacket : public ElementaryMediaPacket {
  /// Array of descriptions of subsamples of which given packet consists of.
  ///
  /// @sa `EncryptedSubsampleDescription`
  std::vector<EncryptedSubsampleDescription> subsamples;

  /// ID of the key (KID) needed to decrypt the packet.
  std::vector<uint8_t> key_id;

  /// Initialization Vector (IV) needed to decrypt the packet.
  std::vector<uint8_t> initialization_vector;

  /// Type of initialization data used for encryption.
  EncryptionMode encryption_mode;
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_ENCRYPTED_ELEMENTARY_MEDIA_PACKET_H_
