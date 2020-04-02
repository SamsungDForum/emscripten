# Copyright 2020 Samsung Electronics Inc.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
import shutil

TAG = '1.1.1d'
HASH = '2bc9f528c27fe644308eb7603c992bac8740e9f0c3601a130af30c9ffebbf7e0f5c28b76a00bbb478bad40fbe89b4223a58d604001e1713da71ff4b7fe6a08a7'


def get(ports, settings, shared):
  if settings.USE_CRYPTO != 1:
    return []

  #TODO Can this be shared between libcrypto and libssl?
  ports.fetch_project(
      'crypto',
      'https://www.openssl.org/source/old/1.1.1/openssl-' + TAG + '.tar.gz',
      'openssl-' + TAG,
      sha512hash=HASH)

  libname = ports.get_lib_name('libcrypto')

  def create():
    logging.info('building port: OpenSSL {}'.format(libname))
    srcs = [
      ['crypto', 'aes', 'aes_cbc.c'],
      ['crypto', 'aes', 'aes_cfb.c'],
      ['crypto', 'aes', 'aes_core.c'],
      ['crypto', 'aes', 'aes_ecb.c'],
      ['crypto', 'aes', 'aes_ige.c'],
      ['crypto', 'aes', 'aes_misc.c'],
      ['crypto', 'aes', 'aes_ofb.c'],
      ['crypto', 'aes', 'aes_wrap.c'],
      ['crypto', 'aria', 'aria.c'],
      ['crypto', 'asn1', 'a_bitstr.c'],
      ['crypto', 'asn1', 'a_d2i_fp.c'],
      ['crypto', 'asn1', 'a_digest.c'],
      ['crypto', 'asn1', 'a_dup.c'],
      ['crypto', 'asn1', 'a_gentm.c'],
      ['crypto', 'asn1', 'a_i2d_fp.c'],
      ['crypto', 'asn1', 'a_int.c'],
      ['crypto', 'asn1', 'a_mbstr.c'],
      ['crypto', 'asn1', 'a_object.c'],
      ['crypto', 'asn1', 'a_octet.c'],
      ['crypto', 'asn1', 'a_print.c'],
      ['crypto', 'asn1', 'a_sign.c'],
      ['crypto', 'asn1', 'a_strex.c'],
      ['crypto', 'asn1', 'a_strnid.c'],
      ['crypto', 'asn1', 'a_time.c'],
      ['crypto', 'asn1', 'a_type.c'],
      ['crypto', 'asn1', 'a_utctm.c'],
      ['crypto', 'asn1', 'a_utf8.c'],
      ['crypto', 'asn1', 'a_verify.c'],
      ['crypto', 'asn1', 'ameth_lib.c'],
      ['crypto', 'asn1', 'asn1_err.c'],
      ['crypto', 'asn1', 'asn1_gen.c'],
      ['crypto', 'asn1', 'asn1_item_list.c'],
      ['crypto', 'asn1', 'asn1_lib.c'],
      ['crypto', 'asn1', 'asn1_par.c'],
      ['crypto', 'asn1', 'asn_mime.c'],
      ['crypto', 'asn1', 'asn_moid.c'],
      ['crypto', 'asn1', 'asn_mstbl.c'],
      ['crypto', 'asn1', 'asn_pack.c'],
      ['crypto', 'asn1', 'bio_asn1.c'],
      ['crypto', 'asn1', 'bio_ndef.c'],
      ['crypto', 'asn1', 'd2i_pr.c'],
      ['crypto', 'asn1', 'd2i_pu.c'],
      ['crypto', 'asn1', 'evp_asn1.c'],
      ['crypto', 'asn1', 'f_int.c'],
      ['crypto', 'asn1', 'f_string.c'],
      ['crypto', 'asn1', 'i2d_pr.c'],
      ['crypto', 'asn1', 'i2d_pu.c'],
      ['crypto', 'asn1', 'n_pkey.c'],
      ['crypto', 'asn1', 'nsseq.c'],
      ['crypto', 'asn1', 'p5_pbe.c'],
      ['crypto', 'asn1', 'p5_pbev2.c'],
      ['crypto', 'asn1', 'p5_scrypt.c'],
      ['crypto', 'asn1', 'p8_pkey.c'],
      ['crypto', 'asn1', 't_bitst.c'],
      ['crypto', 'asn1', 't_pkey.c'],
      ['crypto', 'asn1', 't_spki.c'],
      ['crypto', 'asn1', 'tasn_dec.c'],
      ['crypto', 'asn1', 'tasn_enc.c'],
      ['crypto', 'asn1', 'tasn_fre.c'],
      ['crypto', 'asn1', 'tasn_new.c'],
      ['crypto', 'asn1', 'tasn_prn.c'],
      ['crypto', 'asn1', 'tasn_scn.c'],
      ['crypto', 'asn1', 'tasn_typ.c'],
      ['crypto', 'asn1', 'tasn_utl.c'],
      ['crypto', 'asn1', 'x_algor.c'],
      ['crypto', 'asn1', 'x_bignum.c'],
      ['crypto', 'asn1', 'x_info.c'],
      ['crypto', 'asn1', 'x_int64.c'],
      ['crypto', 'asn1', 'x_long.c'],
      ['crypto', 'asn1', 'x_pkey.c'],
      ['crypto', 'asn1', 'x_sig.c'],
      ['crypto', 'asn1', 'x_spki.c'],
      ['crypto', 'asn1', 'x_val.c'],
      ['crypto', 'async', 'arch', 'async_null.c'],
      ['crypto', 'async', 'arch', 'async_posix.c'],
      ['crypto', 'async', 'arch', 'async_win.c'],
      ['crypto', 'async', 'async.c'],
      ['crypto', 'async', 'async_err.c'],
      ['crypto', 'async', 'async_wait.c'],
      ['crypto', 'bf', 'bf_cfb64.c'],
      ['crypto', 'bf', 'bf_ecb.c'],
      ['crypto', 'bf', 'bf_enc.c'],
      ['crypto', 'bf', 'bf_ofb64.c'],
      ['crypto', 'bf', 'bf_skey.c'],
      ['crypto', 'bio', 'b_addr.c'],
      ['crypto', 'bio', 'b_dump.c'],
      ['crypto', 'bio', 'b_print.c'],
      ['crypto', 'bio', 'b_sock.c'],
      ['crypto', 'bio', 'b_sock2.c'],
      ['crypto', 'bio', 'bf_buff.c'],
      ['crypto', 'bio', 'bf_lbuf.c'],
      ['crypto', 'bio', 'bf_nbio.c'],
      ['crypto', 'bio', 'bf_null.c'],
      ['crypto', 'bio', 'bio_cb.c'],
      ['crypto', 'bio', 'bio_err.c'],
      ['crypto', 'bio', 'bio_lib.c'],
      ['crypto', 'bio', 'bio_meth.c'],
      ['crypto', 'bio', 'bss_acpt.c'],
      ['crypto', 'bio', 'bss_bio.c'],
      ['crypto', 'bio', 'bss_conn.c'],
      ['crypto', 'bio', 'bss_dgram.c'],
      ['crypto', 'bio', 'bss_fd.c'],
      ['crypto', 'bio', 'bss_file.c'],
      ['crypto', 'bio', 'bss_log.c'],
      ['crypto', 'bio', 'bss_mem.c'],
      ['crypto', 'bio', 'bss_null.c'],
      ['crypto', 'bio', 'bss_sock.c'],
      ['crypto', 'blake2', 'blake2b.c'],
      ['crypto', 'blake2', 'blake2s.c'],
      ['crypto', 'blake2', 'm_blake2b.c'],
      ['crypto', 'blake2', 'm_blake2s.c'],
      ['crypto', 'bn', 'bn_add.c'],
      ['crypto', 'bn', 'bn_asm.c'],
      ['crypto', 'bn', 'bn_blind.c'],
      ['crypto', 'bn', 'bn_const.c'],
      ['crypto', 'bn', 'bn_ctx.c'],
      ['crypto', 'bn', 'bn_depr.c'],
      ['crypto', 'bn', 'bn_dh.c'],
      ['crypto', 'bn', 'bn_div.c'],
      ['crypto', 'bn', 'bn_err.c'],
      ['crypto', 'bn', 'bn_exp.c'],
      ['crypto', 'bn', 'bn_exp2.c'],
      ['crypto', 'bn', 'bn_gcd.c'],
      ['crypto', 'bn', 'bn_gf2m.c'],
      ['crypto', 'bn', 'bn_intern.c'],
      ['crypto', 'bn', 'bn_kron.c'],
      ['crypto', 'bn', 'bn_lib.c'],
      ['crypto', 'bn', 'bn_mod.c'],
      ['crypto', 'bn', 'bn_mont.c'],
      ['crypto', 'bn', 'bn_mpi.c'],
      ['crypto', 'bn', 'bn_mul.c'],
      ['crypto', 'bn', 'bn_nist.c'],
      ['crypto', 'bn', 'bn_prime.c'],
      ['crypto', 'bn', 'bn_print.c'],
      ['crypto', 'bn', 'bn_rand.c'],
      ['crypto', 'bn', 'bn_recp.c'],
      ['crypto', 'bn', 'bn_shift.c'],
      ['crypto', 'bn', 'bn_sqr.c'],
      ['crypto', 'bn', 'bn_sqrt.c'],
      ['crypto', 'bn', 'bn_srp.c'],
      ['crypto', 'bn', 'bn_word.c'],
      ['crypto', 'bn', 'bn_x931p.c'],
      ['crypto', 'buffer', 'buf_err.c'],
      ['crypto', 'buffer', 'buffer.c'],
      ['crypto', 'camellia', 'camellia.c'],
      ['crypto', 'camellia', 'cmll_cbc.c'],
      ['crypto', 'camellia', 'cmll_cfb.c'],
      ['crypto', 'camellia', 'cmll_ctr.c'],
      ['crypto', 'camellia', 'cmll_ecb.c'],
      ['crypto', 'camellia', 'cmll_misc.c'],
      ['crypto', 'camellia', 'cmll_ofb.c'],
      ['crypto', 'cast', 'c_cfb64.c'],
      ['crypto', 'cast', 'c_ecb.c'],
      ['crypto', 'cast', 'c_enc.c'],
      ['crypto', 'cast', 'c_ofb64.c'],
      ['crypto', 'cast', 'c_skey.c'],
      ['crypto', 'chacha', 'chacha_enc.c'],
      ['crypto', 'cmac', 'cm_ameth.c'],
      ['crypto', 'cmac', 'cm_pmeth.c'],
      ['crypto', 'cmac', 'cmac.c'],
      ['crypto', 'cms', 'cms_asn1.c'],
      ['crypto', 'cms', 'cms_att.c'],
      ['crypto', 'cms', 'cms_cd.c'],
      ['crypto', 'cms', 'cms_dd.c'],
      ['crypto', 'cms', 'cms_enc.c'],
      ['crypto', 'cms', 'cms_env.c'],
      ['crypto', 'cms', 'cms_err.c'],
      ['crypto', 'cms', 'cms_ess.c'],
      ['crypto', 'cms', 'cms_io.c'],
      ['crypto', 'cms', 'cms_kari.c'],
      ['crypto', 'cms', 'cms_lib.c'],
      ['crypto', 'cms', 'cms_pwri.c'],
      ['crypto', 'cms', 'cms_sd.c'],
      ['crypto', 'cms', 'cms_smime.c'],
      ['crypto', 'comp', 'c_zlib.c'],
      ['crypto', 'comp', 'comp_err.c'],
      ['crypto', 'comp', 'comp_lib.c'],
      ['crypto', 'conf', 'conf_api.c'],
      ['crypto', 'conf', 'conf_def.c'],
      ['crypto', 'conf', 'conf_err.c'],
      ['crypto', 'conf', 'conf_lib.c'],
      ['crypto', 'conf', 'conf_mall.c'],
      ['crypto', 'conf', 'conf_mod.c'],
      ['crypto', 'conf', 'conf_sap.c'],
      ['crypto', 'conf', 'conf_ssl.c'],
      ['crypto', 'cpt_err.c'],
      ['crypto', 'cryptlib.c'],
      ['crypto', 'ct', 'ct_b64.c'],
      ['crypto', 'ct', 'ct_err.c'],
      ['crypto', 'ct', 'ct_log.c'],
      ['crypto', 'ct', 'ct_oct.c'],
      ['crypto', 'ct', 'ct_policy.c'],
      ['crypto', 'ct', 'ct_prn.c'],
      ['crypto', 'ct', 'ct_sct.c'],
      ['crypto', 'ct', 'ct_sct_ctx.c'],
      ['crypto', 'ct', 'ct_vfy.c'],
      ['crypto', 'ct', 'ct_x509v3.c'],
      ['crypto', 'ctype.c'],
      ['crypto', 'cversion.c'],
      ['crypto', 'des', 'cbc_cksm.c'],
      ['crypto', 'des', 'cbc_enc.c'],
      ['crypto', 'des', 'cfb64ede.c'],
      ['crypto', 'des', 'cfb64enc.c'],
      ['crypto', 'des', 'cfb_enc.c'],
      ['crypto', 'des', 'des_enc.c'],
      ['crypto', 'des', 'ecb3_enc.c'],
      ['crypto', 'des', 'ecb_enc.c'],
      ['crypto', 'des', 'fcrypt.c'],
      ['crypto', 'des', 'fcrypt_b.c'],
      ['crypto', 'des', 'ofb64ede.c'],
      ['crypto', 'des', 'ofb64enc.c'],
      ['crypto', 'des', 'ofb_enc.c'],
      ['crypto', 'des', 'pcbc_enc.c'],
      ['crypto', 'des', 'qud_cksm.c'],
      ['crypto', 'des', 'rand_key.c'],
      ['crypto', 'des', 'set_key.c'],
      ['crypto', 'des', 'str2key.c'],
      ['crypto', 'des', 'xcbc_enc.c'],
      ['crypto', 'dh', 'dh_ameth.c'],
      ['crypto', 'dh', 'dh_asn1.c'],
      ['crypto', 'dh', 'dh_check.c'],
      ['crypto', 'dh', 'dh_depr.c'],
      ['crypto', 'dh', 'dh_err.c'],
      ['crypto', 'dh', 'dh_gen.c'],
      ['crypto', 'dh', 'dh_kdf.c'],
      ['crypto', 'dh', 'dh_key.c'],
      ['crypto', 'dh', 'dh_lib.c'],
      ['crypto', 'dh', 'dh_meth.c'],
      ['crypto', 'dh', 'dh_pmeth.c'],
      ['crypto', 'dh', 'dh_prn.c'],
      ['crypto', 'dh', 'dh_rfc5114.c'],
      ['crypto', 'dh', 'dh_rfc7919.c'],
      ['crypto', 'dsa', 'dsa_ameth.c'],
      ['crypto', 'dsa', 'dsa_asn1.c'],
      ['crypto', 'dsa', 'dsa_depr.c'],
      ['crypto', 'dsa', 'dsa_err.c'],
      ['crypto', 'dsa', 'dsa_gen.c'],
      ['crypto', 'dsa', 'dsa_key.c'],
      ['crypto', 'dsa', 'dsa_lib.c'],
      ['crypto', 'dsa', 'dsa_meth.c'],
      ['crypto', 'dsa', 'dsa_ossl.c'],
      ['crypto', 'dsa', 'dsa_pmeth.c'],
      ['crypto', 'dsa', 'dsa_prn.c'],
      ['crypto', 'dsa', 'dsa_sign.c'],
      ['crypto', 'dsa', 'dsa_vrf.c'],
      ['crypto', 'dso', 'dso_dl.c'],
      ['crypto', 'dso', 'dso_dlfcn.c'],
      ['crypto', 'dso', 'dso_err.c'],
      ['crypto', 'dso', 'dso_lib.c'],
      ['crypto', 'dso', 'dso_openssl.c'],
      ['crypto', 'dso', 'dso_vms.c'],
      ['crypto', 'dso', 'dso_win32.c'],
      ['crypto', 'ebcdic.c'],
      ['crypto', 'ec', 'curve25519.c'],
      ['crypto', 'ec', 'curve448', 'arch_32', 'f_impl.c'],
      ['crypto', 'ec', 'curve448', 'curve448.c'],
      ['crypto', 'ec', 'curve448', 'curve448_tables.c'],
      ['crypto', 'ec', 'curve448', 'eddsa.c'],
      ['crypto', 'ec', 'curve448', 'f_generic.c'],
      ['crypto', 'ec', 'curve448', 'scalar.c'],
      ['crypto', 'ec', 'ec2_oct.c'],
      ['crypto', 'ec', 'ec2_smpl.c'],
      ['crypto', 'ec', 'ec_ameth.c'],
      ['crypto', 'ec', 'ec_asn1.c'],
      ['crypto', 'ec', 'ec_check.c'],
      ['crypto', 'ec', 'ec_curve.c'],
      ['crypto', 'ec', 'ec_cvt.c'],
      ['crypto', 'ec', 'ec_err.c'],
      ['crypto', 'ec', 'ec_key.c'],
      ['crypto', 'ec', 'ec_kmeth.c'],
      ['crypto', 'ec', 'ec_lib.c'],
      ['crypto', 'ec', 'ec_mult.c'],
      ['crypto', 'ec', 'ec_oct.c'],
      ['crypto', 'ec', 'ec_pmeth.c'],
      ['crypto', 'ec', 'ec_print.c'],
      ['crypto', 'ec', 'ecdh_kdf.c'],
      ['crypto', 'ec', 'ecdh_ossl.c'],
      ['crypto', 'ec', 'ecdsa_ossl.c'],
      ['crypto', 'ec', 'ecdsa_sign.c'],
      ['crypto', 'ec', 'ecdsa_vrf.c'],
      ['crypto', 'ec', 'eck_prn.c'],
      ['crypto', 'ec', 'ecp_mont.c'],
      ['crypto', 'ec', 'ecp_nist.c'],
      ['crypto', 'ec', 'ecp_nistp224.c'],
      ['crypto', 'ec', 'ecp_nistp256.c'],
      ['crypto', 'ec', 'ecp_nistp521.c'],
      ['crypto', 'ec', 'ecp_nistputil.c'],
      ['crypto', 'ec', 'ecp_oct.c'],
      ['crypto', 'ec', 'ecp_smpl.c'],
      ['crypto', 'ec', 'ecx_meth.c'],
      ['crypto', 'engine', 'eng_all.c'],
      ['crypto', 'engine', 'eng_cnf.c'],
      ['crypto', 'engine', 'eng_ctrl.c'],
      ['crypto', 'engine', 'eng_dyn.c'],
      ['crypto', 'engine', 'eng_err.c'],
      ['crypto', 'engine', 'eng_fat.c'],
      ['crypto', 'engine', 'eng_init.c'],
      ['crypto', 'engine', 'eng_lib.c'],
      ['crypto', 'engine', 'eng_list.c'],
      ['crypto', 'engine', 'eng_openssl.c'],
      ['crypto', 'engine', 'eng_pkey.c'],
      ['crypto', 'engine', 'eng_rdrand.c'],
      ['crypto', 'engine', 'eng_table.c'],
      ['crypto', 'engine', 'tb_asnmth.c'],
      ['crypto', 'engine', 'tb_cipher.c'],
      ['crypto', 'engine', 'tb_dh.c'],
      ['crypto', 'engine', 'tb_digest.c'],
      ['crypto', 'engine', 'tb_dsa.c'],
      ['crypto', 'engine', 'tb_eckey.c'],
      ['crypto', 'engine', 'tb_pkmeth.c'],
      ['crypto', 'engine', 'tb_rand.c'],
      ['crypto', 'engine', 'tb_rsa.c'],
      ['crypto', 'err', 'err.c'],
      ['crypto', 'err', 'err_all.c'],
      ['crypto', 'err', 'err_prn.c'],
      ['crypto', 'evp', 'bio_b64.c'],
      ['crypto', 'evp', 'bio_enc.c'],
      ['crypto', 'evp', 'bio_md.c'],
      ['crypto', 'evp', 'bio_ok.c'],
      ['crypto', 'evp', 'c_allc.c'],
      ['crypto', 'evp', 'c_alld.c'],
      ['crypto', 'evp', 'cmeth_lib.c'],
      ['crypto', 'evp', 'digest.c'],
      ['crypto', 'evp', 'e_aes.c'],
      ['crypto', 'evp', 'e_aes_cbc_hmac_sha1.c'],
      ['crypto', 'evp', 'e_aes_cbc_hmac_sha256.c'],
      ['crypto', 'evp', 'e_aria.c'],
      ['crypto', 'evp', 'e_bf.c'],
      ['crypto', 'evp', 'e_camellia.c'],
      ['crypto', 'evp', 'e_cast.c'],
      ['crypto', 'evp', 'e_chacha20_poly1305.c'],
      ['crypto', 'evp', 'e_des.c'],
      ['crypto', 'evp', 'e_des3.c'],
      ['crypto', 'evp', 'e_idea.c'],
      ['crypto', 'evp', 'e_null.c'],
      ['crypto', 'evp', 'e_old.c'],
      ['crypto', 'evp', 'e_rc2.c'],
      ['crypto', 'evp', 'e_rc4.c'],
      ['crypto', 'evp', 'e_rc4_hmac_md5.c'],
      ['crypto', 'evp', 'e_rc5.c'],
      ['crypto', 'evp', 'e_seed.c'],
      ['crypto', 'evp', 'e_sm4.c'],
      ['crypto', 'evp', 'e_xcbc_d.c'],
      ['crypto', 'evp', 'encode.c'],
      ['crypto', 'evp', 'evp_cnf.c'],
      ['crypto', 'evp', 'evp_enc.c'],
      ['crypto', 'evp', 'evp_err.c'],
      ['crypto', 'evp', 'evp_key.c'],
      ['crypto', 'evp', 'evp_lib.c'],
      ['crypto', 'evp', 'evp_pbe.c'],
      ['crypto', 'evp', 'evp_pkey.c'],
      ['crypto', 'evp', 'm_md2.c'],
      ['crypto', 'evp', 'm_md4.c'],
      ['crypto', 'evp', 'm_md5.c'],
      ['crypto', 'evp', 'm_md5_sha1.c'],
      ['crypto', 'evp', 'm_mdc2.c'],
      ['crypto', 'evp', 'm_null.c'],
      ['crypto', 'evp', 'm_ripemd.c'],
      ['crypto', 'evp', 'm_sha1.c'],
      ['crypto', 'evp', 'm_sha3.c'],
      ['crypto', 'evp', 'm_sigver.c'],
      ['crypto', 'evp', 'm_wp.c'],
      ['crypto', 'evp', 'names.c'],
      ['crypto', 'evp', 'p5_crpt.c'],
      ['crypto', 'evp', 'p5_crpt2.c'],
      ['crypto', 'evp', 'p_dec.c'],
      ['crypto', 'evp', 'p_enc.c'],
      ['crypto', 'evp', 'p_lib.c'],
      ['crypto', 'evp', 'p_open.c'],
      ['crypto', 'evp', 'p_seal.c'],
      ['crypto', 'evp', 'p_sign.c'],
      ['crypto', 'evp', 'p_verify.c'],
      ['crypto', 'evp', 'pbe_scrypt.c'],
      ['crypto', 'evp', 'pmeth_fn.c'],
      ['crypto', 'evp', 'pmeth_gn.c'],
      ['crypto', 'evp', 'pmeth_lib.c'],
      ['crypto', 'ex_data.c'],
      ['crypto', 'getenv.c'],
      ['crypto', 'hmac', 'hm_ameth.c'],
      ['crypto', 'hmac', 'hm_pmeth.c'],
      ['crypto', 'hmac', 'hmac.c'],
      ['crypto', 'idea', 'i_cbc.c'],
      ['crypto', 'idea', 'i_cfb64.c'],
      ['crypto', 'idea', 'i_ecb.c'],
      ['crypto', 'idea', 'i_ofb64.c'],
      ['crypto', 'idea', 'i_skey.c'],
      ['crypto', 'init.c'],
      ['crypto', 'kdf', 'hkdf.c'],
      ['crypto', 'kdf', 'kdf_err.c'],
      ['crypto', 'kdf', 'scrypt.c'],
      ['crypto', 'kdf', 'tls1_prf.c'],
      ['crypto', 'lhash', 'lh_stats.c'],
      ['crypto', 'lhash', 'lhash.c'],
      ['crypto', 'md4', 'md4_dgst.c'],
      ['crypto', 'md4', 'md4_one.c'],
      ['crypto', 'md5', 'md5_dgst.c'],
      ['crypto', 'md5', 'md5_one.c'],
      ['crypto', 'mdc2', 'mdc2_one.c'],
      ['crypto', 'mdc2', 'mdc2dgst.c'],
      ['crypto', 'mem.c'],
      ['crypto', 'mem_clr.c'],
      ['crypto', 'mem_dbg.c'],
      ['crypto', 'mem_sec.c'],
      ['crypto', 'modes', 'cbc128.c'],
      ['crypto', 'modes', 'ccm128.c'],
      ['crypto', 'modes', 'cfb128.c'],
      ['crypto', 'modes', 'ctr128.c'],
      ['crypto', 'modes', 'cts128.c'],
      ['crypto', 'modes', 'gcm128.c'],
      ['crypto', 'modes', 'ocb128.c'],
      ['crypto', 'modes', 'ofb128.c'],
      ['crypto', 'modes', 'wrap128.c'],
      ['crypto', 'modes', 'xts128.c'],
      ['crypto', 'o_dir.c'],
      ['crypto', 'o_fips.c'],
      ['crypto', 'o_fopen.c'],
      ['crypto', 'o_init.c'],
      ['crypto', 'o_str.c'],
      ['crypto', 'o_time.c'],
      ['crypto', 'objects', 'o_names.c'],
      ['crypto', 'objects', 'obj_dat.c'],
      ['crypto', 'objects', 'obj_err.c'],
      ['crypto', 'objects', 'obj_lib.c'],
      ['crypto', 'objects', 'obj_xref.c'],
      ['crypto', 'ocsp', 'ocsp_asn.c'],
      ['crypto', 'ocsp', 'ocsp_cl.c'],
      ['crypto', 'ocsp', 'ocsp_err.c'],
      ['crypto', 'ocsp', 'ocsp_ext.c'],
      ['crypto', 'ocsp', 'ocsp_ht.c'],
      ['crypto', 'ocsp', 'ocsp_lib.c'],
      ['crypto', 'ocsp', 'ocsp_prn.c'],
      ['crypto', 'ocsp', 'ocsp_srv.c'],
      ['crypto', 'ocsp', 'ocsp_vfy.c'],
      ['crypto', 'ocsp', 'v3_ocsp.c'],
      ['crypto', 'pem', 'pem_all.c'],
      ['crypto', 'pem', 'pem_err.c'],
      ['crypto', 'pem', 'pem_info.c'],
      ['crypto', 'pem', 'pem_lib.c'],
      ['crypto', 'pem', 'pem_oth.c'],
      ['crypto', 'pem', 'pem_pk8.c'],
      ['crypto', 'pem', 'pem_pkey.c'],
      ['crypto', 'pem', 'pem_sign.c'],
      ['crypto', 'pem', 'pem_x509.c'],
      ['crypto', 'pem', 'pem_xaux.c'],
      ['crypto', 'pem', 'pvkfmt.c'],
      ['crypto', 'pkcs12', 'p12_add.c'],
      ['crypto', 'pkcs12', 'p12_asn.c'],
      ['crypto', 'pkcs12', 'p12_attr.c'],
      ['crypto', 'pkcs12', 'p12_crpt.c'],
      ['crypto', 'pkcs12', 'p12_crt.c'],
      ['crypto', 'pkcs12', 'p12_decr.c'],
      ['crypto', 'pkcs12', 'p12_init.c'],
      ['crypto', 'pkcs12', 'p12_key.c'],
      ['crypto', 'pkcs12', 'p12_kiss.c'],
      ['crypto', 'pkcs12', 'p12_mutl.c'],
      ['crypto', 'pkcs12', 'p12_npas.c'],
      ['crypto', 'pkcs12', 'p12_p8d.c'],
      ['crypto', 'pkcs12', 'p12_p8e.c'],
      ['crypto', 'pkcs12', 'p12_sbag.c'],
      ['crypto', 'pkcs12', 'p12_utl.c'],
      ['crypto', 'pkcs12', 'pk12err.c'],
      ['crypto', 'pkcs7', 'bio_pk7.c'],
      ['crypto', 'pkcs7', 'pk7_asn1.c'],
      ['crypto', 'pkcs7', 'pk7_attr.c'],
      ['crypto', 'pkcs7', 'pk7_doit.c'],
      ['crypto', 'pkcs7', 'pk7_lib.c'],
      ['crypto', 'pkcs7', 'pk7_mime.c'],
      ['crypto', 'pkcs7', 'pk7_smime.c'],
      ['crypto', 'pkcs7', 'pkcs7err.c'],
      ['crypto', 'poly1305', 'poly1305.c'],
      ['crypto', 'poly1305', 'poly1305_ameth.c'],
      ['crypto', 'poly1305', 'poly1305_pmeth.c'],
      ['crypto', 'rand', 'drbg_ctr.c'],
      ['crypto', 'rand', 'drbg_lib.c'],
      ['crypto', 'rand', 'rand_egd.c'],
      ['crypto', 'rand', 'rand_err.c'],
      ['crypto', 'rand', 'rand_lib.c'],
      ['crypto', 'rand', 'rand_unix.c'],
      ['crypto', 'rand', 'rand_vms.c'],
      ['crypto', 'rand', 'rand_win.c'],
      ['crypto', 'rand', 'randfile.c'],
      ['crypto', 'rc2', 'rc2_cbc.c'],
      ['crypto', 'rc2', 'rc2_ecb.c'],
      ['crypto', 'rc2', 'rc2_skey.c'],
      ['crypto', 'rc2', 'rc2cfb64.c'],
      ['crypto', 'rc2', 'rc2ofb64.c'],
      ['crypto', 'rc4', 'rc4_enc.c'],
      ['crypto', 'rc4', 'rc4_skey.c'],
      ['crypto', 'ripemd', 'rmd_dgst.c'],
      ['crypto', 'ripemd', 'rmd_one.c'],
      ['crypto', 'rsa', 'rsa_ameth.c'],
      ['crypto', 'rsa', 'rsa_asn1.c'],
      ['crypto', 'rsa', 'rsa_chk.c'],
      ['crypto', 'rsa', 'rsa_crpt.c'],
      ['crypto', 'rsa', 'rsa_depr.c'],
      ['crypto', 'rsa', 'rsa_err.c'],
      ['crypto', 'rsa', 'rsa_gen.c'],
      ['crypto', 'rsa', 'rsa_lib.c'],
      ['crypto', 'rsa', 'rsa_meth.c'],
      ['crypto', 'rsa', 'rsa_mp.c'],
      ['crypto', 'rsa', 'rsa_none.c'],
      ['crypto', 'rsa', 'rsa_oaep.c'],
      ['crypto', 'rsa', 'rsa_ossl.c'],
      ['crypto', 'rsa', 'rsa_pk1.c'],
      ['crypto', 'rsa', 'rsa_pmeth.c'],
      ['crypto', 'rsa', 'rsa_prn.c'],
      ['crypto', 'rsa', 'rsa_pss.c'],
      ['crypto', 'rsa', 'rsa_saos.c'],
      ['crypto', 'rsa', 'rsa_sign.c'],
      ['crypto', 'rsa', 'rsa_ssl.c'],
      ['crypto', 'rsa', 'rsa_x931.c'],
      ['crypto', 'rsa', 'rsa_x931g.c'],
      ['crypto', 'seed', 'seed.c'],
      ['crypto', 'seed', 'seed_cbc.c'],
      ['crypto', 'seed', 'seed_cfb.c'],
      ['crypto', 'seed', 'seed_ecb.c'],
      ['crypto', 'seed', 'seed_ofb.c'],
      ['crypto', 'sha', 'keccak1600.c'],
      ['crypto', 'sha', 'sha1_one.c'],
      ['crypto', 'sha', 'sha1dgst.c'],
      ['crypto', 'sha', 'sha256.c'],
      ['crypto', 'sha', 'sha512.c'],
      ['crypto', 'siphash', 'siphash.c'],
      ['crypto', 'siphash', 'siphash_ameth.c'],
      ['crypto', 'siphash', 'siphash_pmeth.c'],
      ['crypto', 'sm2', 'sm2_crypt.c'],
      ['crypto', 'sm2', 'sm2_err.c'],
      ['crypto', 'sm2', 'sm2_pmeth.c'],
      ['crypto', 'sm2', 'sm2_sign.c'],
      ['crypto', 'sm3', 'm_sm3.c'],
      ['crypto', 'sm3', 'sm3.c'],
      ['crypto', 'sm4', 'sm4.c'],
      ['crypto', 'srp', 'srp_lib.c'],
      ['crypto', 'srp', 'srp_vfy.c'],
      ['crypto', 'stack', 'stack.c'],
      ['crypto', 'store', 'loader_file.c'],
      ['crypto', 'store', 'store_err.c'],
      ['crypto', 'store', 'store_init.c'],
      ['crypto', 'store', 'store_lib.c'],
      ['crypto', 'store', 'store_register.c'],
      ['crypto', 'store', 'store_strings.c'],
      ['crypto', 'threads_none.c'],
      ['crypto', 'threads_pthread.c'],
      ['crypto', 'threads_win.c'],
      ['crypto', 'ts', 'ts_asn1.c'],
      ['crypto', 'ts', 'ts_conf.c'],
      ['crypto', 'ts', 'ts_err.c'],
      ['crypto', 'ts', 'ts_lib.c'],
      ['crypto', 'ts', 'ts_req_print.c'],
      ['crypto', 'ts', 'ts_req_utils.c'],
      ['crypto', 'ts', 'ts_rsp_print.c'],
      ['crypto', 'ts', 'ts_rsp_sign.c'],
      ['crypto', 'ts', 'ts_rsp_utils.c'],
      ['crypto', 'ts', 'ts_rsp_verify.c'],
      ['crypto', 'ts', 'ts_verify_ctx.c'],
      ['crypto', 'txt_db', 'txt_db.c'],
      ['crypto', 'ui', 'ui_err.c'],
      ['crypto', 'ui', 'ui_lib.c'],
      ['crypto', 'ui', 'ui_null.c'],
      ['crypto', 'ui', 'ui_openssl.c'],
      ['crypto', 'ui', 'ui_util.c'],
      ['crypto', 'uid.c'],
      ['crypto', 'whrlpool', 'wp_block.c'],
      ['crypto', 'whrlpool', 'wp_dgst.c'],
      ['crypto', 'x509', 'by_dir.c'],
      ['crypto', 'x509', 'by_file.c'],
      ['crypto', 'x509', 't_crl.c'],
      ['crypto', 'x509', 't_req.c'],
      ['crypto', 'x509', 't_x509.c'],
      ['crypto', 'x509', 'x509_att.c'],
      ['crypto', 'x509', 'x509_cmp.c'],
      ['crypto', 'x509', 'x509_d2.c'],
      ['crypto', 'x509', 'x509_def.c'],
      ['crypto', 'x509', 'x509_err.c'],
      ['crypto', 'x509', 'x509_ext.c'],
      ['crypto', 'x509', 'x509_lu.c'],
      ['crypto', 'x509', 'x509_meth.c'],
      ['crypto', 'x509', 'x509_obj.c'],
      ['crypto', 'x509', 'x509_r2x.c'],
      ['crypto', 'x509', 'x509_req.c'],
      ['crypto', 'x509', 'x509_set.c'],
      ['crypto', 'x509', 'x509_trs.c'],
      ['crypto', 'x509', 'x509_txt.c'],
      ['crypto', 'x509', 'x509_v3.c'],
      ['crypto', 'x509', 'x509_vfy.c'],
      ['crypto', 'x509', 'x509_vpm.c'],
      ['crypto', 'x509', 'x509cset.c'],
      ['crypto', 'x509', 'x509name.c'],
      ['crypto', 'x509', 'x509rset.c'],
      ['crypto', 'x509', 'x509spki.c'],
      ['crypto', 'x509', 'x509type.c'],
      ['crypto', 'x509', 'x_all.c'],
      ['crypto', 'x509', 'x_attrib.c'],
      ['crypto', 'x509', 'x_crl.c'],
      ['crypto', 'x509', 'x_exten.c'],
      ['crypto', 'x509', 'x_name.c'],
      ['crypto', 'x509', 'x_pubkey.c'],
      ['crypto', 'x509', 'x_req.c'],
      ['crypto', 'x509', 'x_x509.c'],
      ['crypto', 'x509', 'x_x509a.c'],
      ['crypto', 'x509v3', 'pcy_cache.c'],
      ['crypto', 'x509v3', 'pcy_data.c'],
      ['crypto', 'x509v3', 'pcy_lib.c'],
      ['crypto', 'x509v3', 'pcy_map.c'],
      ['crypto', 'x509v3', 'pcy_node.c'],
      ['crypto', 'x509v3', 'pcy_tree.c'],
      ['crypto', 'x509v3', 'v3_addr.c'],
      ['crypto', 'x509v3', 'v3_admis.c'],
      ['crypto', 'x509v3', 'v3_akey.c'],
      ['crypto', 'x509v3', 'v3_akeya.c'],
      ['crypto', 'x509v3', 'v3_alt.c'],
      ['crypto', 'x509v3', 'v3_asid.c'],
      ['crypto', 'x509v3', 'v3_bcons.c'],
      ['crypto', 'x509v3', 'v3_bitst.c'],
      ['crypto', 'x509v3', 'v3_conf.c'],
      ['crypto', 'x509v3', 'v3_cpols.c'],
      ['crypto', 'x509v3', 'v3_crld.c'],
      ['crypto', 'x509v3', 'v3_enum.c'],
      ['crypto', 'x509v3', 'v3_extku.c'],
      ['crypto', 'x509v3', 'v3_genn.c'],
      ['crypto', 'x509v3', 'v3_ia5.c'],
      ['crypto', 'x509v3', 'v3_info.c'],
      ['crypto', 'x509v3', 'v3_int.c'],
      ['crypto', 'x509v3', 'v3_lib.c'],
      ['crypto', 'x509v3', 'v3_ncons.c'],
      ['crypto', 'x509v3', 'v3_pci.c'],
      ['crypto', 'x509v3', 'v3_pcia.c'],
      ['crypto', 'x509v3', 'v3_pcons.c'],
      ['crypto', 'x509v3', 'v3_pku.c'],
      ['crypto', 'x509v3', 'v3_pmaps.c'],
      ['crypto', 'x509v3', 'v3_prn.c'],
      ['crypto', 'x509v3', 'v3_purp.c'],
      ['crypto', 'x509v3', 'v3_skey.c'],
      ['crypto', 'x509v3', 'v3_sxnet.c'],
      ['crypto', 'x509v3', 'v3_tlsf.c'],
      ['crypto', 'x509v3', 'v3_utl.c'],
      ['crypto', 'x509v3', 'v3err.c'],
      ['engines', 'e_capi.c'],
    ]

    generated_headers = [
      (['crypto', 'include', 'internal', 'bn_conf.h'], bn_conf_h),
      (['crypto', 'include', 'internal', 'dso_conf.h'], dso_conf_h),
      (['include', 'openssl', 'opensslconf.h'], opensslconf_h),
      (['crypto', 'buildinf.h'], buildinf_h),
    ]

    source_path = os.path.join(ports.get_dir(), 'crypto', 'openssl-' + TAG)
    dest_path = os.path.join(ports.get_build_dir(), 'crypto')

    for header in generated_headers:
        open(os.path.join(source_path, *header[0]), 'w').write(header[1])

    source_include_path = os.path.join(source_path, 'include', 'openssl')
    ports.install_headers(source_include_path, target='openssl')

    commands = []
    o_s = []
    for src_path in srcs:
      src = os.path.join(*src_path)
      src_base, c_ext = os.path.splitext(src)
      o_file = os.path.join(ports.get_build_dir(), 'crypto', src_base + '.o')
      shared.safe_ensure_dirs(os.path.dirname(o_file))
      command = [shared.PYTHON, shared.EMCC,
                 '-c', os.path.join(source_path, src),
                 '-o', o_file,
                 '-I' + ports.get_include_dir(),
                 '-I' + os.path.join(source_path),
                 '-I' + os.path.join(source_path, 'include'),
                 '-I' + os.path.join(source_path, 'crypto', 'include'),
                 '-I' + os.path.join(source_path, 'crypto', 'modes'),
                 '-I' + os.path.join(source_path, 'crypto', 'ec', 'curve448', 'arch_32'),
                 '-I' + os.path.join(source_path, 'crypto', 'ec', 'curve448'),
                 '-DOPENSSLDIR="./"',
                 '-DENGINESDIR="./engines-1.1/"',
                 '-O2', '-w']
      if settings.USE_PTHREADS:
        command += ['-s', 'USE_PTHREADS']
      commands.append(command)
      o_s.append(o_file)
    ports.run_commands(commands)

    final = os.path.join(ports.get_build_dir(), 'crypto', libname)
    shared.safe_ensure_dirs(os.path.dirname(final))
    ports.create_lib(final, o_s)
    return final

  return [shared.Cache.get(libname, create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file(ports.get_lib_name('libcrypto'))


def process_args(ports, args, settings, shared):
  if settings.USE_CRYPTO == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_build_dir(), 'openssl', 'include', 'openssl')]
  return args


