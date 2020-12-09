#include <sys/select.h>
#include <signal.h>
#include <stdint.h>
#include <errno.h>
#include "syscall.h"
#include "libc.h"

#ifdef __EMSCRIPTEN__
#include "emscripten_fd.h"
#include "socket_host.h"

static int only_sockets(int nfds, fd_set *fds)
{
	if (fds) {
		for (int i = 0; i < nfds; ++i) {
			if (FD_ISSET(i, fds) && !is_socket(i)) {
				return 0;
			}
		}
	}
	return 1;
}

int select_with_socket_check(int n, fd_set *restrict rfds, fd_set *restrict wfds, fd_set *restrict efds, struct timeval *restrict tv)
{
	if (only_sockets(n, rfds) && only_sockets(n, wfds)
	    && only_sockets(n, efds)) {
		return wasm_select(n, rfds, wfds, efds, tv);
	}
	return normal_select(n, rfds, wfds, efds, tv);
}

int select(int n, fd_set *restrict rfds, fd_set *restrict wfds, fd_set *restrict efds, struct timeval *restrict tv)
{
	return select_internal(n, rfds, wfds, efds, tv);
}

int normal_select(int n, fd_set *restrict rfds, fd_set *restrict wfds, fd_set *restrict efds, struct timeval *restrict tv)
#else
int select(int n, fd_set *restrict rfds, fd_set *restrict wfds, fd_set *restrict efds, struct timeval *restrict tv)
#endif  // __EMSCRIPTEN__
{
#ifdef SYS_select
	return syscall_cp(SYS_select, n, rfds, wfds, efds, tv);
#else
	syscall_arg_t data[2] = { 0, _NSIG/8 };
	struct timespec ts;
	if (tv) {
		if (tv->tv_sec < 0 || tv->tv_usec < 0)
			return __syscall_ret(-EINVAL);
		time_t extra_secs = tv->tv_usec / 1000000;
		ts.tv_nsec = tv->tv_usec % 1000000 * 1000;
		const time_t max_time = (1ULL<<8*sizeof(time_t)-1)-1;
		ts.tv_sec = extra_secs > max_time - tv->tv_sec ?
			max_time : tv->tv_sec + extra_secs;
	}
	return syscall_cp(SYS_pselect6, n, rfds, wfds, efds, tv ? &ts : 0, data);
#endif
}
