#include <unistd.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "emscripten_fd.h"
#include "socket_host.h"

ssize_t read_with_socket_check(int fd, void *buf, size_t count)
{
	if (is_socket(fd)) {
		return wasm_read(fd, buf, count);
	}
	return normal_read(fd, buf, count);
}

ssize_t read(int fd, void *buf, size_t count)
{
	return read_internal(fd, buf, count);
}

ssize_t normal_read(int fd, void *buf, size_t count)
#else
ssize_t read(int fd, void *buf, size_t count)
#endif  // __EMSCRIPTEN__
{
	return syscall_cp(SYS_read, fd, buf, count);
}
