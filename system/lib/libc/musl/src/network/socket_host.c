#ifdef __EMSCRIPTEN__

#include "socket_host.h"
#include "emscripten_fd.h"
#include <emscripten.h>
#include <errno.h>
#include <poll.h>
#include <stddef.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

int wasm_accept4(int sockfd, struct sockaddr* addr, socklen_t* addrlen, int flags)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	socklen_t length = addrlen ? *addrlen : 0;
	int res = _wasm_accept(fd, (struct SockAddr*)addr, length,
	                       addrlen, flags);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	// We have to acquire fd manually.
	fd = acquire_next_fd(1);
	if (fd == -1) {
		_wasm_close(res);
		errno = EMFILE;
		return -1;
	}
	set_mapped_fd(fd, res);
	return fd;
}

int wasm_accept(int sockfd, struct sockaddr* addr, socklen_t* addrlen)
{
	return wasm_accept4(sockfd, addr, addrlen, 0);
}

int wasm_bind(int sockfd, const struct sockaddr* addr, socklen_t addrlen)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_bind(fd, addr, addrlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

extern void _closeSocketOnRenderThread(int fd);

int wasm_close(int sockfd)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_close(fd);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	// Socket stream might have been created on the main thread if certain
	// syscalls (e.g. fcntl) were called on that socket. We should close it
	// now.
	_closeSocketOnRenderThread(sockfd);

	// We have to release fd manually.
	release_fd(sockfd);
	return res;
}

