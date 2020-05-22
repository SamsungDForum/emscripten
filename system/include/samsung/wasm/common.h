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

/// Helper type to carry both an error code and return value.
template <class T>
struct Result {
  /// Return value of an operation, only valid if
  /// <code>operation_result == OperationResult::kSuccess</code>.
  /// Defined if <code>T</code> is not <code>void</code>
  T value;

  /// Operation result.
  OperationResult operation_result;

  /// Checks if the operation ended with success.
  explicit operator bool() const noexcept;

  /// Returns <code>Result::value</code>.
  /// Defined if <code>T</code> is not <code>void</code>
  T& operator*();

  /// @copydoc Result::operator*()
  const T& operator*() const;

  /// Accesses <code>Result::value</code>.
  /// Defined if <code>T</code> is not <code>void</code>
  T* operator->();

  /// @copydoc Result::operator->()
  const T* operator->() const;
};

class JsHandle {
 public:
  JsHandle() : handle_(-1) {}
  JsHandle(int handle) : handle_(handle) {}
  JsHandle(const JsHandle&) = delete;
  JsHandle& operator=(const JsHandle&) = delete;
  JsHandle(JsHandle&& other) : handle_(other.handle_) {
    other.handle_ = 0;
  }
  JsHandle& operator=(JsHandle&& other) {
    handle_ = other.handle_;
    other.handle_ = 0;
  }
  operator int() const { return handle_; }
  bool IsValid() const { return handle_ >= 0; }
 private:
  int handle_;
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
