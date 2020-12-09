#include <sys/socket.h>

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

ssize_t send(int fd, const void *buf, size_t len, int flags)
{
	return send_internal(fd, buf, len, flags);
}

ssize_t normal_send(int fd, const void *buf, size_t len, int flags)
#else
ssize_t send(int fd, const void *buf, size_t len, int flags)
#endif  // __EMSCRIPTEN__
{
	return sendto(fd, buf, len, flags, 0, 0);
}
