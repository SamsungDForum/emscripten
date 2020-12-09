#include <poll.h>
#include <time.h>
#include <signal.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "emscripten_fd.h"
#include "socket_host.h"

int poll_with_socket_check(struct pollfd *fds, nfds_t n, int timeout)
{
	int socket = 1;
	for (nfds_t i = 0; i < n; ++i) {
		if (!is_socket(fds[i].fd)) {
			socket = 0;
			break;
		}
	}
	if (socket) {
		return wasm_poll(fds, n, timeout);
	}
	return normal_poll(fds, n, timeout);
}

int poll(struct pollfd *fds, nfds_t n, int timeout)
{
	return poll_internal(fds, n, timeout);
}

int normal_poll(struct pollfd *fds, nfds_t n, int timeout)
#else
int poll(struct pollfd *fds, nfds_t n, int timeout)
#endif  // __EMSCRIPTEN__
{
#ifdef SYS_poll
	return syscall_cp(SYS_poll, fds, n, timeout);
#else
	return syscall_cp(SYS_ppoll, fds, n, timeout>=0 ?
		&((struct timespec){ .tv_sec = timeout/1000,
		.tv_nsec = timeout%1000*1000000 }) : 0, 0, _NSIG/8);
#endif
}