def show():
  return 'libcrypto from OpensSL (USE_CRYPTO=1; Dual OpenSSL and SSLeay license )'


bn_conf_h = '''/* WARNING: do not edit! */
/* Generated by Makefile from crypto/include/internal/bn_conf.h.in */
/*
 * Copyright 2016 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the OpenSSL license (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#ifndef HEADER_BN_CONF_H
# define HEADER_BN_CONF_H

/*
 * The contents of this file are not used in the UEFI build, as
 * both 32-bit and 64-bit builds are supported from a single run
 * of the Configure script.
 */

/* Should we define BN_DIV2W here? */

/* Only one for the following should be defined */
#undef SIXTY_FOUR_BIT_LONG
#undef SIXTY_FOUR_BIT
#define THIRTY_TWO_BIT

#endif
'''

dso_conf_h = '''/* WARNING: do not edit! */
/* Generated by Makefile from crypto/include/internal/dso_conf.h.in */
/*
 * Copyright 2016-2019 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the OpenSSL license (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#ifndef HEADER_DSO_CONF_H
# define HEADER_DSO_CONF_H
# define DSO_NONE
# define DSO_EXTENSION ""
#endif
'''

opensslconf_h = '''/*
 * WARNING: do not edit!
 * Generated by Makefile from include/openssl/opensslconf.h.in
 *
 * Copyright 2016-2018 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the OpenSSL license (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#include <openssl/opensslv.h>

#ifdef  __cplusplus
extern "C" {
#endif

#ifdef OPENSSL_ALGORITHM_DEFINES
# error OPENSSL_ALGORITHM_DEFINES no longer supported
#endif

/*
 * OpenSSL was configured with the following options:
 */

#ifndef OPENSSL_SYS_emscripten
# define OPENSSL_SYS_emscripten 1
#endif
#ifndef OPENSSL_NO_MD2
# define OPENSSL_NO_MD2
#endif
#ifndef OPENSSL_NO_RC5
# define OPENSSL_NO_RC5
#endif
#ifndef OPENSSL_THREADS
# define OPENSSL_THREADS
#endif
#ifndef OPENSSL_RAND_SEED_OS
# define OPENSSL_RAND_SEED_OS
#endif
#ifndef OPENSSL_NO_ASAN
# define OPENSSL_NO_ASAN
#endif
#ifndef OPENSSL_NO_ASM
# define OPENSSL_NO_ASM
#endif
#ifndef OPENSSL_NO_CRYPTO_MDEBUG
# define OPENSSL_NO_CRYPTO_MDEBUG
#endif
#ifndef OPENSSL_NO_CRYPTO_MDEBUG_BACKTRACE
# define OPENSSL_NO_CRYPTO_MDEBUG_BACKTRACE
#endif
#ifndef OPENSSL_NO_DEVCRYPTOENG
# define OPENSSL_NO_DEVCRYPTOENG
#endif
#ifndef OPENSSL_NO_EC_NISTP_64_GCC_128
# define OPENSSL_NO_EC_NISTP_64_GCC_128
#endif
#ifndef OPENSSL_NO_EGD
# define OPENSSL_NO_EGD
#endif
#ifndef OPENSSL_NO_EXTERNAL_TESTS
# define OPENSSL_NO_EXTERNAL_TESTS
#endif
#ifndef OPENSSL_NO_FUZZ_AFL
# define OPENSSL_NO_FUZZ_AFL
#endif
#ifndef OPENSSL_NO_FUZZ_LIBFUZZER
# define OPENSSL_NO_FUZZ_LIBFUZZER
#endif
#ifndef OPENSSL_NO_HEARTBEATS
# define OPENSSL_NO_HEARTBEATS
#endif
#ifndef OPENSSL_NO_HW
# define OPENSSL_NO_HW
#endif
#ifndef OPENSSL_NO_MSAN
# define OPENSSL_NO_MSAN
#endif
#ifndef OPENSSL_NO_SCTP
# define OPENSSL_NO_SCTP
#endif
#ifndef OPENSSL_NO_SSL_TRACE
# define OPENSSL_NO_SSL_TRACE
#endif
#ifndef OPENSSL_NO_SSL3
# define OPENSSL_NO_SSL3
#endif
#ifndef OPENSSL_NO_SSL3_METHOD
# define OPENSSL_NO_SSL3_METHOD
#endif
#ifndef OPENSSL_NO_UBSAN
# define OPENSSL_NO_UBSAN
#endif
#ifndef OPENSSL_NO_UNIT_TEST
# define OPENSSL_NO_UNIT_TEST
#endif
#ifndef OPENSSL_NO_WEAK_SSL_CIPHERS
# define OPENSSL_NO_WEAK_SSL_CIPHERS
#endif
#ifndef OPENSSL_NO_DYNAMIC_ENGINE
# define OPENSSL_NO_DYNAMIC_ENGINE
#endif
#ifndef OPENSSL_NO_AFALGENG
# define OPENSSL_NO_AFALGENG
#endif


/*
 * Sometimes OPENSSSL_NO_xxx ends up with an empty file and some compilers
 * don't like that.  This will hopefully silence them.
 */
#define NON_EMPTY_TRANSLATION_UNIT static void *dummy = &dummy;

/*
 * Applications should use -DOPENSSL_API_COMPAT=<version> to suppress the
 * declarations of functions deprecated in or before <version>. Otherwise, they
 * still won't see them if the library has been built to disable deprecated
 * functions.
 */
#ifndef DECLARE_DEPRECATED
# define DECLARE_DEPRECATED(f)   f;
# ifdef __GNUC__
#  if __GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ > 0)
#   undef DECLARE_DEPRECATED
#   define DECLARE_DEPRECATED(f)    f __attribute__ ((deprecated));
#  endif
# endif
#endif

#ifndef OPENSSL_FILE
# ifdef OPENSSL_NO_FILENAMES
#  define OPENSSL_FILE ""
#  define OPENSSL_LINE 0
# else
#  define OPENSSL_FILE __FILE__
#  define OPENSSL_LINE __LINE__
# endif
#endif

#ifndef OPENSSL_MIN_API
# define OPENSSL_MIN_API 0
#endif

#if !defined(OPENSSL_API_COMPAT) || OPENSSL_API_COMPAT < OPENSSL_MIN_API
# undef OPENSSL_API_COMPAT
# define OPENSSL_API_COMPAT OPENSSL_MIN_API
#endif

/*
 * Do not deprecate things to be deprecated in version 1.2.0 before the
 * OpenSSL version number matches.
 */
#if OPENSSL_VERSION_NUMBER < 0x10200000L
# define DEPRECATEDIN_1_2_0(f)   f;
#elif OPENSSL_API_COMPAT < 0x10200000L
# define DEPRECATEDIN_1_2_0(f)   DECLARE_DEPRECATED(f)
#else
# define DEPRECATEDIN_1_2_0(f)
#endif

#if OPENSSL_API_COMPAT < 0x10100000L
# define DEPRECATEDIN_1_1_0(f)   DECLARE_DEPRECATED(f)
#else
# define DEPRECATEDIN_1_1_0(f)
#endif

#if OPENSSL_API_COMPAT < 0x10000000L
# define DEPRECATEDIN_1_0_0(f)   DECLARE_DEPRECATED(f)
#else
# define DEPRECATEDIN_1_0_0(f)
#endif

#if OPENSSL_API_COMPAT < 0x00908000L
# define DEPRECATEDIN_0_9_8(f)   DECLARE_DEPRECATED(f)
#else
# define DEPRECATEDIN_0_9_8(f)
#endif

/* Generate 80386 code? */
#undef I386_ONLY

#undef OPENSSL_UNISTD
#define OPENSSL_UNISTD <unistd.h>

#undef OPENSSL_EXPORT_VAR_AS_FUNCTION

/*
 * The following are cipher-specific, but are part of the public API.
 */
#if !defined(OPENSSL_SYS_UEFI)
# define BN_LLONG
/* Only one for the following should be defined */
# undef SIXTY_FOUR_BIT_LONG
# undef SIXTY_FOUR_BIT
# define THIRTY_TWO_BIT
#endif

#define RC4_INT unsigned int

#ifdef  __cplusplus
}
#endif
'''

buildinf_h = '''/*
 * WARNING: do not edit!
 * Generated by util/mkbuildinf.pl
 *
 * Copyright 2014-2017 The OpenSSL Project Authors. All Rights Reserved.
 *
 * Licensed under the OpenSSL license (the "License").  You may not use
 * this file except in compliance with the License.  You can obtain a copy
 * in the file LICENSE in the source distribution or at
 * https://www.openssl.org/source/license.html
 */

#define PLATFORM "platform: wasm-le32emscripten"
#define DATE "built on: Wed Mar  4 13:53:56 2020 UTC"

/*
 * Generate compiler_flags as an array of individual characters. This is a
 * workaround for the situation where CFLAGS gets too long for a C90 string
 * literal
 */
static const char compiler_flags[] = {
    'c','o','m','p','i','l','e','r',':',' ','e','m','c','c',' ',' ',
    ' ','-','O','2',' ','-','D','T','E','R','M','I','O','S',' ','-',
    'D','L','_','E','N','D','I','A','N',' ','-','D','N','D','E','B',
    'U','G',' ','-','D','_','G','N','U','_','S','O','U','R','C','E',
    '\0'
};
'''
