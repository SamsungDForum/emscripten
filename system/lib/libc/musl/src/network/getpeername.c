#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int getpeername(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
{
	return getpeername_internal(fd, addr, len);
}

int normal_getpeername(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#else
int getpeername(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#endif  // __EMSCRIPTEN__
{
	return socketcall(getpeername, fd, addr, len, 0, 0, 0);
}
