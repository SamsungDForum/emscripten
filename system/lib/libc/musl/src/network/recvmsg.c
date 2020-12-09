#include <sys/socket.h>
#include <limits.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

ssize_t recvmsg(int fd, struct msghdr *msg, int flags)
{
	return recvmsg_internal(fd, msg, flags);
}

ssize_t normal_recvmsg(int fd, struct msghdr *msg, int flags)
#else
ssize_t recvmsg(int fd, struct msghdr *msg, int flags)
#endif  // __EMSCRIPTEN__
{
	ssize_t r;
#if LONG_MAX > INT_MAX
	struct msghdr h, *orig = msg;
	if (msg) {
		h = *msg;
		h.__pad1 = h.__pad2 = 0;
		msg = &h;
	}
#endif
	r = socketcall_cp(recvmsg, fd, msg, flags, 0, 0, 0);
#if LONG_MAX > INT_MAX
	if (orig) *orig = h;
#endif
	return r;
}
