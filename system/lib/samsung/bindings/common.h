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

#define LISTENER_OP(...)                                              \
  do {                                                                \
    const auto result = CAPICall<void>(__VA_ARGS__).operation_result; \
    if (result != wasm::OperationResult::kSuccess) {                  \
      return result;                                                  \
    }                                                                 \
  } while (0)

inline bool IsHandleValid(int handle) {
  return handle >= 0;
}

inline samsung::wasm::OperationResult OperationResultFromCAPI(
    EMSSOperationResult capi_result) {
  return static_cast<samsung::wasm::OperationResult>(capi_result);
}

template <class CAPIAsyncResult>
using CAsyncFunction = EMSSOperationResult (*)(int,
                                               void (*)(CAPIAsyncResult, void*),
                                               void*);
template <class CAPIAsyncOperationResult, class Arg>
using CAsyncFunctionWithArg =
    EMSSOperationResult (*)(int,
                            Arg,
                            void (*)(CAPIAsyncOperationResult, void*),
                            void*);

template <class CAPIAsyncOperationResult, class Param, class Arg>
using CAsyncFunctionWithArgAndReturnParam =
    EMSSOperationResult (*)(int,
                            Arg,
                            void (*)(CAPIAsyncOperationResult, Param, void*),
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
constexpr auto CAPICall = [](auto fn, auto... args) {
  Ret ret{};
  const auto error = fn(std::forward<decltype(args)>(args)..., &ret);
  return samsung::wasm::Result<Ret>{ret, OperationResultFromCAPI(error)};
};

template <>
constexpr auto CAPICall<void> = [](auto fn, auto... args) {
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

template <class AsyncOperationResult,
          class Param,
          class CAPIAsyncOperationResult>
void OnCAPICallFinishedWithParam(CAPIAsyncOperationResult error,
                                 Param parameter,
                                 void* userData) {
  using Callback = std::function<void(AsyncOperationResult, Param)>;
  auto cb = std::unique_ptr<Callback>(static_cast<Callback*>(userData));
  (*cb)(static_cast<AsyncOperationResult>(error), parameter);
}

template <class AsyncOperationResult, class CAPIAsyncOperationResult, class Arg>
auto CAPIAsyncCallWithArg(
    CAsyncFunctionWithArg<CAPIAsyncOperationResult, Arg> fn,
    int handle,
    Arg arg,
    std::function<void(AsyncOperationResult)> cb) {
  auto callback = new std::function<void(AsyncOperationResult)>(cb);
  return CAPICall<void>(
      fn, handle, arg,
      OnCAPICallFinished<AsyncOperationResult, CAPIAsyncOperationResult>,
      callback);
}

template <class AsyncOperationResult,
          class Param,
          class CAPIAsyncOperationResult,
          class Arg>
auto CAPIAsyncCallWithArgAndReturnParam(
    CAsyncFunctionWithArgAndReturnParam<CAPIAsyncOperationResult, Param, Arg>
        fn,
    int handle,
    Arg arg,
    std::function<void(AsyncOperationResult, Param)> cb) {
  auto callback = new std::function<void(AsyncOperationResult, Param)>(cb);
  return CAPICall<void>(fn, handle, arg,
                        OnCAPICallFinishedWithParam<AsyncOperationResult, Param,
                                                    CAPIAsyncOperationResult>,
                        callback);
}

#endif  // LIB_SAMSUNG_BINDINGS_COMMON_H_
