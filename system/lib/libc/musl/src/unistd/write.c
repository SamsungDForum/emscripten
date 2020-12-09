#include <unistd.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "emscripten_fd.h"
#include "socket_host.h"

ssize_t write_with_socket_check(int fd, const void *buf, size_t count)
{
	if (is_socket(fd)) {
		return wasm_write(fd, buf, count);
	}
	return normal_write(fd, buf, count);
}

ssize_t write(int fd, const void *buf, size_t count)
{
	return write_internal(fd, buf, count);
}

ssize_t normal_write(int fd, const void *buf, size_t count)
#else
ssize_t write(int fd, const void *buf, size_t count)
#endif  // __EMSCRIPTEN__
{
	return syscall_cp(SYS_write, fd, buf, count);
}
