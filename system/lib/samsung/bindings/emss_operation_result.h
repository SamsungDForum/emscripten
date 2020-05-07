// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_
#define LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_

#ifdef __cplusplus
extern "C" {
#endif

typedef enum EMSSOperationResult {
  EmssSuccess = 0,
  EmssWrongHandle,
  EmssInvalidArgument,
  EmssListenerAlreadySet,
  EmssNoSuchListener,
  EmssFailed,
} EMSSOperationResult;

const char* EMSSOperationResultToString(EMSSOperationResult result);

#ifdef __cplusplus
}
#endif

#endif  // LIB_SAMSUNG_BINDINGS_EMSS_OPERATION_RESULT_H_
