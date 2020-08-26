# Emscripten port for Tizen Smart TVs

This is a fork of the emscripten project adapted to run on Samsung
Tizen TVs. Changes made:

1. Uses fastcomp backend, because '20 Tizen TVs doesn't support Bulk Memory Operations (https://github.com/WebAssembly/bulk-memory-operations). Bulk Memory Operations are requied by LLVM backend to support threads
2. Added features:
- Socketes [Tizen Sockets Extension](https://developer.samsung.com/smarttv/develop/extension-libraries/webassembly/api-reference/tizen-sockets-extension.html)
- WASM Player [Tizen WASM Player](https://developer.samsung.com/smarttv/develop/extension-libraries/webassembly/tizen-wasm-player/overview.html)
3. Features availablem using samsung toolchain:
- Threads
- Emscipten ports: cURL, crypto, ssl

