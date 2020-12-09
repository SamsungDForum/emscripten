#include <sys/socket.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int connect(int fd, const struct sockaddr *addr, socklen_t len)
{
	return connect_internal(fd, addr, len);
}

int normal_connect(int fd, const struct sockaddr *addr, socklen_t len)
#else
int connect(int fd, const struct sockaddr *addr, socklen_t len)
#endif  // __EMSCRIPTEN__
{
	return socketcall_cp(connect, fd, addr, len, 0, 0, 0);
}
