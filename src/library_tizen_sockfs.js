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
      return FS.createNode(null, '/', {{{ cDefine('S_IFDIR') }}} | 511 /* 0777 */, 0);
    },
    createSocket: function(family, type, protocol) {
      var streaming = type == {{{ cDefine('SOCK_STREAM') }}};

      const familyName = SOCKFS.intToFamily(family);
      if (familyName === null || familyName === "af_unspec") {
        SOCKFS.doLog("SOCKFS socket: not supported domain type");
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
        option |= SockFlags.SOCK_CLOEXEC;
        type &= ~SOCK_CLOEXEC;
      }
      if (type & SOCK_NONBLOCK) {
        option |= SockFlags.SOCK_NONBLOCK;
        type &= ~SOCK_NONBLOCK;
      }

      try {
        const sockType = SOCKFS.intToSockType(type);
        if (sockType) {
          socket = SocketsManager.create(familyName, sockType, option);
        } else {
          SOCKFS.doLog("SocketSync js_socket invalid type: " + type);
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }
      } catch (err) {
        SOCKFS.doLog(`SOCKFS socket error creating socket - errno: [${err}]`);
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

      return sock;
    },
    getSocket: function(fd) {
      var stream = FS.getStream(fd);
      if (!stream || !FS.isSocket(stream.node.mode)) {
        return null;
      }
      return stream.node.sock;
    },
    hasSocket: function(fd) {
      const stream = FS.getStream(fd);
      if (!stream || !FS.isSocket(stream.node.mode)) {
        return false;
      }
      return true;
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
        var sock = stream.node.sock;
        var msg = sock.sock_ops.recvmsg(sock, length);
        if (!msg) {
          // socket is closed
          return 0;
        }
        buffer.set(msg.buffer, offset);
        return msg.buffer.length;
      },
      write: function(stream, buffer, offset, length, position /* ignored */ ) {
        var sock = stream.node.sock;
        return sock.sock_ops.sendmsg(sock, buffer, offset, length);
      },
      close: function(stream) {
        var sock = stream.node.sock;
        sock.sock_ops.close(sock);
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
        const events = PollFlags.In
                       | PollFlags.RdNorm
                       | PollFlags.Pri
                       | PollFlags.Out
                       | PollFlags.WrNorm;
        const poll_fd = new PollFd(sock.sock_fd, events);

        try {
          const result = SocketsManager.poll([poll_fd], 0);
        } catch (err) {
          throw new FS.ErrnoError(SocketsManager.getErrorCode());
        }

        return SOCKFS.pollEventsConvert(poll_fd.revents);
      },
      ioctl: function(sock, request, arg) {
        console.log("SOCKFS ioctl() not implemented");
      },
      close: function(sock) {
        try {
          SocketsManager.close(sock.sock_fd);
          sock.sock_fd = -1; // mark thas socket is closed
        } catch (err) {
          SOCKFS.doLog(`SOCKFS close error on socket close errno: [${err}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      bind: function(sock, addr, port) {
        try {
          const netAddr = SOCKFS.createNetAddress(addr, port);
          SocketsManager.bind(sock.sock_fd, netAddr);
        } catch (err) {
          const errorCode = SocketsManager.getErrorCode(sock.sock_fd);
          if (errorCode) {
            throw new FS.ErrnoError(errorCode);
          }
        }
      },
      connect: function(sock, addr, port) {
        try {
          const netAddr = SOCKFS.createNetAddress(addr, port);
          SocketsManager.connect(sock.sock_fd, netAddr);
        } catch (err) {
          const errorCode = SocketsManager.getErrorCode(sock.sock_fd);
          if (errorCode) {
            throw new FS.ErrnoError(errorCode);
          }
        }
      },
      listen: function(sock, backlog) {
        if (sock.type !== SOCKFS.SockType.SOCK_STREAM.value) {
          throw new FS.ErrnoError({{{ cDefine('EOPNOTSUPP') }}});
          return -1;
        }
        try {
          SocketsManager.listen(sock.sock_fd, backlog);
        } catch (err) {
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
        return 0;
      },
      accept: function(listensock, addr, addrlen) {
        try {
          const newSockSync = SocketsManager.accept4(listensock.sock_fd, 0);

          if (addr && addrlen) {
            const peerAddr = SOCKFS.createBytesFromNetAddress(SocketsManager.getPeerName(newSockSync));
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
          let fd= sock.stream.fd;
          let st = FS.getStream(fd);
          return sock;
        } catch (err) {
          SOCKFS.doLog(`SOCKFS accept error - errno: [${SocketsManager.getErrorCode(listensock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(listensock.sock_fd));
        }

      },
      getname: function(sock, peer) {
        console.log("SOCKFS getname() not implemented");
      },
      sendmsg: function(sock, buffer, offset, length, addr, port) {
        if (ArrayBuffer.isView(buffer)) {
          offset += buffer.byteOffset;
          buffer = buffer.buffer;
        }

        let data = new Uint8Array(buffer, offset, length);
        let netAddr = null;

        if (sock.type == SOCKFS.SockType.SOCK_STREAM.value) {
          try {
            return SocketsManager.send(sock.sock_fd, data, 0);
          } catch (err) {
            SOCKFS.doLog(`SOCKFS sendmsg[${sock.sock_fd}] error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
            throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
          }
        } else if (sock.type == SOCKFS.SockType.SOCK_DGRAM.value) {
          if (!addr || port === undefined || port === null) {
            try {
              netAddr = SocketsManager.getPeerName(sock.sock_fd);
            } catch (err) {
              throw new FS.ErrnoError({{{ cDefine('EDESTADDRREQ') }}});
            }
          } else {
            netAddr = SOCKFS.createNetAddress(addr, port);
          }
          try {
            return SocketsManager.sendTo(sock.sock_fd, data, 0, netAddr);
          } catch (err) {
            SOCKFS.doLog(`SOCKFS sendmsg[${sock.sock_fd}] error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
            throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
          }
        }
      },
      recvmsg: function(sock, length) {
        let addr = "", port = 0;
        let data = new Uint8Array(length);
        let buffer;
        try {
          if (sock.type == SOCKFS.SockType.SOCK_STREAM.value) {
            const retVal = SocketsManager.recv(sock.sock_fd, data, 0);
            buffer = new Uint8Array(data.buffer, 0, retVal);
          } else {
            const retVal = SocketsManager.recvFrom(sock.sock_fd, data, 0);
            buffer = new Uint8Array(data.buffer, 0, retVal.bytesRead);
            addr = SOCKFS.createAddrFromNetAddress(retVal.peerAddress);
            port = retVal.peerAddress.port;
          }
        } catch (err) {
          SOCKFS.doLog(`SOCKFS recvmsg error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
        return {
          buffer: buffer,
          addr: addr,
          port: port,
        };
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
          SocketsManager.setSockOpt(sock.sock_fd, args.level, args.option, value);
        } catch (err) {
          SOCKFS.doLog(`SOCKFS setsockopt error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
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
          val = SocketsManager.getSockOpt(sock.sock_fd, args.level, args.option);
        } catch (err) {
          SOCKFS.doLog(`SOCKFS getsockopt error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
        const encVal = SOCKFS.encodeValue(optname, val, _optlen);
        HEAPU8.set(encVal, optval);
        HEAP32[optlen >> 2] = encVal.length;
        return 0;
      },
      getsockname: function(sock, addr, addrlen) {
        try {
          const sockAddress = SocketsManager.getSockName(sock.sock_fd);

          const sockAddr = SOCKFS.createBytesFromNetAddress(sockAddress);
          const len = HEAP32[addrlen >> 2];
          HEAP8.set(sockAddr.subarray(0, len), addr);
          HEAP32[addrlen >> 2] = sockAddr.length;

          return 0;
        } catch (err) {
          SOCKFS.doLog(`SOCKFS getsockname error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
      },
      getpeername: function(sock, addr, addrlen) {
        try {
          const peerAddress = SocketsManager.getPeerName(sock.sock_fd);

          const peerAddr = SOCKFS.createBytesFromNetAddress(peerAddress);
          const len = HEAP32[addrlen >> 2];
          HEAP8.set(peerAddr.subarray(0, len), addr);
          HEAP32[addrlen >> 2] = peerAddr.length;

          return 0;
        } catch (err) {
          SOCKFS.doLog(`SOCKFS getsockname error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
        }
      },
      shutdown: function(sock, how) {
        const howFlag = SOCKFS.intToShutdownType(how);
        if (howFlag === null) {
          SOCKFS.doLog("SOCKFS shutdown: not supported shutdown type");
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
        }

        try {
          SocketsManager.shutdown(sock.sock_fd, howFlag);
          return 0;
        } catch (err) {
          SOCKFS.doLog(`SOCKFS shutdown error - errno: [${SocketsManager.getErrorCode(sock.sock_fd)}]`);
          throw new FS.ErrnoError(SocketsManager.getErrorCode(sock.sock_fd));
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

      return new NetAddress(family, addrBytes, port);
    },
    getLevelAndOptionString: function(level, option, fromGet) {
      let result = null;
      if (level == SOCKFS.levels.IPPROTO_TCP) {
        if (option == SOCKFS.options.TCP_NODELAY) {
          result = {};
          result["level"] = "ipproto_tcp";
          result["option"] = "tcp_nodelay";
        } else {
          SOCKFS.doLog("SOCKFS getLevelAndOptionString: not supported option name");
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
            SOCKFS.doLog("SOCKFS getLevelAndOptionString: not supported option name");
            throw new FS.ErrnoError({{{ cDefine('ENOPROTOOPT') }}});
        }
      } else {
        SOCKFS.doLog("SOCKFS getLevelAndOptionString: not supported level");
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
          value = new SockOptTimeVal(sec, usec);
          break;
        }
        case SOCKFS.options.SO_LINGER: {
          const onoff = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.linger.l_onoff }}}, true);
          const linger = (new DataView(data.buffer)).getUint32(
            {{{ C_STRUCTS.linger.l_linger }}}, true);
          value = new SockOptSoLinger(onoff, linger);
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
          SOCKFS.doLog("SOCKFS createBytesFromNetAddress: not supported address family");
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
          SOCKFS.doLog("SOCKFS createAddrFromNetAddress: not supported address family ("+netAddr.family+")");
          throw new FS.ErrnoError({{{ cDefine('EINVAL') }}});
      }
      return addr;
    },
    pollEventsConvert: function(revents) {
      const flags_map = new Map([
        [ PollFlags.In,     {{{ cDefine('POLLIN')    }}}],
        [ PollFlags.RdNorm, {{{ cDefine('POLLRDNORM')}}}],
        [ PollFlags.RdBand, {{{ cDefine('POLLRDBAND')}}}],
        [ PollFlags.Pri,    {{{ cDefine('POLLPRI')   }}}],
        [ PollFlags.Out,    {{{ cDefine('POLLOUT')   }}}],
        [ PollFlags.WrNorm, {{{ cDefine('POLLWRNORM')}}}],
        [ PollFlags.WrBand, {{{ cDefine('POLLWRBAND')}}}],
        [ PollFlags.Err,    {{{ cDefine('POLLERR')   }}}],
        [ PollFlags.Hup,    {{{ cDefine('POLLHUP')   }}}],
        [ PollFlags.Nval,   {{{ cDefine('POLLNVAL')  }}}],
      ]);
      let result = 0;
      flags_map.forEach((value, key) => {
        if ((revents & key) == key) {
          result |= value;
        }
      });
      return result;
    },
    doLog: function(...args) {
      if (SOCKFS.conf.loggingEnabled) {
        console.log.apply(null, args);
      }
    },
  },
});
