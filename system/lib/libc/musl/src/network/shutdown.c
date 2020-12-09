#include <sys/socket.h>
#include "syscall.h"

#ifdef __EMSCRIPTEN__
#include "socket_host.h"

int shutdown(int fd, int how)
{
	return shutdown_internal(fd, how);
}

int normal_shutdown(int fd, int how)
#else
int shutdown(int fd, int how)
#endif  // __EMSCRIPTEN__
{
	return socketcall(shutdown, fd, how, 0, 0, 0, 0);
}
