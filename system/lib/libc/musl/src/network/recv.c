#include <sys/socket.h>

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

ssize_t recv(int fd, void *buf, size_t len, int flags)
{
	return recv_internal(fd, buf, len, flags);
}

ssize_t normal_recv(int fd, void *buf, size_t len, int flags)
#else
ssize_t recv(int fd, void *buf, size_t len, int flags)
#endif  // __EMSCRIPTEN__
{
	return recvfrom(fd, buf, len, flags, 0, 0);
}
