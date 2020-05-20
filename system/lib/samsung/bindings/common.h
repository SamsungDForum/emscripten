// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_COMMON_H_
#define LIB_SAMSUNG_BINDINGS_COMMON_H_

#include <functional>
#include <memory>
#include <utility>

#include "samsung/bindings/emss_operation_result.h"
#include "samsung/wasm/common.h"
#include "samsung/wasm/operation_result.h"

#define SET_LISTENER(...)                                             \
  do {                                                                \
    const auto result = CAPICall<void>(__VA_ARGS__).operation_result; \
    if (result != wasm::OperationResult::kSuccess) {                  \
      return {result};                                                \
    }                                                                 \
  } while (0)

inline bool IsHandleValid(int handle) { return handle >= 0; }

inline samsung::wasm::OperationResult OperationResultFromCAPI(
    EMSSOperationResult capi_result) {
  return static_cast<samsung::wasm::OperationResult>(capi_result);
}

template <class CAPIAsyncResult>
using CAsyncFunction = EMSSOperationResult (*)(int,
                                               void (*)(CAPIAsyncResult, void*),
                                               void*);

template <class T, class Arg, void (T::*handler)(Arg)>
void ListenerCallback(Arg arg, void* userData) {
  (static_cast<T*>(userData)->*handler)(arg);
}

template <class T, void (T::*handler)()>
void ListenerCallback(void* userData) {
  (static_cast<T*>(userData)->*handler)();
}

template <class Ret>
const auto CAPICall = [](auto fn, auto... args) {
  Ret ret{};
  const auto error = fn(std::forward<decltype(args)>(args)..., &ret);
  return samsung::wasm::Result<Ret>{ret, OperationResultFromCAPI(error)};
};

template <>
const auto CAPICall<void> = [](auto fn, auto... args) {
  return samsung::wasm::Result<void>{
      OperationResultFromCAPI(fn(std::forward<decltype(args)>(args)...))};
};

template <class AsyncResult, class CAPIAsyncResult>
void OnCAPICallFinished(CAPIAsyncResult error, void* userData) {
  using Callback = std::function<void(AsyncResult)>;
  auto cb = std::unique_ptr<Callback>(static_cast<Callback*>(userData));
  (*cb)(static_cast<AsyncResult>(error));
}

template <class AsyncResult, class CAPIAsyncResult, class... Args>
auto CAPIAsyncCall(std::function<void(AsyncResult)> cb, Args&&... args) {
  auto callback = new std::function<void(AsyncResult)>(cb);
  return CAPICall<void>(std::forward<Args>(args)...,
                        OnCAPICallFinished<AsyncResult, CAPIAsyncResult>,
                        callback);
}

#endif  // LIB_SAMSUNG_BINDINGS_COMMON_H_
