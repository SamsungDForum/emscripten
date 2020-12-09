#include <sys/socket.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

ssize_t sendto(int fd, const void *buf, size_t len, int flags, const struct sockaddr *addr, socklen_t alen)
{
	return sendto_internal(fd, buf, len, flags, addr, alen);
}

ssize_t normal_sendto(int fd, const void *buf, size_t len, int flags, const struct sockaddr *addr, socklen_t alen)
#else
ssize_t sendto(int fd, const void *buf, size_t len, int flags, const struct sockaddr *addr, socklen_t alen)
#endif  // __EMSCRIPTEN__
{
	return socketcall_cp(sendto, fd, buf, len, flags, addr, alen);
}
