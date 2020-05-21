// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_
#define INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_

namespace samsung {
namespace wasm {

/// Enumerates possible outcomes of WASM function calls.
enum class OperationResult {
  kSuccess = 0,         ///< Operation ended with success.
  kWrongHandle,         ///< Method was called on an invalid object.
  kInvalidArgument,     ///< Method was called with an invalid argument.
  kListenerAlreadySet,  ///< This object already has a listener.
  kNoSuchListener,      ///< This object doesn't have a listener.
  kNotSupported,        ///< This functionality is not supported on a device.
  kFailed,              ///< Operation failed for an unknown reason.
};

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_OPERATION_RESULT_H_
