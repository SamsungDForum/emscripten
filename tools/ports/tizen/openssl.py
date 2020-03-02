# Copyright 2020 The Emscripten Authors.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
import shutil

TAG = '1.1.1d'
HASH = '2bc9f528c27fe644308eb7603c992bac8740e9f0c3601a130af30c9ffebbf7e0f5c28b76a00bbb478bad40fbe89b4223a58d604001e1713da71ff4b7fe6a08a7'

# Note OpenSSL needs perl during build
def get(ports, settings, shared):
  if settings.USE_OPENSSL != 1:
    return []

  ports.fetch_project(
      'openssl',
      'https://www.openssl.org/source/openssl-' + TAG + '.tar.gz',
      'openssl-' + TAG,
      sha512hash=HASH)

  source_path = os.path.join(ports.get_dir(), 'openssl', 'openssl-' + TAG)
  dest_path = os.path.join(ports.get_build_dir(), 'openssl')
  open(os.path.join(source_path,
                    'Configurations/50-emscripten.conf'),
       'w').write(openssl_emscripten_template_conf)

  # TODO: Currently openssl is built twice once for libcrypto.a and second time
  #       for libssl.a.
  def create(sub_libname):
    logging.info('building port: OpenSSL lib{}.a'.format(sub_libname))
    configure_args = [
      'perl',
      os.path.join(source_path, 'Configure'),
      '--prefix=' + dest_path,
      'no-asm',
      'no-hw',
      '-D_GNU_SOURCE',
      'wasm-le32emscripten'
    ]

    env = shared.Building.get_building_env()
    env['SYSTEM'] = 'wasm'
    env['MACHINE'] = 'le32emscripten'
    # Clear this for OpenSSL as its configure script prepends this to $CC,
    # which is already absolute path.
    env['CROSS_COMPILE'] = ''
    curr_dir = os.getcwd()
    try:
      os.chdir(source_path)
      shared.Building.configure(configure_args, env=env)
      os.chdir(curr_dir)
    except:
      os.chdir(curr_dir)
      raise

    shared.Building.make(['make', '-j%d' % shared.Building.get_num_cores(), '-C' + source_path, 'build_libs'])
    shared.Building.make(['make', '-j%d' % shared.Building.get_num_cores(), '-C' + source_path, 'install_dev'])

    ports.install_header_dir(os.path.join(dest_path, 'include', 'openssl'))

    libname = 'lib' + sub_libname + '.a'
    return os.path.join(dest_path, 'lib', libname)

  def create_crypto():
    return create('crypto')

  def create_ssl():
    return create('ssl')

  return [
      shared.Cache.get('libcrypto.a', create_crypto, what='port'),
      shared.Cache.get('libssl.a', create_ssl, what='port')
  ]


def clear(ports, shared):
  shared.Cache.erase_file('libcrypto.a')
  shared.Cache.erase_file('libssl.a')


def process_args(ports, args, settings, shared):
  if settings.USE_OPENSSL == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_build_dir(), 'openssl', 'include', 'openssl')]
  return args


def show():
  return 'openssl (USE_OPENSSL=1; Dual OpenSSL and SSLeay license )'


# TODO Add support for asm.js
openssl_emscripten_template_conf = '''# -*- Mode: perl -*-
# Values for configuring OpenSSL builds with emscripten
my %targets = (
    "wasm-le32emscripten" => {
      CFLAGS          => "-v -O2 -DTERMIOS",
      sys_id          => "emscripten",
      lib_cppflags    => "-DL_ENDIAN",
      thread_scheme   => "pthreads",
      bn_ops          => "BN_LLONG"
    },
);
'''
