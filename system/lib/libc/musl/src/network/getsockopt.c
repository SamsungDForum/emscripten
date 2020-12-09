#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int getsockopt(int fd, int level, int optname, void *restrict optval, socklen_t *restrict optlen)
{
	return getsockopt_internal(fd, level, optname, optval, optlen);
}

int normal_getsockopt(int fd, int level, int optname, void *restrict optval, socklen_t *restrict optlen)
#else
int getsockopt(int fd, int level, int optname, void *restrict optval, socklen_t *restrict optlen)
#endif  // __EMSCRIPTEN__
{
	return socketcall(getsockopt, fd, level, optname, optval, optlen, 0);
}
