// Copyright 2013 The Emscripten Authors.  All rights reserved.
// Copyright 2019 Samsung Electronics
// Emscripten is available under two separate licenses, the MIT license and the
// University of Illinois/NCSA Open Source License.  Both these licenses can be
// found in the LICENSE file.

mergeInto(LibraryManager.library, {
  $SOCKFS__postset: function() {
    addAtInit('SOCKFS.root = FS.mount(SOCKFS, {}, null);');
  },
  $SOCKFS__deps: ['$FS', '$ERRNO_CODES'], // TODO: avoid ERRNO_CODES
  $SOCKFS: {
    mount: function(mount) {
      SOCKFS.initSocketMap();
      return FS.createNode(null, '/', {{{ cDefine('S_IFDIR') }}} | 511 /* 0777 */, 0);
    },
    createSocket: function(family, type, protocol) {
      var streaming = type == {{{ cDefine('SOCK_STREAM') }}};

      const familyName = SOCKFS.intToFamily(family);
      if (familyName === null || familyName === "af_unspec") {
        throw new FS.ErrnoError({{{ cDefine('EAFNOSUPPORT') }}});
      }

      if (protocol && streaming && protocol != {{{ cDefine('IPPROTO_TCP') }}}) {
        // if SOCK_STREAM, must be tcp
        throw new FS.ErrnoError({{{ cDefine('EAFNOSUPPORT') }}});
      }

      const SOCK_CLOEXEC = {{{ cDefine('SOCK_CLOEXEC') }}};
      const SOCK_NONBLOCK = {{{ cDefine('SOCK_NONBLOCK') }}};
      let option = 0;
      let socket = "socket object";

      if (type & SOCK_CLOEXEC) {
        option |= tizentvwasm.SockFlags.SOCK_CLOEXEC;
        type &= ~SOCK_CLOEXEC;
      }
      if (type & SOCK_NONBLOCK) {
        option |= tizentvwasm.SockFlags.SOCK_NONBLOCK;
        type &= ~SOCK_NONBLOCK;
      }

      try {
        const sockType = SOCKFS.intToSockType(type);
        if (sockType) {
          socket = tizentvwasm.SocketsManager.create(familyName, sockType, option);
        } else {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
      } catch (err) {
        throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
      }

      var sock = {
        family: family,
        type: type,
        protocol: protocol,
        sock_fd: socket,
        sock_ops: SOCKFS.webengine_sock_ops
      };

      // create the filesystem node to store the socket structure
      var name = SOCKFS.nextname();
      var node = FS.createNode(SOCKFS.root, name, {{{ cDefine('S_IFSOCK') }}}, 0);
      node.sock = sock;

      // and the wrapping stream that enables library functions such
      // as read and write to indirectly interact with the socket
      var stream = FS.createStream({
        path: name,
        node: node,
        flags: FS.modeStringToFlags('r+'),
        seekable: false,
        stream_ops: SOCKFS.stream_ops
      });

      // map the new stream to the socket structure (sockets have a 1:1
      // relationship with a stream)
      sock.stream = stream;

      const id = __createSocketOnRenderThread(family, type, protocol, socket);
      FS.moveStream(sock.stream.fd, id);

      return sock;
    },
    socketMapPtr: {{{ makeStaticAlloc(4096) }}}, // 4096 because this is equal FS.MAX_OPEN_FDS
    initSocketMap: function() {
      const ptr = SOCKFS.socketMapPtr >> 2;
      const count = FS.MAX_OPEN_FDS >> 2;
      for (let i = 0; i < count; i++) {
        HEAP32[ptr + i] = 0;
      }
    },
    setSocketFdInMap: function(fd) {
      if (fd < 0 || fd >= FS.MAX_OPEN_FDS) {
        return;
      }
      HEAP8[SOCKFS.socketMapPtr + fd] = 1;
    },
    clearSocketFdInMap: function(fd) {
      if (fd < 0 || fd >= FS.MAX_OPEN_FDS) {
        return;
      }
      HEAP8[SOCKFS.socketMapPtr + fd] = 0;
    },
    hasSocket: function(fd) {
      if (fd < 0 || fd >= FS.MAX_OPEN_FD) {
        return false;
      }
      return HEAP8[SOCKFS.socketMapPtr + fd] === 1;
    },
    createSocketOnCurrentThread: function(family, type, protocol, socket) {
      var sock = {
        family: family,
        type: type,
        protocol: protocol,
        sock_fd: socket,
        sock_ops: SOCKFS.webengine_sock_ops
      };
      // create the filesystem node to store the socket structure
      var name = SOCKFS.nextname();
      var node = FS.createNode(SOCKFS.root, name, {{{ cDefine('S_IFSOCK') }}}, 0);
      node.sock = sock;
      // and the wrapping stream that enables library functions such
      // as read and write to indirectly interact with the socket
      var stream = FS.createStream({
        path: name,
        node: node,
        flags: FS.modeStringToFlags('r+'),
        seekable: false,
        stream_ops: SOCKFS.stream_ops
      });
      sock.stream = stream;
      return sock.stream.fd;
    },
    updateStream: function(fd) {
      let stream = FS.getStream(fd);
      if (!stream) {
        const ptr = __cloneSocketFromRenderThread(fd);
        const family = HEAP32[ptr >> 2];
        const type = HEAP32[(ptr >> 2) + 1];
        const protocol = HEAP32[(ptr >> 2) + 2];
        const sock_fd = HEAP32[(ptr >> 2) + 3];
        const tmp_fd = SOCKFS.createSocketOnCurrentThread(family, type, protocol, sock_fd);
        FS.moveStream(tmp_fd, fd);
        _free(ptr);
        stream = FS.getStream(fd);
        if (!stream) {
          return null;
        }
      }
      return stream;
    },
    getSocket: function(fd) {
      if (!SOCKFS.hasSocket(fd)) {
        return null;
      }
      const stream = SOCKFS.updateStream(fd);
      if (!stream || !FS.isSocket(stream.node.mode)) {
        return null;
      }
      return stream.node.sock;
    },
    getStream: function(fd) {
      return SOCKFS.updateStream(fd);
    },
    getErrorCode: function(sock_fd) {
      const ErrorCodes = tizentvwasm.ErrorCodes;
      const errorCodesMap = new Map([
        [ ErrorCodes.EPERM, {{{ cDefine('EPERM') }}} ],
        [ ErrorCodes.ENOENT, {{{ cDefine('ENOENT') }}} ],
        [ ErrorCodes.ESRCH, {{{ cDefine('ESRCH') }}} ],
        [ ErrorCodes.EINTR, {{{ cDefine('EINTR') }}} ],
        [ ErrorCodes.EIO, {{{ cDefine('EIO') }}} ],
        [ ErrorCodes.ENXIO, {{{ cDefine('ENXIO') }}} ],
        [ ErrorCodes.E2BIG, {{{ cDefine('E2BIG') }}} ],
        [ ErrorCodes.ENOEXEC, {{{ cDefine('ENOEXEC') }}} ],
        [ ErrorCodes.EBADF, {{{ cDefine('EBADF') }}} ],
        [ ErrorCodes.ECHILD, {{{ cDefine('ECHILD') }}} ],
        [ ErrorCodes.EAGAIN, {{{ cDefine('EAGAIN') }}} ],
        [ ErrorCodes.ENOMEM, {{{ cDefine('ENOMEM') }}} ],
        [ ErrorCodes.EACCES, {{{ cDefine('EACCES') }}} ],
        [ ErrorCodes.EFAULT, {{{ cDefine('EFAULT') }}} ],
        [ ErrorCodes.ENOTBLK, {{{ cDefine('ENOTBLK') }}} ],
        [ ErrorCodes.EBUSY, {{{ cDefine('EBUSY') }}} ],
        [ ErrorCodes.EEXIST, {{{ cDefine('EEXIST') }}} ],
        [ ErrorCodes.EXDEV, {{{ cDefine('EXDEV') }}} ],
        [ ErrorCodes.ENODEV, {{{ cDefine('ENODEV') }}} ],
        [ ErrorCodes.ENOTDIR, {{{ cDefine('ENOTDIR') }}} ],
        [ ErrorCodes.EISDIR, {{{ cDefine('EISDIR') }}} ],
        [ ErrorCodes.EINVAL, {{{ cDefine('EINVAL') }}} ],
        [ ErrorCodes.ENFILE, {{{ cDefine('ENFILE') }}} ],
        [ ErrorCodes.EMFILE, {{{ cDefine('EMFILE') }}} ],
        [ ErrorCodes.ENOTTY, {{{ cDefine('ENOTTY') }}} ],
        [ ErrorCodes.ETXTBSY, {{{ cDefine('ETXTBSY') }}} ],
        [ ErrorCodes.EFBIG, {{{ cDefine('EFBIG') }}} ],
        [ ErrorCodes.ENOSPC, {{{ cDefine('ENOSPC') }}} ],
        [ ErrorCodes.ESPIPE, {{{ cDefine('ESPIPE') }}} ],
        [ ErrorCodes.EROFS, {{{ cDefine('EROFS') }}} ],
        [ ErrorCodes.EMLINK, {{{ cDefine('EMLINK') }}} ],
        [ ErrorCodes.EPIPE, {{{ cDefine('EPIPE') }}} ],
        [ ErrorCodes.EDOM, {{{ cDefine('EDOM') }}} ],
        [ ErrorCodes.ERANGE, {{{ cDefine('ERANGE') }}} ],
        [ ErrorCodes.EDEADLK, {{{ cDefine('EDEADLK') }}} ],
        [ ErrorCodes.ENAMETOOLONG, {{{ cDefine('ENAMETOOLONG') }}} ],
        [ ErrorCodes.ENOLCK, {{{ cDefine('ENOLCK') }}} ],
        [ ErrorCodes.ENOSYS, {{{ cDefine('ENOSYS') }}} ],
        [ ErrorCodes.ENOTEMPTY, {{{ cDefine('ENOTEMPTY') }}} ],
        [ ErrorCodes.ELOOP, {{{ cDefine('ELOOP') }}} ],
        [ ErrorCodes.EWOULDBLOCK, {{{ cDefine('EWOULDBLOCK') }}} ],
        [ ErrorCodes.ENOMSG, {{{ cDefine('ENOMSG') }}} ],
        [ ErrorCodes.EIDRM, {{{ cDefine('EIDRM') }}} ],
        [ ErrorCodes.ECHRNG, {{{ cDefine('ECHRNG') }}} ],
        [ ErrorCodes.EL2NSYNC, {{{ cDefine('EL2NSYNC') }}} ],
        [ ErrorCodes.EL3HLT, {{{ cDefine('EL3HLT') }}} ],
        [ ErrorCodes.EL3RST, {{{ cDefine('EL3RST') }}} ],
        [ ErrorCodes.ELNRNG, {{{ cDefine('ELNRNG') }}} ],
        [ ErrorCodes.EUNATCH, {{{ cDefine('EUNATCH') }}} ],
        [ ErrorCodes.ENOCSI, {{{ cDefine('ENOCSI') }}} ],
        [ ErrorCodes.EL2HLT, {{{ cDefine('EL2HLT') }}} ],
        [ ErrorCodes.EBADE, {{{ cDefine('EBADE') }}} ],
        [ ErrorCodes.EBADR, {{{ cDefine('EBADR') }}} ],
        [ ErrorCodes.EXFULL, {{{ cDefine('EXFULL') }}} ],
        [ ErrorCodes.ENOANO, {{{ cDefine('ENOANO') }}} ],
        [ ErrorCodes.EBADRQC, {{{ cDefine('EBADRQC') }}} ],
        [ ErrorCodes.EBADSLT, {{{ cDefine('EBADSLT') }}} ],
        [ ErrorCodes.EDEADLOCK, {{{ cDefine('EDEADLOCK') }}} ],
        [ ErrorCodes.EBFONT, {{{ cDefine('EBFONT') }}} ],
        [ ErrorCodes.ENOSTR, {{{ cDefine('ENOSTR') }}} ],
        [ ErrorCodes.ENODATA, {{{ cDefine('ENODATA') }}} ],
        [ ErrorCodes.ETIME, {{{ cDefine('ETIME') }}} ],
        [ ErrorCodes.ENOSR, {{{ cDefine('ENOSR') }}} ],
        [ ErrorCodes.ENONET, {{{ cDefine('ENONET') }}} ],
        [ ErrorCodes.ENOPKG, {{{ cDefine('ENOPKG') }}} ],
        [ ErrorCodes.EREMOTE, {{{ cDefine('EREMOTE') }}} ],
        [ ErrorCodes.ENOLINK, {{{ cDefine('ENOLINK') }}} ],
        [ ErrorCodes.EADV, {{{ cDefine('EADV') }}} ],
        [ ErrorCodes.ESRMNT, {{{ cDefine('ESRMNT') }}} ],
        [ ErrorCodes.ECOMM, {{{ cDefine('ECOMM') }}} ],
        [ ErrorCodes.EPROTO, {{{ cDefine('EPROTO') }}} ],
        [ ErrorCodes.EMULTIHOP, {{{ cDefine('EMULTIHOP') }}} ],
        [ ErrorCodes.EDOTDOT, {{{ cDefine('EDOTDOT') }}} ],
        [ ErrorCodes.EBADMSG, {{{ cDefine('EBADMSG') }}} ],
        [ ErrorCodes.EOVERFLOW, {{{ cDefine('EOVERFLOW') }}} ],
        [ ErrorCodes.ENOTUNIQ, {{{ cDefine('ENOTUNIQ') }}} ],
        [ ErrorCodes.EBADFD, {{{ cDefine('EBADFD') }}} ],
        [ ErrorCodes.EREMCHG, {{{ cDefine('EREMCHG') }}} ],
        [ ErrorCodes.ELIBACC, {{{ cDefine('ELIBACC') }}} ],
        [ ErrorCodes.ELIBBAD, {{{ cDefine('ELIBBAD') }}} ],
        [ ErrorCodes.ELIBSCN, {{{ cDefine('ELIBSCN') }}} ],
        [ ErrorCodes.ELIBMAX, {{{ cDefine('ELIBMAX') }}} ],
        [ ErrorCodes.ELIBEXEC, {{{ cDefine('ELIBEXEC') }}} ],
        [ ErrorCodes.EILSEQ, {{{ cDefine('EILSEQ') }}} ],
        [ ErrorCodes.ERESTART, {{{ cDefine('ERESTART') }}} ],
        [ ErrorCodes.ESTRPIPE, {{{ cDefine('ESTRPIPE') }}} ],
        [ ErrorCodes.EUSERS, {{{ cDefine('EUSERS') }}} ],
        [ ErrorCodes.ENOTSOCK, {{{ cDefine('ENOTSOCK') }}} ],
        [ ErrorCodes.EDESTADDRREQ, {{{ cDefine('EDESTADDRREQ') }}} ],
        [ ErrorCodes.EMSGSIZE, {{{ cDefine('EMSGSIZE') }}} ],
        [ ErrorCodes.EPROTOTYPE, {{{ cDefine('EPROTOTYPE') }}} ],
        [ ErrorCodes.ENOPROTOOPT, {{{ cDefine('ENOPROTOOPT') }}} ],
        [ ErrorCodes.EPROTONOSUPPORT, {{{ cDefine('EPROTONOSUPPORT') }}} ],
        [ ErrorCodes.ESOCKTNOSUPPORT, {{{ cDefine('ESOCKTNOSUPPORT') }}} ],
        [ ErrorCodes.EOPNOTSUPP, {{{ cDefine('EOPNOTSUPP') }}} ],
        [ ErrorCodes.ENOTSUP, {{{ cDefine('ENOTSUP') }}} ],
        [ ErrorCodes.EPFNOSUPPORT, {{{ cDefine('EPFNOSUPPORT') }}} ],
        [ ErrorCodes.EAFNOSUPPORT, {{{ cDefine('EAFNOSUPPORT') }}} ],
        [ ErrorCodes.EADDRINUSE, {{{ cDefine('EADDRINUSE') }}} ],
        [ ErrorCodes.EADDRNOTAVAIL, {{{ cDefine('EADDRNOTAVAIL') }}} ],
        [ ErrorCodes.ENETDOWN, {{{ cDefine('ENETDOWN') }}} ],
        [ ErrorCodes.ENETUNREACH, {{{ cDefine('ENETUNREACH') }}} ],
        [ ErrorCodes.ENETRESET, {{{ cDefine('ENETRESET') }}} ],
        [ ErrorCodes.ECONNABORTED, {{{ cDefine('ECONNABORTED') }}} ],
        [ ErrorCodes.ECONNRESET, {{{ cDefine('ECONNRESET') }}} ],
        [ ErrorCodes.ENOBUFS, {{{ cDefine('ENOBUFS') }}} ],
        [ ErrorCodes.EISCONN, {{{ cDefine('EISCONN') }}} ],
        [ ErrorCodes.ENOTCONN, {{{ cDefine('ENOTCONN') }}} ],
        [ ErrorCodes.ESHUTDOWN, {{{ cDefine('ESHUTDOWN') }}} ],
        [ ErrorCodes.ETOOMANYREFS, {{{ cDefine('ETOOMANYREFS') }}} ],
        [ ErrorCodes.ETIMEDOUT, {{{ cDefine('ETIMEDOUT') }}} ],
        [ ErrorCodes.ECONNREFUSED, {{{ cDefine('ECONNREFUSED') }}} ],
        [ ErrorCodes.EHOSTDOWN, {{{ cDefine('EHOSTDOWN') }}} ],
        [ ErrorCodes.EHOSTUNREACH, {{{ cDefine('EHOSTUNREACH') }}} ],
        [ ErrorCodes.EALREADY, {{{ cDefine('EALREADY') }}} ],
        [ ErrorCodes.EINPROGRESS, {{{ cDefine('EINPROGRESS') }}} ],
        [ ErrorCodes.ESTALE, {{{ cDefine('ESTALE') }}} ],
        [ ErrorCodes.EUCLEAN, {{{ cDefine('EUCLEAN') }}} ],
        [ ErrorCodes.ENOTNAM, {{{ cDefine('ENOTNAM') }}} ],
        [ ErrorCodes.ENAVAIL, {{{ cDefine('ENAVAIL') }}} ],
        [ ErrorCodes.EISNAM, {{{ cDefine('EISNAM') }}} ],
        [ ErrorCodes.EREMOTEIO, {{{ cDefine('EREMOTEIO') }}} ],
        [ ErrorCodes.EDQUOT, {{{ cDefine('EDQUOT') }}} ],
        [ ErrorCodes.ENOMEDIUM, {{{ cDefine('ENOMEDIUM') }}} ],
        [ ErrorCodes.EMEDIUMTYPE, {{{ cDefine('EMEDIUMTYPE') }}} ],
        [ ErrorCodes.ECANCELED, {{{ cDefine('ECANCELED') }}} ],
        [ ErrorCodes.ENOKEY, {{{ cDefine('ENOKEY') }}} ],
        [ ErrorCodes.EKEYEXPIRED, {{{ cDefine('EKEYEXPIRED') }}} ],
        [ ErrorCodes.EKEYREVOKED, {{{ cDefine('EKEYREVOKED') }}} ],
        [ ErrorCodes.EKEYREJECTED, {{{ cDefine('EKEYREJECTED') }}} ],
        [ ErrorCodes.EOWNERDEAD, {{{ cDefine('EOWNERDEAD') }}} ],
        [ ErrorCodes.ENOTRECOVERABLE, {{{ cDefine('ENOTRECOVERABLE') }}} ],
        [ ErrorCodes.ERFKILL, {{{ cDefine('ERFKILL') }}} ],
        [ ErrorCodes.EHWPOISON, {{{ cDefine('EHWPOISON') }}} ]
      ]);

      const error = (typeof sock_fd == 'undefined' ?
          tizentvwasm.SocketsManager.getErrorCode() :
          tizentvwasm.SocketsManager.getErrorCode(sock_fd));
      if (errorCodesMap.has(error)) {
        return errorCodesMap.get(error);
      } else {
        return 0;
      }
    },
    // node and stream ops are backend agnostic
    stream_ops: {
      poll: function(stream) {
        var sock = stream.node.sock;
        return sock.sock_ops.poll(sock);
      },
      ioctl: function(stream, request, varargs) {
        var sock = stream.node.sock;
        return sock.sock_ops.ioctl(sock, request, varargs);
      },
      read: function(stream, buffer, offset, length, position /* ignored */ ) {
        const sock = stream.node.sock.sock_fd;
        const data = HEAPU8.subarray(offset, offset + length);
        try {
          return tizentvwasm.SocketsManager.recv(sock, data, 0);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock));
        }
      },
      write: function(stream, buffer, offset, length, position /* ignored */ ) {
        var sock = stream.node.sock.sock_fd;
        const data = HEAPU8.subarray(offset, offset + length);
        try {
          return tizentvwasm.SocketsManager.send(sock, data, 0);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock));
        }
      },
      close: function(stream) {
        var sock = stream.node.sock;
        const fd = stream.fd;
        sock.sock_ops.close(sock);
        __closeSocketOnRenderThread(fd);
      }
    },
    nextname: function() {
      if (!SOCKFS.nextname.current) {
        SOCKFS.nextname.current = 0;
      }
      return 'socket[' + (SOCKFS.nextname.current++) + ']';
    },
    // backend-specific stream ops
    webengine_sock_ops: {
      sizeof: {
        SOCKADDR_IN: 16,
        SOCKADDR_IN6: 28,
        HOSTENT: 20,
        FD_SET: 128,
        IPv4ADDR: 4,
        IPv6ADDR: 16,
      },
      //
      // actual sock ops
      //
      poll: function(sock) {
        if (sock.sock_fd === -1) {
          return {{{ cDefine('POLLNVAL') }}};
        }
        const PollFlags = tizentvwasm.PollFlags;
        const events = PollFlags.POLLIN
                       | PollFlags.POLLRDNORM
                       | PollFlags.POLLPRI
                       | PollFlags.POLLOUT
                       | PollFlags.POLLWRNORM;
        const poll_fd = new tizentvwasm.PollFd(sock.sock_fd, events);

        try {
          const result = tizentvwasm.SocketsManager.poll([poll_fd], 0);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode());
        }

        return SOCKFS.pollEventsConvertFromJS(poll_fd.revents);
      },
      ioctl: function(sock, request, arg) {
        console.log("SOCKFS ioctl() not implemented");
      },
      close: function(sock) {
        try {
          tizentvwasm.SocketsManager.close(sock.sock_fd);
          sock.sock_fd = -1; // mark thas socket is closed
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      bind: function(sock, addr, addrlen) {
        if (!addr) {
          throw new FS.ErrnoError({{{ cDefine('EFAULT') }}});
        }
        if (!addrlen) {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
        const sockaddr = HEAPU8.subarray(addr, addr + addrlen);
        const netAddr = SOCKFS.createNetAddressFromBytes(sockaddr);
        try {
          tizentvwasm.SocketsManager.bind(sock.sock_fd, netAddr);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      connect: function(sock, addr, addrlen) {
        if (!addr) {
          throw new FS.ErrnoError({{{ cDefine('EFAULT') }}});
        }
        if (!addrlen) {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
        const sockaddr = HEAPU8.subarray(addr, addr + addrlen);
        const netAddr = SOCKFS.createNetAddressFromBytes(sockaddr);
        try {
          tizentvwasm.SocketsManager.connect(sock.sock_fd, netAddr);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      listen: function(sock, backlog) {
        if (sock.type !== SOCKFS.SockType.SOCK_STREAM.value) {
          throw new FS.ErrnoError({{{ cDefine('EOPNOTSUPP') }}});
          return -1;
        }
        try {
          tizentvwasm.SocketsManager.listen(sock.sock_fd, backlog);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      accept: function(listensock, addr, addrlen) {
        try {
          const newSockSync = tizentvwasm.SocketsManager.accept4(listensock.sock_fd, 0);

          if (addr && addrlen) {
            const peerAddr = SOCKFS.createBytesFromNetAddress(tizentvwasm.SocketsManager.getPeerName(newSockSync));
            const len = HEAP32[addrlen >> 2];
            HEAP8.set(peerAddr.subarray(0, len), addr);
            HEAP32[addrlen >> 2] = peerAddr.length;
          }

          var sock = {
            family: listensock.family,
            type: listensock.type,
            protocol: listensock.protocol,
            sock_fd: newSockSync,
            sock_ops: SOCKFS.webengine_sock_ops
          };

          // create the filesystem node to store the socket structure
          var name = SOCKFS.nextname();
          var node = FS.createNode(SOCKFS.root, name, {{{ cDefine('S_IFSOCK') }}}, 0);
          node.sock = sock;

          // and the wrapping stream that enables library functions such
          // as read and write to indirectly interact with the socket
          var stream = FS.createStream({
            path: name,
            node: node,
            flags: FS.modeStringToFlags('r+'),
            seekable: false,
            stream_ops: SOCKFS.stream_ops
          });

          // map the new stream to the socket structure (sockets have a 1:1
          // relationship with a stream)
          sock.stream = stream;
          const id = __createSocketOnRenderThread(listensock.family, listensock.type, listensock.protocol, newSockSync);
          FS.moveStream(sock.stream.fd, id);
          let fd = sock.stream.fd;
          let st = FS.getStream(fd);
          return sock;
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(listensock.sock_fd));
        }

      },
      getname: function(sock, peer) {
        console.log("SOCKFS getname() not implemented");
      },
      sendto: function(sock, addr, addrlen, flags, dest, destlen) {
        const data = HEAPU8.subarray(addr, addr + addrlen);
        let netAddr = null;
        if (dest && destlen) {
          const sockaddr = HEAPU8.subarray(dest, dest + destlen);
          netAddr = SOCKFS.createNetAddressFromBytes(sockaddr);
          try {
            return tizentvwasm.SocketsManager.sendTo(sock.sock_fd, data, SOCKFS.msgFlagsToJs(flags), netAddr);
          } catch (err) {
            throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
          }
        } else {
          try {
            return tizentvwasm.SocketsManager.send(sock.sock_fd, data, SOCKFS.msgFlagsToJs(flags));
          } catch (err) {
            throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
          }
        }
      },
      sendmsg: function(sock, msgPtr, flags) {
        const name = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_name, '*') }}};
        const namelen = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_namelen, 'i32') }}};
        const iov = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_iov, '*') }}};
        const iovlen = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_iovlen, 'i32') }}};

        let address = null;
        if (name && namelen) {
          const sockaddr = HEAPU8.subarray(name, name + namelen);
          address = SOCKFS.createNetAddressFromBytes(sockaddr);
        }

        let msgs = [];
        for (let i = 0; i < iovlen; ++i) {
          msgs.push(new Uint8Array(
            buffer,
            {{{ makeGetValue('iov', '(' + C_STRUCTS.iovec.__size__ + ' * i) + ' + C_STRUCTS.iovec.iov_base, 'i8*') }}},
            {{{ makeGetValue('iov', '(' + C_STRUCTS.iovec.__size__ + ' * i) + ' + C_STRUCTS.iovec.iov_len, 'i32') }}}));
        }

        try {
          return tizentvwasm.SocketsManager.sendMsg(sock.sock_fd, address, msgs, SOCKFS.msgFlagsToJs(flags));
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
      },
      recvfrom: function(sock, bufPtr, len, flags, addrPtr, addrlenPtr) {
        const data = HEAPU8.subarray(bufPtr, bufPtr + len);
        if (!addrPtr || !addrlenPtr) {
          try {
            return tizentvwasm.SocketsManager.recv(sock, data, SOCKFS.msgFlagsToJs(flags));
          } catch (err) {
            throw new FS.ErrnoError(SOCKFS.getErrorCode(sock));
          }
        }
        let retVal = null;
        try {
          retVal = tizentvwasm.SocketsManager.recvFrom(sock, data, SOCKFS.msgFlagsToJs(flags));
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock));
        }

        if (addrPtr && addrlenPtr && retVal.peerAddress != null) {
          const peerAddr =
              SOCKFS.createBytesFromNetAddress(retVal.peerAddress);
          const addrlen = Math.min(HEAP32[addrlenPtr >> 2], peerAddr.length);
          HEAP8.set(peerAddr.subarray(0, addrlen), addrPtr);
          HEAP32[addrlenPtr >> 2] = addrlen;
        }

        return retVal.bytesRead;
      },
      recvmsg: function(sock, msgPtr, flags) {
        const name = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_name, '*') }}};
        const namelen = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_namelen, 'i32') }}};
        const iov = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_iov, '*') }}};
        const iovlen = {{{ makeGetValue('msgPtr', C_STRUCTS.msghdr.msg_iovlen, 'i32') }}};

        const msgs = [];
        for (let i = 0; i < iovlen; ++i) {
          msgs.push(new Uint8Array(
            buffer,
            {{{ makeGetValue('iov', '(' + C_STRUCTS.iovec.__size__ + ' * i) + ' + C_STRUCTS.iovec.iov_base, 'i8*') }}},
            {{{ makeGetValue('iov', '(' + C_STRUCTS.iovec.__size__ + ' * i) + ' + C_STRUCTS.iovec.iov_len, 'i32') }}}));
        }

        let ret = null;
        try {
          ret = tizentvwasm.SocketsManager.recvMsg(sock, msgs, SOCKFS.msgFlagsToJs(flags));
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock));
        }
        const ret_flags = SOCKFS.msgFlagsFromJs(ret.flags);
        if (name && namelen && ret.peerAddress) {
          const peerAddress = SOCKFS.createBytesFromNetAddress(ret.peerAddress);
          const addrLen = Math.min(namelen, peerAddress.length);
          HEAP8.set(peerAddress.subarray(0, addrLen), name);
          {{{ makeSetValue('msgPtr', C_STRUCTS.msghdr.msg_namelen, 'addrLen', 'i32') }}}
        }
        {{{ makeSetValue('msgPtr', C_STRUCTS.msghdr.msg_flags, 'ret_flags', 'i32') }}};
        return ret.bytesRead;
      },
      setsockopt: function(sock, level, optname, optval, optlen) {
        if (!optval) {
          throw new FS.ErrnoError({{{ cDefine('EFAULT') }}});
        }
        if (!optlen) {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
        const args = SOCKFS.getLevelAndOptionString(level, optname);
        const _optval = HEAPU8.slice(optval, optval + optlen);
        const value = SOCKFS.decodeValue(optname, _optval);

        try {
          tizentvwasm.SocketsManager.setSockOpt(sock.sock_fd, args.level, args.option, value);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      getsockopt: function(sock, level, optname, optval, optlen) {
        if (!optval || !optlen) {
          throw new FS.ErrnoError({{{ cDefine('EFAULT') }}});
        }
        const _optlen = HEAP32[optlen >> 2];
        if (!_optlen) {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
        let val;
        const args = SOCKFS.getLevelAndOptionString(level, optname, true);
        try {
          val = tizentvwasm.SocketsManager.getSockOpt(sock.sock_fd, args.level, args.option);
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
        const encVal = SOCKFS.encodeValue(optname, val, _optlen);
        HEAPU8.set(encVal, optval);
        HEAP32[optlen >> 2] = encVal.length;
        return 0;
      },
      getsockname: function(sock, addr, addrlen) {
        try {
          const sockAddress = tizentvwasm.SocketsManager.getSockName(sock.sock_fd);

          const sockAddr = SOCKFS.createBytesFromNetAddress(sockAddress);
          const len = HEAP32[addrlen >> 2];
          HEAP8.set(sockAddr.subarray(0, len), addr);
          HEAP32[addrlen >> 2] = sockAddr.length;

          return 0;
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
      },
      getpeername: function(sock, addr, addrlen) {
        try {
          const peerAddress = tizentvwasm.SocketsManager.getPeerName(sock.sock_fd);

          const peerAddr = SOCKFS.createBytesFromNetAddress(peerAddress);
          const len = HEAP32[addrlen >> 2];
          HEAP8.set(peerAddr.subarray(0, len), addr);
          HEAP32[addrlen >> 2] = peerAddr.length;

          return 0;
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
      },
      shutdown: function(sock, how) {
        const howFlag = SOCKFS.intToShutdownType(how);
        if (howFlag === null) {
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }

        try {
          tizentvwasm.SocketsManager.shutdown(sock.sock_fd, howFlag);
          return 0;
        } catch (err) {
          throw new FS.ErrnoError(SOCKFS.getErrorCode(sock.sock_fd));
        }
      },
    },
    sizeof: {
      SOCKADDR_IN: 16,
      SOCKADDR_IN6: 28,
      HOSTENT: 20,
      FD_SET: 128,
      IPv4ADDR: 4,
      IPv6ADDR: 16,
    },
    conf: {
      HOST_BUFFER_SIZE: 1024,
      MAX_HOST_ADDRESSES: 35,
      MAX_HOST_ALIASES: 35,
      loggingEnabled: true,
    },
    storage: {
      // TODO(j.gajownik2) sizeof hostent
      host: {{{ makeStaticAlloc(20) }}},
      hostAliasPtrs: {{{ makeStaticAlloc(35) }}}, // max host aliases
      hostAddrPtrs: {{{ makeStaticAlloc(35) }}}, // max addresses
      hostBuffer: {{{ makeStaticAlloc(1024) }}}, // host buffer size
    },

    options: {
      SO_DEBUG: 1,
      SO_ERROR: 4,
      SO_BROADCAST: 6,
      SO_REUSEADDR: 2,
      SO_KEEPALIVE: 9,
      SO_LINGER: 13,
      SO_OOBINLINE: 10,
      SO_SNDBUF: 7,
      SO_RCVBUF: 8,
      SO_DONTROUTE: 5,
      SO_RCVLOWAT: 18,
      SO_RCVTIMEO: 20,
      SO_SNDLOWAT: 19,
      SO_SNDTIMEO: 21,
      TCP_NODELAY: 1,
    },
    levels: {
      SOL_SOCKET: 1,
      IPPROTO_TCP: 6,
    },

    convertToEnum: function(object, integer) {
      for (const key in object) {
        if (object[key].value === integer) {
          return object[key].name;
        }
      }
      return null;
    },
    convertToInt: function(object, enumeration) {
      for (const key in object) {
        if (object[key].name === enumeration) {
          return object[key].value;
        }
      }
    },
    Family: {
      AF_UNSPEC: {name: 'af_unspec', value: {{{ cDefine('AF_UNSPEC') }}} },
      AF_INET: {name: 'af_inet', value: {{{ cDefine('AF_INET') }}} },
      AF_INET6: {name: 'af_inet6', value: {{{ cDefine('AF_INET6') }}} },
    },
    SockType: {
      SOCK_ANY: {name: 'sock_any', value: 0},
      SOCK_STREAM: {name: 'sock_stream', value: {{{ cDefine('SOCK_STREAM') }}} },
      SOCK_DGRAM: {name: 'sock_dgram', value: {{{ cDefine('SOCK_DGRAM') }}} },
    },
    Protocol: {
      IPPROTO_IP: {name: 'ipproto_ip', value: {{{ cDefine('IPPROTO_IP') }}} },
      IPPROTO_TCP: {name: 'ipproto_tcp', value: {{{ cDefine('IPPROTO_TCP') }}} },
      IPPROTO_UDP: {name: 'ipproto_udp', value: {{{ cDefine('IPPROTO_UDP') }}} },
    },
    ShutdownType: {
      SHUT_RD: {name: 'shut_rd', value: {{{ cDefine('SHUT_RD') }}} },
      SHUT_WR: {name: 'shut_wr', value: {{{ cDefine('SHUT_WR') }}} },
      SHUT_RDWR: {name: 'shut_rdwr', value: {{{ cDefine('SHUT_RDWR') }}} },
    },
    intToFamily: function(family) {
      return SOCKFS.convertToEnum(SOCKFS.Family, family);
    },
    intToSockType: function(type) {
      return SOCKFS.convertToEnum(SOCKFS.SockType, type);
    },
    intToShutdownType: function(type) {
      return SOCKFS.convertToEnum(SOCKFS.ShutdownType, type);
    },
    createNetAddress__deps: ['_inet_pton6_raw'],
    createNetAddress: function(address, port) {
      let addrBytes;
      let family;
      const ipv4 = address.split('.');
      if (ipv4.length == 4) {
        addrBytes = new Uint8Array(4);
        for (i in ipv4) {
          addrBytes[i] = parseInt(ipv4[i]);
        }
        family = "af_inet";
      } else {
        let addr = __inet_pton6_raw(address);
        let buffer = new ArrayBuffer(16);
        let view = new Uint16Array(buffer);
        addrBytes = new Uint8Array(buffer);

        for (let i = 0; i < 8; i++) {
          view[i] = addr[i];
        }
        family = "af_inet6";
      }

      return new tizentvwasm.NetAddress(family, addrBytes, port);
    },
    createNetAddressFromBytes: function(bytes) {
      const familyId = bytes[0];
      let family;
      let addrBytes;
      const port = (new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength)).getUint16(2, false);

      switch (familyId) {
        case SOCKFS.Family.AF_INET.value:
          family = "af_inet";
          addrBytes = bytes.subarray(
            {{{ C_STRUCTS.sockaddr_in.sin_addr.s_addr }}},
            {{{ C_STRUCTS.sockaddr_in.sin_addr.s_addr }}} + SOCKFS.sizeof.IPv4ADDR);
          break;
        case SOCKFS.Family.AF_INET6.value:
          family = "af_inet6";
          addrBytes = bytes.subarray(
            {{{ C_STRUCTS.sockaddr_in6.sin6_addr.__in6_union.__s6_addr }}},
            {{{ C_STRUCTS.sockaddr_in6.sin6_addr.__in6_union.__s6_addr }}} +
                SOCKFS.sizeof.IPv6ADDR);
          break;
        default:
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
      }
      return new tizentvwasm.NetAddress(family, addrBytes, port);
    },
    getLevelAndOptionString: function(level, option, fromGet) {
      let result = null;
      if (level == SOCKFS.levels.IPPROTO_TCP) {
        if (option == SOCKFS.options.TCP_NODELAY) {
          result = {};
          result["level"] = "ipproto_tcp";
          result["option"] = "tcp_nodelay";
        } else {
          throw new FS.ErrnoError({{{ cDefine('ENOPROTOOPT') }}});
        }
      } else if (level == SOCKFS.levels.SOL_SOCKET) {
        result = {};
        result["level"] = "sol_socket";
        switch (option) {
          case SOCKFS.options.SO_DEBUG:
            result["option"] = "so_debug";
            break;
          case SOCKFS.options.SO_ERROR:
            result["option"] = "so_error";
            break;
          case SOCKFS.options.SO_BROADCAST:
            result["option"] = "so_broadcast";
            break;
          case SOCKFS.options.SO_REUSEADDR:
            result["option"] = "so_reuseaddr";
            break;
          case SOCKFS.options.SO_KEEPALIVE:
            result["option"] = "so_keepalive";
            break;
          case SOCKFS.options.SO_LINGER:
            result["option"] = "so_linger";
            break;
          case SOCKFS.options.SO_OOBINLINE:
            result["option"] = "so_oobinline";
            break;
          case SOCKFS.options.SO_SNDBUF:
            result["option"] = "so_sndbuf";
            break;
          case SOCKFS.options.SO_RCVBUF:
            result["option"] = "so_rcvbuf";
            break;
          case SOCKFS.options.SO_DONTROUTE:
            result["option"] = "so_dontroute";
            break;
          case SOCKFS.options.SO_RCVLOWAT:
            result["option"] = "so_rcvlowat";
            break;
          case SOCKFS.options.SO_RCVTIMEO:
            result["option"] = "so_rcvtimeo";
            break;
          case SOCKFS.options.SO_SNDLOWAT:
            result["option"] = "so_sndlowat";
            break;
          case SOCKFS.options.SO_SNDTIMEO:
            result["option"] = "so_sndtimeo";
            break;
          default:
            throw new FS.ErrnoError({{{ cDefine('ENOPROTOOPT') }}});
        }
      } else {
        if (fromGet) {
          throw new FS.ErrnoError({{{ cDefine('EOPNOTSUPP') }}});
        } else {
          throw new FS.ErrnoError({{{ cDefine('ENOPROTOOPT') }}});
        }
      }
      return result;
    },
    decodeValue: function(option, data) {
      let value;
      switch (option) {
        case SOCKFS.options.SO_DEBUG:
          // TCP_NODELAY has the same value as SO_DEBUG
          // fallthrough
        case SOCKFS.options.SO_ERROR:
        case SOCKFS.options.SO_BROADCAST:
        case SOCKFS.options.SO_REUSEADDR:
        case SOCKFS.options.SO_KEEPALIVE:
        case SOCKFS.options.SO_OOBINLINE:
        case SOCKFS.options.SO_SNDBUF:
        case SOCKFS.options.SO_RCVBUF:
        case SOCKFS.options.SO_DONTROUTE:
        case SOCKFS.options.SO_RCVLOWAT:
        case SOCKFS.options.SO_SNDLOWAT:
          value = (new DataView(data.buffer)).getUint32(0, true);
          break;
        case SOCKFS.options.SO_RCVTIMEO:
        case SOCKFS.options.SO_SNDTIMEO: {
          const sec = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.timeval.tv_sec }}}, true);
          const usec = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.timeval.tv_usec }}}, true);
          value = new tizentvwasm.SockOptTimeVal(sec, usec);
          break;
        }
        case SOCKFS.options.SO_LINGER: {
          const onoff = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.linger.l_onoff }}}, true);
          const linger = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.linger.l_linger }}}, true);
          value = new tizentvwasm.SockOptSoLinger(onoff, linger);
          break;
        }
      }
      return value;
    },
    encodeValue: function(option, value, len) {
      let encodeVal;
      switch (option) {
        case SOCKFS.options.SO_DEBUG:
          // TCP_NODELAY has the same value as SO_DEBUG
          // fallthrough
        case SOCKFS.options.SO_ERROR:
        case SOCKFS.options.SO_BROADCAST:
        case SOCKFS.options.SO_REUSEADDR:
        case SOCKFS.options.SO_KEEPALIVE:
        case SOCKFS.options.SO_OOBINLINE:
        case SOCKFS.options.SO_SNDBUF:
        case SOCKFS.options.SO_RCVBUF:
        case SOCKFS.options.SO_DONTROUTE:
        case SOCKFS.options.SO_RCVLOWAT:
        case SOCKFS.options.SO_SNDLOWAT:
          if (len < 4) {
            throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
          }
          encodeVal = new Uint8Array(4);
          (new DataView(encodeVal.buffer)).setUint32(0, value, true);
          break;
        case SOCKFS.options.SO_RCVTIMEO:
        case SOCKFS.options.SO_SNDTIMEO:
          if (len < 8) {
            throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
          }
          encodeVal = new Uint8Array(8);
          (new DataView(encodeVal.buffer)).setUint32(
            {{{ C_STRUCTS.timeval.tv_sec }}}, value.seconds, true, true);
          (new DataView(encodeVal.buffer)).setUint32(
            {{{ C_STRUCTS.timeval.tv_usec }}}, value.microseconds, true, true);
          break;
        case SOCKFS.options.SO_LINGER:
          if (len < 4) {
            throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
          }
          encodeVal = new Uint8Array(8);
          (new DataView(encodeVal.buffer)).setUint32(
            {{{ C_STRUCTS.linger.l_onoff }}}, value.onoff, true);
          (new DataView(encodeVal.buffer)).setUint32(
            {{{ C_STRUCTS.linger.l_linger }}}, value.linger, true);
            break;
      }
      return encodeVal;
    },
    createBytesFromNetAddress: function(netAddr) {
      let bytes;
      switch (netAddr.family) {
        case "af_inet":
          bytes = new Uint8Array(SOCKFS.sizeof.SOCKADDR_IN);
          for (let i = 0; i < bytes.length; i++) {
            bytes[i] = 0;
          }
          bytes[{{{ C_STRUCTS.sockaddr_in.sin_family }}}] = SOCKFS.Family.AF_INET.value;
          (new DataView(bytes.buffer)).setUint16({{{ C_STRUCTS.sockaddr_in.sin_port }}}, netAddr.port, false);
          bytes.set(netAddr.bytes, {{{ C_STRUCTS.sockaddr_in.sin_addr.s_addr }}} );
          break;
        case "af_inet6":
          bytes = new Uint8Array(SOCKFS.sizeof.SOCKADDR_IN6);
          for (let i = 0; i < bytes.length; i++) {
            bytes[i] = 0;
          }
          bytes[{{{ C_STRUCTS.sockaddr_in6.sin6_family }}}] = SOCKFS.Family.AF_INET6.value;
          (new DataView(bytes.buffer)).setUint16({{{ C_STRUCTS.sockaddr_in6.sin6_port }}}, netAddr.port, false);
          bytes.set(netAddr.bytes, {{{ C_STRUCTS.sockaddr_in6.sin6_addr.__in6_union.__s6_addr }}});
          break;
        default:
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
      }
      return bytes;
    },
    createAddrFromNetAddress: function(netAddr) {
      let addr;
      let bytes = netAddr.bytes;
      let byte2hex = function(value) {
        return ('0' + value.toString(16)).substr(-2);
      };
      switch (netAddr.family) {
        case "af_inet":
          addr = bytes[0].toString();
          for (let i = 1; i < 4; i++) {
            addr = addr + "." + bytes[i];
          }
          break;
        case "af_inet6":
          addr = byte2hex(bytes[0]);
          addr = addr + byte2hex(bytes[1]);
          for (let i = 1; i < bytes.length / 2; i++) {
            addr = addr + ":" + byte2hex(bytes[2 * i]) + byte2hex(bytes[2 * i + 1]);
          }
          break;
        default:
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
      }
      return addr;
    },
    pollFlagsMap: function() {
      const PollFlags = tizentvwasm.PollFlags;
      const flagsMap = new Map([
        [ PollFlags.POLLIN,     {{{ cDefine('POLLIN')    }}}],
        [ PollFlags.POLLRDNORM, {{{ cDefine('POLLRDNORM')}}}],
        [ PollFlags.POLLRDBAND, {{{ cDefine('POLLRDBAND')}}}],
        [ PollFlags.POLLPRI,    {{{ cDefine('POLLPRI')   }}}],
        [ PollFlags.POLLOUT,    {{{ cDefine('POLLOUT')   }}}],
        [ PollFlags.POLLWRNORM, {{{ cDefine('POLLWRNORM')}}}],
        [ PollFlags.POLLWRBAND, {{{ cDefine('POLLWRBAND')}}}],
        [ PollFlags.POLLERR,    {{{ cDefine('POLLERR')   }}}],
        [ PollFlags.POLLHUP,    {{{ cDefine('POLLHUP')   }}}],
        [ PollFlags.POLLNVAL,   {{{ cDefine('POLLNVAL')  }}}],
      ]);

      return flagsMap;
    },
    pollEventsConvertFromJS: function(revents) {
      let result = 0;
      SOCKFS.pollFlagsMap().forEach((value, key) => {
        if ((revents & key) == key) {
          result |= value;
        }
      });
      return result;
    },
    pollEventsConvertToJS: function(events) {
      let result = 0;
      SOCKFS.pollFlagsMap().forEach((value, key) => {
        if ((events & value) == value) {
          result |= key;
        }
      });
      return result;
    },
    getMsgFlagsMap: function() {
      const MsgFlags = tizentvwasm.MsgFlags;
      return [
        [ MsgFlags.MSG_OOB, {{{ cDefine('MSG_OOB') }}} ],
        [ MsgFlags.MSG_PEEK, {{{ cDefine('MSG_PEEK') }}} ],
        [ MsgFlags.MSG_EOR, {{{ cDefine('MSG_EOR') }}} ],
        [ MsgFlags.MSG_WAITALL, {{{ cDefine('MSG_WAITALL') }}} ],
        [ MsgFlags.MSG_NOSIGNAL, {{{ cDefine('MSG_NOSIGNAL') }}} ]
      ];
    },
    msgFlagsToJs: function(flags) {
      if (flags === 0) {
        return 0;
      }

      let result = 0;
      SOCKFS.getMsgFlagsMap().forEach((item) => {
        if ((flags & item[1]) === item[1]) {
          result |= item[0];
        }
      });
      return result;
    },
    msgFlagsFromJs: function(flags) {
      if (flags === 0) {
        return 0;
      }

      let result = 0;
      SOCKFS.getMsgFlagsMap().forEach((item) => {
        if ((flags & item[0]) === item[0]) {
          result |= item[1];
        }
      });
      return result;
    },
    getFDsUnionAtOffset: function(offset, readfds, writefds, exceptfds) {
      return (readfds ? {{{ makeGetValue('readfds', 'offset', 'i32') }}} : 0)
           | (writefds ? {{{ makeGetValue('writefds', 'offset', 'i32') }}} : 0)
           | (exceptfds ? {{{ makeGetValue('exceptfds', 'offset', 'i32') }}} : 0);
    },
    countFDsInFdSets: function(nfds, readfds, writefds, exceptfds) {
      const ret = {
        total: 0,
        sockets: 0
      };

      const fdSetSize = {{{ cDefine('FD_SETSIZE') }}};
      if (nfds <= 0 || nfds > fdSetSize) {
        return ret;
      }

      let offset = 0;
      let fds = SOCKFS.getFDsUnionAtOffset(offset, readfds, writefds, exceptfds);
      let fdShift = 0;
      for (let fd = 0; fd < nfds; fd++) {
        if ((fds & (1 << fdShift)) !== 0) {
          ret.total++;
          ret.sockets += (SOCKFS.hasSocket(fd) ? 1 : 0);
        }

        ++fdShift;
        if (fdShift === 32) {
          fdShift = 0;
          offset += 4
          fds = SOCKFS.getFDsUnionAtOffset(offset, readfds, writefds, exceptfds);
        }
      }

      return ret;
    },
    fdsToSequence: function(nfds, fdsSetPtr, sockFDMap) {
      if (!fdsSetPtr) {
        return [];
      }

      const ret = [];
      let offset = 0;
      let fds = {{{ makeGetValue('fdsSetPtr', 'offset', 'i32') }}};
      let fdShift = 0;
      for (let fd = 0; fd < nfds; ++fd) {
        if ((fds & (1 << fdShift)) !== 0) {
          const sockFd = SOCKFS.getSocket(fd).sock_fd;
          sockFDMap[sockFd] = fd;
          ret.push(sockFd);
        }

        ++fdShift;
        if (fdShift === 32) {
          fdShift = 0;
          offset += 4;
          fds = {{{ makeGetValue('fdsSetPtr', 'offset', 'i32') }}};
        }
      }

      return ret;
    },
    FD_ZERO: function(s) {  // Same name as FD_ZERO macro in select.h
      for (let i = 0; i < SOCKFS.sizeof.FD_SET; ++i) {
        HEAP8[s + i] = 0;
      }
    },
    FD_SET: function(d, s) {  // Same name as FD_SET macro in select.h
      HEAPU32[(s + ((d)/(8))) >> 2] |= (1 << (d) % (8*4));
    },
    setDescriptors: function(fdsSetPtr, resultSet, sockFDMap) {
      if (!fdsSetPtr) {
        return;
      }

      SOCKFS.FD_ZERO(fdsSetPtr);
      for (const fd of resultSet) {
        SOCKFS.FD_SET(sockFDMap[fd], fdsSetPtr);
      }
    },
    timevalToUSec: function(timeoutPtr) {
      if (!timeoutPtr) {
        return -1;
      }

      const timevalTVSec = {{{ makeGetValue('timeoutPtr', C_STRUCTS.timeval.tv_sec, 'i32') }}};
      const timevalTVUSec = {{{ makeGetValue('timeoutPtr', C_STRUCTS.timeval.tv_usec, 'i32') }}};
      return (timevalTVSec * 1000000) + timevalTVUSec;
    },
    callSelect: function(nfds, readfds, writefds, exceptfds, timeout) {
      const sockFDMap = new Map();
      const readSeq = SOCKFS.fdsToSequence(nfds, readfds, sockFDMap);
      const writeSeq = SOCKFS.fdsToSequence(nfds, writefds, sockFDMap);
      const exceptSeq = SOCKFS.fdsToSequence(nfds, exceptfds, sockFDMap);
      const timeoutUSec = SOCKFS.timevalToUSec(timeout);
      let result = null;
      try {
        result = tizentvwasm.SocketsManager.select(readSeq, writeSeq, exceptSeq, timeoutUSec);
      } catch (err) {
        return -SOCKFS.getErrorCode();
      }

      SOCKFS.setDescriptors(readfds, result.getReadFds(), sockFDMap);
      SOCKFS.setDescriptors(writefds, result.getWriteFds(), sockFDMap);
      SOCKFS.setDescriptors(exceptfds, result.getExceptFds(), sockFDMap);

      return result.getReadFds().length
           + result.getWriteFds().length
           + result.getExceptFds().length;
    },
    countFDsInPollFDs: function(fds, nfds) {
      const ret = {
        total: nfds,
        sockets: 0
      };

      if (nfds <= 0) {
        return ret;
      }

      for (let i = 0; i < nfds; i++) {
        const pollfd = fds + {{{ C_STRUCTS.pollfd.__size__ }}} * i;
        const fd = {{{ makeGetValue('pollfd', C_STRUCTS.pollfd.fd, 'i32') }}};
        ret.sockets += (SOCKFS.hasSocket(fd) ? 1 : 0);
      }

      return ret;
    },
    callPoll: function(fdsPtr, nfds, timeout) {
      const pollFds = [];

      for (let i = 0; i < nfds; i++) {
        const pollfd = fdsPtr + {{{ C_STRUCTS.pollfd.__size__ }}} * i;
        const fd = {{{ makeGetValue('pollfd', C_STRUCTS.pollfd.fd, 'i32') }}};
        const events = {{{ makeGetValue('pollfd', C_STRUCTS.pollfd.events, 'i16') }}};
        const sockFd = SOCKFS.getSocket(fd).sock_fd;
        const pollEvents = SOCKFS.pollEventsConvertToJS(events);

        pollFds.push(new tizentvwasm.PollFd(sockFd, pollEvents));
      }

      let result = -1;
      try {
        result = tizentvwasm.SocketsManager.poll(pollFds, timeout);
      } catch (err) {
        return -SOCKFS.getErrorCode();
      }

      for (let i = 0; i < nfds; i++) {
        const pollfd = fdsPtr + {{{ C_STRUCTS.pollfd.__size__ }}} * i;
        const revents = SOCKFS.pollEventsConvertFromJS(pollFds[i].revents);
        {{{ makeSetValue('pollfd', C_STRUCTS.pollfd.revents, 'revents', 'i16') }}}
      }

      return result;
    },
  },
  _getSocketBuffer__proxy: 'sync',
  _getSocketBuffer: function() {
    return SOCKFS.getSocketMapPtr();
  },
  _createSocketOnRenderThread__proxy: 'sync',
  _createSocketOnRenderThread: function(family, type, protocol, socket) {
    const fd = SOCKFS.createSocketOnCurrentThread(family, type, protocol, socket);
    SOCKFS.setSocketFdInMap(fd);
    return fd;
  },
  _closeSocketOnRenderThread__proxy: 'sync',
  _closeSocketOnRenderThread: function(fd) {
    FS.closeStream(fd);
    SOCKFS.clearSocketFdInMap(fd);
  },
  _cloneSocketFromRenderThread__proxy: 'sync',
  _cloneSocketFromRenderThread: function(fd) {
    const stream = FS.getStream(fd);
    const ptr = _malloc(16);
    HEAP32[ptr >> 2] = stream.node.sock.family;
    HEAP32[(ptr >> 2) + 1] = stream.node.sock.type;
    HEAP32[(ptr >> 2) + 2] = stream.node.sock.protocol;
    HEAP32[(ptr >> 2) + 3] = stream.node.sock.sock_fd;
    return ptr;
  },
});
