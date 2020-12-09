#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int getsockname(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
{
	return getsockname_internal(fd, addr, len);
}

int normal_getsockname(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#else
int getsockname(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#endif  // __EMSCRIPTEN__
{
	return socketcall(getsockname, fd, addr, len, 0, 0, 0);
}
