#include <unistd.h>
#include <errno.h>
#include "syscall.h"
#include "libc.h"

static int dummy(int fd)
{
	return fd;
}

weak_alias(dummy, __aio_close);

#ifdef __EMSCRIPTEN__
#include "emscripten_fd.h"
#include "socket_host.h"

int close_with_socket_check(int fd)
{
	if (is_socket(fd)) {
		return wasm_close(fd);
	}
	return normal_close(fd);
}

int close(int fd) {
	return close_internal(fd);
}

int normal_close(int fd)
#else
int close(int fd) {
#endif  // __EMSCRIPTEN__
{
	fd = __aio_close(fd);
#ifdef __EMSCRIPTEN__
	int r = __wasi_fd_close(fd);
	if (r == __WASI_ERRNO_INTR) r = __WASI_ERRNO_SUCCESS;
	return __wasi_syscall_ret(r);
#else
	int r = __syscall_cp(SYS_close, fd);
	if (r == -EINTR) r = 0;
	return __syscall_ret(r);
#endif
}
