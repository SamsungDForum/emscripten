#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int setsockopt(int fd, int level, int optname, const void *optval, socklen_t optlen)
{
	return setsockopt_internal(fd, level, optname, optval, optlen);
}

int normal_setsockopt(int fd, int level, int optname, const void *optval, socklen_t optlen)
#else
int setsockopt(int fd, int level, int optname, const void *optval, socklen_t optlen)
#endif  // __EMSCRIPTEN__
{
	return socketcall(setsockopt, fd, level, optname, optval, optlen, 0);
}
