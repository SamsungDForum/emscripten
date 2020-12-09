#include <sys/socket.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int accept(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
{
	return accept_internal(fd, addr, len);
}

int normal_accept(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#else
int accept(int fd, struct sockaddr *restrict addr, socklen_t *restrict len)
#endif  // __EMSCRIPTEN__
{
	return socketcall_cp(accept, fd, addr, len, 0, 0, 0);
}
