// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#include "samsung/bindings/emss_operation_result.h"

extern "C" {

const char* EMSSOperationResultToString(EMSSOperationResult result) {
  switch (result) {
    case EmssSuccess:
      return "Success";
    case EmssWrongHandle:
      return "Wrong handle";
    case EmssInvalidArgument:
      return "Invalid argument";
    case EmssListenerAlreadySet:
      return "Listener already set";
    case EmssNoSuchListener:
      return "No such listener";
    case EmssFailed:  // FALLTHROUGH
    default:
      return "Unknown error";
  }
}
}
