#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int listen(int fd, int backlog)
{
	return listen_internal(fd, backlog);
}

int normal_listen(int fd, int backlog)
#else
int listen(int fd, int backlog)
#endif  // __EMSCRIPTEN__
{
	return socketcall(listen, fd, backlog, 0, 0, 0, 0);
}
