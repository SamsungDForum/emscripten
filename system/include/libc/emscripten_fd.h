#ifndef _EMSCRIPTEN_FD_H
#define _EMSCRIPTEN_FD_H

#ifdef __EMSCRIPTEN__

#define MAX_OPEN_FDS 4096

int acquire_next_fd(int is_socket);
void release_fd(int fd);
void set_mapped_fd(int fd, int mapped_fd);
int is_socket(int fd);
int get_mapped_fd(int fd);

#endif  // __EMSCRIPTEN__
#endif  // _EMSCRIPTEN_FD_H
