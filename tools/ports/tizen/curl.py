# Copyright 2020 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
import shutil

TAG = '7.68.0'
HASH = 'ad7390fd700cb74db356a39e842dab011823b87d4047687f2a8c2e0f2920a4f8c6c193ba56391489a75939cc5c39a4dccec4e4ceeac516eb7394f03e0fb7aeae'

def get(ports, settings, shared):
  if settings.USE_CURL != 1:
    return []

  ports.fetch_project(
      'curl',
      'https://curl.haxx.se/download/curl-' + TAG + '.tar.bz2',
      'curl-' + TAG,
      is_tarbz2=True,
      sha512hash=HASH)

  def create():
    logging.info('building port: curl')

    source_path = os.path.join(ports.get_dir(), 'curl', 'curl-' + TAG)
    dest_path = os.path.join(ports.get_build_dir(), 'curl')

    ports.clear_project_build('curl')

    crypto_lib = shared.Cache.get_path('libcrypto.a')
    ssl_lib = shared.Cache.get_path('libssl.a')
    openssl_include = os.path.join(ports.get_include_dir(), 'openssl')
    zlib = shared.Cache.get_path('libz.a')
    configure_args = [
      'cmake',
      '-B' + dest_path,
      '-H' + source_path,
      '-G', 'Unix Makefiles',
      '-C' + shared.path_from_root('tools', 'ports', 'tizen', 'curl_cmake.cache'),
      '-DCMAKE_BUILD_TYPE=Release',
      '-DCMAKE_INSTALL_PREFIX=' + dest_path,
      '-DBUILD_CURL_EXE=OFF',
      '-DBUILD_SHARED_LIBS=OFF',
      '-DENABLE_THREADED_RESOLVER=OFF',
      '-DBUILD_TESTING=OFF',
      '-DOPENSSL_INCLUDE_DIR=' + openssl_include,
      '-DOPENSSL_CRYPTO_LIBRARY=' + crypto_lib,
      '-DOPENSSL_SSL_LIBRARY=' + ssl_lib,
      '-DZLIB_LIBRARY=' + zlib,
      '-DZLIB_INCLUDE_DIR=' + ports.get_include_dir(),
    ]

    shared.Building.configure(configure_args)

    shared.Building.make(['make', '-j%d' % shared.Building.get_num_cores(), '-C' + dest_path])
    shared.Building.make(['make', '-j%d' % shared.Building.get_num_cores(), '-C' + dest_path, 'install'])

    ports.install_header_dir(os.path.join(dest_path, 'include', 'curl'))

    return os.path.join(dest_path, 'lib', 'libcurl.a')

  return [
      shared.Cache.get('libcurl.a', create, what='port'),
  ]


def clear(ports, shared):
  shared.Cache.erase_file('libcurl.a')


def process_dependencies(settings):
  if settings.USE_CURL == 1:
    settings.USE_OPENSSL = 1
    settings.USE_ZLIB = 1


def process_args(ports, args, settings, shared):
  if settings.USE_CURL == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_build_dir(), 'curl', 'include', 'curl')]
  return args


def show():
  return 'curl (USE_CURL=1; MIT style license )'