int wasm_connect(int sockfd, const struct sockaddr* addr, socklen_t addrlen)
{
	if (addr == NULL) {
		errno = EFAULT;
		return -1;
	}
	if (addrlen == 0) {
		errno = EINVAL;
		return -1;
	}
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_connect(fd, addr, addrlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

int wasm_listen(int sockfd, int backlog)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_listen(fd, backlog);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_recv(int sockfd, void* buf, size_t len, int flags)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_recv(fd, buf, len, flags);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_recvfrom(int sockfd, void* buf, size_t len, int flags, struct sockaddr* src_addr, socklen_t* addrlen)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_recvfrom(fd, buf, len, flags,
	                         (struct SockAddr*)src_addr, *addrlen,
	                         addrlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_recvmsg(int socket, struct msghdr* msg, int flags)
{
	int fd = get_mapped_fd(socket);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	} else if (!msg) {
		errno = EINVAL;
		return -1;
	}
	int res = _wasm_recvmsg(fd, msg->msg_name, msg->msg_namelen,
	                        &msg->msg_namelen,
	                        (struct Iovec*)msg->msg_iov,
	                        msg->msg_iovlen, flags, &msg->msg_flags);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_send(int sockfd, const void* buf, size_t len, int flags)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_send(fd, buf, len, flags);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_sendto(int sockfd, const void* buf, size_t len, int flags, const struct sockaddr* dest_addr, socklen_t addrlen)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_sendto(fd, buf, len, flags,
	                       (const struct SockAddr*)dest_addr, addrlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_sendmsg(int socket, const struct msghdr* msg, int flags)
{
	int fd = get_mapped_fd(socket);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	} else if (!msg) {
		errno = EINVAL;
		return -1;
	}
	int res = _wasm_sendmsg(fd, msg->msg_name, msg->msg_namelen,
	                        msg->msg_iov, msg->msg_iovlen, flags);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

ssize_t wasm_read(int sockfd, void* buf, size_t count)
{
	return wasm_recv(sockfd, buf, count, 0);
}

ssize_t wasm_write(int sockfd, const void* buf, size_t count)
{
	return wasm_send(sockfd, buf, count, 0);
}

int wasm_getpeername(int sockfd, struct sockaddr* addr, socklen_t* addrlen)
{
	if (addr == NULL || addrlen == NULL) {
		errno = EFAULT;
		return -1;
	}
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	socklen_t length = addrlen ? *addrlen : 0;
	int res = _wasm_getpeername(fd, addr, length);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	if (addrlen) {
		*addrlen = res;
	}
	return 0;
}

int wasm_getsockname(int sockfd, struct sockaddr* addr, socklen_t* addrlen)
{
	if (addr == NULL || addrlen == NULL) {
		errno = EFAULT;
		return -1;
	}
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_getsockname(fd, addr, *addrlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	*addrlen = res;
	return 0;
}

int wasm_getsockopt(int sockfd, int level, int optname, void* optval, socklen_t* optlen)
{
	if (optval == NULL || optlen == NULL)
	{
		errno = EFAULT;
		return -1;
	}
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_getsockopt(fd, level, optname, optval, *optlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	*optlen = res;
	return 0;
}

int wasm_setsockopt(int sockfd, int level, int optname, const void* optval, socklen_t optlen)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_setsockopt(fd, level, optname, optval, optlen);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

int wasm_shutdown(int sockfd, int how)
{
	int fd = get_mapped_fd(sockfd);
	if (fd == -1) {
		errno = EBADF;
		return -1;
	}
	int res = _wasm_shutdown(fd, how);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	return res;
}

int wasm_poll(struct pollfd fds[], nfds_t nfds, int timeout)
{
	int temp_fds[nfds];
	for (nfds_t i = 0; i < nfds; ++i) {
		temp_fds[i] = fds[i].fd;
		fds[i].fd = get_mapped_fd(fds[i].fd);
	}
	int res = _wasm_poll(fds, nfds, timeout);
	if (res < 0) {
		errno = -res;
		res = -1;
	}
	for (nfds_t i = 0; i < nfds; ++i) {
		fds[i].fd = temp_fds[i];
	}
	return res;
}

static int prepare_fdset_arg(int reversed_map[], int nfds, int *max_fd, const fd_set *fds, fd_set **arg)
{
	if (!fds) {
		*arg = NULL;
		return 0;
	}
	FD_ZERO(*arg);
	for (int i = 0; i < nfds; ++i) {
		if (!FD_ISSET(i, fds)) {
			continue;
		}
		int fd = get_mapped_fd(i);
		if (fd == -1 || FD_SETSIZE <= fd) {
			errno = EBADF;
			return -1;
		} else if (fd > *max_fd) {
			*max_fd = fd;
		}
		reversed_map[fd] = i;
		FD_SET(fd, *arg);
	}
	return 0;
}

static void set_ready_fds(int reversed_map[], int *count, fd_set *fds, const fd_set *fds_arg)
{
	if (!fds) {
		return;
	}
	FD_ZERO(fds);
	for (int i = 0; *count > 0 && i < FD_SETSIZE; ++i) {
		if (FD_ISSET(i, fds_arg)) {
			FD_SET(reversed_map[i], fds);
			--(*count);
		}
	}
}

int wasm_select(int nfds, fd_set* rfds, fd_set* wfds, fd_set* efds, struct timeval* timeout)
{
	int rev_map[FD_SETSIZE];
	int max_fd = 0;
	fd_set mapped_rfds;
	fd_set mapped_wfds;
	fd_set mapped_efds;
	fd_set *rfds_arg = &mapped_rfds;
	fd_set *wfds_arg = &mapped_wfds;
	fd_set *efds_arg = &mapped_efds;

	if (prepare_fdset_arg(rev_map, nfds, &max_fd, rfds, &rfds_arg) < 0
	    || prepare_fdset_arg(rev_map, nfds, &max_fd, wfds, &wfds_arg) < 0
	    || prepare_fdset_arg(rev_map, nfds, &max_fd, efds, &efds_arg) < 0) {
		return -1;
	}
	int res = _wasm_select(max_fd + 1, rfds_arg, wfds_arg, efds_arg,
	                       (const struct Timeval*)timeout);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	int count = res;
	set_ready_fds(rev_map, &count, rfds, rfds_arg);
	set_ready_fds(rev_map, &count, wfds, wfds_arg);
	set_ready_fds(rev_map, &count, efds, efds_arg);
	return res;
}

int wasm_socket(int domain, int type, int protocol)
{
	int res = _wasm_socket(domain, type, protocol);
	if (res < 0) {
		errno = -res;
		return -1;
	}
	// We have to acquire fd manually.
	int fd = acquire_next_fd(1);
	if (fd == -1) {
		_wasm_close(res);
		errno = EMFILE;
		return -1;
	}
	set_mapped_fd(fd, res);
	return fd;
}

int (*accept_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict) = normal_accept;
int (*accept4_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict, int) = normal_accept4;
int (*bind_internal)(int, const struct sockaddr *, socklen_t) = normal_bind;
int (*close_internal)(int) = normal_close;
int (*connect_internal)(int, const struct sockaddr *, socklen_t) = normal_connect;
int (*listen_internal)(int, int) = normal_listen;
ssize_t (*recv_internal)(int, void *, size_t, int) = normal_recv;
ssize_t (*recvfrom_internal)(int, void *__restrict, size_t, int, struct sockaddr *__restrict, socklen_t *__restrict) = normal_recvfrom;
ssize_t (*recvmsg_internal)(int, struct msghdr *, int) = normal_recvmsg;
ssize_t (*send_internal)(int, const void *, size_t, int) = normal_send;
ssize_t (*sendto_internal)(int, const void *, size_t, int, const struct sockaddr *, socklen_t) = normal_sendto;
ssize_t (*sendmsg_internal)(int, const struct msghdr *, int) = normal_sendmsg;
ssize_t (*read_internal)(int, void*, size_t) = normal_read;
ssize_t (*write_internal)(int, const void*, size_t) = normal_write;
int (*getpeername_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict) = normal_getpeername;
int (*getsockname_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict) = normal_getsockname;
int (*getsockopt_internal )(int, int, int, void *__restrict, socklen_t *__restrict) = normal_getsockopt;
int (*setsockopt_internal)(int, int, int, const void *, socklen_t) = normal_setsockopt;
int (*shutdown_internal)(int, int) = normal_shutdown;
int (*poll_internal)(struct pollfd[], nfds_t, int) = normal_poll;
int (*select_internal)(int, fd_set*, fd_set*, fd_set*, struct timeval*) = normal_select;
int (*socket_internal)(int, int, int) = normal_socket;

void EMSCRIPTEN_KEEPALIVE set_host_bindings_impl()
{
	accept_internal = wasm_accept;
	accept4_internal = wasm_accept4;
	bind_internal = wasm_bind;
	close_internal = close_with_socket_check;
	connect_internal = wasm_connect;
	listen_internal = wasm_listen;
	recv_internal = wasm_recv;
	recvfrom_internal = wasm_recvfrom;
	recvmsg_internal = wasm_recvmsg;
	send_internal = wasm_send;
	sendto_internal = wasm_sendto;
	sendmsg_internal = wasm_sendmsg;
	read_internal = read_with_socket_check;
	write_internal = write_with_socket_check;
	getpeername_internal = wasm_getpeername;
	getsockname_internal = wasm_getsockname;
	getsockopt_internal = wasm_getsockopt;
	setsockopt_internal = wasm_setsockopt;
	shutdown_internal = wasm_shutdown;
	poll_internal = poll_with_socket_check;
	select_internal = select_with_socket_check;
	socket_internal = wasm_socket;
}

#endif  // __EMSCRIPTEN__
