#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int bind(int fd, const struct sockaddr *addr, socklen_t len)
{
	return bind_internal(fd, addr, len);
}

int normal_bind(int fd, const struct sockaddr *addr, socklen_t len)
#else
int bind(int fd, const struct sockaddr *addr, socklen_t len)
#endif  // __EMSCRIPTEN__
{
	return socketcall(bind, fd, addr, len, 0, 0, 0);
}
