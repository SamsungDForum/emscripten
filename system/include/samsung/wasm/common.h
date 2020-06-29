// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_WASM_COMMON_H_
#define INCLUDE_SAMSUNG_WASM_COMMON_H_

#include <chrono>

#include "samsung/wasm/operation_result.h"

namespace samsung {
namespace wasm {

/// Helper type which carries both an error code and return value of an
/// operation.
template <class T>
struct Result {
  /// A value returned by an operation, valid only if `operation_result` is
  /// equal to `OperationResult::kSuccess`. Defined if `T` is not `void`.
  T value;

  /// Operation result.
  OperationResult operation_result;

  /// Checks if the operation ended with success.
  explicit operator bool() const noexcept;

  /// Returns `Result<T>::value`. Defined if `T` is not `void`.
  T& operator*();

  /// @copydoc Result::operator*()
  const T& operator*() const;

  /// Accesses `Result<T>::value`. Defined if `T` is not `void`.
  T* operator->();

  /// @copydoc Result::operator->()
  const T* operator->() const;
};

/// @cond 0
template <>
struct Result<void> {
  OperationResult operation_result;

  explicit operator bool() const noexcept;
};
/// @endcond

/// Default duration type used throughout the API.
using Seconds = std::chrono::duration<double>;

template <class T>
Result<T>::operator bool() const noexcept {
  return static_cast<bool>(Result<void>{operation_result});
}

inline Result<void>::operator bool() const noexcept {
  return operation_result == OperationResult::kSuccess;
}

template <class T>
T& Result<T>::operator*() {
  return const_cast<T&>(static_cast<const Result<T>*>(this)->operator*());
}

template <class T>
const T& Result<T>::operator*() const {
  return value;
}

template <class T>
T* Result<T>::operator->() {
  return const_cast<T*>(static_cast<const Result<T>*>(this)->operator->());
}

template <class T>
const T* Result<T>::operator->() const {
  return &value;
}

}  // namespace wasm
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_WASM_COMMON_H_
