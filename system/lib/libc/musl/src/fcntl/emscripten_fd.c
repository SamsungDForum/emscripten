#ifdef __EMSCRIPTEN__

#include "emscripten_fd.h"
#include <pthread.h>
#include <emscripten.h>

enum fd_state {
	FREE,
	SOCKET,
	NON_SOCKET,
};

static enum fd_state fd_states[MAX_OPEN_FDS] = { FREE };
static int fd_map[MAX_OPEN_FDS];
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static int is_in_valid_range(int fd)
{
	return 0 <= fd && fd < MAX_OPEN_FDS;
}

int EMSCRIPTEN_KEEPALIVE acquire_next_fd(int is_socket)
{
	int res = -1;
	pthread_mutex_lock(&lock);
	for (int i = 0; i < MAX_OPEN_FDS; ++i) {
		if (fd_states[i] == FREE) {
			if (is_socket) {
				fd_states[i] = SOCKET;
			} else {
				fd_states[i] = NON_SOCKET;
			}
			// Identity by default.
			fd_map[i] = i;
			res = i;
			break;
		}
	}
	pthread_mutex_unlock(&lock);
	return res;
}

void EMSCRIPTEN_KEEPALIVE release_fd(int fd)
{
	if (is_in_valid_range(fd)) {
		pthread_mutex_lock(&lock);
		fd_states[fd] = FREE;
		pthread_mutex_unlock(&lock);
	}
}

void EMSCRIPTEN_KEEPALIVE set_mapped_fd(int fd, int mapped_fd)
{
	if (!is_in_valid_range(fd)) {
		return;
	}
	pthread_mutex_lock(&lock);
	fd_map[fd] = mapped_fd;
	pthread_mutex_unlock(&lock);
}

int EMSCRIPTEN_KEEPALIVE is_socket(int fd)
{
	if (!is_in_valid_range(fd)) {
		return 0;
	}
	pthread_mutex_lock(&lock);
	int res = fd_states[fd] == SOCKET;
	pthread_mutex_unlock(&lock);
	return res;
}

int EMSCRIPTEN_KEEPALIVE get_mapped_fd(int fd)
{
	if (!is_in_valid_range(fd)) {
		return -1;
	}
	pthread_mutex_lock(&lock);
	if (fd_states[fd] == FREE) {
		pthread_mutex_unlock(&lock);
		return -1;
	}
	int res = fd_map[fd];
	pthread_mutex_unlock(&lock);
	return res;
}

#endif  // __EMSCRIPTEN__
