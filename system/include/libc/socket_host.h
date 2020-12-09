#ifndef _SOCKET_HOST_H_
#define _SOCKET_HOST_H_

#ifdef __EMSCRIPTEN__

#include <poll.h>
#include <stddef.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

struct SockAddr {
	int16_t family;
	uint16_t port;
	uint8_t bytes[124];
};

struct Iovec {
	void* data;
	int32_t data_len;
};

struct Timeval {
	int32_t seconds;
	int32_t microseconds;
};

#ifdef __cplusplus
extern "C" {
#endif
int wasm_accept(int, struct sockaddr *__restrict, socklen_t *__restrict);
int wasm_accept4(int, struct sockaddr *__restrict, socklen_t *__restrict, int);
int wasm_bind(int, const struct sockaddr *, socklen_t);
int wasm_close(int);
int wasm_connect(int, const struct sockaddr *, socklen_t);
int wasm_listen(int, int);
ssize_t wasm_recv(int, void *, size_t, int);
ssize_t wasm_recvfrom(int, void *__restrict, size_t, int, struct sockaddr *__restrict, socklen_t *__restrict);
ssize_t wasm_recvmsg(int, struct msghdr *, int);
ssize_t wasm_send(int, const void *, size_t, int);
ssize_t wasm_sendto(int, const void *, size_t, int, const struct sockaddr *, socklen_t);
ssize_t wasm_sendmsg(int, const struct msghdr *, int);
ssize_t wasm_read(int, void*, size_t);
ssize_t wasm_write(int, const void*, size_t);
int wasm_getpeername(int, struct sockaddr *__restrict, socklen_t *__restrict);
int wasm_getsockname(int, struct sockaddr *__restrict, socklen_t *__restrict);
int wasm_getsockopt(int, int, int, void *__restrict, socklen_t *__restrict);
int wasm_setsockopt(int, int, int, const void *, socklen_t);
int wasm_shutdown(int, int);
int wasm_poll(struct pollfd[], nfds_t, int);
int wasm_select(int, fd_set*, fd_set*, fd_set*, struct timeval*);
int wasm_socket(int, int, int);

int normal_accept(int, struct sockaddr *__restrict, socklen_t *__restrict);
int normal_accept4(int, struct sockaddr *__restrict, socklen_t *__restrict, int);
int normal_bind(int, const struct sockaddr *, socklen_t);
int normal_close(int);
int normal_connect(int, const struct sockaddr *, socklen_t);
int normal_listen(int, int);
ssize_t normal_recv(int, void *, size_t, int);
ssize_t normal_recvfrom(int, void *__restrict, size_t, int, struct sockaddr *__restrict, socklen_t *__restrict);
ssize_t normal_recvmsg(int, struct msghdr *, int);
ssize_t normal_send(int, const void *, size_t, int);
ssize_t normal_sendto(int, const void *, size_t, int, const struct sockaddr *, socklen_t);
ssize_t normal_sendmsg(int, const struct msghdr *, int);
ssize_t normal_read(int, void*, size_t);
ssize_t normal_write(int, const void*, size_t);
int normal_getpeername(int, struct sockaddr *__restrict, socklen_t *__restrict);
int normal_getsockname(int, struct sockaddr *__restrict, socklen_t *__restrict);
int normal_getsockopt(int, int, int, void *__restrict, socklen_t *__restrict);
int normal_setsockopt(int, int, int, const void *, socklen_t);
int normal_shutdown(int, int);
int normal_poll(struct pollfd[], nfds_t, int);
int normal_select(int, fd_set*, fd_set*, fd_set*, struct timeval*);
int normal_socket(int, int, int);

int close_with_socket_check(int);
ssize_t read_with_socket_check(int, void*, size_t);
ssize_t write_with_socket_check(int, const void*, size_t);
int poll_with_socket_check(struct pollfd[], nfds_t, int);
int select_with_socket_check(int, fd_set*, fd_set*, fd_set*, struct timeval*);

extern int (*accept_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict);
extern int (*accept4_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict, int);
extern int (*bind_internal)(int, const struct sockaddr *, socklen_t);
extern int (*close_internal)(int);
extern int (*connect_internal)(int, const struct sockaddr *, socklen_t);
extern int (*listen_internal)(int, int);
extern ssize_t (*recv_internal)(int, void *, size_t, int);
extern ssize_t (*recvfrom_internal)(int, void *__restrict, size_t, int, struct sockaddr *__restrict, socklen_t *__restrict);
extern ssize_t (*recvmsg_internal)(int, struct msghdr *, int);
extern ssize_t (*send_internal)(int, const void *, size_t, int);
extern ssize_t (*sendto_internal)(int, const void *, size_t, int, const struct sockaddr *, socklen_t);
extern ssize_t (*sendmsg_internal)(int, const struct msghdr *, int);
extern ssize_t (*read_internal)(int, void*, size_t);
extern ssize_t (*write_internal)(int, const void*, size_t);
extern int (*getpeername_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict);
extern int (*getsockname_internal)(int, struct sockaddr *__restrict, socklen_t *__restrict);
extern int (*getsockopt_internal )(int, int, int, void *__restrict, socklen_t *__restrict);
extern int (*setsockopt_internal)(int, int, int, const void *, socklen_t);
extern int (*shutdown_internal)(int, int);
extern int (*poll_internal)(struct pollfd[], nfds_t, int);
extern int (*select_internal)(int, fd_set*, fd_set*, fd_set*, struct timeval*);
extern int (*socket_internal)(int, int, int);

extern int _wasm_accept(int, struct SockAddr*, socklen_t, socklen_t*, int);
extern int _wasm_bind(int, const struct sockaddr*, socklen_t);
extern int _wasm_close(int);
extern int _wasm_connect(int, const struct sockaddr*, socklen_t);
extern int _wasm_getpeername(int, struct sockaddr*, socklen_t);
extern int _wasm_getsockname(int, struct sockaddr*, socklen_t);
extern int _wasm_getsockopt(int, int, int, void*, socklen_t);
extern int _wasm_listen(int, int);
extern int _wasm_poll(struct pollfd[], nfds_t, int);
extern int _wasm_recv(int, void*, size_t, int);
extern int _wasm_recvfrom(int, void*, size_t, int, struct SockAddr*, socklen_t, socklen_t*);
extern int _wasm_recvmsg(int, void*, int, socklen_t*, struct Iovec*, int, int, int*);
extern int _wasm_select(int, fd_set*, fd_set*, fd_set*, const struct Timeval*);
extern int _wasm_send(int, const void*, size_t, int);
extern int _wasm_sendmsg(int, void*, socklen_t, const struct iovec*, int, int);
extern int _wasm_sendto(int, const void*, size_t, int, const struct SockAddr*, socklen_t);
extern int _wasm_setsockopt(int, int, int, const void*, socklen_t);
extern int _wasm_shutdown(int, int);
extern int _wasm_socket(int, int, int);
#ifdef __cplusplus
}
#endif

#endif  // __EMSCRIPTEN__
#endif  // SOCKET_HOST_H
