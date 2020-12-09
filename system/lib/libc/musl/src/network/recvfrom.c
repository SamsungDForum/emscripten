#include <sys/socket.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

ssize_t recvfrom(int fd, void *restrict buf, size_t len, int flags, struct sockaddr *restrict addr, socklen_t *restrict alen)
{
	return recvfrom_internal(fd, buf, len, flags, addr, alen);
}

ssize_t normal_recvfrom(int fd, void *restrict buf, size_t len, int flags, struct sockaddr *restrict addr, socklen_t *restrict alen)
#else
ssize_t recvfrom(int fd, void *restrict buf, size_t len, int flags, struct sockaddr *restrict addr, socklen_t *restrict alen)
#endif  // __EMSCRIPTEN__
{
	return socketcall_cp(recvfrom, fd, buf, len, flags, addr, alen);
}
