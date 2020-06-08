# Copyright 2020 Samsung Electronics Inc.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
import shutil

TAG = '1.1.1d'
HASH = '2bc9f528c27fe644308eb7603c992bac8740e9f0c3601a130af30c9ffebbf7e0f5c28b76a00bbb478bad40fbe89b4223a58d604001e1713da71ff4b7fe6a08a7'


def get_libname(ports):
  return ports.get_lib_name('libssl')


def get(ports, settings, shared):
  if settings.USE_SSL != 1:
    return []

  #TODO Can this be shared between libcrypto and libssl?
  ports.fetch_project(
      'ssl',
      'https://www.openssl.org/source/old/1.1.1/openssl-' + TAG + '.tar.gz',
      'openssl-' + TAG,
      sha512hash=HASH)

  libname = get_libname(ports)

  def create():
    logging.info('building port: OpenSSL {}'.format(libname))
    srcs = [
      ['ssl', 'bio_ssl.c'],
      ['ssl', 'd1_lib.c'],
      ['ssl', 'd1_msg.c'],
      ['ssl', 'd1_srtp.c'],
      ['ssl', 'methods.c'],
      ['ssl', 'packet.c'],
      ['ssl', 'pqueue.c'],
      ['ssl', 'record', 'dtls1_bitmap.c'],
      ['ssl', 'record', 'rec_layer_d1.c'],
      ['ssl', 'record', 'rec_layer_s3.c'],
      ['ssl', 'record', 'ssl3_buffer.c'],
      ['ssl', 'record', 'ssl3_record.c'],
      ['ssl', 'record', 'ssl3_record_tls13.c'],
      ['ssl', 's3_cbc.c'],
      ['ssl', 's3_enc.c'],
      ['ssl', 's3_lib.c'],
      ['ssl', 's3_msg.c'],
      ['ssl', 'ssl_asn1.c'],
      ['ssl', 'ssl_cert.c'],
      ['ssl', 'ssl_ciph.c'],
      ['ssl', 'ssl_conf.c'],
      ['ssl', 'ssl_err.c'],
      ['ssl', 'ssl_init.c'],
      ['ssl', 'ssl_lib.c'],
      ['ssl', 'ssl_mcnf.c'],
      ['ssl', 'ssl_rsa.c'],
      ['ssl', 'ssl_sess.c'],
      ['ssl', 'ssl_stat.c'],
      ['ssl', 'ssl_txt.c'],
      ['ssl', 'ssl_utst.c'],
      ['ssl', 'statem', 'extensions.c'],
      ['ssl', 'statem', 'extensions_clnt.c'],
      ['ssl', 'statem', 'extensions_cust.c'],
      ['ssl', 'statem', 'extensions_srvr.c'],
      ['ssl', 'statem', 'statem.c'],
      ['ssl', 'statem', 'statem_clnt.c'],
      ['ssl', 'statem', 'statem_dtls.c'],
      ['ssl', 'statem', 'statem_lib.c'],
      ['ssl', 'statem', 'statem_srvr.c'],
      ['ssl', 't1_enc.c'],
      ['ssl', 't1_lib.c'],
      ['ssl', 't1_trce.c'],
      ['ssl', 'tls13_enc.c'],
      ['ssl', 'tls_srp.c'],
    ]

    source_path = os.path.join(ports.get_dir(), 'ssl', 'openssl-' + TAG)
    dest_path = os.path.join(ports.get_build_dir(), 'ssl')

    source_include_path = os.path.join(source_path, 'include', 'openssl')
    ports.install_headers(source_include_path, target='openssl')

    commands = []
    o_s = []
    for src_path in srcs:
      src = os.path.join(*src_path)
      src_base, c_ext = os.path.splitext(src)
      o_file = os.path.join(ports.get_build_dir(), 'ssl', src_base + '.o')
      shared.safe_ensure_dirs(os.path.dirname(o_file))
      command = [shared.PYTHON, shared.EMCC,
                 '-c', os.path.join(source_path, src),
                 '-o', o_file,
                 '-I' + ports.get_include_dir(),
                 '-I' + os.path.join(source_path),
                 '-I' + os.path.join(source_path, 'include'),
                 '-Os', '-w']
      commands.append(command)
      o_s.append(o_file)
    ports.run_commands(commands)

    final = os.path.join(ports.get_build_dir(), 'ssl', libname)
    shared.safe_ensure_dirs(os.path.dirname(final))
    ports.create_lib(final, o_s)
    return final

  return [shared.Cache.get(libname, create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file(get_libname(ports))


def process_dependencies(settings):
  if settings.USE_SSL == 1:
    settings.USE_CRYPTO = 1


def process_args(ports, args, settings, shared):
  if settings.USE_SSL == 1:
    get(ports, settings, shared)
    # Note: includes are installed by libcrypto
    args += ['-I' + os.path.join(ports.get_build_dir(), 'openssl', 'include', 'openssl')]
  return args


def show():
  return 'libssl from OpensSL (USE_SSL=1; Dual OpenSSL and SSLeay license )'
