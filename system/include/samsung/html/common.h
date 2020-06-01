// Copyright 2020 Samsung Electronics
// TizenTV Emscripten extensions are available under two separate licenses, the
// MIT license and the University of Illinois/NCSA Open Source License.  Both
// these licenses can be found in the LICENSE file.

#ifndef INCLUDE_SAMSUNG_HTML_COMMON_H_
#define INCLUDE_SAMSUNG_HTML_COMMON_H_

namespace samsung {
namespace html {

/// Enumerates possible errors while handling media
/// in an HTML media element
enum class MediaError {
  kMediaErrAborted = 1,
  kMediaErrNetwork,
  kMediaErrDecode,
  kMediaErrSrcNotSupported,
};

}  // namespace html
}  // namespace samsung

#endif  // INCLUDE_SAMSUNG_HTML_COMMON_H_