# Copyright 2020 Samsung Electronics Inc.  All rights reserved.
# Emscripten is available under two separate licenses, the MIT license and the
# University of Illinois/NCSA Open Source License.  Both these licenses can be
# found in the LICENSE file.

import os
import logging
import shutil

TAG = '4.3.1'
HASH = '831a187d8b8f2715a9f11c93c8d3ec126ff579d470797da452d3395178877de113af7ae90ed27fca0b223791ad257972570481e6dbb8361d2b7f3b010924bee8'


def get_libname(ports, use_pthreads):
  return ports.get_lib_name('libffmpeg' + ('-mt' if use_pthreads else ''))


def get(ports, settings, shared):
  if settings.USE_FFMPEG != 1:
    return []

  ports.fetch_project(
      'ffmpeg',
      'https://ffmpeg.org/releases/ffmpeg-' + TAG + '.tar.bz2',
      'ffmpeg-' + TAG,
      is_tarbz2=True,
      sha512hash=HASH)

  # Share the same name in this function and create() functor,
  # which may be called later.
  libname = get_libname(ports, settings.USE_PTHREADS)

  def create():
    logging.info('building port: FFMPEG PTHREADS = ' + str(settings.USE_PTHREADS))
    #ports.clear_project_build('ffmpeg') #Emscripten rebuild everything from scratch every time...
    srcs = [
      ['libavcodec', '012v.c'],
      ['libavcodec', '4xm.c'],
      ['libavcodec', '8bps.c'],
      ['libavcodec', '8svx.c'],
      ['libavcodec', 'a64multienc.c'],
      ['libavcodec', 'aac_ac3_parser.c'],
      ['libavcodec', 'aac_adtstoasc_bsf.c'],
      ['libavcodec', 'aaccoder.c'],
      ['libavcodec', 'aacdec_fixed.c'],
      ['libavcodec', 'aacdec.c'],
      ['libavcodec', 'aacenc_is.c'],
      ['libavcodec', 'aacenc_ltp.c'],
      ['libavcodec', 'aacenc.c'],
      ['libavcodec', 'aacenc_pred.c'],
      ['libavcodec', 'aacenctab.c'],
      ['libavcodec', 'aacenc_tns.c'],
      ['libavcodec', 'aac_parser.c'],
      ['libavcodec', 'aacpsdsp_fixed.c'],
      ['libavcodec', 'aacpsdsp_float.c'],
      ['libavcodec', 'aacps_fixed.c'],
      ['libavcodec', 'aacps_float.c'],
      ['libavcodec', 'aacpsy.c'],
      ['libavcodec', 'aacsbr_fixed.c'],
      ['libavcodec', 'aacsbr.c'],
      ['libavcodec', 'aactab.c'],
      ['libavcodec', 'aandcttab.c'],
      ['libavcodec', 'aasc.c'],
      ['libavcodec', 'ac3dec_data.c'],
      ['libavcodec', 'ac3dec_fixed.c'],
      ['libavcodec', 'ac3dec_float.c'],
      ['libavcodec', 'ac3dsp.c'],
      ['libavcodec', 'ac3enc_fixed.c'],
      ['libavcodec', 'ac3enc_float.c'],
      ['libavcodec', 'ac3enc.c'],
      ['libavcodec', 'ac3.c'],
      ['libavcodec', 'ac3_parser.c'],
      ['libavcodec', 'ac3tab.c'],
      ['libavcodec', 'acelp_filters.c'],
      ['libavcodec', 'acelp_pitch_delay.c'],
      ['libavcodec', 'acelp_vectors.c'],
      ['libavcodec', 'adpcm_data.c'],
      ['libavcodec', 'adpcmenc.c'],
      ['libavcodec', 'adpcm.c'],
      ['libavcodec', 'adts_header.c'],
      ['libavcodec', 'adts_parser.c'],
      ['libavcodec', 'adxdec.c'],
      ['libavcodec', 'adxenc.c'],
      ['libavcodec', 'adx.c'],
      ['libavcodec', 'adx_parser.c'],
      ['libavcodec', 'agm.c'],
      ['libavcodec', 'aic.c'],
      ['libavcodec', 'alac_data.c'],
      ['libavcodec', 'alacdsp.c'],
      ['libavcodec', 'alacenc.c'],
      ['libavcodec', 'alac.c'],
      ['libavcodec', 'aliaspixdec.c'],
      ['libavcodec', 'aliaspixenc.c'],
      ['libavcodec', 'allcodecs.c'],
      ['libavcodec', 'alsdec.c'],
      ['libavcodec', 'amrnbdec.c'],
      ['libavcodec', 'amrwbdec.c'],
      ['libavcodec', 'anm.c'],
      ['libavcodec', 'ansi.c'],
      ['libavcodec', 'apedec.c'],
      ['libavcodec', 'aptxdec.c'],
      ['libavcodec', 'aptxenc.c'],
      ['libavcodec', 'aptx.c'],
      ['libavcodec', 'arbc.c'],
      ['libavcodec', 'assdec.c'],
      ['libavcodec', 'assenc.c'],
      ['libavcodec', 'ass.c'],
      ['libavcodec', 'ass_split.c'],
      ['libavcodec', 'asvdec.c'],
      ['libavcodec', 'asvenc.c'],
      ['libavcodec', 'asv.c'],
      ['libavcodec', 'atrac1.c'],
      ['libavcodec', 'atrac3.c'],
      ['libavcodec', 'atrac3plusdec.c'],
      ['libavcodec', 'atrac3plusdsp.c'],
      ['libavcodec', 'atrac3plus.c'],
      ['libavcodec', 'atrac9dec.c'],
      ['libavcodec', 'atrac.c'],
      ['libavcodec', 'audiodsp.c'],
      ['libavcodec', 'audio_frame_queue.c'],
      ['libavcodec', 'aura.c'],
      ['libavcodec', 'av1_frame_merge_bsf.c'],
      ['libavcodec', 'av1_frame_split_bsf.c'],
      ['libavcodec', 'av1_metadata_bsf.c'],
      ['libavcodec', 'av1_parse.c'],
      ['libavcodec', 'av1_parser.c'],
      ['libavcodec', 'avdct.c'],
      ['libavcodec', 'avfft.c'],
      ['libavcodec', 'avpacket.c'],
      ['libavcodec', 'avpicture.c'],
      ['libavcodec', 'avrndec.c'],
      ['libavcodec', 'avs2_parser.c'],
      ['libavcodec', 'avs.c'],
      ['libavcodec', 'avuidec.c'],
      ['libavcodec', 'avuienc.c'],
      ['libavcodec', 'bethsoftvideo.c'],
      ['libavcodec', 'bfi.c'],
      ['libavcodec', 'bgmc.c'],
      ['libavcodec', 'binkaudio.c'],
      ['libavcodec', 'binkdsp.c'],
      ['libavcodec', 'bink.c'],
      ['libavcodec', 'bintext.c'],
      ['libavcodec', 'bitpacked.c'],
      ['libavcodec', 'bitstream_filter.c'],
      ['libavcodec', 'bitstream_filters.c'],
      ['libavcodec', 'bitstream.c'],
      ['libavcodec', 'blockdsp.c'],
      ['libavcodec', 'bmpenc.c'],
      ['libavcodec', 'bmp.c'],
      ['libavcodec', 'bmp_parser.c'],
      ['libavcodec', 'bmvaudio.c'],
      ['libavcodec', 'bmvvideo.c'],
      ['libavcodec', 'brenderpix.c'],
      ['libavcodec', 'bsf.c'],
      ['libavcodec', 'bswapdsp.c'],
      ['libavcodec', 'c93.c'],
      ['libavcodec', 'cabac.c'],
      ['libavcodec', 'canopus.c'],
      ['libavcodec', 'cavsdata.c'],
      ['libavcodec', 'cavsdec.c'],
      ['libavcodec', 'cavsdsp.c'],
      ['libavcodec', 'cavs.c'],
      ['libavcodec', 'cavs_parser.c'],
      ['libavcodec', 'cbrt_data_fixed.c'],
      ['libavcodec', 'cbrt_data.c'],
      ['libavcodec', 'cbs_av1.c'],
      ['libavcodec', 'cbs_h2645.c'],
      ['libavcodec', 'cbs_mpeg2.c'],
      ['libavcodec', 'cbs.c'],
      ['libavcodec', 'cbs_vp9.c'],
      ['libavcodec', 'ccaption_dec.c'],
      ['libavcodec', 'cdgraphics.c'],
      ['libavcodec', 'cdtoons.c'],
      ['libavcodec', 'cdxl.c'],
      ['libavcodec', 'celp_filters.c'],
      ['libavcodec', 'celp_math.c'],
      ['libavcodec', 'cfhddata.c'],
      ['libavcodec', 'cfhd.c'],
      ['libavcodec', 'cga_data.c'],
      ['libavcodec', 'chomp_bsf.c'],
      ['libavcodec', 'cinepakenc.c'],
      ['libavcodec', 'cinepak.c'],
      ['libavcodec', 'clearvideo.c'],
      ['libavcodec', 'cljrdec.c'],
      ['libavcodec', 'cljrenc.c'],
      ['libavcodec', 'cllc.c'],
      ['libavcodec', 'cngdec.c'],
      ['libavcodec', 'cngenc.c'],
      ['libavcodec', 'codec2utils.c'],
      ['libavcodec', 'codec_desc.c'],
      ['libavcodec', 'cook.c'],
      ['libavcodec', 'cook_parser.c'],
      ['libavcodec', 'cpia.c'],
      ['libavcodec', 'cscd.c'],
      ['libavcodec', 'cyuv.c'],
      ['libavcodec', 'd3d11va.c'],
      ['libavcodec', 'dcaadpcm.c'],
      ['libavcodec', 'dca_core_bsf.c'],
      ['libavcodec', 'dca_core.c'],
      ['libavcodec', 'dcadata.c'],
      ['libavcodec', 'dcadct.c'],
      ['libavcodec', 'dcadec.c'],
      ['libavcodec', 'dcadsp.c'],
      ['libavcodec', 'dcaenc.c'],
      ['libavcodec', 'dca_exss.c'],
      ['libavcodec', 'dcahuff.c'],
      ['libavcodec', 'dca_lbr.c'],
      ['libavcodec', 'dca.c'],
      ['libavcodec', 'dca_parser.c'],
      ['libavcodec', 'dca_xll.c'],
      ['libavcodec', 'dct32_fixed.c'],
      ['libavcodec', 'dct32_float.c'],
      ['libavcodec', 'dct.c'],
      ['libavcodec', 'dds.c'],
      ['libavcodec', 'decode.c'],
      ['libavcodec', 'dfa.c'],
      ['libavcodec', 'dirac_arith.c'],
      ['libavcodec', 'diracdec.c'],
      ['libavcodec', 'diracdsp.c'],
      ['libavcodec', 'dirac_dwt.c'],
      ['libavcodec', 'dirac.c'],
      ['libavcodec', 'dirac_parser.c'],
      ['libavcodec', 'diractab.c'],
      ['libavcodec', 'dirac_vlc.c'],
      ['libavcodec', 'dnxhddata.c'],
      ['libavcodec', 'dnxhddec.c'],
      ['libavcodec', 'dnxhdenc.c'],
      ['libavcodec', 'dnxhd_parser.c'],
      ['libavcodec', 'dolby_e.c'],
      ['libavcodec', 'dpcm.c'],
      ['libavcodec', 'dpxenc.c'],
      ['libavcodec', 'dpx.c'],
      ['libavcodec', 'dpx_parser.c'],
      ['libavcodec', 'dsddec.c'],
      ['libavcodec', 'dsd.c'],
      ['libavcodec', 'dsicinaudio.c'],
      ['libavcodec', 'dsicinvideo.c'],
      ['libavcodec', 'dss_sp.c'],
      ['libavcodec', 'dstdec.c'],
      ['libavcodec', 'dump_extradata_bsf.c'],
      ['libavcodec', 'dvaudiodec.c'],
      ['libavcodec', 'dvaudio_parser.c'],
      ['libavcodec', 'dvbsubdec.c'],
      ['libavcodec', 'dvbsub.c'],
      ['libavcodec', 'dvbsub_parser.c'],
      ['libavcodec', 'dvdata.c'],
      ['libavcodec', 'dvdec.c'],
      ['libavcodec', 'dvd_nav_parser.c'],
      ['libavcodec', 'dvdsubdec.c'],
      ['libavcodec', 'dvdsubenc.c'],
      ['libavcodec', 'dvdsub.c'],
      ['libavcodec', 'dvdsub_parser.c'],
      ['libavcodec', 'dvenc.c'],
      ['libavcodec', 'dv.c'],
      ['libavcodec', 'dv_profile.c'],
      ['libavcodec', 'dxtory.c'],
      ['libavcodec', 'dxv.c'],
      ['libavcodec', 'eac3_core_bsf.c'],
      ['libavcodec', 'eac3_data.c'],
      ['libavcodec', 'eac3enc.c'],
      ['libavcodec', 'eacmv.c'],
      ['libavcodec', 'eaidct.c'],
      ['libavcodec', 'eamad.c'],
      ['libavcodec', 'eatgq.c'],
      ['libavcodec', 'eatgv.c'],
      ['libavcodec', 'eatqi.c'],
      ['libavcodec', 'elbg.c'],
      ['libavcodec', 'encode.c'],
      ['libavcodec', 'error_resilience.c'],
      ['libavcodec', 'escape124.c'],
      ['libavcodec', 'escape130.c'],
      ['libavcodec', 'evrcdec.c'],
      ['libavcodec', 'exif.c'],
      ['libavcodec', 'extract_extradata_bsf.c'],
      ['libavcodec', 'faandct.c'],
      ['libavcodec', 'faanidct.c'],
      ['libavcodec', 'faxcompr.c'],
      ['libavcodec', 'fdctdsp.c'],
      ['libavcodec', 'fft_fixed_32.c'],
      ['libavcodec', 'fft_fixed.c'],
      ['libavcodec', 'fft_float.c'],
      ['libavcodec', 'fft_init_table.c'],
      ['libavcodec', 'ffv1dec.c'],
      ['libavcodec', 'ffv1enc.c'],
      ['libavcodec', 'ffv1.c'],
      ['libavcodec', 'ffwavesynth.c'],
      ['libavcodec', 'fic.c'],
      ['libavcodec', 'filter_units_bsf.c'],
      ['libavcodec', 'fitsdec.c'],
      ['libavcodec', 'fitsenc.c'],
      ['libavcodec', 'fits.c'],
      ['libavcodec', 'flacdata.c'],
      ['libavcodec', 'flacdec.c'],
      ['libavcodec', 'flacdsp.c'],
      ['libavcodec', 'flacenc.c'],
      ['libavcodec', 'flac.c'],
      ['libavcodec', 'flac_parser.c'],
      ['libavcodec', 'flicvideo.c'],
      ['libavcodec', 'flvdec.c'],
      ['libavcodec', 'flvenc.c'],
      ['libavcodec', 'fmtconvert.c'],
      ['libavcodec', 'fmvc.c'],
      ['libavcodec', 'fraps.c'],
      ['libavcodec', 'frwu.c'],
      ['libavcodec', 'g722dec.c'],
      ['libavcodec', 'g722dsp.c'],
      ['libavcodec', 'g722enc.c'],
      ['libavcodec', 'g722.c'],
      ['libavcodec', 'g723_1dec.c'],
      ['libavcodec', 'g723_1enc.c'],
      ['libavcodec', 'g723_1.c'],
      ['libavcodec', 'g723_1_parser.c'],
      ['libavcodec', 'g726.c'],
      ['libavcodec', 'g729dec.c'],
      ['libavcodec', 'g729_parser.c'],
      ['libavcodec', 'g729postfilter.c'],
      ['libavcodec', 'gdv.c'],
      ['libavcodec', 'gifdec.c'],
      ['libavcodec', 'gif.c'],
      ['libavcodec', 'gif_parser.c'],
      ['libavcodec', 'golomb.c'],
      ['libavcodec', 'gsmdec_data.c'],
      ['libavcodec', 'gsmdec.c'],
      ['libavcodec', 'gsm_parser.c'],
      ['libavcodec', 'h261data.c'],
      ['libavcodec', 'h261dec.c'],
      ['libavcodec', 'h261enc.c'],
      ['libavcodec', 'h261.c'],
      ['libavcodec', 'h261_parser.c'],
      ['libavcodec', 'h263data.c'],
      ['libavcodec', 'h263dec.c'],
      ['libavcodec', 'h263dsp.c'],
      ['libavcodec', 'h263.c'],
      ['libavcodec', 'h263_parser.c'],
      ['libavcodec', 'h2645_parse.c'],
      ['libavcodec', 'h264_cabac.c'],
      ['libavcodec', 'h264_cavlc.c'],
      ['libavcodec', 'h264chroma.c'],
      ['libavcodec', 'h264data.c'],
      ['libavcodec', 'h264dec.c'],
      ['libavcodec', 'h264_direct.c'],
      ['libavcodec', 'h264dsp.c'],
      ['libavcodec', 'h264idct.c'],
      ['libavcodec', 'h264_levels.c'],
      ['libavcodec', 'h264_loopfilter.c'],
      ['libavcodec', 'h264_mb.c'],
      ['libavcodec', 'h264_metadata_bsf.c'],
      ['libavcodec', 'h264_mp4toannexb_bsf.c'],
      ['libavcodec', 'h264_parse.c'],
      ['libavcodec', 'h264_parser.c'],
      ['libavcodec', 'h264_picture.c'],
      ['libavcodec', 'h264pred.c'],
      ['libavcodec', 'h264_ps.c'],
      ['libavcodec', 'h264qpel.c'],
      ['libavcodec', 'h264_redundant_pps_bsf.c'],
      ['libavcodec', 'h264_refs.c'],
      ['libavcodec', 'h264_sei.c'],
      ['libavcodec', 'h264_slice.c'],
      ['libavcodec', 'h265_metadata_bsf.c'],
      ['libavcodec', 'h265_profile_level.c'],
      ['libavcodec', 'hapdec.c'],
      ['libavcodec', 'hap.c'],
      ['libavcodec', 'hapqa_extract_bsf.c'],
      ['libavcodec', 'hcadec.c'],
      ['libavcodec', 'hcom.c'],
      ['libavcodec', 'hevc_cabac.c'],
      ['libavcodec', 'hevc_data.c'],
      ['libavcodec', 'hevcdec.c'],
      ['libavcodec', 'hevcdsp.c'],
      ['libavcodec', 'hevc_filter.c'],
      ['libavcodec', 'hevc_mp4toannexb_bsf.c'],
      ['libavcodec', 'hevc_mvs.c'],
      ['libavcodec', 'hevc_parse.c'],
      ['libavcodec', 'hevc_parser.c'],
      ['libavcodec', 'hevcpred.c'],
      ['libavcodec', 'hevc_ps.c'],
      ['libavcodec', 'hevc_refs.c'],
      ['libavcodec', 'hevc_sei.c'],
      ['libavcodec', 'hnm4video.c'],
      ['libavcodec', 'hpeldsp.c'],
      ['libavcodec', 'hq_hqadata.c'],
      ['libavcodec', 'hq_hqadsp.c'],
      ['libavcodec', 'hq_hqa.c'],
      ['libavcodec', 'hqxdsp.c'],
      ['libavcodec', 'hqx.c'],
      ['libavcodec', 'hqxvlc.c'],
      ['libavcodec', 'htmlsubtitles.c'],
      ['libavcodec', 'huffman.c'],
      ['libavcodec', 'huffyuvdec.c'],
      ['libavcodec', 'huffyuvdsp.c'],
      ['libavcodec', 'huffyuvencdsp.c'],
      ['libavcodec', 'huffyuvenc.c'],
      ['libavcodec', 'huffyuv.c'],
      ['libavcodec', 'idcinvideo.c'],
      ['libavcodec', 'idctdsp.c'],
      ['libavcodec', 'iff.c'],
      ['libavcodec', 'iirfilter.c'],
      ['libavcodec', 'ilbcdec.c'],
      ['libavcodec', 'imc.c'],
      ['libavcodec', 'imgconvert.c'],
      ['libavcodec', 'imm4.c'],
      ['libavcodec', 'imm5.c'],
      ['libavcodec', 'imx_dump_header_bsf.c'],
      ['libavcodec', 'indeo2.c'],
      ['libavcodec', 'indeo3.c'],
      ['libavcodec', 'indeo4.c'],
      ['libavcodec', 'indeo5.c'],
      ['libavcodec', 'intelh263dec.c'],
      ['libavcodec', 'interplayacm.c'],
      ['libavcodec', 'interplayvideo.c'],
      ['libavcodec', 'intrax8dsp.c'],
      ['libavcodec', 'intrax8.c'],
      ['libavcodec', 'ituh263dec.c'],
      ['libavcodec', 'ituh263enc.c'],
      ['libavcodec', 'ivi_dsp.c'],
      ['libavcodec', 'ivi.c'],
      ['libavcodec', 'j2kenc.c'],
      ['libavcodec', 'jacosubdec.c'],
      ['libavcodec', 'jfdctfst.c'],
      ['libavcodec', 'jfdctint.c'],
      ['libavcodec', 'jni.c'],
      ['libavcodec', 'jpeg2000dec.c'],
      ['libavcodec', 'jpeg2000dsp.c'],
      ['libavcodec', 'jpeg2000dwt.c'],
      ['libavcodec', 'jpeg2000.c'],
      ['libavcodec', 'jpeg2000_parser.c'],
      ['libavcodec', 'jpeglsdec.c'],
      ['libavcodec', 'jpeglsenc.c'],
      ['libavcodec', 'jpegls.c'],
      ['libavcodec', 'jpegtables.c'],
      ['libavcodec', 'jrevdct.c'],
      ['libavcodec', 'jvdec.c'],
      ['libavcodec', 'kbdwin.c'],
      ['libavcodec', 'kgv1dec.c'],
      ['libavcodec', 'kmvc.c'],
      ['libavcodec', 'lagarith.c'],
      ['libavcodec', 'lagarithrac.c'],
      ['libavcodec', 'latm_parser.c'],
      ['libavcodec', 'lcldec.c'],
      ['libavcodec', 'ljpegenc.c'],
      ['libavcodec', 'loco.c'],
      ['libavcodec', 'lossless_audiodsp.c'],
      ['libavcodec', 'lossless_videodsp.c'],
      ['libavcodec', 'lossless_videoencdsp.c'],
      ['libavcodec', 'lpc.c'],
      ['libavcodec', 'lsp.c'],
      ['libavcodec', 'lzf.c'],
      ['libavcodec', 'lzwenc.c'],
      ['libavcodec', 'lzw.c'],
      ['libavcodec', 'm101.c'],
      ['libavcodec', 'mace.c'],
      ['libavcodec', 'magicyuvenc.c'],
      ['libavcodec', 'magicyuv.c'],
      ['libavcodec', 'mathtables.c'],
      ['libavcodec', 'mdct15.c'],
      ['libavcodec', 'mdct_fixed_32.c'],
      ['libavcodec', 'mdct_fixed.c'],
      ['libavcodec', 'mdct_float.c'],
      ['libavcodec', 'mdec.c'],
      ['libavcodec', 'me_cmp.c'],
      ['libavcodec', 'mediacodec.c'],
      ['libavcodec', 'metasound_data.c'],
      ['libavcodec', 'metasound.c'],
      ['libavcodec', 'microdvddec.c'],
      ['libavcodec', 'midivid.c'],
      ['libavcodec', 'mimic.c'],
      ['libavcodec', 'mjpeg2jpeg_bsf.c'],
      ['libavcodec', 'mjpega_dump_header_bsf.c'],
      ['libavcodec', 'mjpegbdec.c'],
      ['libavcodec', 'mjpegdec.c'],
      ['libavcodec', 'mjpegenc_common.c'],
      ['libavcodec', 'mjpegenc_huffman.c'],
      ['libavcodec', 'mjpegenc.c'],
      ['libavcodec', 'mjpeg_parser.c'],
      ['libavcodec', 'mlpdec.c'],
      ['libavcodec', 'mlpdsp.c'],
      ['libavcodec', 'mlpenc.c'],
      ['libavcodec', 'mlp.c'],
      ['libavcodec', 'mlp_parse.c'],
      ['libavcodec', 'mlp_parser.c'],
      ['libavcodec', 'mlz.c'],
      ['libavcodec', 'mmvideo.c'],
      ['libavcodec', 'motion_est.c'],
      ['libavcodec', 'motionpixels.c'],
      ['libavcodec', 'movsub_bsf.c'],
      ['libavcodec', 'movtextdec.c'],
      ['libavcodec', 'movtextenc.c'],
      ['libavcodec', 'mp3_header_decompress_bsf.c'],
      ['libavcodec', 'mpc7.c'],
      ['libavcodec', 'mpc8.c'],
      ['libavcodec', 'mpc.c'],
      ['libavcodec', 'mpeg12data.c'],
      ['libavcodec', 'mpeg12dec.c'],
      ['libavcodec', 'mpeg12enc.c'],
      ['libavcodec', 'mpeg12framerate.c'],
      ['libavcodec', 'mpeg12.c'],
      ['libavcodec', 'mpeg2_metadata_bsf.c'],
      ['libavcodec', 'mpeg4audio.c'],
      ['libavcodec', 'mpeg4_unpack_bframes_bsf.c'],
      ['libavcodec', 'mpeg4videodec.c'],
      ['libavcodec', 'mpeg4videoenc.c'],
      ['libavcodec', 'mpeg4video.c'],
      ['libavcodec', 'mpeg4video_parser.c'],
      ['libavcodec', 'mpegaudiodata.c'],
      ['libavcodec', 'mpegaudiodec_fixed.c'],
      ['libavcodec', 'mpegaudiodec_float.c'],
      ['libavcodec', 'mpegaudiodecheader.c'],
      ['libavcodec', 'mpegaudiodsp_data.c'],
      ['libavcodec', 'mpegaudiodsp_fixed.c'],
      ['libavcodec', 'mpegaudiodsp_float.c'],
      ['libavcodec', 'mpegaudiodsp.c'],
      ['libavcodec', 'mpegaudioenc_fixed.c'],
      ['libavcodec', 'mpegaudioenc_float.c'],
      ['libavcodec', 'mpegaudio.c'],
      ['libavcodec', 'mpegaudio_parser.c'],
      ['libavcodec', 'mpeg_er.c'],
      ['libavcodec', 'mpegpicture.c'],
      ['libavcodec', 'mpegutils.c'],
      ['libavcodec', 'mpegvideodata.c'],
      ['libavcodec', 'mpegvideodsp.c'],
      ['libavcodec', 'mpegvideoencdsp.c'],
      ['libavcodec', 'mpegvideo_enc.c'],
      ['libavcodec', 'mpegvideo_motion.c'],
      ['libavcodec', 'mpegvideo.c'],
      ['libavcodec', 'mpegvideo_parser.c'],
      ['libavcodec', 'mpl2dec.c'],
      ['libavcodec', 'mqcdec.c'],
      ['libavcodec', 'mqcenc.c'],
      ['libavcodec', 'mqc.c'],
      ['libavcodec', 'msgsmdec.c'],
      ['libavcodec', 'msmpeg4data.c'],
      ['libavcodec', 'msmpeg4dec.c'],
      ['libavcodec', 'msmpeg4enc.c'],
      ['libavcodec', 'msmpeg4.c'],
      ['libavcodec', 'msrledec.c'],
      ['libavcodec', 'msrle.c'],
      ['libavcodec', 'mss12.c'],
      ['libavcodec', 'mss1.c'],
      ['libavcodec', 'mss2dsp.c'],
      ['libavcodec', 'mss2.c'],
      ['libavcodec', 'mss34dsp.c'],
      ['libavcodec', 'mss3.c'],
      ['libavcodec', 'mss4.c'],
      ['libavcodec', 'msvideo1enc.c'],
      ['libavcodec', 'msvideo1.c'],
      ['libavcodec', 'mv30.c'],
      ['libavcodec', 'mvcdec.c'],
      ['libavcodec', 'mxpegdec.c'],
      ['libavcodec', 'nellymoserdec.c'],
      ['libavcodec', 'nellymoserenc.c'],
      ['libavcodec', 'nellymoser.c'],
      ['libavcodec', 'noise_bsf.c'],
      ['libavcodec', 'notchlc.c'],
      ['libavcodec', 'null_bsf.c'],
      ['libavcodec', 'nuv.c'],
      ['libavcodec', 'on2avcdata.c'],
      ['libavcodec', 'on2avc.c'],
      ['libavcodec', 'options.c'],
      ['libavcodec', 'opus_celt.c'],
      ['libavcodec', 'opusdec.c'],
      ['libavcodec', 'opusdsp.c'],
      ['libavcodec', 'opusenc.c'],
      ['libavcodec', 'opusenc_psy.c'],
      ['libavcodec', 'opus_metadata_bsf.c'],
      ['libavcodec', 'opus.c'],
      ['libavcodec', 'opus_parser.c'],
      ['libavcodec', 'opus_pvq.c'],
      ['libavcodec', 'opus_rc.c'],
      ['libavcodec', 'opus_silk.c'],
      ['libavcodec', 'opustab.c'],
      ['libavcodec', 'pafaudio.c'],
      ['libavcodec', 'pafvideo.c'],
      ['libavcodec', 'pamenc.c'],
      ['libavcodec', 'parser.c'],
      ['libavcodec', 'parsers.c'],
      ['libavcodec', 'pcm-bluray.c'],
      ['libavcodec', 'pcm-dvdenc.c'],
      ['libavcodec', 'pcm-dvd.c'],
      ['libavcodec', 'pcm.c'],
      ['libavcodec', 'pcm_rechunk_bsf.c'],
      ['libavcodec', 'pcxenc.c'],
      ['libavcodec', 'pcx.c'],
      ['libavcodec', 'pgssubdec.c'],
      ['libavcodec', 'pictordec.c'],
      ['libavcodec', 'pixblockdsp.c'],
      ['libavcodec', 'pixlet.c'],
      ['libavcodec', 'png_parser.c'],
      ['libavcodec', 'pnmdec.c'],
      ['libavcodec', 'pnmenc.c'],
      ['libavcodec', 'pnm.c'],
      ['libavcodec', 'pnm_parser.c'],
      ['libavcodec', 'profiles.c'],
      ['libavcodec', 'proresdata.c'],
      ['libavcodec', 'proresdec2.c'],
      ['libavcodec', 'proresdsp.c'],
      ['libavcodec', 'proresenc_anatoliy.c'],
      ['libavcodec', 'proresenc_kostya.c'],
      ['libavcodec', 'prores_metadata_bsf.c'],
      ['libavcodec', 'prosumer.c'],
      ['libavcodec', 'psd.c'],
      ['libavcodec', 'psymodel.c'],
      ['libavcodec', 'ptx.c'],
      ['libavcodec', 'qcelpdec.c'],
      ['libavcodec', 'qdm2.c'],
      ['libavcodec', 'qdmc.c'],
      ['libavcodec', 'qdrw.c'],
      ['libavcodec', 'qpeg.c'],
      ['libavcodec', 'qpeldsp.c'],
      ['libavcodec', 'qsv_api.c'],
      ['libavcodec', 'qtrleenc.c'],
      ['libavcodec', 'qtrle.c'],
      ['libavcodec', 'r210dec.c'],
      ['libavcodec', 'r210enc.c'],
      ['libavcodec', 'ra144dec.c'],
      ['libavcodec', 'ra144enc.c'],
      ['libavcodec', 'ra144.c'],
      ['libavcodec', 'ra288.c'],
      ['libavcodec', 'ralf.c'],
      ['libavcodec', 'rangecoder.c'],
      ['libavcodec', 'ratecontrol.c'],
      ['libavcodec', 'rawdec.c'],
      ['libavcodec', 'rawenc.c'],
      ['libavcodec', 'raw.c'],
      ['libavcodec', 'rdft.c'],
      ['libavcodec', 'realtextdec.c'],
      ['libavcodec', 'remove_extradata_bsf.c'],
      ['libavcodec', 'rl2.c'],
      ['libavcodec', 'rle.c'],
      ['libavcodec', 'rl.c'],
      ['libavcodec', 'roqaudioenc.c'],
      ['libavcodec', 'roqvideodec.c'],
      ['libavcodec', 'roqvideoenc.c'],
      ['libavcodec', 'roqvideo.c'],
      ['libavcodec', 'rpza.c'],
      ['libavcodec', 'rtjpeg.c'],
      ['libavcodec', 'rv10enc.c'],
      ['libavcodec', 'rv10.c'],
      ['libavcodec', 'rv20enc.c'],
      ['libavcodec', 'rv30dsp.c'],
      ['libavcodec', 'rv30.c'],
      ['libavcodec', 'rv34dsp.c'],
      ['libavcodec', 'rv34.c'],
      ['libavcodec', 'rv34_parser.c'],
      ['libavcodec', 'rv40dsp.c'],
      ['libavcodec', 'rv40.c'],
      ['libavcodec', 's302menc.c'],
      ['libavcodec', 's302m.c'],
      ['libavcodec', 'samidec.c'],
      ['libavcodec', 'sanm.c'],
      ['libavcodec', 'sbcdec_data.c'],
      ['libavcodec', 'sbcdec.c'],
      ['libavcodec', 'sbcdsp_data.c'],
      ['libavcodec', 'sbcdsp.c'],
      ['libavcodec', 'sbcenc.c'],
      ['libavcodec', 'sbc.c'],
      ['libavcodec', 'sbc_parser.c'],
      ['libavcodec', 'sbrdsp_fixed.c'],
      ['libavcodec', 'sbrdsp.c'],
      ['libavcodec', 'scpr.c'],
      ['libavcodec', 'sgidec.c'],
      ['libavcodec', 'sgienc.c'],
      ['libavcodec', 'sgirledec.c'],
      ['libavcodec', 'sheervideo.c'],
      ['libavcodec', 'shorten.c'],
      ['libavcodec', 'simple_idct.c'],
      ['libavcodec', 'sinewin_fixed.c'],
      ['libavcodec', 'sinewin.c'],
      ['libavcodec', 'sipr16k.c'],
      ['libavcodec', 'sipr.c'],
      ['libavcodec', 'sipr_parser.c'],
      ['libavcodec', 'siren.c'],
      ['libavcodec', 'smacker.c'],
      ['libavcodec', 'smc.c'],
      ['libavcodec', 'smvjpegdec.c'],
      ['libavcodec', 'snappy.c'],
      ['libavcodec', 'snowdec.c'],
      ['libavcodec', 'snow_dwt.c'],
      ['libavcodec', 'snowenc.c'],
      ['libavcodec', 'snow.c'],
      ['libavcodec', 'sonic.c'],
      ['libavcodec', 'sp5xdec.c'],
      ['libavcodec', 'speedhq.c'],
      ['libavcodec', 'srtdec.c'],
      ['libavcodec', 'srtenc.c'],
      ['libavcodec', 'startcode.c'],
      ['libavcodec', 'subviewerdec.c'],
      ['libavcodec', 'sunrastenc.c'],
      ['libavcodec', 'sunrast.c'],
      ['libavcodec', 'svq1dec.c'],
      ['libavcodec', 'svq1enc.c'],
      ['libavcodec', 'svq1.c'],
      ['libavcodec', 'svq3.c'],
      ['libavcodec', 'synth_filter.c'],
      ['libavcodec', 'takdec.c'],
      ['libavcodec', 'takdsp.c'],
      ['libavcodec', 'tak.c'],
      ['libavcodec', 'tak_parser.c'],
      ['libavcodec', 'targaenc.c'],
      ['libavcodec', 'targa.c'],
      ['libavcodec', 'targa_y216dec.c'],
      ['libavcodec', 'textdec.c'],
      ['libavcodec', 'texturedsp.c'],
      ['libavcodec', 'tiertexseqv.c'],
      ['libavcodec', 'tiff_common.c'],
      ['libavcodec', 'tiff_data.c'],
      ['libavcodec', 'tiffenc.c'],
      ['libavcodec', 'tiff.c'],
      ['libavcodec', 'tmv.c'],
      ['libavcodec', 'tpeldsp.c'],
      ['libavcodec', 'trace_headers_bsf.c'],
      ['libavcodec', 'truehd_core_bsf.c'],
      ['libavcodec', 'truemotion1.c'],
      ['libavcodec', 'truemotion2.c'],
      ['libavcodec', 'truemotion2rt.c'],
      ['libavcodec', 'truespeech.c'],
      ['libavcodec', 'tscc2.c'],
      ['libavcodec', 'ttadata.c'],
      ['libavcodec', 'ttadsp.c'],
      ['libavcodec', 'ttaencdsp.c'],
      ['libavcodec', 'ttaenc.c'],
      ['libavcodec', 'tta.c'],
      ['libavcodec', 'twinvqdec.c'],
      ['libavcodec', 'twinvq.c'],
      ['libavcodec', 'txd.c'],
      ['libavcodec', 'ulti.c'],
      ['libavcodec', 'utils.c'],
      ['libavcodec', 'utvideodec.c'],
      ['libavcodec', 'utvideodsp.c'],
      ['libavcodec', 'utvideoenc.c'],
      ['libavcodec', 'utvideo.c'],
      ['libavcodec', 'v210dec.c'],
      ['libavcodec', 'v210enc.c'],
      ['libavcodec', 'v210x.c'],
      ['libavcodec', 'v308dec.c'],
      ['libavcodec', 'v308enc.c'],
      ['libavcodec', 'v408dec.c'],
      ['libavcodec', 'v408enc.c'],
      ['libavcodec', 'v410dec.c'],
      ['libavcodec', 'v410enc.c'],
      ['libavcodec', 'vble.c'],
      ['libavcodec', 'vb.c'],
      ['libavcodec', 'vc1_block.c'],
      ['libavcodec', 'vc1data.c'],
      ['libavcodec', 'vc1dec.c'],
      ['libavcodec', 'vc1dsp.c'],
      ['libavcodec', 'vc1_loopfilter.c'],
      ['libavcodec', 'vc1_mc.c'],
      ['libavcodec', 'vc1.c'],
      ['libavcodec', 'vc1_parser.c'],
      ['libavcodec', 'vc1_pred.c'],
      ['libavcodec', 'vc2enc_dwt.c'],
      ['libavcodec', 'vc2enc.c'],
      ['libavcodec', 'vcr1.c'],
      ['libavcodec', 'videodsp.c'],
      ['libavcodec', 'vima.c'],
      ['libavcodec', 'vmdaudio.c'],
      ['libavcodec', 'vmdvideo.c'],
      ['libavcodec', 'vmnc.c'],
      ['libavcodec', 'vorbis_data.c'],
      ['libavcodec', 'vorbisdec.c'],
      ['libavcodec', 'vorbisdsp.c'],
      ['libavcodec', 'vorbisenc.c'],
      ['libavcodec', 'vorbis.c'],
      ['libavcodec', 'vorbis_parser.c'],
      ['libavcodec', 'vp3dsp.c'],
      ['libavcodec', 'vp3.c'],
      ['libavcodec', 'vp3_parser.c'],
      ['libavcodec', 'vp56data.c'],
      ['libavcodec', 'vp56dsp.c'],
      ['libavcodec', 'vp56.c'],
      ['libavcodec', 'vp56rac.c'],
      ['libavcodec', 'vp5.c'],
      ['libavcodec', 'vp6dsp.c'],
      ['libavcodec', 'vp6.c'],
      ['libavcodec', 'vp8dsp.c'],
      ['libavcodec', 'vp8.c'],
      ['libavcodec', 'vp8_parser.c'],
      ['libavcodec', 'vp9block.c'],
      ['libavcodec', 'vp9data.c'],
      ['libavcodec', 'vp9dsp_10bpp.c'],
      ['libavcodec', 'vp9dsp_12bpp.c'],
      ['libavcodec', 'vp9dsp_8bpp.c'],
      ['libavcodec', 'vp9dsp.c'],
      ['libavcodec', 'vp9lpf.c'],
      ['libavcodec', 'vp9_metadata_bsf.c'],
      ['libavcodec', 'vp9mvs.c'],
      ['libavcodec', 'vp9.c'],
      ['libavcodec', 'vp9_parser.c'],
      ['libavcodec', 'vp9prob.c'],
      ['libavcodec', 'vp9_raw_reorder_bsf.c'],
      ['libavcodec', 'vp9recon.c'],
      ['libavcodec', 'vp9_superframe_bsf.c'],
      ['libavcodec', 'vp9_superframe_split_bsf.c'],
      ['libavcodec', 'vqavideo.c'],
      ['libavcodec', 'wavpackenc.c'],
      ['libavcodec', 'wavpack.c'],
      ['libavcodec', 'webp.c'],
      ['libavcodec', 'webp_parser.c'],
      ['libavcodec', 'webvttdec.c'],
      ['libavcodec', 'webvttenc.c'],
      ['libavcodec', 'wma_common.c'],
      ['libavcodec', 'wmadec.c'],
      ['libavcodec', 'wmaenc.c'],
      ['libavcodec', 'wma_freqs.c'],
      ['libavcodec', 'wmalosslessdec.c'],
      ['libavcodec', 'wma.c'],
      ['libavcodec', 'wmaprodec.c'],
      ['libavcodec', 'wmavoice.c'],
      ['libavcodec', 'wmv2data.c'],
      ['libavcodec', 'wmv2dec.c'],
      ['libavcodec', 'wmv2dsp.c'],
      ['libavcodec', 'wmv2enc.c'],
      ['libavcodec', 'wmv2.c'],
      ['libavcodec', 'wnv1.c'],
      ['libavcodec', 'wrapped_avframe.c'],
      ['libavcodec', 'ws-snd1.c'],
      ['libavcodec', 'xan.c'],
      ['libavcodec', 'xbmdec.c'],
      ['libavcodec', 'xbmenc.c'],
      ['libavcodec', 'xfacedec.c'],
      ['libavcodec', 'xfaceenc.c'],
      ['libavcodec', 'xface.c'],
      ['libavcodec', 'xiph.c'],
      ['libavcodec', 'xl.c'],
      ['libavcodec', 'xma_parser.c'],
      ['libavcodec', 'xpmdec.c'],
      ['libavcodec', 'xsubdec.c'],
      ['libavcodec', 'xsubenc.c'],
      ['libavcodec', 'xvididct.c'],
      ['libavcodec', 'xwddec.c'],
      ['libavcodec', 'xwdenc.c'],
      ['libavcodec', 'xxan.c'],
      ['libavcodec', 'y41pdec.c'],
      ['libavcodec', 'y41penc.c'],
      ['libavcodec', 'ylc.c'],
      ['libavcodec', 'yop.c'],
      ['libavcodec', 'yuv4dec.c'],
      ['libavcodec', 'yuv4enc.c'],
      ['libavcodec/x86', 'aacencdsp_init.c'],
      ['libavcodec/x86', 'aacpsdsp_init.c'],
      ['libavcodec/x86', 'ac3dsp_init.c'],
      ['libavcodec/x86', 'alacdsp_init.c'],
      ['libavcodec/x86', 'audiodsp_init.c'],
      ['libavcodec/x86', 'blockdsp_init.c'],
      ['libavcodec/x86', 'bswapdsp_init.c'],
      ['libavcodec/x86', 'cavsdsp.c'],
      ['libavcodec/x86', 'celt_pvq_init.c'],
      ['libavcodec/x86', 'constants.c'],
      ['libavcodec/x86', 'dcadsp_init.c'],
      ['libavcodec/x86', 'dct_init.c'],
      ['libavcodec/x86', 'diracdsp_init.c'],
      ['libavcodec/x86', 'dirac_dwt_init.c'],
      ['libavcodec/x86', 'dnxhdenc_init.c'],
      ['libavcodec/x86', 'fdctdsp_init.c'],
      ['libavcodec/x86', 'fdct.c'],
      ['libavcodec/x86', 'fft_init.c'],
      ['libavcodec/x86', 'flacdsp_init.c'],
      ['libavcodec/x86', 'fmtconvert_init.c'],
      ['libavcodec/x86', 'g722dsp_init.c'],
      ['libavcodec/x86', 'h263dsp_init.c'],
      ['libavcodec/x86', 'h264chroma_init.c'],
      ['libavcodec/x86', 'h264dsp_init.c'],
      ['libavcodec/x86', 'h264_intrapred_init.c'],
      ['libavcodec/x86', 'h264_qpel.c'],
      ['libavcodec/x86', 'hevcdsp_init.c'],
      ['libavcodec/x86', 'hpeldsp_init.c'],
      ['libavcodec/x86', 'hpeldsp_vp3_init.c'],
      ['libavcodec/x86', 'huffyuvdsp_init.c'],
      ['libavcodec/x86', 'huffyuvencdsp_init.c'],
      ['libavcodec/x86', 'idctdsp_init.c'],
      ['libavcodec/x86', 'jpeg2000dsp_init.c'],
      ['libavcodec/x86', 'lossless_audiodsp_init.c'],
      ['libavcodec/x86', 'lossless_videodsp_init.c'],
      ['libavcodec/x86', 'lossless_videoencdsp_init.c'],
      ['libavcodec/x86', 'lpc.c'],
      ['libavcodec/x86', 'mdct15_init.c'],
      ['libavcodec/x86', 'me_cmp_init.c'],
      ['libavcodec/x86', 'mlpdsp_init.c'],
      ['libavcodec/x86', 'mpegaudiodsp.c'],
      ['libavcodec/x86', 'mpegvideodsp.c'],
      ['libavcodec/x86', 'mpegvideoencdsp_init.c'],
      ['libavcodec/x86', 'mpegvideoenc.c'],
      ['libavcodec/x86', 'mpegvideo.c'],
      ['libavcodec/x86', 'opusdsp_init.c'],
      ['libavcodec/x86', 'pixblockdsp_init.c'],
      ['libavcodec/x86', 'proresdsp_init.c'],
      ['libavcodec/x86', 'qpeldsp_init.c'],
      ['libavcodec/x86', 'rv34dsp_init.c'],
      ['libavcodec/x86', 'rv40dsp_init.c'],
      ['libavcodec/x86', 'sbcdsp_init.c'],
      ['libavcodec/x86', 'sbrdsp_init.c'],
      ['libavcodec/x86', 'snowdsp.c'],
      ['libavcodec/x86', 'svq1enc_init.c'],
      ['libavcodec/x86', 'synth_filter_init.c'],
      ['libavcodec/x86', 'takdsp_init.c'],
      ['libavcodec/x86', 'ttadsp_init.c'],
      ['libavcodec/x86', 'ttaencdsp_init.c'],
      ['libavcodec/x86', 'utvideodsp_init.c'],
      ['libavcodec/x86', 'v210enc_init.c'],
      ['libavcodec/x86', 'v210-init.c'],
      ['libavcodec/x86', 'vc1dsp_init.c'],
      ['libavcodec/x86', 'vc1dsp_mmx.c'],
      ['libavcodec/x86', 'videodsp_init.c'],
      ['libavcodec/x86', 'vorbisdsp_init.c'],
      ['libavcodec/x86', 'vp3dsp_init.c'],
      ['libavcodec/x86', 'vp6dsp_init.c'],
      ['libavcodec/x86', 'vp8dsp_init.c'],
      ['libavcodec/x86', 'vp9dsp_init_10bpp.c'],
      ['libavcodec/x86', 'vp9dsp_init_12bpp.c'],
      ['libavcodec/x86', 'vp9dsp_init_16bpp.c'],
      ['libavcodec/x86', 'vp9dsp_init.c'],
      ['libavcodec/x86', 'xvididct_init.c'],
      ['libavformat', '3dostr.c'],
      ['libavformat', '4xm.c'],
      ['libavformat', 'a64.c'],
      ['libavformat', 'aacdec.c'],
      ['libavformat', 'aadec.c'],
      ['libavformat', 'ac3dec.c'],
      ['libavformat', 'acm.c'],
      ['libavformat', 'act.c'],
      ['libavformat', 'adp.c'],
      ['libavformat', 'ads.c'],
      ['libavformat', 'adtsenc.c'],
      ['libavformat', 'adxdec.c'],
      ['libavformat', 'aea.c'],
      ['libavformat', 'afc.c'],
      ['libavformat', 'aiffdec.c'],
      ['libavformat', 'aiffenc.c'],
      ['libavformat', 'aixdec.c'],
      ['libavformat', 'allformats.c'],
      ['libavformat', 'alp.c'],
      ['libavformat', 'amr.c'],
      ['libavformat', 'anm.c'],
      ['libavformat', 'apc.c'],
      ['libavformat', 'ape.c'],
      ['libavformat', 'apetag.c'],
      ['libavformat', 'apm.c'],
      ['libavformat', 'apngdec.c'],
      ['libavformat', 'apngenc.c'],
      ['libavformat', 'aptxdec.c'],
      ['libavformat', 'aqtitledec.c'],
      ['libavformat', 'argo_asf.c'],
      ['libavformat', 'asfcrypt.c'],
      ['libavformat', 'asfdec_f.c'],
      ['libavformat', 'asfdec_o.c'],
      ['libavformat', 'asfenc.c'],
      ['libavformat', 'asf.c'],
      ['libavformat', 'assdec.c'],
      ['libavformat', 'assenc.c'],
      ['libavformat', 'astdec.c'],
      ['libavformat', 'astenc.c'],
      ['libavformat', 'ast.c'],
      ['libavformat', 'au.c'],
      ['libavformat', 'av1dec.c'],
      ['libavformat', 'av1.c'],
      ['libavformat', 'avc.c'],
      ['libavformat', 'avidec.c'],
      ['libavformat', 'avienc.c'],
      ['libavformat', 'aviobuf.c'],
      ['libavformat', 'avio.c'],
      ['libavformat', 'avlanguage.c'],
      ['libavformat', 'avr.c'],
      ['libavformat', 'avs.c'],
      ['libavformat', 'bethsoftvid.c'],
      ['libavformat', 'bfi.c'],
      ['libavformat', 'bink.c'],
      ['libavformat', 'bintext.c'],
      ['libavformat', 'bit.c'],
      ['libavformat', 'bmv.c'],
      ['libavformat', 'boadec.c'],
      ['libavformat', 'brstm.c'],
      ['libavformat', 'c93.c'],
      ['libavformat', 'cache.c'],
      ['libavformat', 'cafdec.c'],
      ['libavformat', 'cafenc.c'],
      ['libavformat', 'caf.c'],
      ['libavformat', 'cavsvideodec.c'],
      ['libavformat', 'cdg.c'],
      ['libavformat', 'cdxl.c'],
      ['libavformat', 'cinedec.c'],
      ['libavformat', 'codec2.c'],
      ['libavformat', 'concatdec.c'],
      ['libavformat', 'concat.c'],
      ['libavformat', 'crcenc.c'],
      ['libavformat', 'crypto.c'],
      ['libavformat', 'cutils.c'],
      ['libavformat', 'dashenc.c'],
      ['libavformat', 'dash.c'],
      ['libavformat', 'data_uri.c'],
      ['libavformat', 'dauddec.c'],
      ['libavformat', 'daudenc.c'],
      ['libavformat', 'davs2.c'],
      ['libavformat', 'dcstr.c'],
      ['libavformat', 'derf.c'],
      ['libavformat', 'dfa.c'],
      ['libavformat', 'dhav.c'],
      ['libavformat', 'diracdec.c'],
      ['libavformat', 'dnxhddec.c'],
      ['libavformat', 'dsfdec.c'],
      ['libavformat', 'dsicin.c'],
      ['libavformat', 'dss.c'],
      ['libavformat', 'dtsdec.c'],
      ['libavformat', 'dtshddec.c'],
      ['libavformat', 'dump.c'],
      ['libavformat', 'dvbsub.c'],
      ['libavformat', 'dvbtxt.c'],
      ['libavformat', 'dvenc.c'],
      ['libavformat', 'dv.c'],
      ['libavformat', 'dxa.c'],
      ['libavformat', 'eacdata.c'],
      ['libavformat', 'electronicarts.c'],
      ['libavformat', 'epafdec.c'],
      ['libavformat', 'ffmetadec.c'],
      ['libavformat', 'ffmetaenc.c'],
      ['libavformat', 'fifo_test.c'],
      ['libavformat', 'file.c'],
      ['libavformat', 'filmstripdec.c'],
      ['libavformat', 'filmstripenc.c'],
      ['libavformat', 'fitsdec.c'],
      ['libavformat', 'fitsenc.c'],
      ['libavformat', 'flacdec.c'],
      ['libavformat', 'flacenc_header.c'],
      ['libavformat', 'flacenc.c'],
      ['libavformat', 'flac_picture.c'],
      ['libavformat', 'flic.c'],
      ['libavformat', 'flvdec.c'],
      ['libavformat', 'flvenc.c'],
      ['libavformat', 'format.c'],
      ['libavformat', 'framecrcenc.c'],
      ['libavformat', 'framehash.c'],
      ['libavformat', 'frmdec.c'],
      ['libavformat', 'fsb.c'],
      ['libavformat', 'ftp.c'],
      ['libavformat', 'fwse.c'],
      ['libavformat', 'g722.c'],
      ['libavformat', 'g723_1.c'],
      ['libavformat', 'g726.c'],
      ['libavformat', 'g729dec.c'],
      ['libavformat', 'gdv.c'],
      ['libavformat', 'genh.c'],
      ['libavformat', 'gifdec.c'],
      ['libavformat', 'gif.c'],
      ['libavformat', 'gopher.c'],
      ['libavformat', 'gsmdec.c'],
      ['libavformat', 'gxfenc.c'],
      ['libavformat', 'gxf.c'],
      ['libavformat', 'h261dec.c'],
      ['libavformat', 'h263dec.c'],
      ['libavformat', 'h264dec.c'],
      ['libavformat', 'hashenc.c'],
      ['libavformat', 'hca.c'],
      ['libavformat', 'hcom.c'],
      ['libavformat', 'hdsenc.c'],
      ['libavformat', 'hevcdec.c'],
      ['libavformat', 'hevc.c'],
      ['libavformat', 'hlsenc.c'],
      ['libavformat', 'hls.c'],
      ['libavformat', 'hlsplaylist.c'],
      ['libavformat', 'hlsproto.c'],
      ['libavformat', 'hnm.c'],
      ['libavformat', 'httpauth.c'],
      ['libavformat', 'http.c'],
      ['libavformat', 'icecast.c'],
      ['libavformat', 'icodec.c'],
      ['libavformat', 'icoenc.c'],
      ['libavformat', 'id3v1.c'],
      ['libavformat', 'id3v2enc.c'],
      ['libavformat', 'id3v2.c'],
      ['libavformat', 'idcin.c'],
      ['libavformat', 'idroqdec.c'],
      ['libavformat', 'idroqenc.c'],
      ['libavformat', 'iff.c'],
      ['libavformat', 'ifv.c'],
      ['libavformat', 'ilbc.c'],
      ['libavformat', 'img2_alias_pix.c'],
      ['libavformat', 'img2_brender_pix.c'],
      ['libavformat', 'img2dec.c'],
      ['libavformat', 'img2enc.c'],
      ['libavformat', 'img2.c'],
      ['libavformat', 'ingenientdec.c'],
      ['libavformat', 'ipmovie.c'],
      ['libavformat', 'ip.c'],
      ['libavformat', 'ircamdec.c'],
      ['libavformat', 'ircamenc.c'],
      ['libavformat', 'ircam.c'],
      ['libavformat', 'isom.c'],
      ['libavformat', 'iss.c'],
      ['libavformat', 'iv8.c'],
      ['libavformat', 'ivfdec.c'],
      ['libavformat', 'ivfenc.c'],
      ['libavformat', 'jacosubdec.c'],
      ['libavformat', 'jacosubenc.c'],
      ['libavformat', 'jvdec.c'],
      ['libavformat', 'kvag.c'],
      ['libavformat', 'latmenc.c'],
      ['libavformat', 'lmlm4.c'],
      ['libavformat', 'loasdec.c'],
      ['libavformat', 'lrcdec.c'],
      ['libavformat', 'lrcenc.c'],
      ['libavformat', 'lrc.c'],
      ['libavformat', 'lvfdec.c'],
      ['libavformat', 'lxfdec.c'],
      ['libavformat', 'm4vdec.c'],
      ['libavformat', 'matroskadec.c'],
      ['libavformat', 'matroskaenc.c'],
      ['libavformat', 'matroska.c'],
      ['libavformat', 'md5proto.c'],
      ['libavformat', 'metadata.c'],
      ['libavformat', 'mgsts.c'],
      ['libavformat', 'microdvddec.c'],
      ['libavformat', 'microdvdenc.c'],
      ['libavformat', 'mj2kdec.c'],
      ['libavformat', 'mkvtimestamp_v2.c'],
      ['libavformat', 'mlpdec.c'],
      ['libavformat', 'mlvdec.c'],
      ['libavformat', 'mmf.c'],
      ['libavformat', 'mm.c'],
      ['libavformat', 'mmsh.c'],
      ['libavformat', 'mms.c'],
      ['libavformat', 'mmst.c'],
      ['libavformat', 'mov_chan.c'],
      ['libavformat', 'movenccenc.c'],
      ['libavformat', 'movenchint.c'],
      ['libavformat', 'movenc.c'],
      ['libavformat', 'mov_esds.c'],
      ['libavformat', 'mov.c'],
      ['libavformat', 'mp3dec.c'],
      ['libavformat', 'mp3enc.c'],
      ['libavformat', 'mpc8.c'],
      ['libavformat', 'mpc.c'],
      ['libavformat', 'mpegenc.c'],
      ['libavformat', 'mpeg.c'],
      ['libavformat', 'mpegtsenc.c'],
      ['libavformat', 'mpegts.c'],
      ['libavformat', 'mpegvideodec.c'],
      ['libavformat', 'mpjpegdec.c'],
      ['libavformat', 'mpjpeg.c'],
      ['libavformat', 'mpl2dec.c'],
      ['libavformat', 'mpsubdec.c'],
      ['libavformat', 'msf.c'],
      ['libavformat', 'msnwc_tcp.c'],
      ['libavformat', 'mtaf.c'],
      ['libavformat', 'mtv.c'],
      ['libavformat', 'musx.c'],
      ['libavformat', 'mux.c'],
      ['libavformat', 'mvdec.c'],
      ['libavformat', 'mvi.c'],
      ['libavformat', 'mxfdec.c'],
      ['libavformat', 'mxfenc.c'],
      ['libavformat', 'mxf.c'],
      ['libavformat', 'mxg.c'],
      ['libavformat', 'ncdec.c'],
      ['libavformat', 'network.c'],
      ['libavformat', 'nistspheredec.c'],
      ['libavformat', 'nspdec.c'],
      ['libavformat', 'nsvdec.c'],
      ['libavformat', 'nullenc.c'],
      ['libavformat', 'nutdec.c'],
      ['libavformat', 'nutenc.c'],
      ['libavformat', 'nut.c'],
      ['libavformat', 'nuv.c'],
      ['libavformat', 'oggdec.c'],
      ['libavformat', 'oggenc.c'],
      ['libavformat', 'oggparsecelt.c'],
      ['libavformat', 'oggparsedirac.c'],
      ['libavformat', 'oggparseflac.c'],
      ['libavformat', 'oggparseogm.c'],
      ['libavformat', 'oggparseopus.c'],
      ['libavformat', 'oggparseskeleton.c'],
      ['libavformat', 'oggparsespeex.c'],
      ['libavformat', 'oggparsetheora.c'],
      ['libavformat', 'oggparsevorbis.c'],
      ['libavformat', 'oggparsevp8.c'],
      ['libavformat', 'omadec.c'],
      ['libavformat', 'omaenc.c'],
      ['libavformat', 'oma.c'],
      ['libavformat', 'options.c'],
      ['libavformat', 'os_support.c'],
      ['libavformat', 'paf.c'],
      ['libavformat', 'pcmdec.c'],
      ['libavformat', 'pcmenc.c'],
      ['libavformat', 'pcm.c'],
      ['libavformat', 'pjsdec.c'],
      ['libavformat', 'pmpdec.c'],
      ['libavformat', 'pp_bnk.c'],
      ['libavformat', 'prompeg.c'],
      ['libavformat', 'protocols.c'],
      ['libavformat', 'psxstr.c'],
      ['libavformat', 'pva.c'],
      ['libavformat', 'pvfdec.c'],
      ['libavformat', 'qcp.c'],
      ['libavformat', 'qtpalette.c'],
      ['libavformat', 'r3d.c'],
      ['libavformat', 'rawdec.c'],
      ['libavformat', 'rawenc.c'],
      ['libavformat', 'rawutils.c'],
      ['libavformat', 'rawvideodec.c'],
      ['libavformat', 'rdt.c'],
      ['libavformat', 'realtextdec.c'],
      ['libavformat', 'redspark.c'],
      ['libavformat', 'replaygain.c'],
      ['libavformat', 'riffdec.c'],
      ['libavformat', 'riffenc.c'],
      ['libavformat', 'riff.c'],
      ['libavformat', 'rl2.c'],
      ['libavformat', 'rmdec.c'],
      ['libavformat', 'rmenc.c'],
      ['libavformat', 'rm.c'],
      ['libavformat', 'rmsipr.c'],
      ['libavformat', 'rpl.c'],
      ['libavformat', 'rsd.c'],
      ['libavformat', 'rsodec.c'],
      ['libavformat', 'rsoenc.c'],
      ['libavformat', 'rso.c'],
      ['libavformat', 'rtmpdigest.c'],
      ['libavformat', 'rtmphttp.c'],
      ['libavformat', 'rtmppkt.c'],
      ['libavformat', 'rtmpproto.c'],
      ['libavformat', 'rtpdec_ac3.c'],
      ['libavformat', 'rtpdec_amr.c'],
      ['libavformat', 'rtpdec_asf.c'],
      ['libavformat', 'rtpdec_dv.c'],
      ['libavformat', 'rtpdec_g726.c'],
      ['libavformat', 'rtpdec_h261.c'],
      ['libavformat', 'rtpdec_h263.c'],
      ['libavformat', 'rtpdec_h263_rfc2190.c'],
      ['libavformat', 'rtpdec_h264.c'],
      ['libavformat', 'rtpdec_hevc.c'],
      ['libavformat', 'rtpdec_ilbc.c'],
      ['libavformat', 'rtpdec_jpeg.c'],
      ['libavformat', 'rtpdec_latm.c'],
      ['libavformat', 'rtpdec_mpa_robust.c'],
      ['libavformat', 'rtpdec_mpeg12.c'],
      ['libavformat', 'rtpdec_mpeg4.c'],
      ['libavformat', 'rtpdec_mpegts.c'],
      ['libavformat', 'rtpdec.c'],
      ['libavformat', 'rtpdec_qcelp.c'],
      ['libavformat', 'rtpdec_qdm2.c'],
      ['libavformat', 'rtpdec_qt.c'],
      ['libavformat', 'rtpdec_rfc4175.c'],
      ['libavformat', 'rtpdec_svq3.c'],
      ['libavformat', 'rtpdec_vc2hq.c'],
      ['libavformat', 'rtpdec_vp8.c'],
      ['libavformat', 'rtpdec_vp9.c'],
      ['libavformat', 'rtpdec_xiph.c'],
      ['libavformat', 'rtpenc_aac.c'],
      ['libavformat', 'rtpenc_amr.c'],
      ['libavformat', 'rtpenc_chain.c'],
      ['libavformat', 'rtpenc_h261.c'],
      ['libavformat', 'rtpenc_h263.c'],
      ['libavformat', 'rtpenc_h263_rfc2190.c'],
      ['libavformat', 'rtpenc_h264_hevc.c'],
      ['libavformat', 'rtpenc_jpeg.c'],
      ['libavformat', 'rtpenc_latm.c'],
      ['libavformat', 'rtpenc_mpegts.c'],
      ['libavformat', 'rtpenc_mpv.c'],
      ['libavformat', 'rtpenc.c'],
      ['libavformat', 'rtpenc_vc2hq.c'],
      ['libavformat', 'rtpenc_vp8.c'],
      ['libavformat', 'rtpenc_vp9.c'],
      ['libavformat', 'rtpenc_xiph.c'],
      ['libavformat', 'rtp.c'],
      ['libavformat', 'rtpproto.c'],
      ['libavformat', 'rtspdec.c'],
      ['libavformat', 'rtspenc.c'],
      ['libavformat', 'rtsp.c'],
      ['libavformat', 's337m.c'],
      ['libavformat', 'samidec.c'],
      ['libavformat', 'sapdec.c'],
      ['libavformat', 'sapenc.c'],
      ['libavformat', 'sauce.c'],
      ['libavformat', 'sbcdec.c'],
      ['libavformat', 'sbgdec.c'],
      ['libavformat', 'sccdec.c'],
      ['libavformat', 'sccenc.c'],
      ['libavformat', 'sdp.c'],
      ['libavformat', 'sdr2.c'],
      ['libavformat', 'sdsdec.c'],
      ['libavformat', 'sdxdec.c'],
      ['libavformat', 'segafilmenc.c'],
      ['libavformat', 'segafilm.c'],
      ['libavformat', 'segment.c'],
      ['libavformat', 'serdec.c'],
      ['libavformat', 'shortendec.c'],
      ['libavformat', 'sierravmd.c'],
      ['libavformat', 'siff.c'],
      ['libavformat', 'smacker.c'],
      ['libavformat', 'smjpegdec.c'],
      ['libavformat', 'smjpegenc.c'],
      ['libavformat', 'smjpeg.c'],
      ['libavformat', 'smoothstreamingenc.c'],
      ['libavformat', 'smush.c'],
      ['libavformat', 'sol.c'],
      ['libavformat', 'soxdec.c'],
      ['libavformat', 'soxenc.c'],
      ['libavformat', 'spdifdec.c'],
      ['libavformat', 'spdifenc.c'],
      ['libavformat', 'spdif.c'],
      ['libavformat', 'srtdec.c'],
      ['libavformat', 'srtenc.c'],
      ['libavformat', 'srtp.c'],
      ['libavformat', 'srtpproto.c'],
      ['libavformat', 'stldec.c'],
      ['libavformat', 'subfile.c'],
      ['libavformat', 'subtitles.c'],
      ['libavformat', 'subviewer1dec.c'],
      ['libavformat', 'subviewerdec.c'],
      ['libavformat', 'supdec.c'],
      ['libavformat', 'supenc.c'],
      ['libavformat', 'svag.c'],
      ['libavformat', 'swfdec.c'],
      ['libavformat', 'swfenc.c'],
      ['libavformat', 'swf.c'],
      ['libavformat', 'takdec.c'],
      ['libavformat', 'tcp.c'],
      ['libavformat', 'tedcaptionsdec.c'],
      ['libavformat', 'tee_common.c'],
      ['libavformat', 'tee.c'],
      ['libavformat', 'teeproto.c'],
      ['libavformat', 'thp.c'],
      ['libavformat', 'tiertexseq.c'],
      ['libavformat', 'tmv.c'],
      ['libavformat', 'ttaenc.c'],
      ['libavformat', 'tta.c'],
      ['libavformat', 'tty.c'],
      ['libavformat', 'txd.c'],
      ['libavformat', 'ty.c'],
      ['libavformat', 'udp.c'],
      ['libavformat', 'uncodedframecrcenc.c'],
      ['libavformat', 'unix.c'],
      ['libavformat', 'urldecode.c'],
      ['libavformat', 'url.c'],
      ['libavformat', 'utils.c'],
      ['libavformat', 'v210.c'],
      ['libavformat', 'vag.c'],
      ['libavformat', 'vc1dec.c'],
      ['libavformat', 'vc1testenc.c'],
      ['libavformat', 'vc1test.c'],
      ['libavformat', 'vividas.c'],
      ['libavformat', 'vivo.c'],
      ['libavformat', 'vocdec.c'],
      ['libavformat', 'vocenc.c'],
      ['libavformat', 'voc.c'],
      ['libavformat', 'voc_packet.c'],
      ['libavformat', 'vorbiscomment.c'],
      ['libavformat', 'vpcc.c'],
      ['libavformat', 'vpk.c'],
      ['libavformat', 'vplayerdec.c'],
      ['libavformat', 'vqf.c'],
      ['libavformat', 'w64.c'],
      ['libavformat', 'wavdec.c'],
      ['libavformat', 'wavenc.c'],
      ['libavformat', 'wc3movie.c'],
      ['libavformat', 'webm_chunk.c'],
      ['libavformat', 'webmdashenc.c'],
      ['libavformat', 'webpenc.c'],
      ['libavformat', 'webvttdec.c'],
      ['libavformat', 'webvttenc.c'],
      ['libavformat', 'westwood_aud.c'],
      ['libavformat', 'westwood_vqa.c'],
      ['libavformat', 'wsddec.c'],
      ['libavformat', 'wtv_common.c'],
      ['libavformat', 'wtvdec.c'],
      ['libavformat', 'wtvenc.c'],
      ['libavformat', 'wvdec.c'],
      ['libavformat', 'wvedec.c'],
      ['libavformat', 'wvenc.c'],
      ['libavformat', 'wv.c'],
      ['libavformat', 'xa.c'],
      ['libavformat', 'xmv.c'],
      ['libavformat', 'xvag.c'],
      ['libavformat', 'xwma.c'],
      ['libavformat', 'yop.c'],
      ['libavformat', 'yuv4mpegdec.c'],
      ['libavformat', 'yuv4mpegenc.c'],
      ['libavutil', 'adler32.c'],
      ['libavutil', 'aes_ctr.c'],
      ['libavutil', 'aes.c'],
      ['libavutil', 'audio_fifo.c'],
      ['libavutil', 'avsscanf.c'],
      ['libavutil', 'avstring.c'],
      ['libavutil', 'base64.c'],
      ['libavutil', 'blowfish.c'],
      ['libavutil', 'bprint.c'],
      ['libavutil', 'buffer.c'],
      ['libavutil', 'camellia.c'],
      ['libavutil', 'cast5.c'],
      ['libavutil', 'channel_layout.c'],
      ['libavutil', 'color_utils.c'],
      ['libavutil', 'cpu.c'],
      ['libavutil', 'crc.c'],
      ['libavutil', 'des.c'],
      ['libavutil', 'dict.c'],
      ['libavutil', 'display.c'],
      ['libavutil', 'dovi_meta.c'],
      ['libavutil', 'downmix_info.c'],
      ['libavutil', 'encryption_info.c'],
      ['libavutil', 'error.c'],
      ['libavutil', 'eval.c'],
      ['libavutil', 'fifo.c'],
      ['libavutil', 'file.c'],
      ['libavutil', 'file_open.c'],
      ['libavutil', 'fixed_dsp.c'],
      ['libavutil', 'float_dsp.c'],
      ['libavutil', 'frame.c'],
      ['libavutil', 'hash.c'],
      ['libavutil', 'hdr_dynamic_metadata.c'],
      ['libavutil', 'hmac.c'],
      ['libavutil', 'hwcontext.c'],
      ['libavutil', 'imgutils.c'],
      ['libavutil', 'integer.c'],
      ['libavutil', 'intmath.c'],
      ['libavutil', 'lfg.c'],
      ['libavutil', 'lls.c'],
      ['libavutil', 'log2_tab.c'],
      ['libavutil', 'log.c'],
      ['libavutil', 'lzo.c'],
      ['libavutil', 'mastering_display_metadata.c'],
      ['libavutil', 'mathematics.c'],
      ['libavutil', 'md5.c'],
      ['libavutil', 'mem.c'],
      ['libavutil', 'murmur3.c'],
      ['libavutil', 'opt.c'],
      ['libavutil', 'parseutils.c'],
      ['libavutil', 'pixdesc.c'],
      ['libavutil', 'pixelutils.c'],
      ['libavutil', 'random_seed.c'],
      ['libavutil', 'rational.c'],
      ['libavutil', 'rc4.c'],
      ['libavutil', 'reverse.c'],
      ['libavutil', 'ripemd.c'],
      ['libavutil', 'samplefmt.c'],
      ['libavutil', 'sha512.c'],
      ['libavutil', 'sha.c'],
      ['libavutil', 'slicethread.c'],
      ['libavutil', 'spherical.c'],
      ['libavutil', 'stereo3d.c'],
      ['libavutil', 'tea.c'],
      ['libavutil', 'threadmessage.c'],
      ['libavutil', 'timecode.c'],
      ['libavutil', 'time.c'],
      ['libavutil', 'tree.c'],
      ['libavutil', 'twofish.c'],
      ['libavutil', 'tx_double.c'],
      ['libavutil', 'tx_float.c'],
      ['libavutil', 'tx_int32.c'],
      ['libavutil', 'tx.c'],
      ['libavutil', 'utils.c'],
      ['libavutil', 'video_enc_params.c'],
      ['libavutil', 'xga_font_data.c'],
      ['libavutil', 'xtea.c'],
      ['libavutil/x86', 'cpu.c'],
      ['libavutil/x86', 'fixed_dsp_init.c'],
      ['libavutil/x86', 'float_dsp_init.c'],
      ['libavutil/x86', 'imgutils_init.c'],
      ['libavutil/x86', 'lls_init.c'],
      ['libavutil/x86', 'pixelutils_init.c'],
      ['libavfilter', 'aeval.c'],
      ['libavfilter', 'af_acontrast.c'],
      ['libavfilter', 'af_acopy.c'],
      ['libavfilter', 'af_acrossover.c'],
      ['libavfilter', 'af_acrusher.c'],
      ['libavfilter', 'af_adeclick.c'],
      ['libavfilter', 'af_adelay.c'],
      ['libavfilter', 'af_aderivative.c'],
      ['libavfilter', 'af_aecho.c'],
      ['libavfilter', 'af_aemphasis.c'],
      ['libavfilter', 'af_afade.c'],
      ['libavfilter', 'af_afftdn.c'],
      ['libavfilter', 'af_afftfilt.c'],
      ['libavfilter', 'af_afir.c'],
      ['libavfilter', 'af_aformat.c'],
      ['libavfilter', 'af_agate.c'],
      ['libavfilter', 'af_aiir.c'],
      ['libavfilter', 'af_alimiter.c'],
      ['libavfilter', 'af_amerge.c'],
      ['libavfilter', 'af_amix.c'],
      ['libavfilter', 'af_amultiply.c'],
      ['libavfilter', 'af_anequalizer.c'],
      ['libavfilter', 'af_anlmdn.c'],
      ['libavfilter', 'af_anlms.c'],
      ['libavfilter', 'af_anull.c'],
      ['libavfilter', 'af_apad.c'],
      ['libavfilter', 'af_aphaser.c'],
      ['libavfilter', 'af_apulsator.c'],
      ['libavfilter', 'af_aresample.c'],
      ['libavfilter', 'af_arnndn.c'],
      ['libavfilter', 'af_asetnsamples.c'],
      ['libavfilter', 'af_asetrate.c'],
      ['libavfilter', 'af_ashowinfo.c'],
      ['libavfilter', 'af_asoftclip.c'],
      ['libavfilter', 'af_astats.c'],
      ['libavfilter', 'af_asubboost.c'],
      ['libavfilter', 'af_atempo.c'],
      ['libavfilter', 'af_axcorrelate.c'],
      ['libavfilter', 'af_biquads.c'],
      ['libavfilter', 'af_channelmap.c'],
      ['libavfilter', 'af_channelsplit.c'],
      ['libavfilter', 'af_chorus.c'],
      ['libavfilter', 'af_compand.c'],
      ['libavfilter', 'af_compensationdelay.c'],
      ['libavfilter', 'af_crossfeed.c'],
      ['libavfilter', 'af_crystalizer.c'],
      ['libavfilter', 'af_dcshift.c'],
      ['libavfilter', 'af_deesser.c'],
      ['libavfilter', 'af_drmeter.c'],
      ['libavfilter', 'af_dynaudnorm.c'],
      ['libavfilter', 'af_earwax.c'],
      ['libavfilter', 'af_extrastereo.c'],
      ['libavfilter', 'af_firequalizer.c'],
      ['libavfilter', 'af_flanger.c'],
      ['libavfilter', 'af_haas.c'],
      ['libavfilter', 'af_hdcd.c'],
      ['libavfilter', 'af_headphone.c'],
      ['libavfilter', 'af_join.c'],
      ['libavfilter', 'af_loudnorm.c'],
      ['libavfilter', 'af_mcompand.c'],
      ['libavfilter', 'af_pan.c'],
      ['libavfilter', 'af_replaygain.c'],
      ['libavfilter', 'af_sidechaincompress.c'],
      ['libavfilter', 'af_silencedetect.c'],
      ['libavfilter', 'af_silenceremove.c'],
      ['libavfilter', 'af_stereotools.c'],
      ['libavfilter', 'af_stereowiden.c'],
      ['libavfilter', 'af_superequalizer.c'],
      ['libavfilter', 'af_surround.c'],
      ['libavfilter', 'af_tremolo.c'],
      ['libavfilter', 'af_vibrato.c'],
      ['libavfilter', 'af_volumedetect.c'],
      ['libavfilter', 'af_volume.c'],
      ['libavfilter', 'allfilters.c'],
      ['libavfilter', 'asink_anullsink.c'],
      ['libavfilter', 'asrc_afirsrc.c'],
      ['libavfilter', 'asrc_anoisesrc.c'],
      ['libavfilter', 'asrc_anullsrc.c'],
      ['libavfilter', 'asrc_hilbert.c'],
      ['libavfilter', 'asrc_sinc.c'],
      ['libavfilter', 'asrc_sine.c'],
      ['libavfilter', 'audio.c'],
      ['libavfilter', 'avf_abitscope.c'],
      ['libavfilter', 'avf_ahistogram.c'],
      ['libavfilter', 'avf_aphasemeter.c'],
      ['libavfilter', 'avf_avectorscope.c'],
      ['libavfilter', 'avf_concat.c'],
      ['libavfilter', 'avfiltergraph.c'],
      ['libavfilter', 'avfilter.c'],
      ['libavfilter', 'avf_showcqt.c'],
      ['libavfilter', 'avf_showfreqs.c'],
      ['libavfilter', 'avf_showspatial.c'],
      ['libavfilter', 'avf_showspectrum.c'],
      ['libavfilter', 'avf_showvolume.c'],
      ['libavfilter', 'avf_showwaves.c'],
      ['libavfilter', 'bbox.c'],
      ['libavfilter', 'buffersink.c'],
      ['libavfilter', 'buffersrc.c'],
      ['libavfilter', 'colorspacedsp.c'],
      ['libavfilter', 'colorspace.c'],
      ['libavfilter', 'drawutils.c'],
      ['libavfilter', 'ebur128.c'],
      ['libavfilter', 'f_bench.c'],
      ['libavfilter', 'f_cue.c'],
      ['libavfilter', 'f_drawgraph.c'],
      ['libavfilter', 'f_ebur128.c'],
      ['libavfilter', 'f_graphmonitor.c'],
      ['libavfilter', 'fifo.c'],
      ['libavfilter', 'f_interleave.c'],
      ['libavfilter', 'f_loop.c'],
      ['libavfilter', 'f_metadata.c'],
      ['libavfilter', 'formats.c'],
      ['libavfilter', 'f_perms.c'],
      ['libavfilter', 'framepool.c'],
      ['libavfilter', 'framequeue.c'],
      ['libavfilter', 'framesync.c'],
      ['libavfilter', 'f_realtime.c'],
      ['libavfilter', 'f_reverse.c'],
      ['libavfilter', 'f_select.c'],
      ['libavfilter', 'f_sendcmd.c'],
      ['libavfilter', 'f_sidedata.c'],
      ['libavfilter', 'f_streamselect.c'],
      ['libavfilter', 'generate_wave_table.c'],
      ['libavfilter', 'graphdump.c'],
      ['libavfilter', 'graphparser.c'],
      ['libavfilter', 'lavfutils.c'],
      ['libavfilter', 'lswsutils.c'],
      ['libavfilter', 'motion_estimation.c'],
      ['libavfilter', 'scale_eval.c'],
      ['libavfilter', 'scene_sad.c'],
      ['libavfilter', 'setpts.c'],
      ['libavfilter', 'settb.c'],
      ['libavfilter', 'split.c'],
      ['libavfilter', 'src_movie.c'],
      ['libavfilter', 'transform.c'],
      ['libavfilter', 'trim.c'],
      ['libavfilter', 'vaf_spectrumsynth.c'],
      ['libavfilter', 'vf_addroi.c'],
      ['libavfilter', 'vf_alphamerge.c'],
      ['libavfilter', 'vf_amplify.c'],
      ['libavfilter', 'vf_aspect.c'],
      ['libavfilter', 'vf_atadenoise.c'],
      ['libavfilter', 'vf_avgblur.c'],
      ['libavfilter', 'vf_bbox.c'],
      ['libavfilter', 'vf_bilateral.c'],
      ['libavfilter', 'vf_bitplanenoise.c'],
      ['libavfilter', 'vf_blackdetect.c'],
      ['libavfilter', 'vf_blend.c'],
      ['libavfilter', 'vf_bm3d.c'],
      ['libavfilter', 'vf_bwdif.c'],
      ['libavfilter', 'vf_cas.c'],
      ['libavfilter', 'vf_chromakey.c'],
      ['libavfilter', 'vf_chromashift.c'],
      ['libavfilter', 'vf_ciescope.c'],
      ['libavfilter', 'vf_codecview.c'],
      ['libavfilter', 'vf_colorbalance.c'],
      ['libavfilter', 'vf_colorchannelmixer.c'],
      ['libavfilter', 'vf_colorconstancy.c'],
      ['libavfilter', 'vf_colorkey.c'],
      ['libavfilter', 'vf_colorlevels.c'],
      ['libavfilter', 'vf_colorspace.c'],
      ['libavfilter', 'vf_convolution.c'],
      ['libavfilter', 'vf_convolve.c'],
      ['libavfilter', 'vf_copy.c'],
      ['libavfilter', 'vf_crop.c'],
      ['libavfilter', 'vf_curves.c'],
      ['libavfilter', 'vf_datascope.c'],
      ['libavfilter', 'vf_dblur.c'],
      ['libavfilter', 'vf_dctdnoiz.c'],
      ['libavfilter', 'vf_deband.c'],
      ['libavfilter', 'vf_deblock.c'],
      ['libavfilter', 'vf_decimate.c'],
      ['libavfilter', 'vf_dedot.c'],
      ['libavfilter', 'vf_deflicker.c'],
      ['libavfilter', 'vf_dejudder.c'],
      ['libavfilter', 'vf_derain.c'],
      ['libavfilter', 'vf_deshake.c'],
      ['libavfilter', 'vf_despill.c'],
      ['libavfilter', 'vf_detelecine.c'],
      ['libavfilter', 'vf_displace.c'],
      ['libavfilter', 'vf_dnn_processing.c'],
      ['libavfilter', 'vf_drawbox.c'],
      ['libavfilter', 'vf_edgedetect.c'],
      ['libavfilter', 'vf_elbg.c'],
      ['libavfilter', 'vf_entropy.c'],
      ['libavfilter', 'vf_extractplanes.c'],
      ['libavfilter', 'vf_fade.c'],
      ['libavfilter', 'vf_fftdnoiz.c'],
      ['libavfilter', 'vf_fftfilt.c'],
      ['libavfilter', 'vf_fieldhint.c'],
      ['libavfilter', 'vf_fieldmatch.c'],
      ['libavfilter', 'vf_field.c'],
      ['libavfilter', 'vf_fieldorder.c'],
      ['libavfilter', 'vf_fillborders.c'],
      ['libavfilter', 'vf_floodfill.c'],
      ['libavfilter', 'vf_format.c'],
      ['libavfilter', 'vf_fps.c'],
      ['libavfilter', 'vf_framepack.c'],
      ['libavfilter', 'vf_framerate.c'],
      ['libavfilter', 'vf_framestep.c'],
      ['libavfilter', 'vf_freezedetect.c'],
      ['libavfilter', 'vf_freezeframes.c'],
      ['libavfilter', 'vf_gblur.c'],
      ['libavfilter', 'vf_geq.c'],
      ['libavfilter', 'vf_gradfun.c'],
      ['libavfilter', 'vf_hflip.c'],
      ['libavfilter', 'vf_histogram.c'],
      ['libavfilter', 'vf_hqx.c'],
      ['libavfilter', 'vf_hue.c'],
      ['libavfilter', 'vf_hwdownload.c'],
      ['libavfilter', 'vf_hwmap.c'],
      ['libavfilter', 'vf_hwupload.c'],
      ['libavfilter', 'vf_hysteresis.c'],
      ['libavfilter', 'vf_idet.c'],
      ['libavfilter', 'vf_il.c'],
      ['libavfilter', 'vf_lagfun.c'],
      ['libavfilter', 'vf_lenscorrection.c'],
      ['libavfilter', 'vf_limiter.c'],
      ['libavfilter', 'vf_lumakey.c'],
      ['libavfilter', 'vf_lut2.c'],
      ['libavfilter', 'vf_lut3d.c'],
      ['libavfilter', 'vf_lut.c'],
      ['libavfilter', 'vf_maskedclamp.c'],
      ['libavfilter', 'vf_maskedmerge.c'],
      ['libavfilter', 'vf_maskedminmax.c'],
      ['libavfilter', 'vf_maskedthreshold.c'],
      ['libavfilter', 'vf_maskfun.c'],
      ['libavfilter', 'vf_median.c'],
      ['libavfilter', 'vf_mergeplanes.c'],
      ['libavfilter', 'vf_mestimate.c'],
      ['libavfilter', 'vf_midequalizer.c'],
      ['libavfilter', 'vf_minterpolate.c'],
      ['libavfilter', 'vf_mix.c'],
      ['libavfilter', 'vf_neighbor.c'],
      ['libavfilter', 'vf_nlmeans.c'],
      ['libavfilter', 'vf_noise.c'],
      ['libavfilter', 'vf_normalize.c'],
      ['libavfilter', 'vf_null.c'],
      ['libavfilter', 'vf_overlay.c'],
      ['libavfilter', 'vf_pad.c'],
      ['libavfilter', 'vf_palettegen.c'],
      ['libavfilter', 'vf_paletteuse.c'],
      ['libavfilter', 'vf_photosensitivity.c'],
      ['libavfilter', 'vf_pixdesctest.c'],
      ['libavfilter', 'vf_premultiply.c'],
      ['libavfilter', 'vf_pseudocolor.c'],
      ['libavfilter', 'vf_psnr.c'],
      ['libavfilter', 'vf_qp.c'],
      ['libavfilter', 'vf_random.c'],
      ['libavfilter', 'vf_readeia608.c'],
      ['libavfilter', 'vf_readvitc.c'],
      ['libavfilter', 'vf_remap.c'],
      ['libavfilter', 'vf_removegrain.c'],
      ['libavfilter', 'vf_removelogo.c'],
      ['libavfilter', 'vf_rotate.c'],
      ['libavfilter', 'vf_scale.c'],
      ['libavfilter', 'vf_scdet.c'],
      ['libavfilter', 'vf_scroll.c'],
      ['libavfilter', 'vf_selectivecolor.c'],
      ['libavfilter', 'vf_separatefields.c'],
      ['libavfilter', 'vf_setparams.c'],
      ['libavfilter', 'vf_showinfo.c'],
      ['libavfilter', 'vf_showpalette.c'],
      ['libavfilter', 'vf_shuffleframes.c'],
      ['libavfilter', 'vf_shuffleplanes.c'],
      ['libavfilter', 'vf_signalstats.c'],
      ['libavfilter', 'vf_sr.c'],
      ['libavfilter', 'vf_ssim.c'],
      ['libavfilter', 'vf_stack.c'],
      ['libavfilter', 'vf_swaprect.c'],
      ['libavfilter', 'vf_swapuv.c'],
      ['libavfilter', 'vf_telecine.c'],
      ['libavfilter', 'vf_threshold.c'],
      ['libavfilter', 'vf_thumbnail.c'],
      ['libavfilter', 'vf_tile.c'],
      ['libavfilter', 'vf_tonemap.c'],
      ['libavfilter', 'vf_tpad.c'],
      ['libavfilter', 'vf_transpose.c'],
      ['libavfilter', 'vf_unsharp.c'],
      ['libavfilter', 'vf_untile.c'],
      ['libavfilter', 'vf_v360.c'],
      ['libavfilter', 'vf_vectorscope.c'],
      ['libavfilter', 'vf_vflip.c'],
      ['libavfilter', 'vf_vfrdet.c'],
      ['libavfilter', 'vf_vibrance.c'],
      ['libavfilter', 'vf_vignette.c'],
      ['libavfilter', 'vf_vmafmotion.c'],
      ['libavfilter', 'vf_w3fdif.c'],
      ['libavfilter', 'vf_waveform.c'],
      ['libavfilter', 'vf_weave.c'],
      ['libavfilter', 'vf_xbr.c'],
      ['libavfilter', 'vf_xfade.c'],
      ['libavfilter', 'vf_xmedian.c'],
      ['libavfilter', 'vf_yadif.c'],
      ['libavfilter', 'vf_yaepblur.c'],
      ['libavfilter', 'vf_zoompan.c'],
      ['libavfilter', 'video.c'],
      ['libavfilter', 'vsink_nullsink.c'],
      ['libavfilter', 'vsrc_cellauto.c'],
      ['libavfilter', 'vsrc_gradients.c'],
      ['libavfilter', 'vsrc_life.c'],
      ['libavfilter', 'vsrc_mandelbrot.c'],
      ['libavfilter', 'vsrc_sierpinski.c'],
      ['libavfilter', 'vsrc_testsrc.c'],
      ['libavfilter', 'yadif_common.c'],
      ['libavfilter/x86', 'af_afir_init.c'],
      ['libavfilter/x86', 'af_anlmdn_init.c'],
      ['libavfilter/x86', 'af_volume_init.c'],
      ['libavfilter/x86', 'avf_showcqt_init.c'],
      ['libavfilter/x86', 'colorspacedsp_init.c'],
      ['libavfilter/x86', 'scene_sad_init.c'],
      ['libavfilter/x86', 'vf_atadenoise_init.c'],
      ['libavfilter/x86', 'vf_blend_init.c'],
      ['libavfilter/x86', 'vf_bwdif_init.c'],
      ['libavfilter/x86', 'vf_convolution_init.c'],
      ['libavfilter/x86', 'vf_framerate_init.c'],
      ['libavfilter/x86', 'vf_gblur_init.c'],
      ['libavfilter/x86', 'vf_gradfun_init.c'],
      ['libavfilter/x86', 'vf_hflip_init.c'],
      ['libavfilter/x86', 'vf_idet_init.c'],
      ['libavfilter/x86', 'vf_limiter_init.c'],
      ['libavfilter/x86', 'vf_maskedclamp_init.c'],
      ['libavfilter/x86', 'vf_maskedmerge_init.c'],
      ['libavfilter/x86', 'vf_noise.c'],
      ['libavfilter/x86', 'vf_overlay_init.c'],
      ['libavfilter/x86', 'vf_psnr_init.c'],
      ['libavfilter/x86', 'vf_removegrain_init.c'],
      ['libavfilter/x86', 'vf_ssim_init.c'],
      ['libavfilter/x86', 'vf_threshold_init.c'],
      ['libavfilter/x86', 'vf_transpose_init.c'],
      ['libavfilter/x86', 'vf_v360_init.c'],
      ['libavfilter/x86', 'vf_w3fdif_init.c'],
      ['libavfilter/x86', 'vf_yadif_init.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_conv2d.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_depth2space.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_mathbinary.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_mathunary.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_maximum.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layer_pad.c'],
      ['libavfilter/dnn', 'dnn_backend_native_layers.c'],
      ['libavfilter/dnn', 'dnn_backend_native.c'],
      ['libavfilter/dnn', 'dnn_interface.c'],
      ['libavdevice', 'alldevices.c'],
      ['libavdevice', 'lavfi.c'],
      ['libavdevice', 'utils.c'],
      ['libavdevice', 'avdevice.c'],
      ['libswscale', 'alphablend.c'],
      ['libswscale', 'rgb2rgb.c'],
      ['libswscale', 'gamma.c'],
      ['libswscale', 'slice.c'],
      ['libswscale', 'hscale_fast_bilinear.c'],
      ['libswscale', 'swscale.c'],
      ['libswscale', 'hscale.c'],
      ['libswscale', 'swscale_unscaled.c'],
      ['libswscale', 'input.c'],
      ['libswscale', 'utils.c'],
      ['libswscale', 'options.c'],
      ['libswscale', 'vscale.c'],
      ['libswscale', 'output.c'],
      ['libswscale', 'yuv2rgb.c'],
      ['libswscale/x86', 'hscale_fast_bilinear_simd.c'],
      ['libswscale/x86', 'swscale.c'],
      ['libswscale/x86', 'rgb2rgb.c'],
      ['libswscale/x86', 'yuv2rgb.c'],
      ['libswresample', 'audioconvert.c'],
      ['libswresample', 'resample_dsp.c'],
      ['libswresample', 'dither.c'],
      ['libswresample', 'resample.c'],
      ['libswresample', 'options.c'],
      ['libswresample', 'swresample_frame.c'],
      ['libswresample', 'rematrix.c'],
      ['libswresample', 'swresample.c'],
      ['libswresample/x86', 'audio_convert_init.c'],
      ['libswresample/x86', 'resample_init.c'],
      ['libswresample/x86', 'rematrix_init.c'],
      ['fftools', 'ffmpeg_filter.c'],
    ]
    if settings.USE_PTHREADS:
        srcs += [
            ['libavfilter', 'pthread.c'], # Only when pthreads are used - conflicts with avfiltegraph.o because of ff_graph_thread_init function
            ['libavcodec', 'frame_thread_encoder.c'],
            ['libavcodec', 'pthread_frame.c'],
            ['libavcodec', 'pthread.c'],
            ['libavcodec', 'pthread_slice.c'],
            ['libavformat', 'async.c'],
            ['libavformat', 'fifo.c'],
        ]
    else:
        srcs += [
            ['libavdevice', 'sdl2.c'],
        ]


    source_path = os.path.join(ports.get_dir(), 'ffmpeg', 'ffmpeg-' + TAG)
    dest_path = os.path.join(ports.get_build_dir(), 'ffmpeg', ('-mt' if settings.USE_PTHREADS else ''))

    open(os.path.join(source_path, 'libavutil', 'avconfig.h'), 'w').write(avconfig_h)
    open(os.path.join(source_path, 'libavutil', 'ffversion.h'), 'w').write(ffversion_h)
    open(os.path.join(source_path, 'libavcodec', 'codec_list.c'), 'w').write(codec_list_c)
    open(os.path.join(source_path, 'libavcodec', 'bsf_list.c'), 'w').write(bsf_list_c)
    open(os.path.join(source_path, 'libavcodec', 'parser_list.c'), 'w').write(parser_list_c)
    open(os.path.join(source_path, 'libavformat', 'muxer_list.c'), 'w').write(muxer_list_c_pthreads  if settings.USE_PTHREADS else muxer_list_c)
    open(os.path.join(source_path, 'libavformat', 'demuxer_list.c'), 'w').write(demuxer_list_c)
    open(os.path.join(source_path, 'libavformat', 'protocol_list.c'), 'w').write(protocol_list_c_pthread  if settings.USE_PTHREADS else protocol_list_c )
    open(os.path.join(source_path, 'libavfilter', 'filter_list.c'), 'w').write(filter_list_c)
    open(os.path.join(source_path, 'libavdevice', 'outdev_list.c'), 'w').write(outdev_list_c)
    open(os.path.join(source_path, 'libavdevice', 'indev_list.c'), 'w').write(indev_list_c)
    open(os.path.join(source_path, 'config.h'), 'w').write(ffmpeg_config_h_pthread  if settings.USE_PTHREADS else ffmpeg_config_h)



    dest_include_path = os.path.join(dest_path, 'ffmpeg')
    shared.safe_ensure_dirs(dest_include_path);
    export_include_dirs = [
      [ 'libavcodec' ],
      [ 'libavcodec', 'arm' ],
      [ 'libavcodec', 'mips' ],
      [ 'libavfilter' ],
      [ 'libavfilter', 'dnn' ],
      [ 'libavresample' ],
      [ 'libpostproc' ],
      [ 'libswscale' ],
      [ 'libavdevice' ],
      [ 'libavformat' ],
      [ 'libavutil' ],
      [ 'libswresample' ],
    ]
    for include_path in export_include_dirs:
      #Copy headers here
      export_include_dir = os.path.join('ffmpeg', *include_path)
      final_export_include_dir = os.path.join(source_path, *include_path)
      ports.install_headers(final_export_include_dir, target=export_include_dir)

    commands = []
    o_s = []
    for src_path in srcs:
      src = os.path.join(*src_path)
      src_base, c_ext = os.path.splitext(src)
      o_file = os.path.join(dest_path, src_base + '.o')
      shared.safe_ensure_dirs(os.path.dirname(o_file))
      command = [shared.PYTHON, shared.EMCC,
                 '-c', os.path.join(source_path, src),
                 '-o', o_file,
                 '-I' + source_path,
                 '-D_ISOC99_SOURCE',
                 '-D_FILE_OFFSET_BITS=64',
                 '-D_LARGEFILE_SOURCE',
                 '-D_POSIX_C_SOURCE=200112',
                 '-D_XOPEN_SOURCE=600',
                 '-DPIC',
                 '-DHAVE_AV_CONFIG_H',
                 '-std=c11',
                 '-fomit-frame-pointer',
                 '-fPIC',
                 '-g',
                 '-Wdeclaration-after-statement',
                 '-Wall',
                 '-Wdisabled-optimization',
                 '-Wpointer-arith',
                 '-Wredundant-decls',
                 '-Wwrite-strings',
                 '-Wtype-limits',
                 '-Wundef',
                 '-Wmissing-prototypes',
                 '-Wno-pointer-to-int-cast',
                 '-Wno-strict-prototypes',
                 '-Wempty-body',
                 '-Wno-parentheses',
                 '-Wno-switch',
                 '-Wno-format-zero-length',
                 '-Wno-pointer-sign',
                 '-Wno-unused-const-variable',
                 '-Wno-char-subscripts',
                 '-Wno-implicit-function-declaration',
                 '-Wno-deprecated-declarations',
                 '-Wno-unknown-attributes',
                 '-Wno-unused-function',
                 '-Werror=missing-prototypes',
                 '-Werror=return-type',
                 '-Os',
                 '-fno-math-errno',
                 '-fno-signed-zeros',
                 '-s', 'USE_SDL=2'] # Defined in global settings, but has to be defined here as well...
                 #'-Wno-bool-operation', # Not supported
      if settings.USE_PTHREADS:
          command += [
                      '-DBUILDING_avutil',
                      '-pthread'
                      ]
      else:
          command += ['-DBUILDING_avcodec']

      commands.append(command)
      o_s.append(o_file)
    ports.run_commands(commands)

    final = os.path.join(dest_path, libname)
    #shared.safe_ensure_dirs(os.path.dirname(final))
    ports.create_lib(final, o_s)
    return final

  return [shared.Cache.get(libname, create, what='port')]


def clear(ports, shared):
  shared.Cache.erase_file(get_libname(ports, False))
  shared.Cache.erase_file(get_libname(ports, True))


def process_dependencies(settings):
  if settings.USE_FFMPEG == 1:
    settings.USE_SDL = 2


def process_args(ports, args, settings, shared):
  if settings.USE_FFMPEG == 1:
    get(ports, settings, shared)
    args += ['-I' + os.path.join(ports.get_include_dir(), 'ffmpeg')]
  return args


def show():
  return 'ffmpeg (USE_FFMPEG=1; GPL license )'


avconfig_h = '''/* Generated by ffmpeg configure */
#ifndef AVUTIL_AVCONFIG_H
#define AVUTIL_AVCONFIG_H
#define AV_HAVE_BIGENDIAN 0
#define AV_HAVE_FAST_UNALIGNED 1
#endif /* AVUTIL_AVCONFIG_H */
'''

ffversion_h = '''
/* Automatically generated by version.sh, do not manually edit! */
#ifndef AVUTIL_FFVERSION_H
#define AVUTIL_FFVERSION_H
#define FFMPEG_VERSION "n4.3"
#endif /* AVUTIL_FFVERSION_H */
'''

codec_list_c = '''/* Not available by default, generated by configure */
static const AVCodec * const codec_list[] = {
    &ff_a64multi_encoder,
    &ff_a64multi5_encoder,
    &ff_alias_pix_encoder,
    &ff_amv_encoder,
    &ff_asv1_encoder,
    &ff_asv2_encoder,
    &ff_avrp_encoder,
    &ff_avui_encoder,
    &ff_ayuv_encoder,
    &ff_bmp_encoder,
    &ff_cinepak_encoder,
    &ff_cljr_encoder,
    &ff_comfortnoise_encoder,
    &ff_dnxhd_encoder,
    &ff_dpx_encoder,
    &ff_dvvideo_encoder,
    &ff_ffv1_encoder,
    &ff_ffvhuff_encoder,
    &ff_fits_encoder,
    &ff_flv_encoder,
    &ff_gif_encoder,
    &ff_h261_encoder,
    &ff_h263_encoder,
    &ff_h263p_encoder,
    &ff_huffyuv_encoder,
    &ff_jpeg2000_encoder,
    &ff_jpegls_encoder,
    &ff_ljpeg_encoder,
    &ff_magicyuv_encoder,
    &ff_mjpeg_encoder,
    &ff_mpeg1video_encoder,
    &ff_mpeg2video_encoder,
    &ff_mpeg4_encoder,
    &ff_msmpeg4v2_encoder,
    &ff_msmpeg4v3_encoder,
    &ff_msvideo1_encoder,
    &ff_pam_encoder,
    &ff_pbm_encoder,
    &ff_pcx_encoder,
    &ff_pgm_encoder,
    &ff_pgmyuv_encoder,
    &ff_ppm_encoder,
    &ff_prores_encoder,
    &ff_prores_aw_encoder,
    &ff_prores_ks_encoder,
    &ff_qtrle_encoder,
    &ff_r10k_encoder,
    &ff_r210_encoder,
    &ff_rawvideo_encoder,
    &ff_roq_encoder,
    &ff_rv10_encoder,
    &ff_rv20_encoder,
    &ff_s302m_encoder,
    &ff_sgi_encoder,
    &ff_snow_encoder,
    &ff_sunrast_encoder,
    &ff_svq1_encoder,
    &ff_targa_encoder,
    &ff_tiff_encoder,
    &ff_utvideo_encoder,
    &ff_v210_encoder,
    &ff_v308_encoder,
    &ff_v408_encoder,
    &ff_v410_encoder,
    &ff_vc2_encoder,
    &ff_wrapped_avframe_encoder,
    &ff_wmv1_encoder,
    &ff_wmv2_encoder,
    &ff_xbm_encoder,
    &ff_xface_encoder,
    &ff_xwd_encoder,
    &ff_y41p_encoder,
    &ff_yuv4_encoder,
    &ff_aac_encoder,
    &ff_ac3_encoder,
    &ff_ac3_fixed_encoder,
    &ff_alac_encoder,
    &ff_aptx_encoder,
    &ff_aptx_hd_encoder,
    &ff_dca_encoder,
    &ff_eac3_encoder,
    &ff_flac_encoder,
    &ff_g723_1_encoder,
    &ff_mlp_encoder,
    &ff_mp2_encoder,
    &ff_mp2fixed_encoder,
    &ff_nellymoser_encoder,
    &ff_opus_encoder,
    &ff_ra_144_encoder,
    &ff_sbc_encoder,
    &ff_sonic_encoder,
    &ff_sonic_ls_encoder,
    &ff_truehd_encoder,
    &ff_tta_encoder,
    &ff_vorbis_encoder,
    &ff_wavpack_encoder,
    &ff_wmav1_encoder,
    &ff_wmav2_encoder,
    &ff_pcm_alaw_encoder,
    &ff_pcm_dvd_encoder,
    &ff_pcm_f32be_encoder,
    &ff_pcm_f32le_encoder,
    &ff_pcm_f64be_encoder,
    &ff_pcm_f64le_encoder,
    &ff_pcm_mulaw_encoder,
    &ff_pcm_s8_encoder,
    &ff_pcm_s8_planar_encoder,
    &ff_pcm_s16be_encoder,
    &ff_pcm_s16be_planar_encoder,
    &ff_pcm_s16le_encoder,
    &ff_pcm_s16le_planar_encoder,
    &ff_pcm_s24be_encoder,
    &ff_pcm_s24daud_encoder,
    &ff_pcm_s24le_encoder,
    &ff_pcm_s24le_planar_encoder,
    &ff_pcm_s32be_encoder,
    &ff_pcm_s32le_encoder,
    &ff_pcm_s32le_planar_encoder,
    &ff_pcm_s64be_encoder,
    &ff_pcm_s64le_encoder,
    &ff_pcm_u8_encoder,
    &ff_pcm_u16be_encoder,
    &ff_pcm_u16le_encoder,
    &ff_pcm_u24be_encoder,
    &ff_pcm_u24le_encoder,
    &ff_pcm_u32be_encoder,
    &ff_pcm_u32le_encoder,
    &ff_pcm_vidc_encoder,
    &ff_roq_dpcm_encoder,
    &ff_adpcm_adx_encoder,
    &ff_adpcm_g722_encoder,
    &ff_adpcm_g726_encoder,
    &ff_adpcm_g726le_encoder,
    &ff_adpcm_ima_qt_encoder,
    &ff_adpcm_ima_ssi_encoder,
    &ff_adpcm_ima_wav_encoder,
    &ff_adpcm_ms_encoder,
    &ff_adpcm_swf_encoder,
    &ff_adpcm_yamaha_encoder,
    &ff_ssa_encoder,
    &ff_ass_encoder,
    &ff_dvbsub_encoder,
    &ff_dvdsub_encoder,
    &ff_movtext_encoder,
    &ff_srt_encoder,
    &ff_subrip_encoder,
    &ff_text_encoder,
    &ff_webvtt_encoder,
    &ff_xsub_encoder,
    &ff_aasc_decoder,
    &ff_aic_decoder,
    &ff_alias_pix_decoder,
    &ff_agm_decoder,
    &ff_amv_decoder,
    &ff_anm_decoder,
    &ff_ansi_decoder,
    &ff_arbc_decoder,
    &ff_asv1_decoder,
    &ff_asv2_decoder,
    &ff_aura_decoder,
    &ff_aura2_decoder,
    &ff_avrp_decoder,
    &ff_avrn_decoder,
    &ff_avs_decoder,
    &ff_avui_decoder,
    &ff_ayuv_decoder,
    &ff_bethsoftvid_decoder,
    &ff_bfi_decoder,
    &ff_bink_decoder,
    &ff_bitpacked_decoder,
    &ff_bmp_decoder,
    &ff_bmv_video_decoder,
    &ff_brender_pix_decoder,
    &ff_c93_decoder,
    &ff_cavs_decoder,
    &ff_cdgraphics_decoder,
    &ff_cdtoons_decoder,
    &ff_cdxl_decoder,
    &ff_cfhd_decoder,
    &ff_cinepak_decoder,
    &ff_clearvideo_decoder,
    &ff_cljr_decoder,
    &ff_cllc_decoder,
    &ff_comfortnoise_decoder,
    &ff_cpia_decoder,
    &ff_cscd_decoder,
    &ff_cyuv_decoder,
    &ff_dds_decoder,
    &ff_dfa_decoder,
    &ff_dirac_decoder,
    &ff_dnxhd_decoder,
    &ff_dpx_decoder,
    &ff_dsicinvideo_decoder,
    &ff_dvaudio_decoder,
    &ff_dvvideo_decoder,
    &ff_dxtory_decoder,
    &ff_dxv_decoder,
    &ff_eacmv_decoder,
    &ff_eamad_decoder,
    &ff_eatgq_decoder,
    &ff_eatgv_decoder,
    &ff_eatqi_decoder,
    &ff_eightbps_decoder,
    &ff_eightsvx_exp_decoder,
    &ff_eightsvx_fib_decoder,
    &ff_escape124_decoder,
    &ff_escape130_decoder,
    &ff_ffv1_decoder,
    &ff_ffvhuff_decoder,
    &ff_fic_decoder,
    &ff_fits_decoder,
    &ff_flic_decoder,
    &ff_flv_decoder,
    &ff_fmvc_decoder,
    &ff_fourxm_decoder,
    &ff_fraps_decoder,
    &ff_frwu_decoder,
    &ff_gdv_decoder,
    &ff_gif_decoder,
    &ff_h261_decoder,
    &ff_h263_decoder,
    &ff_h263i_decoder,
    &ff_h263p_decoder,
    &ff_h264_decoder,
    &ff_hap_decoder,
    &ff_hevc_decoder,
    &ff_hnm4_video_decoder,
    &ff_hq_hqa_decoder,
    &ff_hqx_decoder,
    &ff_huffyuv_decoder,
    &ff_hymt_decoder,
    &ff_idcin_decoder,
    &ff_iff_ilbm_decoder,
    &ff_imm4_decoder,
    &ff_imm5_decoder,
    &ff_indeo2_decoder,
    &ff_indeo3_decoder,
    &ff_indeo4_decoder,
    &ff_indeo5_decoder,
    &ff_interplay_video_decoder,
    &ff_jpeg2000_decoder,
    &ff_jpegls_decoder,
    &ff_jv_decoder,
    &ff_kgv1_decoder,
    &ff_kmvc_decoder,
    &ff_lagarith_decoder,
    &ff_loco_decoder,
    &ff_m101_decoder,
    &ff_magicyuv_decoder,
    &ff_mdec_decoder,
    &ff_mimic_decoder,
    &ff_mjpeg_decoder,
    &ff_mjpegb_decoder,
    &ff_mmvideo_decoder,
    &ff_motionpixels_decoder,
    &ff_mpeg1video_decoder,
    &ff_mpeg2video_decoder,
    &ff_mpeg4_decoder,
    &ff_mpegvideo_decoder,
    &ff_msa1_decoder,
    &ff_msmpeg4v1_decoder,
    &ff_msmpeg4v2_decoder,
    &ff_msmpeg4v3_decoder,
    &ff_msrle_decoder,
    &ff_mss1_decoder,
    &ff_mss2_decoder,
    &ff_msvideo1_decoder,
    &ff_mszh_decoder,
    &ff_mts2_decoder,
    &ff_mv30_decoder,
    &ff_mvc1_decoder,
    &ff_mvc2_decoder,
    &ff_mvdv_decoder,
    &ff_mxpeg_decoder,
    &ff_notchlc_decoder,
    &ff_nuv_decoder,
    &ff_paf_video_decoder,
    &ff_pam_decoder,
    &ff_pbm_decoder,
    &ff_pcx_decoder,
    &ff_pfm_decoder,
    &ff_pgm_decoder,
    &ff_pgmyuv_decoder,
    &ff_pictor_decoder,
    &ff_pixlet_decoder,
    &ff_ppm_decoder,
    &ff_prores_decoder,
    &ff_prosumer_decoder,
    &ff_psd_decoder,
    &ff_ptx_decoder,
    &ff_qdraw_decoder,
    &ff_qpeg_decoder,
    &ff_qtrle_decoder,
    &ff_r10k_decoder,
    &ff_r210_decoder,
    &ff_rawvideo_decoder,
    &ff_rl2_decoder,
    &ff_roq_decoder,
    &ff_rpza_decoder,
    &ff_rv10_decoder,
    &ff_rv20_decoder,
    &ff_rv30_decoder,
    &ff_rv40_decoder,
    &ff_s302m_decoder,
    &ff_sanm_decoder,
    &ff_scpr_decoder,
    &ff_sgi_decoder,
    &ff_sgirle_decoder,
    &ff_sheervideo_decoder,
    &ff_smacker_decoder,
    &ff_smc_decoder,
    &ff_smvjpeg_decoder,
    &ff_snow_decoder,
    &ff_sp5x_decoder,
    &ff_speedhq_decoder,
    &ff_sunrast_decoder,
    &ff_svq1_decoder,
    &ff_svq3_decoder,
    &ff_targa_decoder,
    &ff_targa_y216_decoder,
    &ff_theora_decoder,
    &ff_thp_decoder,
    &ff_tiertexseqvideo_decoder,
    &ff_tiff_decoder,
    &ff_tmv_decoder,
    &ff_truemotion1_decoder,
    &ff_truemotion2_decoder,
    &ff_truemotion2rt_decoder,
    &ff_tscc2_decoder,
    &ff_txd_decoder,
    &ff_ulti_decoder,
    &ff_utvideo_decoder,
    &ff_v210_decoder,
    &ff_v210x_decoder,
    &ff_v308_decoder,
    &ff_v408_decoder,
    &ff_v410_decoder,
    &ff_vb_decoder,
    &ff_vble_decoder,
    &ff_vc1_decoder,
    &ff_vc1image_decoder,
    &ff_vcr1_decoder,
    &ff_vmdvideo_decoder,
    &ff_vmnc_decoder,
    &ff_vp3_decoder,
    &ff_vp4_decoder,
    &ff_vp5_decoder,
    &ff_vp6_decoder,
    &ff_vp6a_decoder,
    &ff_vp6f_decoder,
    &ff_vp7_decoder,
    &ff_vp8_decoder,
    &ff_vp9_decoder,
    &ff_vqa_decoder,
    &ff_webp_decoder,
    &ff_wrapped_avframe_decoder,
    &ff_wmv1_decoder,
    &ff_wmv2_decoder,
    &ff_wmv3_decoder,
    &ff_wmv3image_decoder,
    &ff_wnv1_decoder,
    &ff_xan_wc3_decoder,
    &ff_xan_wc4_decoder,
    &ff_xbm_decoder,
    &ff_xface_decoder,
    &ff_xl_decoder,
    &ff_xpm_decoder,
    &ff_xwd_decoder,
    &ff_y41p_decoder,
    &ff_ylc_decoder,
    &ff_yop_decoder,
    &ff_yuv4_decoder,
    &ff_zero12v_decoder,
    &ff_aac_decoder,
    &ff_aac_fixed_decoder,
    &ff_aac_latm_decoder,
    &ff_ac3_decoder,
    &ff_ac3_fixed_decoder,
    &ff_acelp_kelvin_decoder,
    &ff_alac_decoder,
    &ff_als_decoder,
    &ff_amrnb_decoder,
    &ff_amrwb_decoder,
    &ff_ape_decoder,
    &ff_aptx_decoder,
    &ff_aptx_hd_decoder,
    &ff_atrac1_decoder,
    &ff_atrac3_decoder,
    &ff_atrac3al_decoder,
    &ff_atrac3p_decoder,
    &ff_atrac3pal_decoder,
    &ff_atrac9_decoder,
    &ff_binkaudio_dct_decoder,
    &ff_binkaudio_rdft_decoder,
    &ff_bmv_audio_decoder,
    &ff_cook_decoder,
    &ff_dca_decoder,
    &ff_dolby_e_decoder,
    &ff_dsd_lsbf_decoder,
    &ff_dsd_msbf_decoder,
    &ff_dsd_lsbf_planar_decoder,
    &ff_dsd_msbf_planar_decoder,
    &ff_dsicinaudio_decoder,
    &ff_dss_sp_decoder,
    &ff_dst_decoder,
    &ff_eac3_decoder,
    &ff_evrc_decoder,
    &ff_ffwavesynth_decoder,
    &ff_flac_decoder,
    &ff_g723_1_decoder,
    &ff_g729_decoder,
    &ff_gsm_decoder,
    &ff_gsm_ms_decoder,
    &ff_hca_decoder,
    &ff_hcom_decoder,
    &ff_iac_decoder,
    &ff_ilbc_decoder,
    &ff_imc_decoder,
    &ff_interplay_acm_decoder,
    &ff_mace3_decoder,
    &ff_mace6_decoder,
    &ff_metasound_decoder,
    &ff_mlp_decoder,
    &ff_mp1_decoder,
    &ff_mp1float_decoder,
    &ff_mp2_decoder,
    &ff_mp2float_decoder,
    &ff_mp3float_decoder,
    &ff_mp3_decoder,
    &ff_mp3adufloat_decoder,
    &ff_mp3adu_decoder,
    &ff_mp3on4float_decoder,
    &ff_mp3on4_decoder,
    &ff_mpc7_decoder,
    &ff_mpc8_decoder,
    &ff_nellymoser_decoder,
    &ff_on2avc_decoder,
    &ff_opus_decoder,
    &ff_paf_audio_decoder,
    &ff_qcelp_decoder,
    &ff_qdm2_decoder,
    &ff_qdmc_decoder,
    &ff_ra_144_decoder,
    &ff_ra_288_decoder,
    &ff_ralf_decoder,
    &ff_sbc_decoder,
    &ff_shorten_decoder,
    &ff_sipr_decoder,
    &ff_siren_decoder,
    &ff_smackaud_decoder,
    &ff_sonic_decoder,
    &ff_tak_decoder,
    &ff_truehd_decoder,
    &ff_truespeech_decoder,
    &ff_tta_decoder,
    &ff_twinvq_decoder,
    &ff_vmdaudio_decoder,
    &ff_vorbis_decoder,
    &ff_wavpack_decoder,
    &ff_wmalossless_decoder,
    &ff_wmapro_decoder,
    &ff_wmav1_decoder,
    &ff_wmav2_decoder,
    &ff_wmavoice_decoder,
    &ff_ws_snd1_decoder,
    &ff_xma1_decoder,
    &ff_xma2_decoder,
    &ff_pcm_alaw_decoder,
    &ff_pcm_bluray_decoder,
    &ff_pcm_dvd_decoder,
    &ff_pcm_f16le_decoder,
    &ff_pcm_f24le_decoder,
    &ff_pcm_f32be_decoder,
    &ff_pcm_f32le_decoder,
    &ff_pcm_f64be_decoder,
    &ff_pcm_f64le_decoder,
    &ff_pcm_lxf_decoder,
    &ff_pcm_mulaw_decoder,
    &ff_pcm_s8_decoder,
    &ff_pcm_s8_planar_decoder,
    &ff_pcm_s16be_decoder,
    &ff_pcm_s16be_planar_decoder,
    &ff_pcm_s16le_decoder,
    &ff_pcm_s16le_planar_decoder,
    &ff_pcm_s24be_decoder,
    &ff_pcm_s24daud_decoder,
    &ff_pcm_s24le_decoder,
    &ff_pcm_s24le_planar_decoder,
    &ff_pcm_s32be_decoder,
    &ff_pcm_s32le_decoder,
    &ff_pcm_s32le_planar_decoder,
    &ff_pcm_s64be_decoder,
    &ff_pcm_s64le_decoder,
    &ff_pcm_u8_decoder,
    &ff_pcm_u16be_decoder,
    &ff_pcm_u16le_decoder,
    &ff_pcm_u24be_decoder,
    &ff_pcm_u24le_decoder,
    &ff_pcm_u32be_decoder,
    &ff_pcm_u32le_decoder,
    &ff_pcm_vidc_decoder,
    &ff_derf_dpcm_decoder,
    &ff_gremlin_dpcm_decoder,
    &ff_interplay_dpcm_decoder,
    &ff_roq_dpcm_decoder,
    &ff_sdx2_dpcm_decoder,
    &ff_sol_dpcm_decoder,
    &ff_xan_dpcm_decoder,
    &ff_adpcm_4xm_decoder,
    &ff_adpcm_adx_decoder,
    &ff_adpcm_afc_decoder,
    &ff_adpcm_agm_decoder,
    &ff_adpcm_aica_decoder,
    &ff_adpcm_argo_decoder,
    &ff_adpcm_ct_decoder,
    &ff_adpcm_dtk_decoder,
    &ff_adpcm_ea_decoder,
    &ff_adpcm_ea_maxis_xa_decoder,
    &ff_adpcm_ea_r1_decoder,
    &ff_adpcm_ea_r2_decoder,
    &ff_adpcm_ea_r3_decoder,
    &ff_adpcm_ea_xas_decoder,
    &ff_adpcm_g722_decoder,
    &ff_adpcm_g726_decoder,
    &ff_adpcm_g726le_decoder,
    &ff_adpcm_ima_amv_decoder,
    &ff_adpcm_ima_alp_decoder,
    &ff_adpcm_ima_apc_decoder,
    &ff_adpcm_ima_apm_decoder,
    &ff_adpcm_ima_cunning_decoder,
    &ff_adpcm_ima_dat4_decoder,
    &ff_adpcm_ima_dk3_decoder,
    &ff_adpcm_ima_dk4_decoder,
    &ff_adpcm_ima_ea_eacs_decoder,
    &ff_adpcm_ima_ea_sead_decoder,
    &ff_adpcm_ima_iss_decoder,
    &ff_adpcm_ima_mtf_decoder,
    &ff_adpcm_ima_oki_decoder,
    &ff_adpcm_ima_qt_decoder,
    &ff_adpcm_ima_rad_decoder,
    &ff_adpcm_ima_ssi_decoder,
    &ff_adpcm_ima_smjpeg_decoder,
    &ff_adpcm_ima_wav_decoder,
    &ff_adpcm_ima_ws_decoder,
    &ff_adpcm_ms_decoder,
    &ff_adpcm_mtaf_decoder,
    &ff_adpcm_psx_decoder,
    &ff_adpcm_sbpro_2_decoder,
    &ff_adpcm_sbpro_3_decoder,
    &ff_adpcm_sbpro_4_decoder,
    &ff_adpcm_swf_decoder,
    &ff_adpcm_thp_decoder,
    &ff_adpcm_thp_le_decoder,
    &ff_adpcm_vima_decoder,
    &ff_adpcm_xa_decoder,
    &ff_adpcm_yamaha_decoder,
    &ff_adpcm_zork_decoder,
    &ff_ssa_decoder,
    &ff_ass_decoder,
    &ff_ccaption_decoder,
    &ff_dvbsub_decoder,
    &ff_dvdsub_decoder,
    &ff_jacosub_decoder,
    &ff_microdvd_decoder,
    &ff_movtext_decoder,
    &ff_mpl2_decoder,
    &ff_pgssub_decoder,
    &ff_pjs_decoder,
    &ff_realtext_decoder,
    &ff_sami_decoder,
    &ff_srt_decoder,
    &ff_stl_decoder,
    &ff_subrip_decoder,
    &ff_subviewer_decoder,
    &ff_subviewer1_decoder,
    &ff_text_decoder,
    &ff_vplayer_decoder,
    &ff_webvtt_decoder,
    &ff_xsub_decoder,
    &ff_bintext_decoder,
    &ff_xbin_decoder,
    &ff_idf_decoder,
    NULL };
'''

bsf_list_c = '''/* Not available by default, generated by configure */
static const AVBitStreamFilter * const bitstream_filters[] = {
    &ff_aac_adtstoasc_bsf,
    &ff_av1_frame_merge_bsf,
    &ff_av1_frame_split_bsf,
    &ff_av1_metadata_bsf,
    &ff_chomp_bsf,
    &ff_dump_extradata_bsf,
    &ff_dca_core_bsf,
    &ff_eac3_core_bsf,
    &ff_extract_extradata_bsf,
    &ff_filter_units_bsf,
    &ff_h264_metadata_bsf,
    &ff_h264_mp4toannexb_bsf,
    &ff_h264_redundant_pps_bsf,
    &ff_hapqa_extract_bsf,
    &ff_hevc_metadata_bsf,
    &ff_hevc_mp4toannexb_bsf,
    &ff_imx_dump_header_bsf,
    &ff_mjpeg2jpeg_bsf,
    &ff_mjpega_dump_header_bsf,
    &ff_mp3_header_decompress_bsf,
    &ff_mpeg2_metadata_bsf,
    &ff_mpeg4_unpack_bframes_bsf,
    &ff_mov2textsub_bsf,
    &ff_noise_bsf,
    &ff_null_bsf,
    &ff_opus_metadata_bsf,
    &ff_pcm_rechunk_bsf,
    &ff_prores_metadata_bsf,
    &ff_remove_extradata_bsf,
    &ff_text2movsub_bsf,
    &ff_trace_headers_bsf,
    &ff_truehd_core_bsf,
    &ff_vp9_metadata_bsf,
    &ff_vp9_raw_reorder_bsf,
    &ff_vp9_superframe_bsf,
    &ff_vp9_superframe_split_bsf,
    NULL };
'''

parser_list_c = '''/* Not available by default, generated by configure */
static const AVCodecParser * const parser_list[] = {
    &ff_aac_parser,
    &ff_aac_latm_parser,
    &ff_ac3_parser,
    &ff_adx_parser,
    &ff_av1_parser,
    &ff_avs2_parser,
    &ff_bmp_parser,
    &ff_cavsvideo_parser,
    &ff_cook_parser,
    &ff_dca_parser,
    &ff_dirac_parser,
    &ff_dnxhd_parser,
    &ff_dpx_parser,
    &ff_dvaudio_parser,
    &ff_dvbsub_parser,
    &ff_dvdsub_parser,
    &ff_dvd_nav_parser,
    &ff_flac_parser,
    &ff_g723_1_parser,
    &ff_g729_parser,
    &ff_gif_parser,
    &ff_gsm_parser,
    &ff_h261_parser,
    &ff_h263_parser,
    &ff_h264_parser,
    &ff_hevc_parser,
    &ff_jpeg2000_parser,
    &ff_mjpeg_parser,
    &ff_mlp_parser,
    &ff_mpeg4video_parser,
    &ff_mpegaudio_parser,
    &ff_mpegvideo_parser,
    &ff_opus_parser,
    &ff_png_parser,
    &ff_pnm_parser,
    &ff_rv30_parser,
    &ff_rv40_parser,
    &ff_sbc_parser,
    &ff_sipr_parser,
    &ff_tak_parser,
    &ff_vc1_parser,
    &ff_vorbis_parser,
    &ff_vp3_parser,
    &ff_vp8_parser,
    &ff_vp9_parser,
    &ff_webp_parser,
    &ff_xma_parser,
    NULL };
'''

muxer_list_c_pthreads = '''
static const AVOutputFormat * const muxer_list[] = {
    &ff_a64_muxer,
    &ff_ac3_muxer,
    &ff_adts_muxer,
    &ff_adx_muxer,
    &ff_aiff_muxer,
    &ff_amr_muxer,
    &ff_apng_muxer,
    &ff_aptx_muxer,
    &ff_aptx_hd_muxer,
    &ff_asf_muxer,
    &ff_ass_muxer,
    &ff_ast_muxer,
    &ff_asf_stream_muxer,
    &ff_au_muxer,
    &ff_avi_muxer,
    &ff_avm2_muxer,
    &ff_avs2_muxer,
    &ff_bit_muxer,
    &ff_caf_muxer,
    &ff_cavsvideo_muxer,
    &ff_codec2_muxer,
    &ff_codec2raw_muxer,
    &ff_crc_muxer,
    &ff_dash_muxer,
    &ff_data_muxer,
    &ff_daud_muxer,
    &ff_dirac_muxer,
    &ff_dnxhd_muxer,
    &ff_dts_muxer,
    &ff_dv_muxer,
    &ff_eac3_muxer,
    &ff_f4v_muxer,
    &ff_ffmetadata_muxer,
    &ff_fifo_muxer,
    &ff_fifo_test_muxer,
    &ff_filmstrip_muxer,
    &ff_fits_muxer,
    &ff_flac_muxer,
    &ff_flv_muxer,
    &ff_framecrc_muxer,
    &ff_framehash_muxer,
    &ff_framemd5_muxer,
    &ff_g722_muxer,
    &ff_g723_1_muxer,
    &ff_g726_muxer,
    &ff_g726le_muxer,
    &ff_gif_muxer,
    &ff_gsm_muxer,
    &ff_gxf_muxer,
    &ff_h261_muxer,
    &ff_h263_muxer,
    &ff_h264_muxer,
    &ff_hash_muxer,
    &ff_hds_muxer,
    &ff_hevc_muxer,
    &ff_hls_muxer,
    &ff_ico_muxer,
    &ff_ilbc_muxer,
    &ff_image2_muxer,
    &ff_image2pipe_muxer,
    &ff_ipod_muxer,
    &ff_ircam_muxer,
    &ff_ismv_muxer,
    &ff_ivf_muxer,
    &ff_jacosub_muxer,
    &ff_kvag_muxer,
    &ff_latm_muxer,
    &ff_lrc_muxer,
    &ff_m4v_muxer,
    &ff_md5_muxer,
    &ff_matroska_muxer,
    &ff_matroska_audio_muxer,
    &ff_microdvd_muxer,
    &ff_mjpeg_muxer,
    &ff_mlp_muxer,
    &ff_mmf_muxer,
    &ff_mov_muxer,
    &ff_mp2_muxer,
    &ff_mp3_muxer,
    &ff_mp4_muxer,
    &ff_mpeg1system_muxer,
    &ff_mpeg1vcd_muxer,
    &ff_mpeg1video_muxer,
    &ff_mpeg2dvd_muxer,
    &ff_mpeg2svcd_muxer,
    &ff_mpeg2video_muxer,
    &ff_mpeg2vob_muxer,
    &ff_mpegts_muxer,
    &ff_mpjpeg_muxer,
    &ff_mxf_muxer,
    &ff_mxf_d10_muxer,
    &ff_mxf_opatom_muxer,
    &ff_null_muxer,
    &ff_nut_muxer,
    &ff_oga_muxer,
    &ff_ogg_muxer,
    &ff_ogv_muxer,
    &ff_oma_muxer,
    &ff_opus_muxer,
    &ff_pcm_alaw_muxer,
    &ff_pcm_mulaw_muxer,
    &ff_pcm_vidc_muxer,
    &ff_pcm_f64be_muxer,
    &ff_pcm_f64le_muxer,
    &ff_pcm_f32be_muxer,
    &ff_pcm_f32le_muxer,
    &ff_pcm_s32be_muxer,
    &ff_pcm_s32le_muxer,
    &ff_pcm_s24be_muxer,
    &ff_pcm_s24le_muxer,
    &ff_pcm_s16be_muxer,
    &ff_pcm_s16le_muxer,
    &ff_pcm_s8_muxer,
    &ff_pcm_u32be_muxer,
    &ff_pcm_u32le_muxer,
    &ff_pcm_u24be_muxer,
    &ff_pcm_u24le_muxer,
    &ff_pcm_u16be_muxer,
    &ff_pcm_u16le_muxer,
    &ff_pcm_u8_muxer,
    &ff_psp_muxer,
    &ff_rawvideo_muxer,
    &ff_rm_muxer,
    &ff_roq_muxer,
    &ff_rso_muxer,
    &ff_rtp_muxer,
    &ff_rtp_mpegts_muxer,
    &ff_rtsp_muxer,
    &ff_sap_muxer,
    &ff_sbc_muxer,
    &ff_scc_muxer,
    &ff_segafilm_muxer,
    &ff_segment_muxer,
    &ff_stream_segment_muxer,
    &ff_singlejpeg_muxer,
    &ff_smjpeg_muxer,
    &ff_smoothstreaming_muxer,
    &ff_sox_muxer,
    &ff_spx_muxer,
    &ff_spdif_muxer,
    &ff_srt_muxer,
    &ff_streamhash_muxer,
    &ff_sup_muxer,
    &ff_swf_muxer,
    &ff_tee_muxer,
    &ff_tg2_muxer,
    &ff_tgp_muxer,
    &ff_mkvtimestamp_v2_muxer,
    &ff_truehd_muxer,
    &ff_tta_muxer,
    &ff_uncodedframecrc_muxer,
    &ff_vc1_muxer,
    &ff_vc1t_muxer,
    &ff_voc_muxer,
    &ff_w64_muxer,
    &ff_wav_muxer,
    &ff_webm_muxer,
    &ff_webm_dash_manifest_muxer,
    &ff_webm_chunk_muxer,
    &ff_webp_muxer,
    &ff_webvtt_muxer,
    &ff_wtv_muxer,
    &ff_wv_muxer,
    &ff_yuv4mpegpipe_muxer,
    NULL };
'''

muxer_list_c = '''
static const AVOutputFormat * const muxer_list[] = {
    &ff_a64_muxer,
    &ff_ac3_muxer,
    &ff_adts_muxer,
    &ff_adx_muxer,
    &ff_aiff_muxer,
    &ff_amr_muxer,
    &ff_apng_muxer,
    &ff_aptx_muxer,
    &ff_aptx_hd_muxer,
    &ff_asf_muxer,
    &ff_ass_muxer,
    &ff_ast_muxer,
    &ff_asf_stream_muxer,
    &ff_au_muxer,
    &ff_avi_muxer,
    &ff_avm2_muxer,
    &ff_avs2_muxer,
    &ff_bit_muxer,
    &ff_caf_muxer,
    &ff_cavsvideo_muxer,
    &ff_codec2_muxer,
    &ff_codec2raw_muxer,
    &ff_crc_muxer,
    &ff_dash_muxer,
    &ff_data_muxer,
    &ff_daud_muxer,
    &ff_dirac_muxer,
    &ff_dnxhd_muxer,
    &ff_dts_muxer,
    &ff_dv_muxer,
    &ff_eac3_muxer,
    &ff_f4v_muxer,
    &ff_ffmetadata_muxer,
    &ff_fifo_test_muxer,
    &ff_filmstrip_muxer,
    &ff_fits_muxer,
    &ff_flac_muxer,
    &ff_flv_muxer,
    &ff_framecrc_muxer,
    &ff_framehash_muxer,
    &ff_framemd5_muxer,
    &ff_g722_muxer,
    &ff_g723_1_muxer,
    &ff_g726_muxer,
    &ff_g726le_muxer,
    &ff_gif_muxer,
    &ff_gsm_muxer,
    &ff_gxf_muxer,
    &ff_h261_muxer,
    &ff_h263_muxer,
    &ff_h264_muxer,
    &ff_hash_muxer,
    &ff_hds_muxer,
    &ff_hevc_muxer,
    &ff_hls_muxer,
    &ff_ico_muxer,
    &ff_ilbc_muxer,
    &ff_image2_muxer,
    &ff_image2pipe_muxer,
    &ff_ipod_muxer,
    &ff_ircam_muxer,
    &ff_ismv_muxer,
    &ff_ivf_muxer,
    &ff_jacosub_muxer,
    &ff_kvag_muxer,
    &ff_latm_muxer,
    &ff_lrc_muxer,
    &ff_m4v_muxer,
    &ff_md5_muxer,
    &ff_matroska_muxer,
    &ff_matroska_audio_muxer,
    &ff_microdvd_muxer,
    &ff_mjpeg_muxer,
    &ff_mlp_muxer,
    &ff_mmf_muxer,
    &ff_mov_muxer,
    &ff_mp2_muxer,
    &ff_mp3_muxer,
    &ff_mp4_muxer,
    &ff_mpeg1system_muxer,
    &ff_mpeg1vcd_muxer,
    &ff_mpeg1video_muxer,
    &ff_mpeg2dvd_muxer,
    &ff_mpeg2svcd_muxer,
    &ff_mpeg2video_muxer,
    &ff_mpeg2vob_muxer,
    &ff_mpegts_muxer,
    &ff_mpjpeg_muxer,
    &ff_mxf_muxer,
    &ff_mxf_d10_muxer,
    &ff_mxf_opatom_muxer,
    &ff_null_muxer,
    &ff_nut_muxer,
    &ff_oga_muxer,
    &ff_ogg_muxer,
    &ff_ogv_muxer,
    &ff_oma_muxer,
    &ff_opus_muxer,
    &ff_pcm_alaw_muxer,
    &ff_pcm_mulaw_muxer,
    &ff_pcm_vidc_muxer,
    &ff_pcm_f64be_muxer,
    &ff_pcm_f64le_muxer,
    &ff_pcm_f32be_muxer,
    &ff_pcm_f32le_muxer,
    &ff_pcm_s32be_muxer,
    &ff_pcm_s32le_muxer,
    &ff_pcm_s24be_muxer,
    &ff_pcm_s24le_muxer,
    &ff_pcm_s16be_muxer,
    &ff_pcm_s16le_muxer,
    &ff_pcm_s8_muxer,
    &ff_pcm_u32be_muxer,
    &ff_pcm_u32le_muxer,
    &ff_pcm_u24be_muxer,
    &ff_pcm_u24le_muxer,
    &ff_pcm_u16be_muxer,
    &ff_pcm_u16le_muxer,
    &ff_pcm_u8_muxer,
    &ff_psp_muxer,
    &ff_rawvideo_muxer,
    &ff_rm_muxer,
    &ff_roq_muxer,
    &ff_rso_muxer,
    &ff_rtp_muxer,
    &ff_rtp_mpegts_muxer,
    &ff_rtsp_muxer,
    &ff_sap_muxer,
    &ff_sbc_muxer,
    &ff_scc_muxer,
    &ff_segafilm_muxer,
    &ff_segment_muxer,
    &ff_stream_segment_muxer,
    &ff_singlejpeg_muxer,
    &ff_smjpeg_muxer,
    &ff_smoothstreaming_muxer,
    &ff_sox_muxer,
    &ff_spx_muxer,
    &ff_spdif_muxer,
    &ff_srt_muxer,
    &ff_streamhash_muxer,
    &ff_sup_muxer,
    &ff_swf_muxer,
    &ff_tee_muxer,
    &ff_tg2_muxer,
    &ff_tgp_muxer,
    &ff_mkvtimestamp_v2_muxer,
    &ff_truehd_muxer,
    &ff_tta_muxer,
    &ff_uncodedframecrc_muxer,
    &ff_vc1_muxer,
    &ff_vc1t_muxer,
    &ff_voc_muxer,
    &ff_w64_muxer,
    &ff_wav_muxer,
    &ff_webm_muxer,
    &ff_webm_dash_manifest_muxer,
    &ff_webm_chunk_muxer,
    &ff_webp_muxer,
    &ff_webvtt_muxer,
    &ff_wtv_muxer,
    &ff_wv_muxer,
    &ff_yuv4mpegpipe_muxer,
    NULL };
'''

demuxer_list_c = '''
static const AVInputFormat * const demuxer_list[] = {
    &ff_aa_demuxer,
    &ff_aac_demuxer,
    &ff_ac3_demuxer,
    &ff_acm_demuxer,
    &ff_act_demuxer,
    &ff_adf_demuxer,
    &ff_adp_demuxer,
    &ff_ads_demuxer,
    &ff_adx_demuxer,
    &ff_aea_demuxer,
    &ff_afc_demuxer,
    &ff_aiff_demuxer,
    &ff_aix_demuxer,
    &ff_alp_demuxer,
    &ff_amr_demuxer,
    &ff_amrnb_demuxer,
    &ff_amrwb_demuxer,
    &ff_anm_demuxer,
    &ff_apc_demuxer,
    &ff_ape_demuxer,
    &ff_apm_demuxer,
    &ff_apng_demuxer,
    &ff_aptx_demuxer,
    &ff_aptx_hd_demuxer,
    &ff_aqtitle_demuxer,
    &ff_argo_asf_demuxer,
    &ff_asf_demuxer,
    &ff_asf_o_demuxer,
    &ff_ass_demuxer,
    &ff_ast_demuxer,
    &ff_au_demuxer,
    &ff_av1_demuxer,
    &ff_avi_demuxer,
    &ff_avr_demuxer,
    &ff_avs_demuxer,
    &ff_avs2_demuxer,
    &ff_bethsoftvid_demuxer,
    &ff_bfi_demuxer,
    &ff_bintext_demuxer,
    &ff_bink_demuxer,
    &ff_bit_demuxer,
    &ff_bmv_demuxer,
    &ff_bfstm_demuxer,
    &ff_brstm_demuxer,
    &ff_boa_demuxer,
    &ff_c93_demuxer,
    &ff_caf_demuxer,
    &ff_cavsvideo_demuxer,
    &ff_cdg_demuxer,
    &ff_cdxl_demuxer,
    &ff_cine_demuxer,
    &ff_codec2_demuxer,
    &ff_codec2raw_demuxer,
    &ff_concat_demuxer,
    &ff_data_demuxer,
    &ff_daud_demuxer,
    &ff_dcstr_demuxer,
    &ff_derf_demuxer,
    &ff_dfa_demuxer,
    &ff_dhav_demuxer,
    &ff_dirac_demuxer,
    &ff_dnxhd_demuxer,
    &ff_dsf_demuxer,
    &ff_dsicin_demuxer,
    &ff_dss_demuxer,
    &ff_dts_demuxer,
    &ff_dtshd_demuxer,
    &ff_dv_demuxer,
    &ff_dvbsub_demuxer,
    &ff_dvbtxt_demuxer,
    &ff_dxa_demuxer,
    &ff_ea_demuxer,
    &ff_ea_cdata_demuxer,
    &ff_eac3_demuxer,
    &ff_epaf_demuxer,
    &ff_ffmetadata_demuxer,
    &ff_filmstrip_demuxer,
    &ff_fits_demuxer,
    &ff_flac_demuxer,
    &ff_flic_demuxer,
    &ff_flv_demuxer,
    &ff_live_flv_demuxer,
    &ff_fourxm_demuxer,
    &ff_frm_demuxer,
    &ff_fsb_demuxer,
    &ff_fwse_demuxer,
    &ff_g722_demuxer,
    &ff_g723_1_demuxer,
    &ff_g726_demuxer,
    &ff_g726le_demuxer,
    &ff_g729_demuxer,
    &ff_gdv_demuxer,
    &ff_genh_demuxer,
    &ff_gif_demuxer,
    &ff_gsm_demuxer,
    &ff_gxf_demuxer,
    &ff_h261_demuxer,
    &ff_h263_demuxer,
    &ff_h264_demuxer,
    &ff_hca_demuxer,
    &ff_hcom_demuxer,
    &ff_hevc_demuxer,
    &ff_hls_demuxer,
    &ff_hnm_demuxer,
    &ff_ico_demuxer,
    &ff_idcin_demuxer,
    &ff_idf_demuxer,
    &ff_iff_demuxer,
    &ff_ifv_demuxer,
    &ff_ilbc_demuxer,
    &ff_image2_demuxer,
    &ff_image2pipe_demuxer,
    &ff_image2_alias_pix_demuxer,
    &ff_image2_brender_pix_demuxer,
    &ff_ingenient_demuxer,
    &ff_ipmovie_demuxer,
    &ff_ircam_demuxer,
    &ff_iss_demuxer,
    &ff_iv8_demuxer,
    &ff_ivf_demuxer,
    &ff_ivr_demuxer,
    &ff_jacosub_demuxer,
    &ff_jv_demuxer,
    &ff_kux_demuxer,
    &ff_kvag_demuxer,
    &ff_lmlm4_demuxer,
    &ff_loas_demuxer,
    &ff_lrc_demuxer,
    &ff_lvf_demuxer,
    &ff_lxf_demuxer,
    &ff_m4v_demuxer,
    &ff_matroska_demuxer,
    &ff_mgsts_demuxer,
    &ff_microdvd_demuxer,
    &ff_mjpeg_demuxer,
    &ff_mjpeg_2000_demuxer,
    &ff_mlp_demuxer,
    &ff_mlv_demuxer,
    &ff_mm_demuxer,
    &ff_mmf_demuxer,
    &ff_mov_demuxer,
    &ff_mp3_demuxer,
    &ff_mpc_demuxer,
    &ff_mpc8_demuxer,
    &ff_mpegps_demuxer,
    &ff_mpegts_demuxer,
    &ff_mpegtsraw_demuxer,
    &ff_mpegvideo_demuxer,
    &ff_mpjpeg_demuxer,
    &ff_mpl2_demuxer,
    &ff_mpsub_demuxer,
    &ff_msf_demuxer,
    &ff_msnwc_tcp_demuxer,
    &ff_mtaf_demuxer,
    &ff_mtv_demuxer,
    &ff_musx_demuxer,
    &ff_mv_demuxer,
    &ff_mvi_demuxer,
    &ff_mxf_demuxer,
    &ff_mxg_demuxer,
    &ff_nc_demuxer,
    &ff_nistsphere_demuxer,
    &ff_nsp_demuxer,
    &ff_nsv_demuxer,
    &ff_nut_demuxer,
    &ff_nuv_demuxer,
    &ff_ogg_demuxer,
    &ff_oma_demuxer,
    &ff_paf_demuxer,
    &ff_pcm_alaw_demuxer,
    &ff_pcm_mulaw_demuxer,
    &ff_pcm_vidc_demuxer,
    &ff_pcm_f64be_demuxer,
    &ff_pcm_f64le_demuxer,
    &ff_pcm_f32be_demuxer,
    &ff_pcm_f32le_demuxer,
    &ff_pcm_s32be_demuxer,
    &ff_pcm_s32le_demuxer,
    &ff_pcm_s24be_demuxer,
    &ff_pcm_s24le_demuxer,
    &ff_pcm_s16be_demuxer,
    &ff_pcm_s16le_demuxer,
    &ff_pcm_s8_demuxer,
    &ff_pcm_u32be_demuxer,
    &ff_pcm_u32le_demuxer,
    &ff_pcm_u24be_demuxer,
    &ff_pcm_u24le_demuxer,
    &ff_pcm_u16be_demuxer,
    &ff_pcm_u16le_demuxer,
    &ff_pcm_u8_demuxer,
    &ff_pjs_demuxer,
    &ff_pmp_demuxer,
    &ff_pp_bnk_demuxer,
    &ff_pva_demuxer,
    &ff_pvf_demuxer,
    &ff_qcp_demuxer,
    &ff_r3d_demuxer,
    &ff_rawvideo_demuxer,
    &ff_realtext_demuxer,
    &ff_redspark_demuxer,
    &ff_rl2_demuxer,
    &ff_rm_demuxer,
    &ff_roq_demuxer,
    &ff_rpl_demuxer,
    &ff_rsd_demuxer,
    &ff_rso_demuxer,
    &ff_rtp_demuxer,
    &ff_rtsp_demuxer,
    &ff_s337m_demuxer,
    &ff_sami_demuxer,
    &ff_sap_demuxer,
    &ff_sbc_demuxer,
    &ff_sbg_demuxer,
    &ff_scc_demuxer,
    &ff_sdp_demuxer,
    &ff_sdr2_demuxer,
    &ff_sds_demuxer,
    &ff_sdx_demuxer,
    &ff_segafilm_demuxer,
    &ff_ser_demuxer,
    &ff_shorten_demuxer,
    &ff_siff_demuxer,
    &ff_sln_demuxer,
    &ff_smacker_demuxer,
    &ff_smjpeg_demuxer,
    &ff_smush_demuxer,
    &ff_sol_demuxer,
    &ff_sox_demuxer,
    &ff_spdif_demuxer,
    &ff_srt_demuxer,
    &ff_str_demuxer,
    &ff_stl_demuxer,
    &ff_subviewer1_demuxer,
    &ff_subviewer_demuxer,
    &ff_sup_demuxer,
    &ff_svag_demuxer,
    &ff_swf_demuxer,
    &ff_tak_demuxer,
    &ff_tedcaptions_demuxer,
    &ff_thp_demuxer,
    &ff_threedostr_demuxer,
    &ff_tiertexseq_demuxer,
    &ff_tmv_demuxer,
    &ff_truehd_demuxer,
    &ff_tta_demuxer,
    &ff_txd_demuxer,
    &ff_tty_demuxer,
    &ff_ty_demuxer,
    &ff_v210_demuxer,
    &ff_v210x_demuxer,
    &ff_vag_demuxer,
    &ff_vc1_demuxer,
    &ff_vc1t_demuxer,
    &ff_vividas_demuxer,
    &ff_vivo_demuxer,
    &ff_vmd_demuxer,
    &ff_vobsub_demuxer,
    &ff_voc_demuxer,
    &ff_vpk_demuxer,
    &ff_vplayer_demuxer,
    &ff_vqf_demuxer,
    &ff_w64_demuxer,
    &ff_wav_demuxer,
    &ff_wc3_demuxer,
    &ff_webm_dash_manifest_demuxer,
    &ff_webvtt_demuxer,
    &ff_wsaud_demuxer,
    &ff_wsd_demuxer,
    &ff_wsvqa_demuxer,
    &ff_wtv_demuxer,
    &ff_wve_demuxer,
    &ff_wv_demuxer,
    &ff_xa_demuxer,
    &ff_xbin_demuxer,
    &ff_xmv_demuxer,
    &ff_xvag_demuxer,
    &ff_xwma_demuxer,
    &ff_yop_demuxer,
    &ff_yuv4mpegpipe_demuxer,
    &ff_image_bmp_pipe_demuxer,
    &ff_image_dds_pipe_demuxer,
    &ff_image_dpx_pipe_demuxer,
    &ff_image_exr_pipe_demuxer,
    &ff_image_gif_pipe_demuxer,
    &ff_image_j2k_pipe_demuxer,
    &ff_image_jpeg_pipe_demuxer,
    &ff_image_jpegls_pipe_demuxer,
    &ff_image_pam_pipe_demuxer,
    &ff_image_pbm_pipe_demuxer,
    &ff_image_pcx_pipe_demuxer,
    &ff_image_pgmyuv_pipe_demuxer,
    &ff_image_pgm_pipe_demuxer,
    &ff_image_pictor_pipe_demuxer,
    &ff_image_png_pipe_demuxer,
    &ff_image_ppm_pipe_demuxer,
    &ff_image_psd_pipe_demuxer,
    &ff_image_qdraw_pipe_demuxer,
    &ff_image_sgi_pipe_demuxer,
    &ff_image_svg_pipe_demuxer,
    &ff_image_sunrast_pipe_demuxer,
    &ff_image_tiff_pipe_demuxer,
    &ff_image_webp_pipe_demuxer,
    &ff_image_xpm_pipe_demuxer,
    &ff_image_xwd_pipe_demuxer,
    NULL };
'''
protocol_list_c_pthread = '''
static const URLProtocol * const url_protocols[] = {
    &ff_async_protocol,
    &ff_cache_protocol,
    &ff_concat_protocol,
    &ff_crypto_protocol,
    &ff_data_protocol,
    &ff_ffrtmphttp_protocol,
    &ff_file_protocol,
    &ff_ftp_protocol,
    &ff_gopher_protocol,
    &ff_hls_protocol,
    &ff_http_protocol,
    &ff_httpproxy_protocol,
    &ff_icecast_protocol,
    &ff_mmsh_protocol,
    &ff_mmst_protocol,
    &ff_md5_protocol,
    &ff_pipe_protocol,
    &ff_prompeg_protocol,
    &ff_rtmp_protocol,
    &ff_rtmpt_protocol,
    &ff_rtp_protocol,
    &ff_srtp_protocol,
    &ff_subfile_protocol,
    &ff_tee_protocol,
    &ff_tcp_protocol,
    &ff_udp_protocol,
    &ff_udplite_protocol,
    &ff_unix_protocol,
    NULL };
'''

protocol_list_c = '''
static const URLProtocol * const url_protocols[] = {
    &ff_cache_protocol,
    &ff_concat_protocol,
    &ff_crypto_protocol,
    &ff_data_protocol,
    &ff_ffrtmphttp_protocol,
    &ff_file_protocol,
    &ff_ftp_protocol,
    &ff_gopher_protocol,
    &ff_hls_protocol,
    &ff_http_protocol,
    &ff_httpproxy_protocol,
    &ff_icecast_protocol,
    &ff_mmsh_protocol,
    &ff_mmst_protocol,
    &ff_md5_protocol,
    &ff_pipe_protocol,
    &ff_prompeg_protocol,
    &ff_rtmp_protocol,
    &ff_rtmpt_protocol,
    &ff_rtp_protocol,
    &ff_srtp_protocol,
    &ff_subfile_protocol,
    &ff_tee_protocol,
    &ff_tcp_protocol,
    &ff_udp_protocol,
    &ff_udplite_protocol,
    &ff_unix_protocol,
    NULL };
'''

filter_list_c = '''static const AVFilter * const filter_list[] = {
    &ff_af_abench,
    &ff_af_acompressor,
    &ff_af_acontrast,
    &ff_af_acopy,
    &ff_af_acue,
    &ff_af_acrossfade,
    &ff_af_acrossover,
    &ff_af_acrusher,
    &ff_af_adeclick,
    &ff_af_adeclip,
    &ff_af_adelay,
    &ff_af_aderivative,
    &ff_af_aecho,
    &ff_af_aemphasis,
    &ff_af_aeval,
    &ff_af_afade,
    &ff_af_afftdn,
    &ff_af_afftfilt,
    &ff_af_afir,
    &ff_af_aformat,
    &ff_af_agate,
    &ff_af_aiir,
    &ff_af_aintegral,
    &ff_af_ainterleave,
    &ff_af_alimiter,
    &ff_af_allpass,
    &ff_af_aloop,
    &ff_af_amerge,
    &ff_af_ametadata,
    &ff_af_amix,
    &ff_af_amultiply,
    &ff_af_anequalizer,
    &ff_af_anlmdn,
    &ff_af_anlms,
    &ff_af_anull,
    &ff_af_apad,
    &ff_af_aperms,
    &ff_af_aphaser,
    &ff_af_apulsator,
    &ff_af_arealtime,
    &ff_af_aresample,
    &ff_af_areverse,
    &ff_af_arnndn,
    &ff_af_aselect,
    &ff_af_asendcmd,
    &ff_af_asetnsamples,
    &ff_af_asetpts,
    &ff_af_asetrate,
    &ff_af_asettb,
    &ff_af_ashowinfo,
    &ff_af_asidedata,
    &ff_af_asoftclip,
    &ff_af_asplit,
    &ff_af_astats,
    &ff_af_astreamselect,
    &ff_af_asubboost,
    &ff_af_atempo,
    &ff_af_atrim,
    &ff_af_axcorrelate,
    &ff_af_bandpass,
    &ff_af_bandreject,
    &ff_af_bass,
    &ff_af_biquad,
    &ff_af_channelmap,
    &ff_af_channelsplit,
    &ff_af_chorus,
    &ff_af_compand,
    &ff_af_compensationdelay,
    &ff_af_crossfeed,
    &ff_af_crystalizer,
    &ff_af_dcshift,
    &ff_af_deesser,
    &ff_af_drmeter,
    &ff_af_dynaudnorm,
    &ff_af_earwax,
    &ff_af_ebur128,
    &ff_af_equalizer,
    &ff_af_extrastereo,
    &ff_af_firequalizer,
    &ff_af_flanger,
    &ff_af_haas,
    &ff_af_hdcd,
    &ff_af_headphone,
    &ff_af_highpass,
    &ff_af_highshelf,
    &ff_af_join,
    &ff_af_loudnorm,
    &ff_af_lowpass,
    &ff_af_lowshelf,
    &ff_af_mcompand,
    &ff_af_pan,
    &ff_af_replaygain,
    &ff_af_sidechaincompress,
    &ff_af_sidechaingate,
    &ff_af_silencedetect,
    &ff_af_silenceremove,
    &ff_af_stereotools,
    &ff_af_stereowiden,
    &ff_af_superequalizer,
    &ff_af_surround,
    &ff_af_treble,
    &ff_af_tremolo,
    &ff_af_vibrato,
    &ff_af_volume,
    &ff_af_volumedetect,
    &ff_asrc_aevalsrc,
    &ff_asrc_afirsrc,
    &ff_asrc_anoisesrc,
    &ff_asrc_anullsrc,
    &ff_asrc_hilbert,
    &ff_asrc_sinc,
    &ff_asrc_sine,
    &ff_asink_anullsink,
    &ff_vf_addroi,
    &ff_vf_alphaextract,
    &ff_vf_alphamerge,
    &ff_vf_amplify,
    &ff_vf_atadenoise,
    &ff_vf_avgblur,
    &ff_vf_bbox,
    &ff_vf_bench,
    &ff_vf_bilateral,
    &ff_vf_bitplanenoise,
    &ff_vf_blackdetect,
    &ff_vf_blend,
    &ff_vf_bm3d,
    &ff_vf_bwdif,
    &ff_vf_cas,
    &ff_vf_chromahold,
    &ff_vf_chromakey,
    &ff_vf_chromashift,
    &ff_vf_ciescope,
    &ff_vf_codecview,
    &ff_vf_colorbalance,
    &ff_vf_colorchannelmixer,
    &ff_vf_colorkey,
    &ff_vf_colorhold,
    &ff_vf_colorlevels,
    &ff_vf_colorspace,
    &ff_vf_convolution,
    &ff_vf_convolve,
    &ff_vf_copy,
    &ff_vf_crop,
    &ff_vf_cue,
    &ff_vf_curves,
    &ff_vf_datascope,
    &ff_vf_dblur,
    &ff_vf_dctdnoiz,
    &ff_vf_deband,
    &ff_vf_deblock,
    &ff_vf_decimate,
    &ff_vf_deconvolve,
    &ff_vf_dedot,
    &ff_vf_deflate,
    &ff_vf_deflicker,
    &ff_vf_dejudder,
    &ff_vf_derain,
    &ff_vf_deshake,
    &ff_vf_despill,
    &ff_vf_detelecine,
    &ff_vf_dilation,
    &ff_vf_displace,
    &ff_vf_dnn_processing,
    &ff_vf_doubleweave,
    &ff_vf_drawbox,
    &ff_vf_drawgraph,
    &ff_vf_drawgrid,
    &ff_vf_edgedetect,
    &ff_vf_elbg,
    &ff_vf_entropy,
    &ff_vf_erosion,
    &ff_vf_extractplanes,
    &ff_vf_fade,
    &ff_vf_fftdnoiz,
    &ff_vf_fftfilt,
    &ff_vf_field,
    &ff_vf_fieldhint,
    &ff_vf_fieldmatch,
    &ff_vf_fieldorder,
    &ff_vf_fillborders,
    &ff_vf_floodfill,
    &ff_vf_format,
    &ff_vf_fps,
    &ff_vf_framepack,
    &ff_vf_framerate,
    &ff_vf_framestep,
    &ff_vf_freezedetect,
    &ff_vf_freezeframes,
    &ff_vf_gblur,
    &ff_vf_geq,
    &ff_vf_gradfun,
    &ff_vf_graphmonitor,
    &ff_vf_greyedge,
    &ff_vf_haldclut,
    &ff_vf_hflip,
    &ff_vf_histogram,
    &ff_vf_hqx,
    &ff_vf_hstack,
    &ff_vf_hue,
    &ff_vf_hwdownload,
    &ff_vf_hwmap,
    &ff_vf_hwupload,
    &ff_vf_hysteresis,
    &ff_vf_idet,
    &ff_vf_il,
    &ff_vf_inflate,
    &ff_vf_interleave,
    &ff_vf_lagfun,
    &ff_vf_lenscorrection,
    &ff_vf_limiter,
    &ff_vf_loop,
    &ff_vf_lumakey,
    &ff_vf_lut,
    &ff_vf_lut1d,
    &ff_vf_lut2,
    &ff_vf_lut3d,
    &ff_vf_lutrgb,
    &ff_vf_lutyuv,
    &ff_vf_maskedclamp,
    &ff_vf_maskedmax,
    &ff_vf_maskedmerge,
    &ff_vf_maskedmin,
    &ff_vf_maskedthreshold,
    &ff_vf_maskfun,
    &ff_vf_median,
    &ff_vf_mergeplanes,
    &ff_vf_mestimate,
    &ff_vf_metadata,
    &ff_vf_midequalizer,
    &ff_vf_minterpolate,
    &ff_vf_mix,
    &ff_vf_negate,
    &ff_vf_nlmeans,
    &ff_vf_noformat,
    &ff_vf_noise,
    &ff_vf_normalize,
    &ff_vf_null,
    &ff_vf_oscilloscope,
    &ff_vf_overlay,
    &ff_vf_pad,
    &ff_vf_palettegen,
    &ff_vf_paletteuse,
    &ff_vf_perms,
    &ff_vf_photosensitivity,
    &ff_vf_pixdesctest,
    &ff_vf_pixscope,
    &ff_vf_premultiply,
    &ff_vf_prewitt,
    &ff_vf_pseudocolor,
    &ff_vf_psnr,
    &ff_vf_qp,
    &ff_vf_random,
    &ff_vf_readeia608,
    &ff_vf_readvitc,
    &ff_vf_realtime,
    &ff_vf_remap,
    &ff_vf_removegrain,
    &ff_vf_removelogo,
    &ff_vf_reverse,
    &ff_vf_rgbashift,
    &ff_vf_roberts,
    &ff_vf_rotate,
    &ff_vf_scale,
    &ff_vf_scale2ref,
    &ff_vf_scdet,
    &ff_vf_scroll,
    &ff_vf_select,
    &ff_vf_selectivecolor,
    &ff_vf_sendcmd,
    &ff_vf_separatefields,
    &ff_vf_setdar,
    &ff_vf_setfield,
    &ff_vf_setparams,
    &ff_vf_setpts,
    &ff_vf_setrange,
    &ff_vf_setsar,
    &ff_vf_settb,
    &ff_vf_showinfo,
    &ff_vf_showpalette,
    &ff_vf_shuffleframes,
    &ff_vf_shuffleplanes,
    &ff_vf_sidedata,
    &ff_vf_signalstats,
    &ff_vf_sobel,
    &ff_vf_split,
    &ff_vf_sr,
    &ff_vf_ssim,
    &ff_vf_streamselect,
    &ff_vf_swaprect,
    &ff_vf_swapuv,
    &ff_vf_tblend,
    &ff_vf_telecine,
    &ff_vf_thistogram,
    &ff_vf_threshold,
    &ff_vf_thumbnail,
    &ff_vf_tile,
    &ff_vf_tlut2,
    &ff_vf_tmedian,
    &ff_vf_tmix,
    &ff_vf_tonemap,
    &ff_vf_tpad,
    &ff_vf_transpose,
    &ff_vf_trim,
    &ff_vf_unpremultiply,
    &ff_vf_unsharp,
    &ff_vf_untile,
    &ff_vf_v360,
    &ff_vf_vectorscope,
    &ff_vf_vflip,
    &ff_vf_vfrdet,
    &ff_vf_vibrance,
    &ff_vf_vignette,
    &ff_vf_vmafmotion,
    &ff_vf_vstack,
    &ff_vf_w3fdif,
    &ff_vf_waveform,
    &ff_vf_weave,
    &ff_vf_xbr,
    &ff_vf_xfade,
    &ff_vf_xmedian,
    &ff_vf_xstack,
    &ff_vf_yadif,
    &ff_vf_yaepblur,
    &ff_vf_zoompan,
    &ff_vsrc_allrgb,
    &ff_vsrc_allyuv,
    &ff_vsrc_cellauto,
    &ff_vsrc_color,
    &ff_vsrc_gradients,
    &ff_vsrc_haldclutsrc,
    &ff_vsrc_life,
    &ff_vsrc_mandelbrot,
    &ff_vsrc_nullsrc,
    &ff_vsrc_pal75bars,
    &ff_vsrc_pal100bars,
    &ff_vsrc_rgbtestsrc,
    &ff_vsrc_sierpinski,
    &ff_vsrc_smptebars,
    &ff_vsrc_smptehdbars,
    &ff_vsrc_testsrc,
    &ff_vsrc_testsrc2,
    &ff_vsrc_yuvtestsrc,
    &ff_vsink_nullsink,
    &ff_avf_abitscope,
    &ff_avf_adrawgraph,
    &ff_avf_agraphmonitor,
    &ff_avf_ahistogram,
    &ff_avf_aphasemeter,
    &ff_avf_avectorscope,
    &ff_avf_concat,
    &ff_avf_showcqt,
    &ff_avf_showfreqs,
    &ff_avf_showspatial,
    &ff_avf_showspectrum,
    &ff_avf_showspectrumpic,
    &ff_avf_showvolume,
    &ff_avf_showwaves,
    &ff_avf_showwavespic,
    &ff_vaf_spectrumsynth,
    &ff_avsrc_amovie,
    &ff_avsrc_movie,
    &ff_af_afifo,
    &ff_vf_fifo,
    &ff_asrc_abuffer,
    &ff_vsrc_buffer,
    &ff_asink_abuffer,
    &ff_vsink_buffer,
    NULL };
'''

outdev_list_c = '''static const AVOutputFormat * const outdev_list[] = {
    NULL };
'''

indev_list_c = '''static const AVInputFormat * const indev_list[] = {
    &ff_lavfi_demuxer,
    NULL };
'''

ffmpeg_config_h_pthread = '''
/* Automatically generated by configure - do not modify! */
#ifndef FFMPEG_CONFIG_H
#define FFMPEG_CONFIG_H
#define FFMPEG_CONFIGURATION "--disable-x86asm --disable-inline-asm --disable-doc --disable-ffprobe --nm=llvm-nm --ar=emar --cc=emcc --cxx=em++ --objcc=emcc --dep-cc=emcc --ranlib='emar s' --enable-pic"
#define FFMPEG_LICENSE "LGPL version 2.1 or later"
#define CONFIG_THIS_YEAR 2020
#define FFMPEG_DATADIR "/usr/local/share/ffmpeg"
#define AVCONV_DATADIR "/usr/local/share/ffmpeg"
#define CC_IDENT "emcc (Emscripten gcc/clang-like replacement) 1.39.11"
#define av_restrict restrict
#define EXTERN_PREFIX ""
#define EXTERN_ASM
#define BUILDSUF ""
#define SLIBSUF ".so"
#define HAVE_MMX2 HAVE_MMXEXT
#define SWS_MAX_FILTER_SIZE 256
#define ARCH_AARCH64 0
#define ARCH_ALPHA 0
#define ARCH_ARM 0
#define ARCH_AVR32 0
#define ARCH_AVR32_AP 0
#define ARCH_AVR32_UC 0
#define ARCH_BFIN 0
#define ARCH_IA64 0
#define ARCH_M68K 0
#define ARCH_MIPS 0
#define ARCH_MIPS64 0
#define ARCH_PARISC 0
#define ARCH_PPC 0
#define ARCH_PPC64 0
#define ARCH_S390 0
#define ARCH_SH4 0
#define ARCH_SPARC 0
#define ARCH_SPARC64 0
#define ARCH_TILEGX 0
#define ARCH_TILEPRO 0
#define ARCH_TOMI 0
#define ARCH_X86 1
#define ARCH_X86_32 1
#define ARCH_X86_64 0
#define HAVE_ARMV5TE 0
#define HAVE_ARMV6 0
#define HAVE_ARMV6T2 0
#define HAVE_ARMV8 0
#define HAVE_NEON 0
#define HAVE_VFP 0
#define HAVE_VFPV3 0
#define HAVE_SETEND 0
#define HAVE_ALTIVEC 0
#define HAVE_DCBZL 0
#define HAVE_LDBRX 0
#define HAVE_POWER8 0
#define HAVE_PPC4XX 0
#define HAVE_VSX 0
#define HAVE_AESNI 1
#define HAVE_AMD3DNOW 1
#define HAVE_AMD3DNOWEXT 1
#define HAVE_AVX 1
#define HAVE_AVX2 1
#define HAVE_AVX512 1
#define HAVE_FMA3 1
#define HAVE_FMA4 1
#define HAVE_MMX 1
#define HAVE_MMXEXT 1
#define HAVE_SSE 1
#define HAVE_SSE2 1
#define HAVE_SSE3 1
#define HAVE_SSE4 1
#define HAVE_SSE42 1
#define HAVE_SSSE3 1
#define HAVE_XOP 1
#define HAVE_CPUNOP 1
#define HAVE_I686 1
#define HAVE_MIPSFPU 0
#define HAVE_MIPS32R2 0
#define HAVE_MIPS32R5 0
#define HAVE_MIPS64R2 0
#define HAVE_MIPS32R6 0
#define HAVE_MIPS64R6 0
#define HAVE_MIPSDSP 0
#define HAVE_MIPSDSPR2 0
#define HAVE_MSA 0
#define HAVE_MSA2 0
#define HAVE_LOONGSON2 0
#define HAVE_LOONGSON3 0
#define HAVE_MMI 0
#define HAVE_ARMV5TE_EXTERNAL 0
#define HAVE_ARMV6_EXTERNAL 0
#define HAVE_ARMV6T2_EXTERNAL 0
#define HAVE_ARMV8_EXTERNAL 0
#define HAVE_NEON_EXTERNAL 0
#define HAVE_VFP_EXTERNAL 0
#define HAVE_VFPV3_EXTERNAL 0
#define HAVE_SETEND_EXTERNAL 0
#define HAVE_ALTIVEC_EXTERNAL 0
#define HAVE_DCBZL_EXTERNAL 0
#define HAVE_LDBRX_EXTERNAL 0
#define HAVE_POWER8_EXTERNAL 0
#define HAVE_PPC4XX_EXTERNAL 0
#define HAVE_VSX_EXTERNAL 0
#define HAVE_AESNI_EXTERNAL 0
#define HAVE_AMD3DNOW_EXTERNAL 0
#define HAVE_AMD3DNOWEXT_EXTERNAL 0
#define HAVE_AVX_EXTERNAL 0
#define HAVE_AVX2_EXTERNAL 0
#define HAVE_AVX512_EXTERNAL 0
#define HAVE_FMA3_EXTERNAL 0
#define HAVE_FMA4_EXTERNAL 0
#define HAVE_MMX_EXTERNAL 0
#define HAVE_MMXEXT_EXTERNAL 0
#define HAVE_SSE_EXTERNAL 0
#define HAVE_SSE2_EXTERNAL 0
#define HAVE_SSE3_EXTERNAL 0
#define HAVE_SSE4_EXTERNAL 0
#define HAVE_SSE42_EXTERNAL 0
#define HAVE_SSSE3_EXTERNAL 0
#define HAVE_XOP_EXTERNAL 0
#define HAVE_CPUNOP_EXTERNAL 0
#define HAVE_I686_EXTERNAL 0
#define HAVE_MIPSFPU_EXTERNAL 0
#define HAVE_MIPS32R2_EXTERNAL 0
#define HAVE_MIPS32R5_EXTERNAL 0
#define HAVE_MIPS64R2_EXTERNAL 0
#define HAVE_MIPS32R6_EXTERNAL 0
#define HAVE_MIPS64R6_EXTERNAL 0
#define HAVE_MIPSDSP_EXTERNAL 0
#define HAVE_MIPSDSPR2_EXTERNAL 0
#define HAVE_MSA_EXTERNAL 0
#define HAVE_MSA2_EXTERNAL 0
#define HAVE_LOONGSON2_EXTERNAL 0
#define HAVE_LOONGSON3_EXTERNAL 0
#define HAVE_MMI_EXTERNAL 0
#define HAVE_ARMV5TE_INLINE 0
#define HAVE_ARMV6_INLINE 0
#define HAVE_ARMV6T2_INLINE 0
#define HAVE_ARMV8_INLINE 0
#define HAVE_NEON_INLINE 0
#define HAVE_VFP_INLINE 0
#define HAVE_VFPV3_INLINE 0
#define HAVE_SETEND_INLINE 0
#define HAVE_ALTIVEC_INLINE 0
#define HAVE_DCBZL_INLINE 0
#define HAVE_LDBRX_INLINE 0
#define HAVE_POWER8_INLINE 0
#define HAVE_PPC4XX_INLINE 0
#define HAVE_VSX_INLINE 0
#define HAVE_AESNI_INLINE 0
#define HAVE_AMD3DNOW_INLINE 0
#define HAVE_AMD3DNOWEXT_INLINE 0
#define HAVE_AVX_INLINE 0
#define HAVE_AVX2_INLINE 0
#define HAVE_AVX512_INLINE 0
#define HAVE_FMA3_INLINE 0
#define HAVE_FMA4_INLINE 0
#define HAVE_MMX_INLINE 0
#define HAVE_MMXEXT_INLINE 0
#define HAVE_SSE_INLINE 0
#define HAVE_SSE2_INLINE 0
#define HAVE_SSE3_INLINE 0
#define HAVE_SSE4_INLINE 0
#define HAVE_SSE42_INLINE 0
#define HAVE_SSSE3_INLINE 0
#define HAVE_XOP_INLINE 0
#define HAVE_CPUNOP_INLINE 0
#define HAVE_I686_INLINE 0
#define HAVE_MIPSFPU_INLINE 0
#define HAVE_MIPS32R2_INLINE 0
#define HAVE_MIPS32R5_INLINE 0
#define HAVE_MIPS64R2_INLINE 0
#define HAVE_MIPS32R6_INLINE 0
#define HAVE_MIPS64R6_INLINE 0
#define HAVE_MIPSDSP_INLINE 0
#define HAVE_MIPSDSPR2_INLINE 0
#define HAVE_MSA_INLINE 0
#define HAVE_MSA2_INLINE 0
#define HAVE_LOONGSON2_INLINE 0
#define HAVE_LOONGSON3_INLINE 0
#define HAVE_MMI_INLINE 0
#define HAVE_ALIGNED_STACK 1
#define HAVE_FAST_64BIT 0
#define HAVE_FAST_CLZ 1
#define HAVE_FAST_CMOV 0
#define HAVE_LOCAL_ALIGNED 1
#define HAVE_SIMD_ALIGN_16 1
#define HAVE_SIMD_ALIGN_32 1
#define HAVE_SIMD_ALIGN_64 1
#define HAVE_ATOMIC_CAS_PTR 0
#define HAVE_MACHINE_RW_BARRIER 0
#define HAVE_MEMORYBARRIER 0
#define HAVE_MM_EMPTY 0
#define HAVE_RDTSC 0
#define HAVE_SEM_TIMEDWAIT 1
#define HAVE_SYNC_VAL_COMPARE_AND_SWAP 1
#define HAVE_CABS 0
#define HAVE_CEXP 0
#define HAVE_INLINE_ASM 0
#define HAVE_SYMVER 0
#define HAVE_X86ASM 0
#define HAVE_BIGENDIAN 0
#define HAVE_FAST_UNALIGNED 1
#define HAVE_ARPA_INET_H 1
#define HAVE_ASM_TYPES_H 0
#define HAVE_CDIO_PARANOIA_H 0
#define HAVE_CDIO_PARANOIA_PARANOIA_H 0
#define HAVE_CUDA_H 0
#define HAVE_DISPATCH_DISPATCH_H 0
#define HAVE_DEV_BKTR_IOCTL_BT848_H 0
#define HAVE_DEV_BKTR_IOCTL_METEOR_H 0
#define HAVE_DEV_IC_BT8XX_H 0
#define HAVE_DEV_VIDEO_BKTR_IOCTL_BT848_H 0
#define HAVE_DEV_VIDEO_METEOR_IOCTL_METEOR_H 0
#define HAVE_DIRECT_H 0
#define HAVE_DIRENT_H 1
#define HAVE_DXGIDEBUG_H 0
#define HAVE_DXVA_H 0
#define HAVE_ES2_GL_H 0
#define HAVE_GSM_H 0
#define HAVE_IO_H 0
#define HAVE_LINUX_PERF_EVENT_H 0
#define HAVE_MACHINE_IOCTL_BT848_H 0
#define HAVE_MACHINE_IOCTL_METEOR_H 0
#define HAVE_MALLOC_H 1
#define HAVE_OPENCV2_CORE_CORE_C_H 0
#define HAVE_OPENGL_GL3_H 0
#define HAVE_POLL_H 1
#define HAVE_SYS_PARAM_H 1
#define HAVE_SYS_RESOURCE_H 1
#define HAVE_SYS_SELECT_H 1
#define HAVE_SYS_SOUNDCARD_H 0
#define HAVE_SYS_TIME_H 1
#define HAVE_SYS_UN_H 1
#define HAVE_SYS_VIDEOIO_H 0
#define HAVE_TERMIOS_H 1
#define HAVE_UDPLITE_H 0
#define HAVE_UNISTD_H 1
#define HAVE_VALGRIND_VALGRIND_H 0
#define HAVE_WINDOWS_H 0
#define HAVE_WINSOCK2_H 0
#define HAVE_INTRINSICS_NEON 0
#define HAVE_ATANF 0
#define HAVE_ATAN2F 0
#define HAVE_CBRT 1
#define HAVE_CBRTF 1
#define HAVE_COPYSIGN 1
#define HAVE_COSF 0
#define HAVE_ERF 1
#define HAVE_EXP2 0
#define HAVE_EXP2F 0
#define HAVE_EXPF 0
#define HAVE_HYPOT 1
#define HAVE_ISFINITE 1
#define HAVE_ISINF 1
#define HAVE_ISNAN 1
#define HAVE_LDEXPF 0
#define HAVE_LLRINT 0
#define HAVE_LLRINTF 0
#define HAVE_LOG2 0
#define HAVE_LOG2F 0
#define HAVE_LOG10F 0
#define HAVE_LRINT 1
#define HAVE_LRINTF 1
#define HAVE_POWF 0
#define HAVE_RINT 1
#define HAVE_ROUND 1
#define HAVE_ROUNDF 1
#define HAVE_SINF 0
#define HAVE_TRUNC 1
#define HAVE_TRUNCF 1
#define HAVE_DOS_PATHS 0
#define HAVE_LIBC_MSVCRT 0
#define HAVE_MMAL_PARAMETER_VIDEO_MAX_NUM_CALLBACKS 0
#define HAVE_SECTION_DATA_REL_RO 1
#define HAVE_THREADS 1
#define HAVE_UWP 0
#define HAVE_WINRT 0
#define HAVE_ACCESS 1
#define HAVE_ALIGNED_MALLOC 0
#define HAVE_ARC4RANDOM 0
#define HAVE_CLOCK_GETTIME 1
#define HAVE_CLOSESOCKET 0
#define HAVE_COMMANDLINETOARGVW 0
#define HAVE_FCNTL 1
#define HAVE_GETADDRINFO 1
#define HAVE_GETHRTIME 0
#define HAVE_GETOPT 1
#define HAVE_GETMODULEHANDLE 0
#define HAVE_GETPROCESSAFFINITYMASK 0
#define HAVE_GETPROCESSMEMORYINFO 0
#define HAVE_GETPROCESSTIMES 0
#define HAVE_GETRUSAGE 1
#define HAVE_GETSTDHANDLE 0
#define HAVE_GETSYSTEMTIMEASFILETIME 0
#define HAVE_GETTIMEOFDAY 1
#define HAVE_GLOB 1
#define HAVE_GLXGETPROCADDRESS 0
#define HAVE_GMTIME_R 1
#define HAVE_INET_ATON 1
#define HAVE_ISATTY 1
#define HAVE_KBHIT 0
#define HAVE_LOCALTIME_R 1
#define HAVE_LSTAT 1
#define HAVE_LZO1X_999_COMPRESS 0
#define HAVE_MACH_ABSOLUTE_TIME 0
#define HAVE_MAPVIEWOFFILE 0
#define HAVE_MEMALIGN 1
#define HAVE_MKSTEMP 1
#define HAVE_MMAP 1
#define HAVE_MPROTECT 1
#define HAVE_NANOSLEEP 1
#define HAVE_PEEKNAMEDPIPE 0
#define HAVE_POSIX_MEMALIGN 1
#define HAVE_PTHREAD_CANCEL 1
#define HAVE_SCHED_GETAFFINITY 0
#define HAVE_SECITEMIMPORT 0
#define HAVE_SETCONSOLETEXTATTRIBUTE 0
#define HAVE_SETCONSOLECTRLHANDLER 0
#define HAVE_SETDLLDIRECTORY 0
#define HAVE_SETMODE 0
#define HAVE_SETRLIMIT 1
#define HAVE_SLEEP 0
#define HAVE_STRERROR_R 1
#define HAVE_SYSCONF 1
#define HAVE_SYSCTL 0
#define HAVE_USLEEP 1
#define HAVE_UTGETOSTYPEFROMSTRING 0
#define HAVE_VIRTUALALLOC 0
#define HAVE_WGLGETPROCADDRESS 0
#define HAVE_BCRYPT 0
#define HAVE_VAAPI_DRM 0
#define HAVE_VAAPI_X11 0
#define HAVE_VDPAU_X11 0
#define HAVE_PTHREADS 1
#define HAVE_OS2THREADS 0
#define HAVE_W32THREADS 0
#define HAVE_AS_ARCH_DIRECTIVE 0
#define HAVE_AS_DN_DIRECTIVE 0
#define HAVE_AS_FPU_DIRECTIVE 0
#define HAVE_AS_FUNC 0
#define HAVE_AS_OBJECT_ARCH 0
#define HAVE_ASM_MOD_Q 0
#define HAVE_BLOCKS_EXTENSION 0
#define HAVE_EBP_AVAILABLE 0
#define HAVE_EBX_AVAILABLE 0
#define HAVE_GNU_AS 0
#define HAVE_GNU_WINDRES 0
#define HAVE_IBM_ASM 0
#define HAVE_INLINE_ASM_DIRECT_SYMBOL_REFS 0
#define HAVE_INLINE_ASM_LABELS 1
#define HAVE_INLINE_ASM_NONLOCAL_LABELS 0
#define HAVE_PRAGMA_DEPRECATED 1
#define HAVE_RSYNC_CONTIMEOUT 1
#define HAVE_SYMVER_ASM_LABEL 0
#define HAVE_SYMVER_GNU_ASM 0
#define HAVE_VFP_ARGS 0
#define HAVE_XFORM_ASM 0
#define HAVE_XMM_CLOBBERS 0
#define HAVE_KCMVIDEOCODECTYPE_HEVC 0
#define HAVE_KCVPIXELFORMATTYPE_420YPCBCR10BIPLANARVIDEORANGE 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_SMPTE_ST_2084_PQ 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_ITU_R_2100_HLG 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_LINEAR 0
#define HAVE_SOCKLEN_T 1
#define HAVE_STRUCT_ADDRINFO 1
#define HAVE_STRUCT_GROUP_SOURCE_REQ 1
#define HAVE_STRUCT_IP_MREQ_SOURCE 1
#define HAVE_STRUCT_IPV6_MREQ 1
#define HAVE_STRUCT_MSGHDR_MSG_FLAGS 1
#define HAVE_STRUCT_POLLFD 1
#define HAVE_STRUCT_RUSAGE_RU_MAXRSS 1
#define HAVE_STRUCT_SCTP_EVENT_SUBSCRIBE 0
#define HAVE_STRUCT_SOCKADDR_IN6 1
#define HAVE_STRUCT_SOCKADDR_SA_LEN 0
#define HAVE_STRUCT_SOCKADDR_STORAGE 1
#define HAVE_STRUCT_STAT_ST_MTIM_TV_NSEC 1
#define HAVE_STRUCT_V4L2_FRMIVALENUM_DISCRETE 0
#define HAVE_MAKEINFO 1
#define HAVE_MAKEINFO_HTML 1
#define HAVE_OPENCL_D3D11 0
#define HAVE_OPENCL_DRM_ARM 0
#define HAVE_OPENCL_DRM_BEIGNET 0
#define HAVE_OPENCL_DXVA2 0
#define HAVE_OPENCL_VAAPI_BEIGNET 0
#define HAVE_OPENCL_VAAPI_INTEL_MEDIA 0
#define HAVE_PERL 1
#define HAVE_POD2MAN 1
#define HAVE_TEXI2HTML 0
#define CONFIG_DOC 0
#define CONFIG_HTMLPAGES 1
#define CONFIG_MANPAGES 1
#define CONFIG_PODPAGES 1
#define CONFIG_TXTPAGES 1
#define CONFIG_AVIO_LIST_DIR_EXAMPLE 1
#define CONFIG_AVIO_READING_EXAMPLE 1
#define CONFIG_DECODE_AUDIO_EXAMPLE 1
#define CONFIG_DECODE_VIDEO_EXAMPLE 1
#define CONFIG_DEMUXING_DECODING_EXAMPLE 1
#define CONFIG_ENCODE_AUDIO_EXAMPLE 1
#define CONFIG_ENCODE_VIDEO_EXAMPLE 1
#define CONFIG_EXTRACT_MVS_EXAMPLE 1
#define CONFIG_FILTER_AUDIO_EXAMPLE 1
#define CONFIG_FILTERING_AUDIO_EXAMPLE 1
#define CONFIG_FILTERING_VIDEO_EXAMPLE 1
#define CONFIG_HTTP_MULTICLIENT_EXAMPLE 1
#define CONFIG_HW_DECODE_EXAMPLE 1
#define CONFIG_METADATA_EXAMPLE 1
#define CONFIG_MUXING_EXAMPLE 1
#define CONFIG_QSVDEC_EXAMPLE 0
#define CONFIG_REMUXING_EXAMPLE 1
#define CONFIG_RESAMPLING_AUDIO_EXAMPLE 1
#define CONFIG_SCALING_VIDEO_EXAMPLE 1
#define CONFIG_TRANSCODE_AAC_EXAMPLE 1
#define CONFIG_TRANSCODING_EXAMPLE 1
#define CONFIG_VAAPI_ENCODE_EXAMPLE 0
#define CONFIG_VAAPI_TRANSCODE_EXAMPLE 0
#define CONFIG_AVISYNTH 0
#define CONFIG_FREI0R 0
#define CONFIG_LIBCDIO 0
#define CONFIG_LIBDAVS2 0
#define CONFIG_LIBRUBBERBAND 0
#define CONFIG_LIBVIDSTAB 0
#define CONFIG_LIBX264 0
#define CONFIG_LIBX265 0
#define CONFIG_LIBXAVS 0
#define CONFIG_LIBXAVS2 0
#define CONFIG_LIBXVID 0
#define CONFIG_DECKLINK 0
#define CONFIG_LIBFDK_AAC 0
#define CONFIG_OPENSSL 0
#define CONFIG_LIBTLS 0
#define CONFIG_GMP 0
#define CONFIG_LIBARIBB24 0
#define CONFIG_LIBLENSFUN 0
#define CONFIG_LIBOPENCORE_AMRNB 0
#define CONFIG_LIBOPENCORE_AMRWB 0
#define CONFIG_LIBVMAF 0
#define CONFIG_LIBVO_AMRWBENC 0
#define CONFIG_MBEDTLS 0
#define CONFIG_RKMPP 0
#define CONFIG_LIBSMBCLIENT 0
#define CONFIG_CHROMAPRINT 0
#define CONFIG_GCRYPT 0
#define CONFIG_GNUTLS 0
#define CONFIG_JNI 0
#define CONFIG_LADSPA 0
#define CONFIG_LIBAOM 0
#define CONFIG_LIBASS 0
#define CONFIG_LIBBLURAY 0
#define CONFIG_LIBBS2B 0
#define CONFIG_LIBCACA 0
#define CONFIG_LIBCELT 0
#define CONFIG_LIBCODEC2 0
#define CONFIG_LIBDAV1D 0
#define CONFIG_LIBDC1394 0
#define CONFIG_LIBDRM 0
#define CONFIG_LIBFLITE 0
#define CONFIG_LIBFONTCONFIG 0
#define CONFIG_LIBFREETYPE 0
#define CONFIG_LIBFRIBIDI 0
#define CONFIG_LIBGLSLANG 0
#define CONFIG_LIBGME 0
#define CONFIG_LIBGSM 0
#define CONFIG_LIBIEC61883 0
#define CONFIG_LIBILBC 0
#define CONFIG_LIBJACK 0
#define CONFIG_LIBKLVANC 0
#define CONFIG_LIBKVAZAAR 0
#define CONFIG_LIBMODPLUG 0
#define CONFIG_LIBMP3LAME 0
#define CONFIG_LIBMYSOFA 0
#define CONFIG_LIBOPENCV 0
#define CONFIG_LIBOPENH264 0
#define CONFIG_LIBOPENJPEG 0
#define CONFIG_LIBOPENMPT 0
#define CONFIG_LIBOPUS 0
#define CONFIG_LIBPULSE 0
#define CONFIG_LIBRABBITMQ 0
#define CONFIG_LIBRAV1E 0
#define CONFIG_LIBRSVG 0
#define CONFIG_LIBRTMP 0
#define CONFIG_LIBSHINE 0
#define CONFIG_LIBSMBCLIENT 0
#define CONFIG_LIBSNAPPY 0
#define CONFIG_LIBSOXR 0
#define CONFIG_LIBSPEEX 0
#define CONFIG_LIBSRT 0
#define CONFIG_LIBSSH 0
#define CONFIG_LIBTENSORFLOW 0
#define CONFIG_LIBTESSERACT 0
#define CONFIG_LIBTHEORA 0
#define CONFIG_LIBTWOLAME 0
#define CONFIG_LIBV4L2 0
#define CONFIG_LIBVORBIS 0
#define CONFIG_LIBVPX 0
#define CONFIG_LIBWAVPACK 0
#define CONFIG_LIBWEBP 0
#define CONFIG_LIBXML2 0
#define CONFIG_LIBZIMG 0
#define CONFIG_LIBZMQ 0
#define CONFIG_LIBZVBI 0
#define CONFIG_LV2 0
#define CONFIG_MEDIACODEC 0
#define CONFIG_OPENAL 0
#define CONFIG_OPENGL 0
#define CONFIG_POCKETSPHINX 0
#define CONFIG_VAPOURSYNTH 0
#define CONFIG_ALSA 0
#define CONFIG_APPKIT 0
#define CONFIG_AVFOUNDATION 0
#define CONFIG_BZLIB 0
#define CONFIG_COREIMAGE 0
#define CONFIG_ICONV 0
#define CONFIG_LIBXCB 0
#define CONFIG_LIBXCB_SHM 0
#define CONFIG_LIBXCB_SHAPE 0
#define CONFIG_LIBXCB_XFIXES 0
#define CONFIG_LZMA 0
#define CONFIG_MEDIAFOUNDATION 0
#define CONFIG_SCHANNEL 0
#define CONFIG_SDL2 0
#define CONFIG_SECURETRANSPORT 0
#define CONFIG_SNDIO 0
#define CONFIG_XLIB 0
#define CONFIG_ZLIB 0
#define CONFIG_CUDA_NVCC 0
#define CONFIG_CUDA_SDK 0
#define CONFIG_LIBNPP 0
#define CONFIG_LIBMFX 0
#define CONFIG_MMAL 0
#define CONFIG_OMX 0
#define CONFIG_OPENCL 0
#define CONFIG_VULKAN 0
#define CONFIG_AMF 0
#define CONFIG_AUDIOTOOLBOX 0
#define CONFIG_CRYSTALHD 0
#define CONFIG_CUDA 0
#define CONFIG_CUDA_LLVM 0
#define CONFIG_CUVID 0
#define CONFIG_D3D11VA 0
#define CONFIG_DXVA2 0
#define CONFIG_FFNVCODEC 0
#define CONFIG_NVDEC 0
#define CONFIG_NVENC 0
#define CONFIG_VAAPI 0
#define CONFIG_VDPAU 0
#define CONFIG_VIDEOTOOLBOX 0
#define CONFIG_V4L2_M2M 0
#define CONFIG_XVMC 0
#define CONFIG_FTRAPV 0
#define CONFIG_GRAY 0
#define CONFIG_HARDCODED_TABLES 0
#define CONFIG_OMX_RPI 0
#define CONFIG_RUNTIME_CPUDETECT 1
#define CONFIG_SAFE_BITSTREAM_READER 1
#define CONFIG_SHARED 0
#define CONFIG_SMALL 0
#define CONFIG_STATIC 1
#define CONFIG_SWSCALE_ALPHA 1
#define CONFIG_GPL 0
#define CONFIG_NONFREE 0
#define CONFIG_VERSION3 0
#define CONFIG_AVDEVICE 1
#define CONFIG_AVFILTER 1
#define CONFIG_SWSCALE 1
#define CONFIG_POSTPROC 0
#define CONFIG_AVFORMAT 1
#define CONFIG_AVCODEC 1
#define CONFIG_SWRESAMPLE 1
#define CONFIG_AVRESAMPLE 0
#define CONFIG_AVUTIL 1
#define CONFIG_FFPLAY 0
#define CONFIG_FFPROBE 0
#define CONFIG_FFMPEG 1
#define CONFIG_DCT 1
#define CONFIG_DWT 1
#define CONFIG_ERROR_RESILIENCE 1
#define CONFIG_FAAN 1
#define CONFIG_FAST_UNALIGNED 1
#define CONFIG_FFT 1
#define CONFIG_LSP 1
#define CONFIG_LZO 1
#define CONFIG_MDCT 1
#define CONFIG_PIXELUTILS 1
#define CONFIG_NETWORK 1
#define CONFIG_RDFT 1
#define CONFIG_AUTODETECT 0
#define CONFIG_FONTCONFIG 0
#define CONFIG_LARGE_TESTS 1
#define CONFIG_LINUX_PERF 0
#define CONFIG_MEMORY_POISONING 0
#define CONFIG_NEON_CLOBBER_TEST 0
#define CONFIG_OSSFUZZ 0
#define CONFIG_PIC 1
#define CONFIG_THUMB 0
#define CONFIG_VALGRIND_BACKTRACE 0
#define CONFIG_XMM_CLOBBER_TEST 0
#define CONFIG_BSFS 1
#define CONFIG_DECODERS 1
#define CONFIG_ENCODERS 1
#define CONFIG_HWACCELS 0
#define CONFIG_PARSERS 1
#define CONFIG_INDEVS 1
#define CONFIG_OUTDEVS 0
#define CONFIG_FILTERS 1
#define CONFIG_DEMUXERS 1
#define CONFIG_MUXERS 1
#define CONFIG_PROTOCOLS 1
#define CONFIG_AANDCTTABLES 1
#define CONFIG_AC3DSP 1
#define CONFIG_ADTS_HEADER 1
#define CONFIG_AUDIO_FRAME_QUEUE 1
#define CONFIG_AUDIODSP 1
#define CONFIG_BLOCKDSP 1
#define CONFIG_BSWAPDSP 1
#define CONFIG_CABAC 1
#define CONFIG_CBS 1
#define CONFIG_CBS_AV1 1
#define CONFIG_CBS_H264 1
#define CONFIG_CBS_H265 1
#define CONFIG_CBS_JPEG 0
#define CONFIG_CBS_MPEG2 1
#define CONFIG_CBS_VP9 1
#define CONFIG_DIRAC_PARSE 1
#define CONFIG_DNN 1
#define CONFIG_DVPROFILE 1
#define CONFIG_EXIF 1
#define CONFIG_FAANDCT 1
#define CONFIG_FAANIDCT 1
#define CONFIG_FDCTDSP 1
#define CONFIG_FLACDSP 1
#define CONFIG_FMTCONVERT 1
#define CONFIG_FRAME_THREAD_ENCODER 1
#define CONFIG_G722DSP 1
#define CONFIG_GOLOMB 1
#define CONFIG_GPLV3 0
#define CONFIG_H263DSP 1
#define CONFIG_H264CHROMA 1
#define CONFIG_H264DSP 1
#define CONFIG_H264PARSE 1
#define CONFIG_H264PRED 1
#define CONFIG_H264QPEL 1
#define CONFIG_HEVCPARSE 1
#define CONFIG_HPELDSP 1
#define CONFIG_HUFFMAN 1
#define CONFIG_HUFFYUVDSP 1
#define CONFIG_HUFFYUVENCDSP 1
#define CONFIG_IDCTDSP 1
#define CONFIG_IIRFILTER 1
#define CONFIG_MDCT15 1
#define CONFIG_INTRAX8 1
#define CONFIG_ISO_MEDIA 1
#define CONFIG_IVIDSP 1
#define CONFIG_JPEGTABLES 1
#define CONFIG_LGPLV3 0
#define CONFIG_LIBX262 0
#define CONFIG_LLAUDDSP 1
#define CONFIG_LLVIDDSP 1
#define CONFIG_LLVIDENCDSP 1
#define CONFIG_LPC 1
#define CONFIG_LZF 1
#define CONFIG_ME_CMP 1
#define CONFIG_MPEG_ER 1
#define CONFIG_MPEGAUDIO 1
#define CONFIG_MPEGAUDIODSP 1
#define CONFIG_MPEGAUDIOHEADER 1
#define CONFIG_MPEGVIDEO 1
#define CONFIG_MPEGVIDEOENC 1
#define CONFIG_MSS34DSP 1
#define CONFIG_PIXBLOCKDSP 1
#define CONFIG_QPELDSP 1
#define CONFIG_QSV 0
#define CONFIG_QSVDEC 0
#define CONFIG_QSVENC 0
#define CONFIG_QSVVPP 0
#define CONFIG_RANGECODER 1
#define CONFIG_RIFFDEC 1
#define CONFIG_RIFFENC 1
#define CONFIG_RTPDEC 1
#define CONFIG_RTPENC_CHAIN 1
#define CONFIG_RV34DSP 1
#define CONFIG_SCENE_SAD 1
#define CONFIG_SINEWIN 1
#define CONFIG_SNAPPY 1
#define CONFIG_SRTP 1
#define CONFIG_STARTCODE 1
#define CONFIG_TEXTUREDSP 1
#define CONFIG_TEXTUREDSPENC 0
#define CONFIG_TPELDSP 1
#define CONFIG_VAAPI_1 0
#define CONFIG_VAAPI_ENCODE 0
#define CONFIG_VC1DSP 1
#define CONFIG_VIDEODSP 1
#define CONFIG_VP3DSP 1
#define CONFIG_VP56DSP 1
#define CONFIG_VP8DSP 1
#define CONFIG_WMA_FREQS 1
#define CONFIG_WMV2DSP 1
#define CONFIG_AAC_ADTSTOASC_BSF 1
#define CONFIG_AV1_FRAME_MERGE_BSF 1
#define CONFIG_AV1_FRAME_SPLIT_BSF 1
#define CONFIG_AV1_METADATA_BSF 1
#define CONFIG_CHOMP_BSF 1
#define CONFIG_DUMP_EXTRADATA_BSF 1
#define CONFIG_DCA_CORE_BSF 1
#define CONFIG_EAC3_CORE_BSF 1
#define CONFIG_EXTRACT_EXTRADATA_BSF 1
#define CONFIG_FILTER_UNITS_BSF 1
#define CONFIG_H264_METADATA_BSF 1
#define CONFIG_H264_MP4TOANNEXB_BSF 1
#define CONFIG_H264_REDUNDANT_PPS_BSF 1
#define CONFIG_HAPQA_EXTRACT_BSF 1
#define CONFIG_HEVC_METADATA_BSF 1
#define CONFIG_HEVC_MP4TOANNEXB_BSF 1
#define CONFIG_IMX_DUMP_HEADER_BSF 1
#define CONFIG_MJPEG2JPEG_BSF 1
#define CONFIG_MJPEGA_DUMP_HEADER_BSF 1
#define CONFIG_MP3_HEADER_DECOMPRESS_BSF 1
#define CONFIG_MPEG2_METADATA_BSF 1
#define CONFIG_MPEG4_UNPACK_BFRAMES_BSF 1
#define CONFIG_MOV2TEXTSUB_BSF 1
#define CONFIG_NOISE_BSF 1
#define CONFIG_NULL_BSF 1
#define CONFIG_OPUS_METADATA_BSF 1
#define CONFIG_PCM_RECHUNK_BSF 1
#define CONFIG_PRORES_METADATA_BSF 1
#define CONFIG_REMOVE_EXTRADATA_BSF 1
#define CONFIG_TEXT2MOVSUB_BSF 1
#define CONFIG_TRACE_HEADERS_BSF 1
#define CONFIG_TRUEHD_CORE_BSF 1
#define CONFIG_VP9_METADATA_BSF 1
#define CONFIG_VP9_RAW_REORDER_BSF 1
#define CONFIG_VP9_SUPERFRAME_BSF 1
#define CONFIG_VP9_SUPERFRAME_SPLIT_BSF 1
#define CONFIG_AASC_DECODER 1
#define CONFIG_AIC_DECODER 1
#define CONFIG_ALIAS_PIX_DECODER 1
#define CONFIG_AGM_DECODER 1
#define CONFIG_AMV_DECODER 1
#define CONFIG_ANM_DECODER 1
#define CONFIG_ANSI_DECODER 1
#define CONFIG_APNG_DECODER 0
#define CONFIG_ARBC_DECODER 1
#define CONFIG_ASV1_DECODER 1
#define CONFIG_ASV2_DECODER 1
#define CONFIG_AURA_DECODER 1
#define CONFIG_AURA2_DECODER 1
#define CONFIG_AVRP_DECODER 1
#define CONFIG_AVRN_DECODER 1
#define CONFIG_AVS_DECODER 1
#define CONFIG_AVUI_DECODER 1
#define CONFIG_AYUV_DECODER 1
#define CONFIG_BETHSOFTVID_DECODER 1
#define CONFIG_BFI_DECODER 1
#define CONFIG_BINK_DECODER 1
#define CONFIG_BITPACKED_DECODER 1
#define CONFIG_BMP_DECODER 1
#define CONFIG_BMV_VIDEO_DECODER 1
#define CONFIG_BRENDER_PIX_DECODER 1
#define CONFIG_C93_DECODER 1
#define CONFIG_CAVS_DECODER 1
#define CONFIG_CDGRAPHICS_DECODER 1
#define CONFIG_CDTOONS_DECODER 1
#define CONFIG_CDXL_DECODER 1
#define CONFIG_CFHD_DECODER 1
#define CONFIG_CINEPAK_DECODER 1
#define CONFIG_CLEARVIDEO_DECODER 1
#define CONFIG_CLJR_DECODER 1
#define CONFIG_CLLC_DECODER 1
#define CONFIG_COMFORTNOISE_DECODER 1
#define CONFIG_CPIA_DECODER 1
#define CONFIG_CSCD_DECODER 1
#define CONFIG_CYUV_DECODER 1
#define CONFIG_DDS_DECODER 1
#define CONFIG_DFA_DECODER 1
#define CONFIG_DIRAC_DECODER 1
#define CONFIG_DNXHD_DECODER 1
#define CONFIG_DPX_DECODER 1
#define CONFIG_DSICINVIDEO_DECODER 1
#define CONFIG_DVAUDIO_DECODER 1
#define CONFIG_DVVIDEO_DECODER 1
#define CONFIG_DXA_DECODER 0
#define CONFIG_DXTORY_DECODER 1
#define CONFIG_DXV_DECODER 1
#define CONFIG_EACMV_DECODER 1
#define CONFIG_EAMAD_DECODER 1
#define CONFIG_EATGQ_DECODER 1
#define CONFIG_EATGV_DECODER 1
#define CONFIG_EATQI_DECODER 1
#define CONFIG_EIGHTBPS_DECODER 1
#define CONFIG_EIGHTSVX_EXP_DECODER 1
#define CONFIG_EIGHTSVX_FIB_DECODER 1
#define CONFIG_ESCAPE124_DECODER 1
#define CONFIG_ESCAPE130_DECODER 1
#define CONFIG_EXR_DECODER 0
#define CONFIG_FFV1_DECODER 1
#define CONFIG_FFVHUFF_DECODER 1
#define CONFIG_FIC_DECODER 1
#define CONFIG_FITS_DECODER 1
#define CONFIG_FLASHSV_DECODER 0
#define CONFIG_FLASHSV2_DECODER 0
#define CONFIG_FLIC_DECODER 1
#define CONFIG_FLV_DECODER 1
#define CONFIG_FMVC_DECODER 1
#define CONFIG_FOURXM_DECODER 1
#define CONFIG_FRAPS_DECODER 1
#define CONFIG_FRWU_DECODER 1
#define CONFIG_G2M_DECODER 0
#define CONFIG_GDV_DECODER 1
#define CONFIG_GIF_DECODER 1
#define CONFIG_H261_DECODER 1
#define CONFIG_H263_DECODER 1
#define CONFIG_H263I_DECODER 1
#define CONFIG_H263P_DECODER 1
#define CONFIG_H263_V4L2M2M_DECODER 0
#define CONFIG_H264_DECODER 1
#define CONFIG_H264_CRYSTALHD_DECODER 0
#define CONFIG_H264_V4L2M2M_DECODER 0
#define CONFIG_H264_MEDIACODEC_DECODER 0
#define CONFIG_H264_MMAL_DECODER 0
#define CONFIG_H264_QSV_DECODER 0
#define CONFIG_H264_RKMPP_DECODER 0
#define CONFIG_HAP_DECODER 1
#define CONFIG_HEVC_DECODER 1
#define CONFIG_HEVC_QSV_DECODER 0
#define CONFIG_HEVC_RKMPP_DECODER 0
#define CONFIG_HEVC_V4L2M2M_DECODER 0
#define CONFIG_HNM4_VIDEO_DECODER 1
#define CONFIG_HQ_HQA_DECODER 1
#define CONFIG_HQX_DECODER 1
#define CONFIG_HUFFYUV_DECODER 1
#define CONFIG_HYMT_DECODER 1
#define CONFIG_IDCIN_DECODER 1
#define CONFIG_IFF_ILBM_DECODER 1
#define CONFIG_IMM4_DECODER 1
#define CONFIG_IMM5_DECODER 1
#define CONFIG_INDEO2_DECODER 1
#define CONFIG_INDEO3_DECODER 1
#define CONFIG_INDEO4_DECODER 1
#define CONFIG_INDEO5_DECODER 1
#define CONFIG_INTERPLAY_VIDEO_DECODER 1
#define CONFIG_JPEG2000_DECODER 1
#define CONFIG_JPEGLS_DECODER 1
#define CONFIG_JV_DECODER 1
#define CONFIG_KGV1_DECODER 1
#define CONFIG_KMVC_DECODER 1
#define CONFIG_LAGARITH_DECODER 1
#define CONFIG_LOCO_DECODER 1
#define CONFIG_LSCR_DECODER 0
#define CONFIG_M101_DECODER 1
#define CONFIG_MAGICYUV_DECODER 1
#define CONFIG_MDEC_DECODER 1
#define CONFIG_MIMIC_DECODER 1
#define CONFIG_MJPEG_DECODER 1
#define CONFIG_MJPEGB_DECODER 1
#define CONFIG_MMVIDEO_DECODER 1
#define CONFIG_MOTIONPIXELS_DECODER 1
#define CONFIG_MPEG1VIDEO_DECODER 1
#define CONFIG_MPEG2VIDEO_DECODER 1
#define CONFIG_MPEG4_DECODER 1
#define CONFIG_MPEG4_CRYSTALHD_DECODER 0
#define CONFIG_MPEG4_V4L2M2M_DECODER 0
#define CONFIG_MPEG4_MMAL_DECODER 0
#define CONFIG_MPEGVIDEO_DECODER 1
#define CONFIG_MPEG1_V4L2M2M_DECODER 0
#define CONFIG_MPEG2_MMAL_DECODER 0
#define CONFIG_MPEG2_CRYSTALHD_DECODER 0
#define CONFIG_MPEG2_V4L2M2M_DECODER 0
#define CONFIG_MPEG2_QSV_DECODER 0
#define CONFIG_MPEG2_MEDIACODEC_DECODER 0
#define CONFIG_MSA1_DECODER 1
#define CONFIG_MSCC_DECODER 0
#define CONFIG_MSMPEG4V1_DECODER 1
#define CONFIG_MSMPEG4V2_DECODER 1
#define CONFIG_MSMPEG4V3_DECODER 1
#define CONFIG_MSMPEG4_CRYSTALHD_DECODER 0
#define CONFIG_MSRLE_DECODER 1
#define CONFIG_MSS1_DECODER 1
#define CONFIG_MSS2_DECODER 1
#define CONFIG_MSVIDEO1_DECODER 1
#define CONFIG_MSZH_DECODER 1
#define CONFIG_MTS2_DECODER 1
#define CONFIG_MV30_DECODER 1
#define CONFIG_MVC1_DECODER 1
#define CONFIG_MVC2_DECODER 1
#define CONFIG_MVDV_DECODER 1
#define CONFIG_MVHA_DECODER 0
#define CONFIG_MWSC_DECODER 0
#define CONFIG_MXPEG_DECODER 1
#define CONFIG_NOTCHLC_DECODER 1
#define CONFIG_NUV_DECODER 1
#define CONFIG_PAF_VIDEO_DECODER 1
#define CONFIG_PAM_DECODER 1
#define CONFIG_PBM_DECODER 1
#define CONFIG_PCX_DECODER 1
#define CONFIG_PFM_DECODER 1
#define CONFIG_PGM_DECODER 1
#define CONFIG_PGMYUV_DECODER 1
#define CONFIG_PICTOR_DECODER 1
#define CONFIG_PIXLET_DECODER 1
#define CONFIG_PNG_DECODER 0
#define CONFIG_PPM_DECODER 1
#define CONFIG_PRORES_DECODER 1
#define CONFIG_PROSUMER_DECODER 1
#define CONFIG_PSD_DECODER 1
#define CONFIG_PTX_DECODER 1
#define CONFIG_QDRAW_DECODER 1
#define CONFIG_QPEG_DECODER 1
#define CONFIG_QTRLE_DECODER 1
#define CONFIG_R10K_DECODER 1
#define CONFIG_R210_DECODER 1
#define CONFIG_RASC_DECODER 0
#define CONFIG_RAWVIDEO_DECODER 1
#define CONFIG_RL2_DECODER 1
#define CONFIG_ROQ_DECODER 1
#define CONFIG_RPZA_DECODER 1
#define CONFIG_RSCC_DECODER 0
#define CONFIG_RV10_DECODER 1
#define CONFIG_RV20_DECODER 1
#define CONFIG_RV30_DECODER 1
#define CONFIG_RV40_DECODER 1
#define CONFIG_S302M_DECODER 1
#define CONFIG_SANM_DECODER 1
#define CONFIG_SCPR_DECODER 1
#define CONFIG_SCREENPRESSO_DECODER 0
#define CONFIG_SGI_DECODER 1
#define CONFIG_SGIRLE_DECODER 1
#define CONFIG_SHEERVIDEO_DECODER 1
#define CONFIG_SMACKER_DECODER 1
#define CONFIG_SMC_DECODER 1
#define CONFIG_SMVJPEG_DECODER 1
#define CONFIG_SNOW_DECODER 1
#define CONFIG_SP5X_DECODER 1
#define CONFIG_SPEEDHQ_DECODER 1
#define CONFIG_SRGC_DECODER 0
#define CONFIG_SUNRAST_DECODER 1
#define CONFIG_SVQ1_DECODER 1
#define CONFIG_SVQ3_DECODER 1
#define CONFIG_TARGA_DECODER 1
#define CONFIG_TARGA_Y216_DECODER 1
#define CONFIG_TDSC_DECODER 0
#define CONFIG_THEORA_DECODER 1
#define CONFIG_THP_DECODER 1
#define CONFIG_TIERTEXSEQVIDEO_DECODER 1
#define CONFIG_TIFF_DECODER 1
#define CONFIG_TMV_DECODER 1
#define CONFIG_TRUEMOTION1_DECODER 1
#define CONFIG_TRUEMOTION2_DECODER 1
#define CONFIG_TRUEMOTION2RT_DECODER 1
#define CONFIG_TSCC_DECODER 0
#define CONFIG_TSCC2_DECODER 1
#define CONFIG_TXD_DECODER 1
#define CONFIG_ULTI_DECODER 1
#define CONFIG_UTVIDEO_DECODER 1
#define CONFIG_V210_DECODER 1
#define CONFIG_V210X_DECODER 1
#define CONFIG_V308_DECODER 1
#define CONFIG_V408_DECODER 1
#define CONFIG_V410_DECODER 1
#define CONFIG_VB_DECODER 1
#define CONFIG_VBLE_DECODER 1
#define CONFIG_VC1_DECODER 1
#define CONFIG_VC1_CRYSTALHD_DECODER 0
#define CONFIG_VC1IMAGE_DECODER 1
#define CONFIG_VC1_MMAL_DECODER 0
#define CONFIG_VC1_QSV_DECODER 0
#define CONFIG_VC1_V4L2M2M_DECODER 0
#define CONFIG_VCR1_DECODER 1
#define CONFIG_VMDVIDEO_DECODER 1
#define CONFIG_VMNC_DECODER 1
#define CONFIG_VP3_DECODER 1
#define CONFIG_VP4_DECODER 1
#define CONFIG_VP5_DECODER 1
#define CONFIG_VP6_DECODER 1
#define CONFIG_VP6A_DECODER 1
#define CONFIG_VP6F_DECODER 1
#define CONFIG_VP7_DECODER 1
#define CONFIG_VP8_DECODER 1
#define CONFIG_VP8_RKMPP_DECODER 0
#define CONFIG_VP8_V4L2M2M_DECODER 0
#define CONFIG_VP9_DECODER 1
#define CONFIG_VP9_RKMPP_DECODER 0
#define CONFIG_VP9_V4L2M2M_DECODER 0
#define CONFIG_VQA_DECODER 1
#define CONFIG_WEBP_DECODER 1
#define CONFIG_WCMV_DECODER 0
#define CONFIG_WRAPPED_AVFRAME_DECODER 1
#define CONFIG_WMV1_DECODER 1
#define CONFIG_WMV2_DECODER 1
#define CONFIG_WMV3_DECODER 1
#define CONFIG_WMV3_CRYSTALHD_DECODER 0
#define CONFIG_WMV3IMAGE_DECODER 1
#define CONFIG_WNV1_DECODER 1
#define CONFIG_XAN_WC3_DECODER 1
#define CONFIG_XAN_WC4_DECODER 1
#define CONFIG_XBM_DECODER 1
#define CONFIG_XFACE_DECODER 1
#define CONFIG_XL_DECODER 1
#define CONFIG_XPM_DECODER 1
#define CONFIG_XWD_DECODER 1
#define CONFIG_Y41P_DECODER 1
#define CONFIG_YLC_DECODER 1
#define CONFIG_YOP_DECODER 1
#define CONFIG_YUV4_DECODER 1
#define CONFIG_ZERO12V_DECODER 1
#define CONFIG_ZEROCODEC_DECODER 0
#define CONFIG_ZLIB_DECODER 0
#define CONFIG_ZMBV_DECODER 0
#define CONFIG_AAC_DECODER 1
#define CONFIG_AAC_FIXED_DECODER 1
#define CONFIG_AAC_LATM_DECODER 1
#define CONFIG_AC3_DECODER 1
#define CONFIG_AC3_FIXED_DECODER 1
#define CONFIG_ACELP_KELVIN_DECODER 1
#define CONFIG_ALAC_DECODER 1
#define CONFIG_ALS_DECODER 1
#define CONFIG_AMRNB_DECODER 1
#define CONFIG_AMRWB_DECODER 1
#define CONFIG_APE_DECODER 1
#define CONFIG_APTX_DECODER 1
#define CONFIG_APTX_HD_DECODER 1
#define CONFIG_ATRAC1_DECODER 1
#define CONFIG_ATRAC3_DECODER 1
#define CONFIG_ATRAC3AL_DECODER 1
#define CONFIG_ATRAC3P_DECODER 1
#define CONFIG_ATRAC3PAL_DECODER 1
#define CONFIG_ATRAC9_DECODER 1
#define CONFIG_BINKAUDIO_DCT_DECODER 1
#define CONFIG_BINKAUDIO_RDFT_DECODER 1
#define CONFIG_BMV_AUDIO_DECODER 1
#define CONFIG_COOK_DECODER 1
#define CONFIG_DCA_DECODER 1
#define CONFIG_DOLBY_E_DECODER 1
#define CONFIG_DSD_LSBF_DECODER 1
#define CONFIG_DSD_MSBF_DECODER 1
#define CONFIG_DSD_LSBF_PLANAR_DECODER 1
#define CONFIG_DSD_MSBF_PLANAR_DECODER 1
#define CONFIG_DSICINAUDIO_DECODER 1
#define CONFIG_DSS_SP_DECODER 1
#define CONFIG_DST_DECODER 1
#define CONFIG_EAC3_DECODER 1
#define CONFIG_EVRC_DECODER 1
#define CONFIG_FFWAVESYNTH_DECODER 1
#define CONFIG_FLAC_DECODER 1
#define CONFIG_G723_1_DECODER 1
#define CONFIG_G729_DECODER 1
#define CONFIG_GSM_DECODER 1
#define CONFIG_GSM_MS_DECODER 1
#define CONFIG_HCA_DECODER 1
#define CONFIG_HCOM_DECODER 1
#define CONFIG_IAC_DECODER 1
#define CONFIG_ILBC_DECODER 1
#define CONFIG_IMC_DECODER 1
#define CONFIG_INTERPLAY_ACM_DECODER 1
#define CONFIG_MACE3_DECODER 1
#define CONFIG_MACE6_DECODER 1
#define CONFIG_METASOUND_DECODER 1
#define CONFIG_MLP_DECODER 1
#define CONFIG_MP1_DECODER 1
#define CONFIG_MP1FLOAT_DECODER 1
#define CONFIG_MP2_DECODER 1
#define CONFIG_MP2FLOAT_DECODER 1
#define CONFIG_MP3FLOAT_DECODER 1
#define CONFIG_MP3_DECODER 1
#define CONFIG_MP3ADUFLOAT_DECODER 1
#define CONFIG_MP3ADU_DECODER 1
#define CONFIG_MP3ON4FLOAT_DECODER 1
#define CONFIG_MP3ON4_DECODER 1
#define CONFIG_MPC7_DECODER 1
#define CONFIG_MPC8_DECODER 1
#define CONFIG_NELLYMOSER_DECODER 1
#define CONFIG_ON2AVC_DECODER 1
#define CONFIG_OPUS_DECODER 1
#define CONFIG_PAF_AUDIO_DECODER 1
#define CONFIG_QCELP_DECODER 1
#define CONFIG_QDM2_DECODER 1
#define CONFIG_QDMC_DECODER 1
#define CONFIG_RA_144_DECODER 1
#define CONFIG_RA_288_DECODER 1
#define CONFIG_RALF_DECODER 1
#define CONFIG_SBC_DECODER 1
#define CONFIG_SHORTEN_DECODER 1
#define CONFIG_SIPR_DECODER 1
#define CONFIG_SIREN_DECODER 1
#define CONFIG_SMACKAUD_DECODER 1
#define CONFIG_SONIC_DECODER 1
#define CONFIG_TAK_DECODER 1
#define CONFIG_TRUEHD_DECODER 1
#define CONFIG_TRUESPEECH_DECODER 1
#define CONFIG_TTA_DECODER 1
#define CONFIG_TWINVQ_DECODER 1
#define CONFIG_VMDAUDIO_DECODER 1
#define CONFIG_VORBIS_DECODER 1
#define CONFIG_WAVPACK_DECODER 1
#define CONFIG_WMALOSSLESS_DECODER 1
#define CONFIG_WMAPRO_DECODER 1
#define CONFIG_WMAV1_DECODER 1
#define CONFIG_WMAV2_DECODER 1
#define CONFIG_WMAVOICE_DECODER 1
#define CONFIG_WS_SND1_DECODER 1
#define CONFIG_XMA1_DECODER 1
#define CONFIG_XMA2_DECODER 1
#define CONFIG_PCM_ALAW_DECODER 1
#define CONFIG_PCM_BLURAY_DECODER 1
#define CONFIG_PCM_DVD_DECODER 1
#define CONFIG_PCM_F16LE_DECODER 1
#define CONFIG_PCM_F24LE_DECODER 1
#define CONFIG_PCM_F32BE_DECODER 1
#define CONFIG_PCM_F32LE_DECODER 1
#define CONFIG_PCM_F64BE_DECODER 1
#define CONFIG_PCM_F64LE_DECODER 1
#define CONFIG_PCM_LXF_DECODER 1
#define CONFIG_PCM_MULAW_DECODER 1
#define CONFIG_PCM_S8_DECODER 1
#define CONFIG_PCM_S8_PLANAR_DECODER 1
#define CONFIG_PCM_S16BE_DECODER 1
#define CONFIG_PCM_S16BE_PLANAR_DECODER 1
#define CONFIG_PCM_S16LE_DECODER 1
#define CONFIG_PCM_S16LE_PLANAR_DECODER 1
#define CONFIG_PCM_S24BE_DECODER 1
#define CONFIG_PCM_S24DAUD_DECODER 1
#define CONFIG_PCM_S24LE_DECODER 1
#define CONFIG_PCM_S24LE_PLANAR_DECODER 1
#define CONFIG_PCM_S32BE_DECODER 1
#define CONFIG_PCM_S32LE_DECODER 1
#define CONFIG_PCM_S32LE_PLANAR_DECODER 1
#define CONFIG_PCM_S64BE_DECODER 1
#define CONFIG_PCM_S64LE_DECODER 1
#define CONFIG_PCM_U8_DECODER 1
#define CONFIG_PCM_U16BE_DECODER 1
#define CONFIG_PCM_U16LE_DECODER 1
#define CONFIG_PCM_U24BE_DECODER 1
#define CONFIG_PCM_U24LE_DECODER 1
#define CONFIG_PCM_U32BE_DECODER 1
#define CONFIG_PCM_U32LE_DECODER 1
#define CONFIG_PCM_VIDC_DECODER 1
#define CONFIG_DERF_DPCM_DECODER 1
#define CONFIG_GREMLIN_DPCM_DECODER 1
#define CONFIG_INTERPLAY_DPCM_DECODER 1
#define CONFIG_ROQ_DPCM_DECODER 1
#define CONFIG_SDX2_DPCM_DECODER 1
#define CONFIG_SOL_DPCM_DECODER 1
#define CONFIG_XAN_DPCM_DECODER 1
#define CONFIG_ADPCM_4XM_DECODER 1
#define CONFIG_ADPCM_ADX_DECODER 1
#define CONFIG_ADPCM_AFC_DECODER 1
#define CONFIG_ADPCM_AGM_DECODER 1
#define CONFIG_ADPCM_AICA_DECODER 1
#define CONFIG_ADPCM_ARGO_DECODER 1
#define CONFIG_ADPCM_CT_DECODER 1
#define CONFIG_ADPCM_DTK_DECODER 1
#define CONFIG_ADPCM_EA_DECODER 1
#define CONFIG_ADPCM_EA_MAXIS_XA_DECODER 1
#define CONFIG_ADPCM_EA_R1_DECODER 1
#define CONFIG_ADPCM_EA_R2_DECODER 1
#define CONFIG_ADPCM_EA_R3_DECODER 1
#define CONFIG_ADPCM_EA_XAS_DECODER 1
#define CONFIG_ADPCM_G722_DECODER 1
#define CONFIG_ADPCM_G726_DECODER 1
#define CONFIG_ADPCM_G726LE_DECODER 1
#define CONFIG_ADPCM_IMA_AMV_DECODER 1
#define CONFIG_ADPCM_IMA_ALP_DECODER 1
#define CONFIG_ADPCM_IMA_APC_DECODER 1
#define CONFIG_ADPCM_IMA_APM_DECODER 1
#define CONFIG_ADPCM_IMA_CUNNING_DECODER 1
#define CONFIG_ADPCM_IMA_DAT4_DECODER 1
#define CONFIG_ADPCM_IMA_DK3_DECODER 1
#define CONFIG_ADPCM_IMA_DK4_DECODER 1
#define CONFIG_ADPCM_IMA_EA_EACS_DECODER 1
#define CONFIG_ADPCM_IMA_EA_SEAD_DECODER 1
#define CONFIG_ADPCM_IMA_ISS_DECODER 1
#define CONFIG_ADPCM_IMA_MTF_DECODER 1
#define CONFIG_ADPCM_IMA_OKI_DECODER 1
#define CONFIG_ADPCM_IMA_QT_DECODER 1
#define CONFIG_ADPCM_IMA_RAD_DECODER 1
#define CONFIG_ADPCM_IMA_SSI_DECODER 1
#define CONFIG_ADPCM_IMA_SMJPEG_DECODER 1
#define CONFIG_ADPCM_IMA_WAV_DECODER 1
#define CONFIG_ADPCM_IMA_WS_DECODER 1
#define CONFIG_ADPCM_MS_DECODER 1
#define CONFIG_ADPCM_MTAF_DECODER 1
#define CONFIG_ADPCM_PSX_DECODER 1
#define CONFIG_ADPCM_SBPRO_2_DECODER 1
#define CONFIG_ADPCM_SBPRO_3_DECODER 1
#define CONFIG_ADPCM_SBPRO_4_DECODER 1
#define CONFIG_ADPCM_SWF_DECODER 1
#define CONFIG_ADPCM_THP_DECODER 1
#define CONFIG_ADPCM_THP_LE_DECODER 1
#define CONFIG_ADPCM_VIMA_DECODER 1
#define CONFIG_ADPCM_XA_DECODER 1
#define CONFIG_ADPCM_YAMAHA_DECODER 1
#define CONFIG_ADPCM_ZORK_DECODER 1
#define CONFIG_SSA_DECODER 1
#define CONFIG_ASS_DECODER 1
#define CONFIG_CCAPTION_DECODER 1
#define CONFIG_DVBSUB_DECODER 1
#define CONFIG_DVDSUB_DECODER 1
#define CONFIG_JACOSUB_DECODER 1
#define CONFIG_MICRODVD_DECODER 1
#define CONFIG_MOVTEXT_DECODER 1
#define CONFIG_MPL2_DECODER 1
#define CONFIG_PGSSUB_DECODER 1
#define CONFIG_PJS_DECODER 1
#define CONFIG_REALTEXT_DECODER 1
#define CONFIG_SAMI_DECODER 1
#define CONFIG_SRT_DECODER 1
#define CONFIG_STL_DECODER 1
#define CONFIG_SUBRIP_DECODER 1
#define CONFIG_SUBVIEWER_DECODER 1
#define CONFIG_SUBVIEWER1_DECODER 1
#define CONFIG_TEXT_DECODER 1
#define CONFIG_VPLAYER_DECODER 1
#define CONFIG_WEBVTT_DECODER 1
#define CONFIG_XSUB_DECODER 1
#define CONFIG_AAC_AT_DECODER 0
#define CONFIG_AC3_AT_DECODER 0
#define CONFIG_ADPCM_IMA_QT_AT_DECODER 0
#define CONFIG_ALAC_AT_DECODER 0
#define CONFIG_AMR_NB_AT_DECODER 0
#define CONFIG_EAC3_AT_DECODER 0
#define CONFIG_GSM_MS_AT_DECODER 0
#define CONFIG_ILBC_AT_DECODER 0
#define CONFIG_MP1_AT_DECODER 0
#define CONFIG_MP2_AT_DECODER 0
#define CONFIG_MP3_AT_DECODER 0
#define CONFIG_PCM_ALAW_AT_DECODER 0
#define CONFIG_PCM_MULAW_AT_DECODER 0
#define CONFIG_QDMC_AT_DECODER 0
#define CONFIG_QDM2_AT_DECODER 0
#define CONFIG_LIBARIBB24_DECODER 0
#define CONFIG_LIBCELT_DECODER 0
#define CONFIG_LIBCODEC2_DECODER 0
#define CONFIG_LIBDAV1D_DECODER 0
#define CONFIG_LIBDAVS2_DECODER 0
#define CONFIG_LIBFDK_AAC_DECODER 0
#define CONFIG_LIBGSM_DECODER 0
#define CONFIG_LIBGSM_MS_DECODER 0
#define CONFIG_LIBILBC_DECODER 0
#define CONFIG_LIBOPENCORE_AMRNB_DECODER 0
#define CONFIG_LIBOPENCORE_AMRWB_DECODER 0
#define CONFIG_LIBOPENJPEG_DECODER 0
#define CONFIG_LIBOPUS_DECODER 0
#define CONFIG_LIBRSVG_DECODER 0
#define CONFIG_LIBSPEEX_DECODER 0
#define CONFIG_LIBVORBIS_DECODER 0
#define CONFIG_LIBVPX_VP8_DECODER 0
#define CONFIG_LIBVPX_VP9_DECODER 0
#define CONFIG_LIBZVBI_TELETEXT_DECODER 0
#define CONFIG_BINTEXT_DECODER 1
#define CONFIG_XBIN_DECODER 1
#define CONFIG_IDF_DECODER 1
#define CONFIG_LIBAOM_AV1_DECODER 0
#define CONFIG_LIBOPENH264_DECODER 0
#define CONFIG_H264_CUVID_DECODER 0
#define CONFIG_HEVC_CUVID_DECODER 0
#define CONFIG_HEVC_MEDIACODEC_DECODER 0
#define CONFIG_MJPEG_CUVID_DECODER 0
#define CONFIG_MJPEG_QSV_DECODER 0
#define CONFIG_MPEG1_CUVID_DECODER 0
#define CONFIG_MPEG2_CUVID_DECODER 0
#define CONFIG_MPEG4_CUVID_DECODER 0
#define CONFIG_MPEG4_MEDIACODEC_DECODER 0
#define CONFIG_VC1_CUVID_DECODER 0
#define CONFIG_VP8_CUVID_DECODER 0
#define CONFIG_VP8_MEDIACODEC_DECODER 0
#define CONFIG_VP8_QSV_DECODER 0
#define CONFIG_VP9_CUVID_DECODER 0
#define CONFIG_VP9_MEDIACODEC_DECODER 0
#define CONFIG_VP9_QSV_DECODER 0
#define CONFIG_A64MULTI_ENCODER 1
#define CONFIG_A64MULTI5_ENCODER 1
#define CONFIG_ALIAS_PIX_ENCODER 1
#define CONFIG_AMV_ENCODER 1
#define CONFIG_APNG_ENCODER 0
#define CONFIG_ASV1_ENCODER 1
#define CONFIG_ASV2_ENCODER 1
#define CONFIG_AVRP_ENCODER 1
#define CONFIG_AVUI_ENCODER 1
#define CONFIG_AYUV_ENCODER 1
#define CONFIG_BMP_ENCODER 1
#define CONFIG_CINEPAK_ENCODER 1
#define CONFIG_CLJR_ENCODER 1
#define CONFIG_COMFORTNOISE_ENCODER 1
#define CONFIG_DNXHD_ENCODER 1
#define CONFIG_DPX_ENCODER 1
#define CONFIG_DVVIDEO_ENCODER 1
#define CONFIG_FFV1_ENCODER 1
#define CONFIG_FFVHUFF_ENCODER 1
#define CONFIG_FITS_ENCODER 1
#define CONFIG_FLASHSV_ENCODER 0
#define CONFIG_FLASHSV2_ENCODER 0
#define CONFIG_FLV_ENCODER 1
#define CONFIG_GIF_ENCODER 1
#define CONFIG_H261_ENCODER 1
#define CONFIG_H263_ENCODER 1
#define CONFIG_H263P_ENCODER 1
#define CONFIG_HAP_ENCODER 0
#define CONFIG_HUFFYUV_ENCODER 1
#define CONFIG_JPEG2000_ENCODER 1
#define CONFIG_JPEGLS_ENCODER 1
#define CONFIG_LJPEG_ENCODER 1
#define CONFIG_MAGICYUV_ENCODER 1
#define CONFIG_MJPEG_ENCODER 1
#define CONFIG_MPEG1VIDEO_ENCODER 1
#define CONFIG_MPEG2VIDEO_ENCODER 1
#define CONFIG_MPEG4_ENCODER 1
#define CONFIG_MSMPEG4V2_ENCODER 1
#define CONFIG_MSMPEG4V3_ENCODER 1
#define CONFIG_MSVIDEO1_ENCODER 1
#define CONFIG_PAM_ENCODER 1
#define CONFIG_PBM_ENCODER 1
#define CONFIG_PCX_ENCODER 1
#define CONFIG_PGM_ENCODER 1
#define CONFIG_PGMYUV_ENCODER 1
#define CONFIG_PNG_ENCODER 0
#define CONFIG_PPM_ENCODER 1
#define CONFIG_PRORES_ENCODER 1
#define CONFIG_PRORES_AW_ENCODER 1
#define CONFIG_PRORES_KS_ENCODER 1
#define CONFIG_QTRLE_ENCODER 1
#define CONFIG_R10K_ENCODER 1
#define CONFIG_R210_ENCODER 1
#define CONFIG_RAWVIDEO_ENCODER 1
#define CONFIG_ROQ_ENCODER 1
#define CONFIG_RV10_ENCODER 1
#define CONFIG_RV20_ENCODER 1
#define CONFIG_S302M_ENCODER 1
#define CONFIG_SGI_ENCODER 1
#define CONFIG_SNOW_ENCODER 1
#define CONFIG_SUNRAST_ENCODER 1
#define CONFIG_SVQ1_ENCODER 1
#define CONFIG_TARGA_ENCODER 1
#define CONFIG_TIFF_ENCODER 1
#define CONFIG_UTVIDEO_ENCODER 1
#define CONFIG_V210_ENCODER 1
#define CONFIG_V308_ENCODER 1
#define CONFIG_V408_ENCODER 1
#define CONFIG_V410_ENCODER 1
#define CONFIG_VC2_ENCODER 1
#define CONFIG_WRAPPED_AVFRAME_ENCODER 1
#define CONFIG_WMV1_ENCODER 1
#define CONFIG_WMV2_ENCODER 1
#define CONFIG_XBM_ENCODER 1
#define CONFIG_XFACE_ENCODER 1
#define CONFIG_XWD_ENCODER 1
#define CONFIG_Y41P_ENCODER 1
#define CONFIG_YUV4_ENCODER 1
#define CONFIG_ZLIB_ENCODER 0
#define CONFIG_ZMBV_ENCODER 0
#define CONFIG_AAC_ENCODER 1
#define CONFIG_AC3_ENCODER 1
#define CONFIG_AC3_FIXED_ENCODER 1
#define CONFIG_ALAC_ENCODER 1
#define CONFIG_APTX_ENCODER 1
#define CONFIG_APTX_HD_ENCODER 1
#define CONFIG_DCA_ENCODER 1
#define CONFIG_EAC3_ENCODER 1
#define CONFIG_FLAC_ENCODER 1
#define CONFIG_G723_1_ENCODER 1
#define CONFIG_MLP_ENCODER 1
#define CONFIG_MP2_ENCODER 1
#define CONFIG_MP2FIXED_ENCODER 1
#define CONFIG_NELLYMOSER_ENCODER 1
#define CONFIG_OPUS_ENCODER 1
#define CONFIG_RA_144_ENCODER 1
#define CONFIG_SBC_ENCODER 1
#define CONFIG_SONIC_ENCODER 1
#define CONFIG_SONIC_LS_ENCODER 1
#define CONFIG_TRUEHD_ENCODER 1
#define CONFIG_TTA_ENCODER 1
#define CONFIG_VORBIS_ENCODER 1
#define CONFIG_WAVPACK_ENCODER 1
#define CONFIG_WMAV1_ENCODER 1
#define CONFIG_WMAV2_ENCODER 1
#define CONFIG_PCM_ALAW_ENCODER 1
#define CONFIG_PCM_DVD_ENCODER 1
#define CONFIG_PCM_F32BE_ENCODER 1
#define CONFIG_PCM_F32LE_ENCODER 1
#define CONFIG_PCM_F64BE_ENCODER 1
#define CONFIG_PCM_F64LE_ENCODER 1
#define CONFIG_PCM_MULAW_ENCODER 1
#define CONFIG_PCM_S8_ENCODER 1
#define CONFIG_PCM_S8_PLANAR_ENCODER 1
#define CONFIG_PCM_S16BE_ENCODER 1
#define CONFIG_PCM_S16BE_PLANAR_ENCODER 1
#define CONFIG_PCM_S16LE_ENCODER 1
#define CONFIG_PCM_S16LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S24BE_ENCODER 1
#define CONFIG_PCM_S24DAUD_ENCODER 1
#define CONFIG_PCM_S24LE_ENCODER 1
#define CONFIG_PCM_S24LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S32BE_ENCODER 1
#define CONFIG_PCM_S32LE_ENCODER 1
#define CONFIG_PCM_S32LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S64BE_ENCODER 1
#define CONFIG_PCM_S64LE_ENCODER 1
#define CONFIG_PCM_U8_ENCODER 1
#define CONFIG_PCM_U16BE_ENCODER 1
#define CONFIG_PCM_U16LE_ENCODER 1
#define CONFIG_PCM_U24BE_ENCODER 1
#define CONFIG_PCM_U24LE_ENCODER 1
#define CONFIG_PCM_U32BE_ENCODER 1
#define CONFIG_PCM_U32LE_ENCODER 1
#define CONFIG_PCM_VIDC_ENCODER 1
#define CONFIG_ROQ_DPCM_ENCODER 1
#define CONFIG_ADPCM_ADX_ENCODER 1
#define CONFIG_ADPCM_G722_ENCODER 1
#define CONFIG_ADPCM_G726_ENCODER 1
#define CONFIG_ADPCM_G726LE_ENCODER 1
#define CONFIG_ADPCM_IMA_QT_ENCODER 1
#define CONFIG_ADPCM_IMA_SSI_ENCODER 1
#define CONFIG_ADPCM_IMA_WAV_ENCODER 1
#define CONFIG_ADPCM_MS_ENCODER 1
#define CONFIG_ADPCM_SWF_ENCODER 1
#define CONFIG_ADPCM_YAMAHA_ENCODER 1
#define CONFIG_SSA_ENCODER 1
#define CONFIG_ASS_ENCODER 1
#define CONFIG_DVBSUB_ENCODER 1
#define CONFIG_DVDSUB_ENCODER 1
#define CONFIG_MOVTEXT_ENCODER 1
#define CONFIG_SRT_ENCODER 1
#define CONFIG_SUBRIP_ENCODER 1
#define CONFIG_TEXT_ENCODER 1
#define CONFIG_WEBVTT_ENCODER 1
#define CONFIG_XSUB_ENCODER 1
#define CONFIG_AAC_AT_ENCODER 0
#define CONFIG_AAC_MF_ENCODER 0
#define CONFIG_AC3_MF_ENCODER 0
#define CONFIG_ALAC_AT_ENCODER 0
#define CONFIG_ILBC_AT_ENCODER 0
#define CONFIG_MP3_MF_ENCODER 0
#define CONFIG_PCM_ALAW_AT_ENCODER 0
#define CONFIG_PCM_MULAW_AT_ENCODER 0
#define CONFIG_LIBAOM_AV1_ENCODER 0
#define CONFIG_LIBCODEC2_ENCODER 0
#define CONFIG_LIBFDK_AAC_ENCODER 0
#define CONFIG_LIBGSM_ENCODER 0
#define CONFIG_LIBGSM_MS_ENCODER 0
#define CONFIG_LIBILBC_ENCODER 0
#define CONFIG_LIBMP3LAME_ENCODER 0
#define CONFIG_LIBOPENCORE_AMRNB_ENCODER 0
#define CONFIG_LIBOPENJPEG_ENCODER 0
#define CONFIG_LIBOPUS_ENCODER 0
#define CONFIG_LIBRAV1E_ENCODER 0
#define CONFIG_LIBSHINE_ENCODER 0
#define CONFIG_LIBSPEEX_ENCODER 0
#define CONFIG_LIBTHEORA_ENCODER 0
#define CONFIG_LIBTWOLAME_ENCODER 0
#define CONFIG_LIBVO_AMRWBENC_ENCODER 0
#define CONFIG_LIBVORBIS_ENCODER 0
#define CONFIG_LIBVPX_VP8_ENCODER 0
#define CONFIG_LIBVPX_VP9_ENCODER 0
#define CONFIG_LIBWAVPACK_ENCODER 0
#define CONFIG_LIBWEBP_ANIM_ENCODER 0
#define CONFIG_LIBWEBP_ENCODER 0
#define CONFIG_LIBX262_ENCODER 0
#define CONFIG_LIBX264_ENCODER 0
#define CONFIG_LIBX264RGB_ENCODER 0
#define CONFIG_LIBX265_ENCODER 0
#define CONFIG_LIBXAVS_ENCODER 0
#define CONFIG_LIBXAVS2_ENCODER 0
#define CONFIG_LIBXVID_ENCODER 0
#define CONFIG_H263_V4L2M2M_ENCODER 0
#define CONFIG_LIBOPENH264_ENCODER 0
#define CONFIG_H264_AMF_ENCODER 0
#define CONFIG_H264_MF_ENCODER 0
#define CONFIG_H264_NVENC_ENCODER 0
#define CONFIG_H264_OMX_ENCODER 0
#define CONFIG_H264_QSV_ENCODER 0
#define CONFIG_H264_V4L2M2M_ENCODER 0
#define CONFIG_H264_VAAPI_ENCODER 0
#define CONFIG_H264_VIDEOTOOLBOX_ENCODER 0
#define CONFIG_NVENC_ENCODER 0
#define CONFIG_NVENC_H264_ENCODER 0
#define CONFIG_NVENC_HEVC_ENCODER 0
#define CONFIG_HEVC_AMF_ENCODER 0
#define CONFIG_HEVC_MF_ENCODER 0
#define CONFIG_HEVC_NVENC_ENCODER 0
#define CONFIG_HEVC_QSV_ENCODER 0
#define CONFIG_HEVC_V4L2M2M_ENCODER 0
#define CONFIG_HEVC_VAAPI_ENCODER 0
#define CONFIG_HEVC_VIDEOTOOLBOX_ENCODER 0
#define CONFIG_LIBKVAZAAR_ENCODER 0
#define CONFIG_MJPEG_QSV_ENCODER 0
#define CONFIG_MJPEG_VAAPI_ENCODER 0
#define CONFIG_MPEG2_QSV_ENCODER 0
#define CONFIG_MPEG2_VAAPI_ENCODER 0
#define CONFIG_MPEG4_OMX_ENCODER 0
#define CONFIG_MPEG4_V4L2M2M_ENCODER 0
#define CONFIG_VP8_V4L2M2M_ENCODER 0
#define CONFIG_VP8_VAAPI_ENCODER 0
#define CONFIG_VP9_VAAPI_ENCODER 0
#define CONFIG_VP9_QSV_ENCODER 0
#define CONFIG_H263_VAAPI_HWACCEL 0
#define CONFIG_H263_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_H264_D3D11VA_HWACCEL 0
#define CONFIG_H264_D3D11VA2_HWACCEL 0
#define CONFIG_H264_DXVA2_HWACCEL 0
#define CONFIG_H264_NVDEC_HWACCEL 0
#define CONFIG_H264_VAAPI_HWACCEL 0
#define CONFIG_H264_VDPAU_HWACCEL 0
#define CONFIG_H264_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_HEVC_D3D11VA_HWACCEL 0
#define CONFIG_HEVC_D3D11VA2_HWACCEL 0
#define CONFIG_HEVC_DXVA2_HWACCEL 0
#define CONFIG_HEVC_NVDEC_HWACCEL 0
#define CONFIG_HEVC_VAAPI_HWACCEL 0
#define CONFIG_HEVC_VDPAU_HWACCEL 0
#define CONFIG_HEVC_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MJPEG_NVDEC_HWACCEL 0
#define CONFIG_MJPEG_VAAPI_HWACCEL 0
#define CONFIG_MPEG1_NVDEC_HWACCEL 0
#define CONFIG_MPEG1_VDPAU_HWACCEL 0
#define CONFIG_MPEG1_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MPEG1_XVMC_HWACCEL 0
#define CONFIG_MPEG2_D3D11VA_HWACCEL 0
#define CONFIG_MPEG2_D3D11VA2_HWACCEL 0
#define CONFIG_MPEG2_NVDEC_HWACCEL 0
#define CONFIG_MPEG2_DXVA2_HWACCEL 0
#define CONFIG_MPEG2_VAAPI_HWACCEL 0
#define CONFIG_MPEG2_VDPAU_HWACCEL 0
#define CONFIG_MPEG2_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MPEG2_XVMC_HWACCEL 0
#define CONFIG_MPEG4_NVDEC_HWACCEL 0
#define CONFIG_MPEG4_VAAPI_HWACCEL 0
#define CONFIG_MPEG4_VDPAU_HWACCEL 0
#define CONFIG_MPEG4_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_VC1_D3D11VA_HWACCEL 0
#define CONFIG_VC1_D3D11VA2_HWACCEL 0
#define CONFIG_VC1_DXVA2_HWACCEL 0
#define CONFIG_VC1_NVDEC_HWACCEL 0
#define CONFIG_VC1_VAAPI_HWACCEL 0
#define CONFIG_VC1_VDPAU_HWACCEL 0
#define CONFIG_VP8_NVDEC_HWACCEL 0
#define CONFIG_VP8_VAAPI_HWACCEL 0
#define CONFIG_VP9_D3D11VA_HWACCEL 0
#define CONFIG_VP9_D3D11VA2_HWACCEL 0
#define CONFIG_VP9_DXVA2_HWACCEL 0
#define CONFIG_VP9_NVDEC_HWACCEL 0
#define CONFIG_VP9_VAAPI_HWACCEL 0
#define CONFIG_VP9_VDPAU_HWACCEL 0
#define CONFIG_WMV3_D3D11VA_HWACCEL 0
#define CONFIG_WMV3_D3D11VA2_HWACCEL 0
#define CONFIG_WMV3_DXVA2_HWACCEL 0
#define CONFIG_WMV3_NVDEC_HWACCEL 0
#define CONFIG_WMV3_VAAPI_HWACCEL 0
#define CONFIG_WMV3_VDPAU_HWACCEL 0
#define CONFIG_AAC_PARSER 1
#define CONFIG_AAC_LATM_PARSER 1
#define CONFIG_AC3_PARSER 1
#define CONFIG_ADX_PARSER 1
#define CONFIG_AV1_PARSER 1
#define CONFIG_AVS2_PARSER 1
#define CONFIG_BMP_PARSER 1
#define CONFIG_CAVSVIDEO_PARSER 1
#define CONFIG_COOK_PARSER 1
#define CONFIG_DCA_PARSER 1
#define CONFIG_DIRAC_PARSER 1
#define CONFIG_DNXHD_PARSER 1
#define CONFIG_DPX_PARSER 1
#define CONFIG_DVAUDIO_PARSER 1
#define CONFIG_DVBSUB_PARSER 1
#define CONFIG_DVDSUB_PARSER 1
#define CONFIG_DVD_NAV_PARSER 1
#define CONFIG_FLAC_PARSER 1
#define CONFIG_G723_1_PARSER 1
#define CONFIG_G729_PARSER 1
#define CONFIG_GIF_PARSER 1
#define CONFIG_GSM_PARSER 1
#define CONFIG_H261_PARSER 1
#define CONFIG_H263_PARSER 1
#define CONFIG_H264_PARSER 1
#define CONFIG_HEVC_PARSER 1
#define CONFIG_JPEG2000_PARSER 1
#define CONFIG_MJPEG_PARSER 1
#define CONFIG_MLP_PARSER 1
#define CONFIG_MPEG4VIDEO_PARSER 1
#define CONFIG_MPEGAUDIO_PARSER 1
#define CONFIG_MPEGVIDEO_PARSER 1
#define CONFIG_OPUS_PARSER 1
#define CONFIG_PNG_PARSER 1
#define CONFIG_PNM_PARSER 1
#define CONFIG_RV30_PARSER 1
#define CONFIG_RV40_PARSER 1
#define CONFIG_SBC_PARSER 1
#define CONFIG_SIPR_PARSER 1
#define CONFIG_TAK_PARSER 1
#define CONFIG_VC1_PARSER 1
#define CONFIG_VORBIS_PARSER 1
#define CONFIG_VP3_PARSER 1
#define CONFIG_VP8_PARSER 1
#define CONFIG_VP9_PARSER 1
#define CONFIG_WEBP_PARSER 1
#define CONFIG_XMA_PARSER 1
#define CONFIG_ALSA_INDEV 0
#define CONFIG_ANDROID_CAMERA_INDEV 0
#define CONFIG_AVFOUNDATION_INDEV 0
#define CONFIG_BKTR_INDEV 0
#define CONFIG_DECKLINK_INDEV 0
#define CONFIG_DSHOW_INDEV 0
#define CONFIG_FBDEV_INDEV 0
#define CONFIG_GDIGRAB_INDEV 0
#define CONFIG_IEC61883_INDEV 0
#define CONFIG_JACK_INDEV 0
#define CONFIG_KMSGRAB_INDEV 0
#define CONFIG_LAVFI_INDEV 1
#define CONFIG_OPENAL_INDEV 0
#define CONFIG_OSS_INDEV 0
#define CONFIG_PULSE_INDEV 0
#define CONFIG_SNDIO_INDEV 0
#define CONFIG_V4L2_INDEV 0
#define CONFIG_VFWCAP_INDEV 0
#define CONFIG_XCBGRAB_INDEV 0
#define CONFIG_LIBCDIO_INDEV 0
#define CONFIG_LIBDC1394_INDEV 0
#define CONFIG_ALSA_OUTDEV 0
#define CONFIG_CACA_OUTDEV 0
#define CONFIG_DECKLINK_OUTDEV 0
#define CONFIG_FBDEV_OUTDEV 0
#define CONFIG_OPENGL_OUTDEV 0
#define CONFIG_OSS_OUTDEV 0
#define CONFIG_PULSE_OUTDEV 0
#define CONFIG_SDL2_OUTDEV 0
#define CONFIG_SNDIO_OUTDEV 0
#define CONFIG_V4L2_OUTDEV 0
#define CONFIG_XV_OUTDEV 0
#define CONFIG_ABENCH_FILTER 1
#define CONFIG_ACOMPRESSOR_FILTER 1
#define CONFIG_ACONTRAST_FILTER 1
#define CONFIG_ACOPY_FILTER 1
#define CONFIG_ACUE_FILTER 1
#define CONFIG_ACROSSFADE_FILTER 1
#define CONFIG_ACROSSOVER_FILTER 1
#define CONFIG_ACRUSHER_FILTER 1
#define CONFIG_ADECLICK_FILTER 1
#define CONFIG_ADECLIP_FILTER 1
#define CONFIG_ADELAY_FILTER 1
#define CONFIG_ADERIVATIVE_FILTER 1
#define CONFIG_AECHO_FILTER 1
#define CONFIG_AEMPHASIS_FILTER 1
#define CONFIG_AEVAL_FILTER 1
#define CONFIG_AFADE_FILTER 1
#define CONFIG_AFFTDN_FILTER 1
#define CONFIG_AFFTFILT_FILTER 1
#define CONFIG_AFIR_FILTER 1
#define CONFIG_AFORMAT_FILTER 1
#define CONFIG_AGATE_FILTER 1
#define CONFIG_AIIR_FILTER 1
#define CONFIG_AINTEGRAL_FILTER 1
#define CONFIG_AINTERLEAVE_FILTER 1
#define CONFIG_ALIMITER_FILTER 1
#define CONFIG_ALLPASS_FILTER 1
#define CONFIG_ALOOP_FILTER 1
#define CONFIG_AMERGE_FILTER 1
#define CONFIG_AMETADATA_FILTER 1
#define CONFIG_AMIX_FILTER 1
#define CONFIG_AMULTIPLY_FILTER 1
#define CONFIG_ANEQUALIZER_FILTER 1
#define CONFIG_ANLMDN_FILTER 1
#define CONFIG_ANLMS_FILTER 1
#define CONFIG_ANULL_FILTER 1
#define CONFIG_APAD_FILTER 1
#define CONFIG_APERMS_FILTER 1
#define CONFIG_APHASER_FILTER 1
#define CONFIG_APULSATOR_FILTER 1
#define CONFIG_AREALTIME_FILTER 1
#define CONFIG_ARESAMPLE_FILTER 1
#define CONFIG_AREVERSE_FILTER 1
#define CONFIG_ARNNDN_FILTER 1
#define CONFIG_ASELECT_FILTER 1
#define CONFIG_ASENDCMD_FILTER 1
#define CONFIG_ASETNSAMPLES_FILTER 1
#define CONFIG_ASETPTS_FILTER 1
#define CONFIG_ASETRATE_FILTER 1
#define CONFIG_ASETTB_FILTER 1
#define CONFIG_ASHOWINFO_FILTER 1
#define CONFIG_ASIDEDATA_FILTER 1
#define CONFIG_ASOFTCLIP_FILTER 1
#define CONFIG_ASPLIT_FILTER 1
#define CONFIG_ASR_FILTER 0
#define CONFIG_ASTATS_FILTER 1
#define CONFIG_ASTREAMSELECT_FILTER 1
#define CONFIG_ASUBBOOST_FILTER 1
#define CONFIG_ATEMPO_FILTER 1
#define CONFIG_ATRIM_FILTER 1
#define CONFIG_AXCORRELATE_FILTER 1
#define CONFIG_AZMQ_FILTER 0
#define CONFIG_BANDPASS_FILTER 1
#define CONFIG_BANDREJECT_FILTER 1
#define CONFIG_BASS_FILTER 1
#define CONFIG_BIQUAD_FILTER 1
#define CONFIG_BS2B_FILTER 0
#define CONFIG_CHROMABER_VULKAN_FILTER 0
#define CONFIG_CHANNELMAP_FILTER 1
#define CONFIG_CHANNELSPLIT_FILTER 1
#define CONFIG_CHORUS_FILTER 1
#define CONFIG_COMPAND_FILTER 1
#define CONFIG_COMPENSATIONDELAY_FILTER 1
#define CONFIG_CROSSFEED_FILTER 1
#define CONFIG_CRYSTALIZER_FILTER 1
#define CONFIG_DCSHIFT_FILTER 1
#define CONFIG_DEESSER_FILTER 1
#define CONFIG_DRMETER_FILTER 1
#define CONFIG_DYNAUDNORM_FILTER 1
#define CONFIG_EARWAX_FILTER 1
#define CONFIG_EBUR128_FILTER 1
#define CONFIG_EQUALIZER_FILTER 1
#define CONFIG_EXTRASTEREO_FILTER 1
#define CONFIG_FIREQUALIZER_FILTER 1
#define CONFIG_FLANGER_FILTER 1
#define CONFIG_HAAS_FILTER 1
#define CONFIG_HDCD_FILTER 1
#define CONFIG_HEADPHONE_FILTER 1
#define CONFIG_HIGHPASS_FILTER 1
#define CONFIG_HIGHSHELF_FILTER 1
#define CONFIG_JOIN_FILTER 1
#define CONFIG_LADSPA_FILTER 0
#define CONFIG_LOUDNORM_FILTER 1
#define CONFIG_LOWPASS_FILTER 1
#define CONFIG_LOWSHELF_FILTER 1
#define CONFIG_LV2_FILTER 0
#define CONFIG_MCOMPAND_FILTER 1
#define CONFIG_PAN_FILTER 1
#define CONFIG_REPLAYGAIN_FILTER 1
#define CONFIG_RESAMPLE_FILTER 0
#define CONFIG_RUBBERBAND_FILTER 0
#define CONFIG_SIDECHAINCOMPRESS_FILTER 1
#define CONFIG_SIDECHAINGATE_FILTER 1
#define CONFIG_SILENCEDETECT_FILTER 1
#define CONFIG_SILENCEREMOVE_FILTER 1
#define CONFIG_SOFALIZER_FILTER 0
#define CONFIG_STEREOTOOLS_FILTER 1
#define CONFIG_STEREOWIDEN_FILTER 1
#define CONFIG_SUPEREQUALIZER_FILTER 1
#define CONFIG_SURROUND_FILTER 1
#define CONFIG_TREBLE_FILTER 1
#define CONFIG_TREMOLO_FILTER 1
#define CONFIG_VIBRATO_FILTER 1
#define CONFIG_VOLUME_FILTER 1
#define CONFIG_VOLUMEDETECT_FILTER 1
#define CONFIG_AEVALSRC_FILTER 1
#define CONFIG_AFIRSRC_FILTER 1
#define CONFIG_ANOISESRC_FILTER 1
#define CONFIG_ANULLSRC_FILTER 1
#define CONFIG_FLITE_FILTER 0
#define CONFIG_HILBERT_FILTER 1
#define CONFIG_SINC_FILTER 1
#define CONFIG_SINE_FILTER 1
#define CONFIG_ANULLSINK_FILTER 1
#define CONFIG_ADDROI_FILTER 1
#define CONFIG_ALPHAEXTRACT_FILTER 1
#define CONFIG_ALPHAMERGE_FILTER 1
#define CONFIG_AMPLIFY_FILTER 1
#define CONFIG_ASS_FILTER 0
#define CONFIG_ATADENOISE_FILTER 1
#define CONFIG_AVGBLUR_FILTER 1
#define CONFIG_AVGBLUR_OPENCL_FILTER 0
#define CONFIG_AVGBLUR_VULKAN_FILTER 0
#define CONFIG_BBOX_FILTER 1
#define CONFIG_BENCH_FILTER 1
#define CONFIG_BILATERAL_FILTER 1
#define CONFIG_BITPLANENOISE_FILTER 1
#define CONFIG_BLACKDETECT_FILTER 1
#define CONFIG_BLACKFRAME_FILTER 0
#define CONFIG_BLEND_FILTER 1
#define CONFIG_BM3D_FILTER 1
#define CONFIG_BOXBLUR_FILTER 0
#define CONFIG_BOXBLUR_OPENCL_FILTER 0
#define CONFIG_BWDIF_FILTER 1
#define CONFIG_CAS_FILTER 1
#define CONFIG_CHROMAHOLD_FILTER 1
#define CONFIG_CHROMAKEY_FILTER 1
#define CONFIG_CHROMASHIFT_FILTER 1
#define CONFIG_CIESCOPE_FILTER 1
#define CONFIG_CODECVIEW_FILTER 1
#define CONFIG_COLORBALANCE_FILTER 1
#define CONFIG_COLORCHANNELMIXER_FILTER 1
#define CONFIG_COLORKEY_FILTER 1
#define CONFIG_COLORKEY_OPENCL_FILTER 0
#define CONFIG_COLORHOLD_FILTER 1
#define CONFIG_COLORLEVELS_FILTER 1
#define CONFIG_COLORMATRIX_FILTER 0
#define CONFIG_COLORSPACE_FILTER 1
#define CONFIG_CONVOLUTION_FILTER 1
#define CONFIG_CONVOLUTION_OPENCL_FILTER 0
#define CONFIG_CONVOLVE_FILTER 1
#define CONFIG_COPY_FILTER 1
#define CONFIG_COREIMAGE_FILTER 0
#define CONFIG_COVER_RECT_FILTER 0
#define CONFIG_CROP_FILTER 1
#define CONFIG_CROPDETECT_FILTER 0
#define CONFIG_CUE_FILTER 1
#define CONFIG_CURVES_FILTER 1
#define CONFIG_DATASCOPE_FILTER 1
#define CONFIG_DBLUR_FILTER 1
#define CONFIG_DCTDNOIZ_FILTER 1
#define CONFIG_DEBAND_FILTER 1
#define CONFIG_DEBLOCK_FILTER 1
#define CONFIG_DECIMATE_FILTER 1
#define CONFIG_DECONVOLVE_FILTER 1
#define CONFIG_DEDOT_FILTER 1
#define CONFIG_DEFLATE_FILTER 1
#define CONFIG_DEFLICKER_FILTER 1
#define CONFIG_DEINTERLACE_QSV_FILTER 0
#define CONFIG_DEINTERLACE_VAAPI_FILTER 0
#define CONFIG_DEJUDDER_FILTER 1
#define CONFIG_DELOGO_FILTER 0
#define CONFIG_DENOISE_VAAPI_FILTER 0
#define CONFIG_DERAIN_FILTER 1
#define CONFIG_DESHAKE_FILTER 1
#define CONFIG_DESHAKE_OPENCL_FILTER 0
#define CONFIG_DESPILL_FILTER 1
#define CONFIG_DETELECINE_FILTER 1
#define CONFIG_DILATION_FILTER 1
#define CONFIG_DILATION_OPENCL_FILTER 0
#define CONFIG_DISPLACE_FILTER 1
#define CONFIG_DNN_PROCESSING_FILTER 1
#define CONFIG_DOUBLEWEAVE_FILTER 1
#define CONFIG_DRAWBOX_FILTER 1
#define CONFIG_DRAWGRAPH_FILTER 1
#define CONFIG_DRAWGRID_FILTER 1
#define CONFIG_DRAWTEXT_FILTER 0
#define CONFIG_EDGEDETECT_FILTER 1
#define CONFIG_ELBG_FILTER 1
#define CONFIG_ENTROPY_FILTER 1
#define CONFIG_EQ_FILTER 0
#define CONFIG_EROSION_FILTER 1
#define CONFIG_EROSION_OPENCL_FILTER 0
#define CONFIG_EXTRACTPLANES_FILTER 1
#define CONFIG_FADE_FILTER 1
#define CONFIG_FFTDNOIZ_FILTER 1
#define CONFIG_FFTFILT_FILTER 1
#define CONFIG_FIELD_FILTER 1
#define CONFIG_FIELDHINT_FILTER 1
#define CONFIG_FIELDMATCH_FILTER 1
#define CONFIG_FIELDORDER_FILTER 1
#define CONFIG_FILLBORDERS_FILTER 1
#define CONFIG_FIND_RECT_FILTER 0
#define CONFIG_FLOODFILL_FILTER 1
#define CONFIG_FORMAT_FILTER 1
#define CONFIG_FPS_FILTER 1
#define CONFIG_FRAMEPACK_FILTER 1
#define CONFIG_FRAMERATE_FILTER 1
#define CONFIG_FRAMESTEP_FILTER 1
#define CONFIG_FREEZEDETECT_FILTER 1
#define CONFIG_FREEZEFRAMES_FILTER 1
#define CONFIG_FREI0R_FILTER 0
#define CONFIG_FSPP_FILTER 0
#define CONFIG_GBLUR_FILTER 1
#define CONFIG_GEQ_FILTER 1
#define CONFIG_GRADFUN_FILTER 1
#define CONFIG_GRAPHMONITOR_FILTER 1
#define CONFIG_GREYEDGE_FILTER 1
#define CONFIG_HALDCLUT_FILTER 1
#define CONFIG_HFLIP_FILTER 1
#define CONFIG_HISTEQ_FILTER 0
#define CONFIG_HISTOGRAM_FILTER 1
#define CONFIG_HQDN3D_FILTER 0
#define CONFIG_HQX_FILTER 1
#define CONFIG_HSTACK_FILTER 1
#define CONFIG_HUE_FILTER 1
#define CONFIG_HWDOWNLOAD_FILTER 1
#define CONFIG_HWMAP_FILTER 1
#define CONFIG_HWUPLOAD_FILTER 1
#define CONFIG_HWUPLOAD_CUDA_FILTER 0
#define CONFIG_HYSTERESIS_FILTER 1
#define CONFIG_IDET_FILTER 1
#define CONFIG_IL_FILTER 1
#define CONFIG_INFLATE_FILTER 1
#define CONFIG_INTERLACE_FILTER 0
#define CONFIG_INTERLEAVE_FILTER 1
#define CONFIG_KERNDEINT_FILTER 0
#define CONFIG_LAGFUN_FILTER 1
#define CONFIG_LENSCORRECTION_FILTER 1
#define CONFIG_LENSFUN_FILTER 0
#define CONFIG_LIBVMAF_FILTER 0
#define CONFIG_LIMITER_FILTER 1
#define CONFIG_LOOP_FILTER 1
#define CONFIG_LUMAKEY_FILTER 1
#define CONFIG_LUT_FILTER 1
#define CONFIG_LUT1D_FILTER 1
#define CONFIG_LUT2_FILTER 1
#define CONFIG_LUT3D_FILTER 1
#define CONFIG_LUTRGB_FILTER 1
#define CONFIG_LUTYUV_FILTER 1
#define CONFIG_MASKEDCLAMP_FILTER 1
#define CONFIG_MASKEDMAX_FILTER 1
#define CONFIG_MASKEDMERGE_FILTER 1
#define CONFIG_MASKEDMIN_FILTER 1
#define CONFIG_MASKEDTHRESHOLD_FILTER 1
#define CONFIG_MASKFUN_FILTER 1
#define CONFIG_MCDEINT_FILTER 0
#define CONFIG_MEDIAN_FILTER 1
#define CONFIG_MERGEPLANES_FILTER 1
#define CONFIG_MESTIMATE_FILTER 1
#define CONFIG_METADATA_FILTER 1
#define CONFIG_MIDEQUALIZER_FILTER 1
#define CONFIG_MINTERPOLATE_FILTER 1
#define CONFIG_MIX_FILTER 1
#define CONFIG_MPDECIMATE_FILTER 0
#define CONFIG_NEGATE_FILTER 1
#define CONFIG_NLMEANS_FILTER 1
#define CONFIG_NLMEANS_OPENCL_FILTER 0
#define CONFIG_NNEDI_FILTER 0
#define CONFIG_NOFORMAT_FILTER 1
#define CONFIG_NOISE_FILTER 1
#define CONFIG_NORMALIZE_FILTER 1
#define CONFIG_NULL_FILTER 1
#define CONFIG_OCR_FILTER 0
#define CONFIG_OCV_FILTER 0
#define CONFIG_OSCILLOSCOPE_FILTER 1
#define CONFIG_OVERLAY_FILTER 1
#define CONFIG_OVERLAY_OPENCL_FILTER 0
#define CONFIG_OVERLAY_QSV_FILTER 0
#define CONFIG_OVERLAY_VULKAN_FILTER 0
#define CONFIG_OVERLAY_CUDA_FILTER 0
#define CONFIG_OWDENOISE_FILTER 0
#define CONFIG_PAD_FILTER 1
#define CONFIG_PAD_OPENCL_FILTER 0
#define CONFIG_PALETTEGEN_FILTER 1
#define CONFIG_PALETTEUSE_FILTER 1
#define CONFIG_PERMS_FILTER 1
#define CONFIG_PERSPECTIVE_FILTER 0
#define CONFIG_PHASE_FILTER 0
#define CONFIG_PHOTOSENSITIVITY_FILTER 1
#define CONFIG_PIXDESCTEST_FILTER 1
#define CONFIG_PIXSCOPE_FILTER 1
#define CONFIG_PP_FILTER 0
#define CONFIG_PP7_FILTER 0
#define CONFIG_PREMULTIPLY_FILTER 1
#define CONFIG_PREWITT_FILTER 1
#define CONFIG_PREWITT_OPENCL_FILTER 0
#define CONFIG_PROCAMP_VAAPI_FILTER 0
#define CONFIG_PROGRAM_OPENCL_FILTER 0
#define CONFIG_PSEUDOCOLOR_FILTER 1
#define CONFIG_PSNR_FILTER 1
#define CONFIG_PULLUP_FILTER 0
#define CONFIG_QP_FILTER 1
#define CONFIG_RANDOM_FILTER 1
#define CONFIG_READEIA608_FILTER 1
#define CONFIG_READVITC_FILTER 1
#define CONFIG_REALTIME_FILTER 1
#define CONFIG_REMAP_FILTER 1
#define CONFIG_REMOVEGRAIN_FILTER 1
#define CONFIG_REMOVELOGO_FILTER 1
#define CONFIG_REPEATFIELDS_FILTER 0
#define CONFIG_REVERSE_FILTER 1
#define CONFIG_RGBASHIFT_FILTER 1
#define CONFIG_ROBERTS_FILTER 1
#define CONFIG_ROBERTS_OPENCL_FILTER 0
#define CONFIG_ROTATE_FILTER 1
#define CONFIG_SAB_FILTER 0
#define CONFIG_SCALE_FILTER 1
#define CONFIG_SCALE_CUDA_FILTER 0
#define CONFIG_SCALE_NPP_FILTER 0
#define CONFIG_SCALE_QSV_FILTER 0
#define CONFIG_SCALE_VAAPI_FILTER 0
#define CONFIG_SCALE_VULKAN_FILTER 0
#define CONFIG_SCALE2REF_FILTER 1
#define CONFIG_SCDET_FILTER 1
#define CONFIG_SCROLL_FILTER 1
#define CONFIG_SELECT_FILTER 1
#define CONFIG_SELECTIVECOLOR_FILTER 1
#define CONFIG_SENDCMD_FILTER 1
#define CONFIG_SEPARATEFIELDS_FILTER 1
#define CONFIG_SETDAR_FILTER 1
#define CONFIG_SETFIELD_FILTER 1
#define CONFIG_SETPARAMS_FILTER 1
#define CONFIG_SETPTS_FILTER 1
#define CONFIG_SETRANGE_FILTER 1
#define CONFIG_SETSAR_FILTER 1
#define CONFIG_SETTB_FILTER 1
#define CONFIG_SHARPNESS_VAAPI_FILTER 0
#define CONFIG_SHOWINFO_FILTER 1
#define CONFIG_SHOWPALETTE_FILTER 1
#define CONFIG_SHUFFLEFRAMES_FILTER 1
#define CONFIG_SHUFFLEPLANES_FILTER 1
#define CONFIG_SIDEDATA_FILTER 1
#define CONFIG_SIGNALSTATS_FILTER 1
#define CONFIG_SIGNATURE_FILTER 0
#define CONFIG_SMARTBLUR_FILTER 0
#define CONFIG_SOBEL_FILTER 1
#define CONFIG_SOBEL_OPENCL_FILTER 0
#define CONFIG_SPLIT_FILTER 1
#define CONFIG_SPP_FILTER 0
#define CONFIG_SR_FILTER 1
#define CONFIG_SSIM_FILTER 1
#define CONFIG_STEREO3D_FILTER 0
#define CONFIG_STREAMSELECT_FILTER 1
#define CONFIG_SUBTITLES_FILTER 0
#define CONFIG_SUPER2XSAI_FILTER 0
#define CONFIG_SWAPRECT_FILTER 1
#define CONFIG_SWAPUV_FILTER 1
#define CONFIG_TBLEND_FILTER 1
#define CONFIG_TELECINE_FILTER 1
#define CONFIG_THISTOGRAM_FILTER 1
#define CONFIG_THRESHOLD_FILTER 1
#define CONFIG_THUMBNAIL_FILTER 1
#define CONFIG_THUMBNAIL_CUDA_FILTER 0
#define CONFIG_TILE_FILTER 1
#define CONFIG_TINTERLACE_FILTER 0
#define CONFIG_TLUT2_FILTER 1
#define CONFIG_TMEDIAN_FILTER 1
#define CONFIG_TMIX_FILTER 1
#define CONFIG_TONEMAP_FILTER 1
#define CONFIG_TONEMAP_OPENCL_FILTER 0
#define CONFIG_TONEMAP_VAAPI_FILTER 0
#define CONFIG_TPAD_FILTER 1
#define CONFIG_TRANSPOSE_FILTER 1
#define CONFIG_TRANSPOSE_NPP_FILTER 0
#define CONFIG_TRANSPOSE_OPENCL_FILTER 0
#define CONFIG_TRANSPOSE_VAAPI_FILTER 0
#define CONFIG_TRIM_FILTER 1
#define CONFIG_UNPREMULTIPLY_FILTER 1
#define CONFIG_UNSHARP_FILTER 1
#define CONFIG_UNSHARP_OPENCL_FILTER 0
#define CONFIG_UNTILE_FILTER 1
#define CONFIG_USPP_FILTER 0
#define CONFIG_V360_FILTER 1
#define CONFIG_VAGUEDENOISER_FILTER 0
#define CONFIG_VECTORSCOPE_FILTER 1
#define CONFIG_VFLIP_FILTER 1
#define CONFIG_VFRDET_FILTER 1
#define CONFIG_VIBRANCE_FILTER 1
#define CONFIG_VIDSTABDETECT_FILTER 0
#define CONFIG_VIDSTABTRANSFORM_FILTER 0
#define CONFIG_VIGNETTE_FILTER 1
#define CONFIG_VMAFMOTION_FILTER 1
#define CONFIG_VPP_QSV_FILTER 0
#define CONFIG_VSTACK_FILTER 1
#define CONFIG_W3FDIF_FILTER 1
#define CONFIG_WAVEFORM_FILTER 1
#define CONFIG_WEAVE_FILTER 1
#define CONFIG_XBR_FILTER 1
#define CONFIG_XFADE_FILTER 1
#define CONFIG_XFADE_OPENCL_FILTER 0
#define CONFIG_XMEDIAN_FILTER 1
#define CONFIG_XSTACK_FILTER 1
#define CONFIG_YADIF_FILTER 1
#define CONFIG_YADIF_CUDA_FILTER 0
#define CONFIG_YAEPBLUR_FILTER 1
#define CONFIG_ZMQ_FILTER 0
#define CONFIG_ZOOMPAN_FILTER 1
#define CONFIG_ZSCALE_FILTER 0
#define CONFIG_ALLRGB_FILTER 1
#define CONFIG_ALLYUV_FILTER 1
#define CONFIG_CELLAUTO_FILTER 1
#define CONFIG_COLOR_FILTER 1
#define CONFIG_COREIMAGESRC_FILTER 0
#define CONFIG_FREI0R_SRC_FILTER 0
#define CONFIG_GRADIENTS_FILTER 1
#define CONFIG_HALDCLUTSRC_FILTER 1
#define CONFIG_LIFE_FILTER 1
#define CONFIG_MANDELBROT_FILTER 1
#define CONFIG_MPTESTSRC_FILTER 0
#define CONFIG_NULLSRC_FILTER 1
#define CONFIG_OPENCLSRC_FILTER 0
#define CONFIG_PAL75BARS_FILTER 1
#define CONFIG_PAL100BARS_FILTER 1
#define CONFIG_RGBTESTSRC_FILTER 1
#define CONFIG_SIERPINSKI_FILTER 1
#define CONFIG_SMPTEBARS_FILTER 1
#define CONFIG_SMPTEHDBARS_FILTER 1
#define CONFIG_TESTSRC_FILTER 1
#define CONFIG_TESTSRC2_FILTER 1
#define CONFIG_YUVTESTSRC_FILTER 1
#define CONFIG_NULLSINK_FILTER 1
#define CONFIG_ABITSCOPE_FILTER 1
#define CONFIG_ADRAWGRAPH_FILTER 1
#define CONFIG_AGRAPHMONITOR_FILTER 1
#define CONFIG_AHISTOGRAM_FILTER 1
#define CONFIG_APHASEMETER_FILTER 1
#define CONFIG_AVECTORSCOPE_FILTER 1
#define CONFIG_CONCAT_FILTER 1
#define CONFIG_SHOWCQT_FILTER 1
#define CONFIG_SHOWFREQS_FILTER 1
#define CONFIG_SHOWSPATIAL_FILTER 1
#define CONFIG_SHOWSPECTRUM_FILTER 1
#define CONFIG_SHOWSPECTRUMPIC_FILTER 1
#define CONFIG_SHOWVOLUME_FILTER 1
#define CONFIG_SHOWWAVES_FILTER 1
#define CONFIG_SHOWWAVESPIC_FILTER 1
#define CONFIG_SPECTRUMSYNTH_FILTER 1
#define CONFIG_AMOVIE_FILTER 1
#define CONFIG_MOVIE_FILTER 1
#define CONFIG_AFIFO_FILTER 1
#define CONFIG_FIFO_FILTER 1
#define CONFIG_AA_DEMUXER 1
#define CONFIG_AAC_DEMUXER 1
#define CONFIG_AC3_DEMUXER 1
#define CONFIG_ACM_DEMUXER 1
#define CONFIG_ACT_DEMUXER 1
#define CONFIG_ADF_DEMUXER 1
#define CONFIG_ADP_DEMUXER 1
#define CONFIG_ADS_DEMUXER 1
#define CONFIG_ADX_DEMUXER 1
#define CONFIG_AEA_DEMUXER 1
#define CONFIG_AFC_DEMUXER 1
#define CONFIG_AIFF_DEMUXER 1
#define CONFIG_AIX_DEMUXER 1
#define CONFIG_ALP_DEMUXER 1
#define CONFIG_AMR_DEMUXER 1
#define CONFIG_AMRNB_DEMUXER 1
#define CONFIG_AMRWB_DEMUXER 1
#define CONFIG_ANM_DEMUXER 1
#define CONFIG_APC_DEMUXER 1
#define CONFIG_APE_DEMUXER 1
#define CONFIG_APM_DEMUXER 1
#define CONFIG_APNG_DEMUXER 1
#define CONFIG_APTX_DEMUXER 1
#define CONFIG_APTX_HD_DEMUXER 1
#define CONFIG_AQTITLE_DEMUXER 1
#define CONFIG_ARGO_ASF_DEMUXER 1
#define CONFIG_ASF_DEMUXER 1
#define CONFIG_ASF_O_DEMUXER 1
#define CONFIG_ASS_DEMUXER 1
#define CONFIG_AST_DEMUXER 1
#define CONFIG_AU_DEMUXER 1
#define CONFIG_AV1_DEMUXER 1
#define CONFIG_AVI_DEMUXER 1
#define CONFIG_AVISYNTH_DEMUXER 0
#define CONFIG_AVR_DEMUXER 1
#define CONFIG_AVS_DEMUXER 1
#define CONFIG_AVS2_DEMUXER 1
#define CONFIG_BETHSOFTVID_DEMUXER 1
#define CONFIG_BFI_DEMUXER 1
#define CONFIG_BINTEXT_DEMUXER 1
#define CONFIG_BINK_DEMUXER 1
#define CONFIG_BIT_DEMUXER 1
#define CONFIG_BMV_DEMUXER 1
#define CONFIG_BFSTM_DEMUXER 1
#define CONFIG_BRSTM_DEMUXER 1
#define CONFIG_BOA_DEMUXER 1
#define CONFIG_C93_DEMUXER 1
#define CONFIG_CAF_DEMUXER 1
#define CONFIG_CAVSVIDEO_DEMUXER 1
#define CONFIG_CDG_DEMUXER 1
#define CONFIG_CDXL_DEMUXER 1
#define CONFIG_CINE_DEMUXER 1
#define CONFIG_CODEC2_DEMUXER 1
#define CONFIG_CODEC2RAW_DEMUXER 1
#define CONFIG_CONCAT_DEMUXER 1
#define CONFIG_DASH_DEMUXER 0
#define CONFIG_DATA_DEMUXER 1
#define CONFIG_DAUD_DEMUXER 1
#define CONFIG_DCSTR_DEMUXER 1
#define CONFIG_DERF_DEMUXER 1
#define CONFIG_DFA_DEMUXER 1
#define CONFIG_DHAV_DEMUXER 1
#define CONFIG_DIRAC_DEMUXER 1
#define CONFIG_DNXHD_DEMUXER 1
#define CONFIG_DSF_DEMUXER 1
#define CONFIG_DSICIN_DEMUXER 1
#define CONFIG_DSS_DEMUXER 1
#define CONFIG_DTS_DEMUXER 1
#define CONFIG_DTSHD_DEMUXER 1
#define CONFIG_DV_DEMUXER 1
#define CONFIG_DVBSUB_DEMUXER 1
#define CONFIG_DVBTXT_DEMUXER 1
#define CONFIG_DXA_DEMUXER 1
#define CONFIG_EA_DEMUXER 1
#define CONFIG_EA_CDATA_DEMUXER 1
#define CONFIG_EAC3_DEMUXER 1
#define CONFIG_EPAF_DEMUXER 1
#define CONFIG_FFMETADATA_DEMUXER 1
#define CONFIG_FILMSTRIP_DEMUXER 1
#define CONFIG_FITS_DEMUXER 1
#define CONFIG_FLAC_DEMUXER 1
#define CONFIG_FLIC_DEMUXER 1
#define CONFIG_FLV_DEMUXER 1
#define CONFIG_LIVE_FLV_DEMUXER 1
#define CONFIG_FOURXM_DEMUXER 1
#define CONFIG_FRM_DEMUXER 1
#define CONFIG_FSB_DEMUXER 1
#define CONFIG_FWSE_DEMUXER 1
#define CONFIG_G722_DEMUXER 1
#define CONFIG_G723_1_DEMUXER 1
#define CONFIG_G726_DEMUXER 1
#define CONFIG_G726LE_DEMUXER 1
#define CONFIG_G729_DEMUXER 1
#define CONFIG_GDV_DEMUXER 1
#define CONFIG_GENH_DEMUXER 1
#define CONFIG_GIF_DEMUXER 1
#define CONFIG_GSM_DEMUXER 1
#define CONFIG_GXF_DEMUXER 1
#define CONFIG_H261_DEMUXER 1
#define CONFIG_H263_DEMUXER 1
#define CONFIG_H264_DEMUXER 1
#define CONFIG_HCA_DEMUXER 1
#define CONFIG_HCOM_DEMUXER 1
#define CONFIG_HEVC_DEMUXER 1
#define CONFIG_HLS_DEMUXER 1
#define CONFIG_HNM_DEMUXER 1
#define CONFIG_ICO_DEMUXER 1
#define CONFIG_IDCIN_DEMUXER 1
#define CONFIG_IDF_DEMUXER 1
#define CONFIG_IFF_DEMUXER 1
#define CONFIG_IFV_DEMUXER 1
#define CONFIG_ILBC_DEMUXER 1
#define CONFIG_IMAGE2_DEMUXER 1
#define CONFIG_IMAGE2PIPE_DEMUXER 1
#define CONFIG_IMAGE2_ALIAS_PIX_DEMUXER 1
#define CONFIG_IMAGE2_BRENDER_PIX_DEMUXER 1
#define CONFIG_INGENIENT_DEMUXER 1
#define CONFIG_IPMOVIE_DEMUXER 1
#define CONFIG_IRCAM_DEMUXER 1
#define CONFIG_ISS_DEMUXER 1
#define CONFIG_IV8_DEMUXER 1
#define CONFIG_IVF_DEMUXER 1
#define CONFIG_IVR_DEMUXER 1
#define CONFIG_JACOSUB_DEMUXER 1
#define CONFIG_JV_DEMUXER 1
#define CONFIG_KUX_DEMUXER 1
#define CONFIG_KVAG_DEMUXER 1
#define CONFIG_LMLM4_DEMUXER 1
#define CONFIG_LOAS_DEMUXER 1
#define CONFIG_LRC_DEMUXER 1
#define CONFIG_LVF_DEMUXER 1
#define CONFIG_LXF_DEMUXER 1
#define CONFIG_M4V_DEMUXER 1
#define CONFIG_MATROSKA_DEMUXER 1
#define CONFIG_MGSTS_DEMUXER 1
#define CONFIG_MICRODVD_DEMUXER 1
#define CONFIG_MJPEG_DEMUXER 1
#define CONFIG_MJPEG_2000_DEMUXER 1
#define CONFIG_MLP_DEMUXER 1
#define CONFIG_MLV_DEMUXER 1
#define CONFIG_MM_DEMUXER 1
#define CONFIG_MMF_DEMUXER 1
#define CONFIG_MOV_DEMUXER 1
#define CONFIG_MP3_DEMUXER 1
#define CONFIG_MPC_DEMUXER 1
#define CONFIG_MPC8_DEMUXER 1
#define CONFIG_MPEGPS_DEMUXER 1
#define CONFIG_MPEGTS_DEMUXER 1
#define CONFIG_MPEGTSRAW_DEMUXER 1
#define CONFIG_MPEGVIDEO_DEMUXER 1
#define CONFIG_MPJPEG_DEMUXER 1
#define CONFIG_MPL2_DEMUXER 1
#define CONFIG_MPSUB_DEMUXER 1
#define CONFIG_MSF_DEMUXER 1
#define CONFIG_MSNWC_TCP_DEMUXER 1
#define CONFIG_MTAF_DEMUXER 1
#define CONFIG_MTV_DEMUXER 1
#define CONFIG_MUSX_DEMUXER 1
#define CONFIG_MV_DEMUXER 1
#define CONFIG_MVI_DEMUXER 1
#define CONFIG_MXF_DEMUXER 1
#define CONFIG_MXG_DEMUXER 1
#define CONFIG_NC_DEMUXER 1
#define CONFIG_NISTSPHERE_DEMUXER 1
#define CONFIG_NSP_DEMUXER 1
#define CONFIG_NSV_DEMUXER 1
#define CONFIG_NUT_DEMUXER 1
#define CONFIG_NUV_DEMUXER 1
#define CONFIG_OGG_DEMUXER 1
#define CONFIG_OMA_DEMUXER 1
#define CONFIG_PAF_DEMUXER 1
#define CONFIG_PCM_ALAW_DEMUXER 1
#define CONFIG_PCM_MULAW_DEMUXER 1
#define CONFIG_PCM_VIDC_DEMUXER 1
#define CONFIG_PCM_F64BE_DEMUXER 1
#define CONFIG_PCM_F64LE_DEMUXER 1
#define CONFIG_PCM_F32BE_DEMUXER 1
#define CONFIG_PCM_F32LE_DEMUXER 1
#define CONFIG_PCM_S32BE_DEMUXER 1
#define CONFIG_PCM_S32LE_DEMUXER 1
#define CONFIG_PCM_S24BE_DEMUXER 1
#define CONFIG_PCM_S24LE_DEMUXER 1
#define CONFIG_PCM_S16BE_DEMUXER 1
#define CONFIG_PCM_S16LE_DEMUXER 1
#define CONFIG_PCM_S8_DEMUXER 1
#define CONFIG_PCM_U32BE_DEMUXER 1
#define CONFIG_PCM_U32LE_DEMUXER 1
#define CONFIG_PCM_U24BE_DEMUXER 1
#define CONFIG_PCM_U24LE_DEMUXER 1
#define CONFIG_PCM_U16BE_DEMUXER 1
#define CONFIG_PCM_U16LE_DEMUXER 1
#define CONFIG_PCM_U8_DEMUXER 1
#define CONFIG_PJS_DEMUXER 1
#define CONFIG_PMP_DEMUXER 1
#define CONFIG_PP_BNK_DEMUXER 1
#define CONFIG_PVA_DEMUXER 1
#define CONFIG_PVF_DEMUXER 1
#define CONFIG_QCP_DEMUXER 1
#define CONFIG_R3D_DEMUXER 1
#define CONFIG_RAWVIDEO_DEMUXER 1
#define CONFIG_REALTEXT_DEMUXER 1
#define CONFIG_REDSPARK_DEMUXER 1
#define CONFIG_RL2_DEMUXER 1
#define CONFIG_RM_DEMUXER 1
#define CONFIG_ROQ_DEMUXER 1
#define CONFIG_RPL_DEMUXER 1
#define CONFIG_RSD_DEMUXER 1
#define CONFIG_RSO_DEMUXER 1
#define CONFIG_RTP_DEMUXER 1
#define CONFIG_RTSP_DEMUXER 1
#define CONFIG_S337M_DEMUXER 1
#define CONFIG_SAMI_DEMUXER 1
#define CONFIG_SAP_DEMUXER 1
#define CONFIG_SBC_DEMUXER 1
#define CONFIG_SBG_DEMUXER 1
#define CONFIG_SCC_DEMUXER 1
#define CONFIG_SDP_DEMUXER 1
#define CONFIG_SDR2_DEMUXER 1
#define CONFIG_SDS_DEMUXER 1
#define CONFIG_SDX_DEMUXER 1
#define CONFIG_SEGAFILM_DEMUXER 1
#define CONFIG_SER_DEMUXER 1
#define CONFIG_SHORTEN_DEMUXER 1
#define CONFIG_SIFF_DEMUXER 1
#define CONFIG_SLN_DEMUXER 1
#define CONFIG_SMACKER_DEMUXER 1
#define CONFIG_SMJPEG_DEMUXER 1
#define CONFIG_SMUSH_DEMUXER 1
#define CONFIG_SOL_DEMUXER 1
#define CONFIG_SOX_DEMUXER 1
#define CONFIG_SPDIF_DEMUXER 1
#define CONFIG_SRT_DEMUXER 1
#define CONFIG_STR_DEMUXER 1
#define CONFIG_STL_DEMUXER 1
#define CONFIG_SUBVIEWER1_DEMUXER 1
#define CONFIG_SUBVIEWER_DEMUXER 1
#define CONFIG_SUP_DEMUXER 1
#define CONFIG_SVAG_DEMUXER 1
#define CONFIG_SWF_DEMUXER 1
#define CONFIG_TAK_DEMUXER 1
#define CONFIG_TEDCAPTIONS_DEMUXER 1
#define CONFIG_THP_DEMUXER 1
#define CONFIG_THREEDOSTR_DEMUXER 1
#define CONFIG_TIERTEXSEQ_DEMUXER 1
#define CONFIG_TMV_DEMUXER 1
#define CONFIG_TRUEHD_DEMUXER 1
#define CONFIG_TTA_DEMUXER 1
#define CONFIG_TXD_DEMUXER 1
#define CONFIG_TTY_DEMUXER 1
#define CONFIG_TY_DEMUXER 1
#define CONFIG_V210_DEMUXER 1
#define CONFIG_V210X_DEMUXER 1
#define CONFIG_VAG_DEMUXER 1
#define CONFIG_VC1_DEMUXER 1
#define CONFIG_VC1T_DEMUXER 1
#define CONFIG_VIVIDAS_DEMUXER 1
#define CONFIG_VIVO_DEMUXER 1
#define CONFIG_VMD_DEMUXER 1
#define CONFIG_VOBSUB_DEMUXER 1
#define CONFIG_VOC_DEMUXER 1
#define CONFIG_VPK_DEMUXER 1
#define CONFIG_VPLAYER_DEMUXER 1
#define CONFIG_VQF_DEMUXER 1
#define CONFIG_W64_DEMUXER 1
#define CONFIG_WAV_DEMUXER 1
#define CONFIG_WC3_DEMUXER 1
#define CONFIG_WEBM_DASH_MANIFEST_DEMUXER 1
#define CONFIG_WEBVTT_DEMUXER 1
#define CONFIG_WSAUD_DEMUXER 1
#define CONFIG_WSD_DEMUXER 1
#define CONFIG_WSVQA_DEMUXER 1
#define CONFIG_WTV_DEMUXER 1
#define CONFIG_WVE_DEMUXER 1
#define CONFIG_WV_DEMUXER 1
#define CONFIG_XA_DEMUXER 1
#define CONFIG_XBIN_DEMUXER 1
#define CONFIG_XMV_DEMUXER 1
#define CONFIG_XVAG_DEMUXER 1
#define CONFIG_XWMA_DEMUXER 1
#define CONFIG_YOP_DEMUXER 1
#define CONFIG_YUV4MPEGPIPE_DEMUXER 1
#define CONFIG_IMAGE_BMP_PIPE_DEMUXER 1
#define CONFIG_IMAGE_DDS_PIPE_DEMUXER 1
#define CONFIG_IMAGE_DPX_PIPE_DEMUXER 1
#define CONFIG_IMAGE_EXR_PIPE_DEMUXER 1
#define CONFIG_IMAGE_GIF_PIPE_DEMUXER 1
#define CONFIG_IMAGE_J2K_PIPE_DEMUXER 1
#define CONFIG_IMAGE_JPEG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_JPEGLS_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PAM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PBM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PCX_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PGMYUV_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PGM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PICTOR_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PNG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PPM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PSD_PIPE_DEMUXER 1
#define CONFIG_IMAGE_QDRAW_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SGI_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SVG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SUNRAST_PIPE_DEMUXER 1
#define CONFIG_IMAGE_TIFF_PIPE_DEMUXER 1
#define CONFIG_IMAGE_WEBP_PIPE_DEMUXER 1
#define CONFIG_IMAGE_XPM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_XWD_PIPE_DEMUXER 1
#define CONFIG_LIBGME_DEMUXER 0
#define CONFIG_LIBMODPLUG_DEMUXER 0
#define CONFIG_LIBOPENMPT_DEMUXER 0
#define CONFIG_VAPOURSYNTH_DEMUXER 0
#define CONFIG_A64_MUXER 1
#define CONFIG_AC3_MUXER 1
#define CONFIG_ADTS_MUXER 1
#define CONFIG_ADX_MUXER 1
#define CONFIG_AIFF_MUXER 1
#define CONFIG_AMR_MUXER 1
#define CONFIG_APNG_MUXER 1
#define CONFIG_APTX_MUXER 1
#define CONFIG_APTX_HD_MUXER 1
#define CONFIG_ASF_MUXER 1
#define CONFIG_ASS_MUXER 1
#define CONFIG_AST_MUXER 1
#define CONFIG_ASF_STREAM_MUXER 1
#define CONFIG_AU_MUXER 1
#define CONFIG_AVI_MUXER 1
#define CONFIG_AVM2_MUXER 1
#define CONFIG_AVS2_MUXER 1
#define CONFIG_BIT_MUXER 1
#define CONFIG_CAF_MUXER 1
#define CONFIG_CAVSVIDEO_MUXER 1
#define CONFIG_CODEC2_MUXER 1
#define CONFIG_CODEC2RAW_MUXER 1
#define CONFIG_CRC_MUXER 1
#define CONFIG_DASH_MUXER 1
#define CONFIG_DATA_MUXER 1
#define CONFIG_DAUD_MUXER 1
#define CONFIG_DIRAC_MUXER 1
#define CONFIG_DNXHD_MUXER 1
#define CONFIG_DTS_MUXER 1
#define CONFIG_DV_MUXER 1
#define CONFIG_EAC3_MUXER 1
#define CONFIG_F4V_MUXER 1
#define CONFIG_FFMETADATA_MUXER 1
#define CONFIG_FIFO_MUXER 1
#define CONFIG_FIFO_TEST_MUXER 1
#define CONFIG_FILMSTRIP_MUXER 1
#define CONFIG_FITS_MUXER 1
#define CONFIG_FLAC_MUXER 1
#define CONFIG_FLV_MUXER 1
#define CONFIG_FRAMECRC_MUXER 1
#define CONFIG_FRAMEHASH_MUXER 1
#define CONFIG_FRAMEMD5_MUXER 1
#define CONFIG_G722_MUXER 1
#define CONFIG_G723_1_MUXER 1
#define CONFIG_G726_MUXER 1
#define CONFIG_G726LE_MUXER 1
#define CONFIG_GIF_MUXER 1
#define CONFIG_GSM_MUXER 1
#define CONFIG_GXF_MUXER 1
#define CONFIG_H261_MUXER 1
#define CONFIG_H263_MUXER 1
#define CONFIG_H264_MUXER 1
#define CONFIG_HASH_MUXER 1
#define CONFIG_HDS_MUXER 1
#define CONFIG_HEVC_MUXER 1
#define CONFIG_HLS_MUXER 1
#define CONFIG_ICO_MUXER 1
#define CONFIG_ILBC_MUXER 1
#define CONFIG_IMAGE2_MUXER 1
#define CONFIG_IMAGE2PIPE_MUXER 1
#define CONFIG_IPOD_MUXER 1
#define CONFIG_IRCAM_MUXER 1
#define CONFIG_ISMV_MUXER 1
#define CONFIG_IVF_MUXER 1
#define CONFIG_JACOSUB_MUXER 1
#define CONFIG_KVAG_MUXER 1
#define CONFIG_LATM_MUXER 1
#define CONFIG_LRC_MUXER 1
#define CONFIG_M4V_MUXER 1
#define CONFIG_MD5_MUXER 1
#define CONFIG_MATROSKA_MUXER 1
#define CONFIG_MATROSKA_AUDIO_MUXER 1
#define CONFIG_MICRODVD_MUXER 1
#define CONFIG_MJPEG_MUXER 1
#define CONFIG_MLP_MUXER 1
#define CONFIG_MMF_MUXER 1
#define CONFIG_MOV_MUXER 1
#define CONFIG_MP2_MUXER 1
#define CONFIG_MP3_MUXER 1
#define CONFIG_MP4_MUXER 1
#define CONFIG_MPEG1SYSTEM_MUXER 1
#define CONFIG_MPEG1VCD_MUXER 1
#define CONFIG_MPEG1VIDEO_MUXER 1
#define CONFIG_MPEG2DVD_MUXER 1
#define CONFIG_MPEG2SVCD_MUXER 1
#define CONFIG_MPEG2VIDEO_MUXER 1
#define CONFIG_MPEG2VOB_MUXER 1
#define CONFIG_MPEGTS_MUXER 1
#define CONFIG_MPJPEG_MUXER 1
#define CONFIG_MXF_MUXER 1
#define CONFIG_MXF_D10_MUXER 1
#define CONFIG_MXF_OPATOM_MUXER 1
#define CONFIG_NULL_MUXER 1
#define CONFIG_NUT_MUXER 1
#define CONFIG_OGA_MUXER 1
#define CONFIG_OGG_MUXER 1
#define CONFIG_OGV_MUXER 1
#define CONFIG_OMA_MUXER 1
#define CONFIG_OPUS_MUXER 1
#define CONFIG_PCM_ALAW_MUXER 1
#define CONFIG_PCM_MULAW_MUXER 1
#define CONFIG_PCM_VIDC_MUXER 1
#define CONFIG_PCM_F64BE_MUXER 1
#define CONFIG_PCM_F64LE_MUXER 1
#define CONFIG_PCM_F32BE_MUXER 1
#define CONFIG_PCM_F32LE_MUXER 1
#define CONFIG_PCM_S32BE_MUXER 1
#define CONFIG_PCM_S32LE_MUXER 1
#define CONFIG_PCM_S24BE_MUXER 1
#define CONFIG_PCM_S24LE_MUXER 1
#define CONFIG_PCM_S16BE_MUXER 1
#define CONFIG_PCM_S16LE_MUXER 1
#define CONFIG_PCM_S8_MUXER 1
#define CONFIG_PCM_U32BE_MUXER 1
#define CONFIG_PCM_U32LE_MUXER 1
#define CONFIG_PCM_U24BE_MUXER 1
#define CONFIG_PCM_U24LE_MUXER 1
#define CONFIG_PCM_U16BE_MUXER 1
#define CONFIG_PCM_U16LE_MUXER 1
#define CONFIG_PCM_U8_MUXER 1
#define CONFIG_PSP_MUXER 1
#define CONFIG_RAWVIDEO_MUXER 1
#define CONFIG_RM_MUXER 1
#define CONFIG_ROQ_MUXER 1
#define CONFIG_RSO_MUXER 1
#define CONFIG_RTP_MUXER 1
#define CONFIG_RTP_MPEGTS_MUXER 1
#define CONFIG_RTSP_MUXER 1
#define CONFIG_SAP_MUXER 1
#define CONFIG_SBC_MUXER 1
#define CONFIG_SCC_MUXER 1
#define CONFIG_SEGAFILM_MUXER 1
#define CONFIG_SEGMENT_MUXER 1
#define CONFIG_STREAM_SEGMENT_MUXER 1
#define CONFIG_SINGLEJPEG_MUXER 1
#define CONFIG_SMJPEG_MUXER 1
#define CONFIG_SMOOTHSTREAMING_MUXER 1
#define CONFIG_SOX_MUXER 1
#define CONFIG_SPX_MUXER 1
#define CONFIG_SPDIF_MUXER 1
#define CONFIG_SRT_MUXER 1
#define CONFIG_STREAMHASH_MUXER 1
#define CONFIG_SUP_MUXER 1
#define CONFIG_SWF_MUXER 1
#define CONFIG_TEE_MUXER 1
#define CONFIG_TG2_MUXER 1
#define CONFIG_TGP_MUXER 1
#define CONFIG_MKVTIMESTAMP_V2_MUXER 1
#define CONFIG_TRUEHD_MUXER 1
#define CONFIG_TTA_MUXER 1
#define CONFIG_UNCODEDFRAMECRC_MUXER 1
#define CONFIG_VC1_MUXER 1
#define CONFIG_VC1T_MUXER 1
#define CONFIG_VOC_MUXER 1
#define CONFIG_W64_MUXER 1
#define CONFIG_WAV_MUXER 1
#define CONFIG_WEBM_MUXER 1
#define CONFIG_WEBM_DASH_MANIFEST_MUXER 1
#define CONFIG_WEBM_CHUNK_MUXER 1
#define CONFIG_WEBP_MUXER 1
#define CONFIG_WEBVTT_MUXER 1
#define CONFIG_WTV_MUXER 1
#define CONFIG_WV_MUXER 1
#define CONFIG_YUV4MPEGPIPE_MUXER 1
#define CONFIG_CHROMAPRINT_MUXER 0
#define CONFIG_ASYNC_PROTOCOL 1
#define CONFIG_BLURAY_PROTOCOL 0
#define CONFIG_CACHE_PROTOCOL 1
#define CONFIG_CONCAT_PROTOCOL 1
#define CONFIG_CRYPTO_PROTOCOL 1
#define CONFIG_DATA_PROTOCOL 1
#define CONFIG_FFRTMPCRYPT_PROTOCOL 0
#define CONFIG_FFRTMPHTTP_PROTOCOL 1
#define CONFIG_FILE_PROTOCOL 1
#define CONFIG_FTP_PROTOCOL 1
#define CONFIG_GOPHER_PROTOCOL 1
#define CONFIG_HLS_PROTOCOL 1
#define CONFIG_HTTP_PROTOCOL 1
#define CONFIG_HTTPPROXY_PROTOCOL 1
#define CONFIG_HTTPS_PROTOCOL 0
#define CONFIG_ICECAST_PROTOCOL 1
#define CONFIG_MMSH_PROTOCOL 1
#define CONFIG_MMST_PROTOCOL 1
#define CONFIG_MD5_PROTOCOL 1
#define CONFIG_PIPE_PROTOCOL 1
#define CONFIG_PROMPEG_PROTOCOL 1
#define CONFIG_RTMP_PROTOCOL 1
#define CONFIG_RTMPE_PROTOCOL 0
#define CONFIG_RTMPS_PROTOCOL 0
#define CONFIG_RTMPT_PROTOCOL 1
#define CONFIG_RTMPTE_PROTOCOL 0
#define CONFIG_RTMPTS_PROTOCOL 0
#define CONFIG_RTP_PROTOCOL 1
#define CONFIG_SCTP_PROTOCOL 0
#define CONFIG_SRTP_PROTOCOL 1
#define CONFIG_SUBFILE_PROTOCOL 1
#define CONFIG_TEE_PROTOCOL 1
#define CONFIG_TCP_PROTOCOL 1
#define CONFIG_TLS_PROTOCOL 0
#define CONFIG_UDP_PROTOCOL 1
#define CONFIG_UDPLITE_PROTOCOL 1
#define CONFIG_UNIX_PROTOCOL 1
#define CONFIG_LIBAMQP_PROTOCOL 0
#define CONFIG_LIBRTMP_PROTOCOL 0
#define CONFIG_LIBRTMPE_PROTOCOL 0
#define CONFIG_LIBRTMPS_PROTOCOL 0
#define CONFIG_LIBRTMPT_PROTOCOL 0
#define CONFIG_LIBRTMPTE_PROTOCOL 0
#define CONFIG_LIBSRT_PROTOCOL 0
#define CONFIG_LIBSSH_PROTOCOL 0
#define CONFIG_LIBSMBCLIENT_PROTOCOL 0
#define CONFIG_LIBZMQ_PROTOCOL 0
#endif /* FFMPEG_CONFIG_H */
'''

ffmpeg_config_h = '''/* config.h for ffmpeg build. Generated by configure  */
/* Customized by Samsung manually */

/* Automatically generated by configure - do not modify! */
#ifndef FFMPEG_CONFIG_H
#define FFMPEG_CONFIG_H
#define FFMPEG_CONFIGURATION "--disable-x86asm --disable-inline-asm --disable-doc --disable-ffprobe --nm=llvm-nm --ar=emar --cc=emcc --cxx=em++ --objcc=emcc --dep-cc=emcc --ranlib='emar s' --disable-pthreads --enable-pic"
#define FFMPEG_LICENSE "LGPL version 2.1 or later"
#define CONFIG_THIS_YEAR 2020
#define FFMPEG_DATADIR "/usr/local/share/ffmpeg"
#define AVCONV_DATADIR "/usr/local/share/ffmpeg"
#define CC_IDENT "emcc (Emscripten gcc/clang-like replacement) 1.39.14"
#define av_restrict restrict
#define EXTERN_PREFIX ""
#define EXTERN_ASM
#define BUILDSUF ""
#define SLIBSUF ".so"
#define HAVE_MMX2 HAVE_MMXEXT
#define SWS_MAX_FILTER_SIZE 256
#define ARCH_AARCH64 0
#define ARCH_ALPHA 0
#define ARCH_ARM 0
#define ARCH_AVR32 0
#define ARCH_AVR32_AP 0
#define ARCH_AVR32_UC 0
#define ARCH_BFIN 0
#define ARCH_IA64 0
#define ARCH_M68K 0
#define ARCH_MIPS 0
#define ARCH_MIPS64 0
#define ARCH_PARISC 0
#define ARCH_PPC 0
#define ARCH_PPC64 0
#define ARCH_S390 0
#define ARCH_SH4 0
#define ARCH_SPARC 0
#define ARCH_SPARC64 0
#define ARCH_TILEGX 0
#define ARCH_TILEPRO 0
#define ARCH_TOMI 0
#define ARCH_X86 1
#define ARCH_X86_32 1
#define ARCH_X86_64 0
#define HAVE_ARMV5TE 0
#define HAVE_ARMV6 0
#define HAVE_ARMV6T2 0
#define HAVE_ARMV8 0
#define HAVE_NEON 0
#define HAVE_VFP 0
#define HAVE_VFPV3 0
#define HAVE_SETEND 0
#define HAVE_ALTIVEC 0
#define HAVE_DCBZL 0
#define HAVE_LDBRX 0
#define HAVE_POWER8 0
#define HAVE_PPC4XX 0
#define HAVE_VSX 0
#define HAVE_AESNI 1
#define HAVE_AMD3DNOW 1
#define HAVE_AMD3DNOWEXT 1
#define HAVE_AVX 1
#define HAVE_AVX2 1
#define HAVE_AVX512 1
#define HAVE_FMA3 1
#define HAVE_FMA4 1
#define HAVE_MMX 1
#define HAVE_MMXEXT 1
#define HAVE_SSE 1
#define HAVE_SSE2 1
#define HAVE_SSE3 1
#define HAVE_SSE4 1
#define HAVE_SSE42 1
#define HAVE_SSSE3 1
#define HAVE_XOP 1
#define HAVE_CPUNOP 1
#define HAVE_I686 1
#define HAVE_MIPSFPU 0
#define HAVE_MIPS32R2 0
#define HAVE_MIPS32R5 0
#define HAVE_MIPS64R2 0
#define HAVE_MIPS32R6 0
#define HAVE_MIPS64R6 0
#define HAVE_MIPSDSP 0
#define HAVE_MIPSDSPR2 0
#define HAVE_MSA 0
#define HAVE_MSA2 0
#define HAVE_LOONGSON2 0
#define HAVE_LOONGSON3 0
#define HAVE_MMI 0
#define HAVE_ARMV5TE_EXTERNAL 0
#define HAVE_ARMV6_EXTERNAL 0
#define HAVE_ARMV6T2_EXTERNAL 0
#define HAVE_ARMV8_EXTERNAL 0
#define HAVE_NEON_EXTERNAL 0
#define HAVE_VFP_EXTERNAL 0
#define HAVE_VFPV3_EXTERNAL 0
#define HAVE_SETEND_EXTERNAL 0
#define HAVE_ALTIVEC_EXTERNAL 0
#define HAVE_DCBZL_EXTERNAL 0
#define HAVE_LDBRX_EXTERNAL 0
#define HAVE_POWER8_EXTERNAL 0
#define HAVE_PPC4XX_EXTERNAL 0
#define HAVE_VSX_EXTERNAL 0
#define HAVE_AESNI_EXTERNAL 0
#define HAVE_AMD3DNOW_EXTERNAL 0
#define HAVE_AMD3DNOWEXT_EXTERNAL 0
#define HAVE_AVX_EXTERNAL 0
#define HAVE_AVX2_EXTERNAL 0
#define HAVE_AVX512_EXTERNAL 0
#define HAVE_FMA3_EXTERNAL 0
#define HAVE_FMA4_EXTERNAL 0
#define HAVE_MMX_EXTERNAL 0
#define HAVE_MMXEXT_EXTERNAL 0
#define HAVE_SSE_EXTERNAL 0
#define HAVE_SSE2_EXTERNAL 0
#define HAVE_SSE3_EXTERNAL 0
#define HAVE_SSE4_EXTERNAL 0
#define HAVE_SSE42_EXTERNAL 0
#define HAVE_SSSE3_EXTERNAL 0
#define HAVE_XOP_EXTERNAL 0
#define HAVE_CPUNOP_EXTERNAL 0
#define HAVE_I686_EXTERNAL 0
#define HAVE_MIPSFPU_EXTERNAL 0
#define HAVE_MIPS32R2_EXTERNAL 0
#define HAVE_MIPS32R5_EXTERNAL 0
#define HAVE_MIPS64R2_EXTERNAL 0
#define HAVE_MIPS32R6_EXTERNAL 0
#define HAVE_MIPS64R6_EXTERNAL 0
#define HAVE_MIPSDSP_EXTERNAL 0
#define HAVE_MIPSDSPR2_EXTERNAL 0
#define HAVE_MSA_EXTERNAL 0
#define HAVE_MSA2_EXTERNAL 0
#define HAVE_LOONGSON2_EXTERNAL 0
#define HAVE_LOONGSON3_EXTERNAL 0
#define HAVE_MMI_EXTERNAL 0
#define HAVE_ARMV5TE_INLINE 0
#define HAVE_ARMV6_INLINE 0
#define HAVE_ARMV6T2_INLINE 0
#define HAVE_ARMV8_INLINE 0
#define HAVE_NEON_INLINE 0
#define HAVE_VFP_INLINE 0
#define HAVE_VFPV3_INLINE 0
#define HAVE_SETEND_INLINE 0
#define HAVE_ALTIVEC_INLINE 0
#define HAVE_DCBZL_INLINE 0
#define HAVE_LDBRX_INLINE 0
#define HAVE_POWER8_INLINE 0
#define HAVE_PPC4XX_INLINE 0
#define HAVE_VSX_INLINE 0
#define HAVE_AESNI_INLINE 0
#define HAVE_AMD3DNOW_INLINE 0
#define HAVE_AMD3DNOWEXT_INLINE 0
#define HAVE_AVX_INLINE 0
#define HAVE_AVX2_INLINE 0
#define HAVE_AVX512_INLINE 0
#define HAVE_FMA3_INLINE 0
#define HAVE_FMA4_INLINE 0
#define HAVE_MMX_INLINE 0
#define HAVE_MMXEXT_INLINE 0
#define HAVE_SSE_INLINE 0
#define HAVE_SSE2_INLINE 0
#define HAVE_SSE3_INLINE 0
#define HAVE_SSE4_INLINE 0
#define HAVE_SSE42_INLINE 0
#define HAVE_SSSE3_INLINE 0
#define HAVE_XOP_INLINE 0
#define HAVE_CPUNOP_INLINE 0
#define HAVE_I686_INLINE 0
#define HAVE_MIPSFPU_INLINE 0
#define HAVE_MIPS32R2_INLINE 0
#define HAVE_MIPS32R5_INLINE 0
#define HAVE_MIPS64R2_INLINE 0
#define HAVE_MIPS32R6_INLINE 0
#define HAVE_MIPS64R6_INLINE 0
#define HAVE_MIPSDSP_INLINE 0
#define HAVE_MIPSDSPR2_INLINE 0
#define HAVE_MSA_INLINE 0
#define HAVE_MSA2_INLINE 0
#define HAVE_LOONGSON2_INLINE 0
#define HAVE_LOONGSON3_INLINE 0
#define HAVE_MMI_INLINE 0
#define HAVE_ALIGNED_STACK 1
#define HAVE_FAST_64BIT 0
#define HAVE_FAST_CLZ 1
#define HAVE_FAST_CMOV 0
#define HAVE_LOCAL_ALIGNED 1
#define HAVE_SIMD_ALIGN_16 1
#define HAVE_SIMD_ALIGN_32 1
#define HAVE_SIMD_ALIGN_64 1
#define HAVE_ATOMIC_CAS_PTR 0
#define HAVE_MACHINE_RW_BARRIER 0
#define HAVE_MEMORYBARRIER 0
#define HAVE_MM_EMPTY 0
#define HAVE_RDTSC 0
#define HAVE_SEM_TIMEDWAIT 0
#define HAVE_SYNC_VAL_COMPARE_AND_SWAP 1
#define HAVE_CABS 1
#define HAVE_CEXP 1
#define HAVE_INLINE_ASM 0
#define HAVE_SYMVER 0
#define HAVE_X86ASM 0
#define HAVE_BIGENDIAN 0
#define HAVE_FAST_UNALIGNED 1
#define HAVE_ARPA_INET_H 1
#define HAVE_ASM_TYPES_H 0
#define HAVE_CDIO_PARANOIA_H 0
#define HAVE_CDIO_PARANOIA_PARANOIA_H 0
#define HAVE_CUDA_H 0
#define HAVE_DISPATCH_DISPATCH_H 0
#define HAVE_DEV_BKTR_IOCTL_BT848_H 0
#define HAVE_DEV_BKTR_IOCTL_METEOR_H 0
#define HAVE_DEV_IC_BT8XX_H 0
#define HAVE_DEV_VIDEO_BKTR_IOCTL_BT848_H 0
#define HAVE_DEV_VIDEO_METEOR_IOCTL_METEOR_H 0
#define HAVE_DIRECT_H 0
#define HAVE_DIRENT_H 1
#define HAVE_DXGIDEBUG_H 0
#define HAVE_DXVA_H 0
#define HAVE_ES2_GL_H 0
#define HAVE_GSM_H 0
#define HAVE_IO_H 0
#define HAVE_LINUX_PERF_EVENT_H 0
#define HAVE_MACHINE_IOCTL_BT848_H 0
#define HAVE_MACHINE_IOCTL_METEOR_H 0
#define HAVE_MALLOC_H 1
#define HAVE_OPENCV2_CORE_CORE_C_H 0
#define HAVE_OPENGL_GL3_H 0
#define HAVE_POLL_H 1
#define HAVE_SYS_PARAM_H 1
#define HAVE_SYS_RESOURCE_H 1
#define HAVE_SYS_SELECT_H 1
#define HAVE_SYS_SOUNDCARD_H 0
#define HAVE_SYS_TIME_H 1
#define HAVE_SYS_UN_H 1
#define HAVE_SYS_VIDEOIO_H 0
#define HAVE_TERMIOS_H 1
#define HAVE_UDPLITE_H 0
#define HAVE_UNISTD_H 1
#define HAVE_VALGRIND_VALGRIND_H 0
#define HAVE_WINDOWS_H 0
#define HAVE_WINSOCK2_H 0
#define HAVE_INTRINSICS_NEON 0
#define HAVE_ATANF 1
#define HAVE_ATAN2F 1
#define HAVE_CBRT 1
#define HAVE_CBRTF 1
#define HAVE_COPYSIGN 1
#define HAVE_COSF 1
#define HAVE_ERF 1
#define HAVE_EXP2 1
#define HAVE_EXP2F 1
#define HAVE_EXPF 1
#define HAVE_HYPOT 1
#define HAVE_ISFINITE 1
#define HAVE_ISINF 1
#define HAVE_ISNAN 1
#define HAVE_LDEXPF 1
#define HAVE_LLRINT 1
#define HAVE_LLRINTF 1
#define HAVE_LOG2 1
#define HAVE_LOG2F 1
#define HAVE_LOG10F 1
#define HAVE_LRINT 1
#define HAVE_LRINTF 1
#define HAVE_POWF 1
#define HAVE_RINT 1
#define HAVE_ROUND 1
#define HAVE_ROUNDF 1
#define HAVE_SINF 1
#define HAVE_TRUNC 1
#define HAVE_TRUNCF 1
#define HAVE_DOS_PATHS 0
#define HAVE_LIBC_MSVCRT 0
#define HAVE_MMAL_PARAMETER_VIDEO_MAX_NUM_CALLBACKS 0
#define HAVE_SECTION_DATA_REL_RO 1
#define HAVE_THREADS 0
#define HAVE_UWP 0
#define HAVE_WINRT 0
#define HAVE_ACCESS 1
#define HAVE_ALIGNED_MALLOC 0
#define HAVE_ARC4RANDOM 0
#define HAVE_CLOCK_GETTIME 1
#define HAVE_CLOSESOCKET 0
#define HAVE_COMMANDLINETOARGVW 0
#define HAVE_FCNTL 1
#define HAVE_GETADDRINFO 1
#define HAVE_GETHRTIME 0
#define HAVE_GETOPT 1
#define HAVE_GETMODULEHANDLE 0
#define HAVE_GETPROCESSAFFINITYMASK 0
#define HAVE_GETPROCESSMEMORYINFO 0
#define HAVE_GETPROCESSTIMES 0
#define HAVE_GETRUSAGE 1
#define HAVE_GETSTDHANDLE 0
#define HAVE_GETSYSTEMTIMEASFILETIME 0
#define HAVE_GETTIMEOFDAY 1
#define HAVE_GLOB 1
#define HAVE_GLXGETPROCADDRESS 0
#define HAVE_GMTIME_R 1
#define HAVE_INET_ATON 1
#define HAVE_ISATTY 1
#define HAVE_KBHIT 0
#define HAVE_LOCALTIME_R 1
#define HAVE_LSTAT 1
#define HAVE_LZO1X_999_COMPRESS 0
#define HAVE_MACH_ABSOLUTE_TIME 0
#define HAVE_MAPVIEWOFFILE 0
#define HAVE_MEMALIGN 1
#define HAVE_MKSTEMP 1
#define HAVE_MMAP 1
#define HAVE_MPROTECT 1
#define HAVE_NANOSLEEP 1
#define HAVE_PEEKNAMEDPIPE 0
#define HAVE_POSIX_MEMALIGN 1
#define HAVE_PTHREAD_CANCEL 0
#define HAVE_SCHED_GETAFFINITY 0
#define HAVE_SECITEMIMPORT 0
#define HAVE_SETCONSOLETEXTATTRIBUTE 0
#define HAVE_SETCONSOLECTRLHANDLER 0
#define HAVE_SETDLLDIRECTORY 0
#define HAVE_SETMODE 0
#define HAVE_SETRLIMIT 1
#define HAVE_SLEEP 0
#define HAVE_STRERROR_R 1
#define HAVE_SYSCONF 1
#define HAVE_SYSCTL 0
#define HAVE_USLEEP 1
#define HAVE_UTGETOSTYPEFROMSTRING 0
#define HAVE_VIRTUALALLOC 0
#define HAVE_WGLGETPROCADDRESS 0
#define HAVE_BCRYPT 0
#define HAVE_VAAPI_DRM 0
#define HAVE_VAAPI_X11 0
#define HAVE_VDPAU_X11 0
#define HAVE_PTHREADS 0
#define HAVE_OS2THREADS 0
#define HAVE_W32THREADS 0
#define HAVE_AS_ARCH_DIRECTIVE 0
#define HAVE_AS_DN_DIRECTIVE 0
#define HAVE_AS_FPU_DIRECTIVE 0
#define HAVE_AS_FUNC 0
#define HAVE_AS_OBJECT_ARCH 0
#define HAVE_ASM_MOD_Q 0
#define HAVE_BLOCKS_EXTENSION 0
#define HAVE_EBP_AVAILABLE 0
#define HAVE_EBX_AVAILABLE 0
#define HAVE_GNU_AS 0
#define HAVE_GNU_WINDRES 0
#define HAVE_IBM_ASM 0
#define HAVE_INLINE_ASM_DIRECT_SYMBOL_REFS 0
#define HAVE_INLINE_ASM_LABELS 1
#define HAVE_INLINE_ASM_NONLOCAL_LABELS 0
#define HAVE_PRAGMA_DEPRECATED 1
#define HAVE_RSYNC_CONTIMEOUT 1
#define HAVE_SYMVER_ASM_LABEL 0
#define HAVE_SYMVER_GNU_ASM 0
#define HAVE_VFP_ARGS 0
#define HAVE_XFORM_ASM 0
#define HAVE_XMM_CLOBBERS 0
#define HAVE_KCMVIDEOCODECTYPE_HEVC 0
#define HAVE_KCVPIXELFORMATTYPE_420YPCBCR10BIPLANARVIDEORANGE 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_SMPTE_ST_2084_PQ 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_ITU_R_2100_HLG 0
#define HAVE_KCVIMAGEBUFFERTRANSFERFUNCTION_LINEAR 0
#define HAVE_SOCKLEN_T 1
#define HAVE_STRUCT_ADDRINFO 1
#define HAVE_STRUCT_GROUP_SOURCE_REQ 1
#define HAVE_STRUCT_IP_MREQ_SOURCE 1
#define HAVE_STRUCT_IPV6_MREQ 1
#define HAVE_STRUCT_MSGHDR_MSG_FLAGS 1
#define HAVE_STRUCT_POLLFD 1
#define HAVE_STRUCT_RUSAGE_RU_MAXRSS 1
#define HAVE_STRUCT_SCTP_EVENT_SUBSCRIBE 0
#define HAVE_STRUCT_SOCKADDR_IN6 1
#define HAVE_STRUCT_SOCKADDR_SA_LEN 0
#define HAVE_STRUCT_SOCKADDR_STORAGE 1
#define HAVE_STRUCT_STAT_ST_MTIM_TV_NSEC 1
#define HAVE_STRUCT_V4L2_FRMIVALENUM_DISCRETE 0
#define HAVE_MAKEINFO 0
#define HAVE_MAKEINFO_HTML 0
#define HAVE_OPENCL_D3D11 0
#define HAVE_OPENCL_DRM_ARM 0
#define HAVE_OPENCL_DRM_BEIGNET 0
#define HAVE_OPENCL_DXVA2 0
#define HAVE_OPENCL_VAAPI_BEIGNET 0
#define HAVE_OPENCL_VAAPI_INTEL_MEDIA 0
#define HAVE_PERL 1
#define HAVE_POD2MAN 1
#define HAVE_TEXI2HTML 0
#define CONFIG_DOC 0
#define CONFIG_HTMLPAGES 0
#define CONFIG_MANPAGES 1
#define CONFIG_PODPAGES 1
#define CONFIG_TXTPAGES 0
#define CONFIG_AVIO_LIST_DIR_EXAMPLE 1
#define CONFIG_AVIO_READING_EXAMPLE 1
#define CONFIG_DECODE_AUDIO_EXAMPLE 1
#define CONFIG_DECODE_VIDEO_EXAMPLE 1
#define CONFIG_DEMUXING_DECODING_EXAMPLE 1
#define CONFIG_ENCODE_AUDIO_EXAMPLE 1
#define CONFIG_ENCODE_VIDEO_EXAMPLE 1
#define CONFIG_EXTRACT_MVS_EXAMPLE 1
#define CONFIG_FILTER_AUDIO_EXAMPLE 1
#define CONFIG_FILTERING_AUDIO_EXAMPLE 1
#define CONFIG_FILTERING_VIDEO_EXAMPLE 1
#define CONFIG_HTTP_MULTICLIENT_EXAMPLE 1
#define CONFIG_HW_DECODE_EXAMPLE 1
#define CONFIG_METADATA_EXAMPLE 1
#define CONFIG_MUXING_EXAMPLE 1
#define CONFIG_QSVDEC_EXAMPLE 0
#define CONFIG_REMUXING_EXAMPLE 1
#define CONFIG_RESAMPLING_AUDIO_EXAMPLE 1
#define CONFIG_SCALING_VIDEO_EXAMPLE 1
#define CONFIG_TRANSCODE_AAC_EXAMPLE 1
#define CONFIG_TRANSCODING_EXAMPLE 1
#define CONFIG_VAAPI_ENCODE_EXAMPLE 0
#define CONFIG_VAAPI_TRANSCODE_EXAMPLE 0
#define CONFIG_AVISYNTH 0
#define CONFIG_FREI0R 0
#define CONFIG_LIBCDIO 0
#define CONFIG_LIBDAVS2 0
#define CONFIG_LIBRUBBERBAND 0
#define CONFIG_LIBVIDSTAB 0
#define CONFIG_LIBX264 0
#define CONFIG_LIBX265 0
#define CONFIG_LIBXAVS 0
#define CONFIG_LIBXAVS2 0
#define CONFIG_LIBXVID 0
#define CONFIG_DECKLINK 0
#define CONFIG_LIBFDK_AAC 0
#define CONFIG_OPENSSL 0
#define CONFIG_LIBTLS 0
#define CONFIG_GMP 0
#define CONFIG_LIBARIBB24 0
#define CONFIG_LIBLENSFUN 0
#define CONFIG_LIBOPENCORE_AMRNB 0
#define CONFIG_LIBOPENCORE_AMRWB 0
#define CONFIG_LIBVMAF 0
#define CONFIG_LIBVO_AMRWBENC 0
#define CONFIG_MBEDTLS 0
#define CONFIG_RKMPP 0
#define CONFIG_LIBSMBCLIENT 0
#define CONFIG_CHROMAPRINT 0
#define CONFIG_GCRYPT 0
#define CONFIG_GNUTLS 0
#define CONFIG_JNI 0
#define CONFIG_LADSPA 0
#define CONFIG_LIBAOM 0
#define CONFIG_LIBASS 0
#define CONFIG_LIBBLURAY 0
#define CONFIG_LIBBS2B 0
#define CONFIG_LIBCACA 0
#define CONFIG_LIBCELT 0
#define CONFIG_LIBCODEC2 0
#define CONFIG_LIBDAV1D 0
#define CONFIG_LIBDC1394 0
#define CONFIG_LIBDRM 0
#define CONFIG_LIBFLITE 0
#define CONFIG_LIBFONTCONFIG 0
#define CONFIG_LIBFREETYPE 0
#define CONFIG_LIBFRIBIDI 0
#define CONFIG_LIBGLSLANG 0
#define CONFIG_LIBGME 0
#define CONFIG_LIBGSM 0
#define CONFIG_LIBIEC61883 0
#define CONFIG_LIBILBC 0
#define CONFIG_LIBJACK 0
#define CONFIG_LIBKLVANC 0
#define CONFIG_LIBKVAZAAR 0
#define CONFIG_LIBMODPLUG 0
#define CONFIG_LIBMP3LAME 0
#define CONFIG_LIBMYSOFA 0
#define CONFIG_LIBOPENCV 0
#define CONFIG_LIBOPENH264 0
#define CONFIG_LIBOPENJPEG 0
#define CONFIG_LIBOPENMPT 0
#define CONFIG_LIBOPUS 0
#define CONFIG_LIBPULSE 0
#define CONFIG_LIBRABBITMQ 0
#define CONFIG_LIBRAV1E 0
#define CONFIG_LIBRSVG 0
#define CONFIG_LIBRTMP 0
#define CONFIG_LIBSHINE 0
#define CONFIG_LIBSMBCLIENT 0
#define CONFIG_LIBSNAPPY 0
#define CONFIG_LIBSOXR 0
#define CONFIG_LIBSPEEX 0
#define CONFIG_LIBSRT 0
#define CONFIG_LIBSSH 0
#define CONFIG_LIBTENSORFLOW 0
#define CONFIG_LIBTESSERACT 0
#define CONFIG_LIBTHEORA 0
#define CONFIG_LIBTWOLAME 0
#define CONFIG_LIBV4L2 0
#define CONFIG_LIBVORBIS 0
#define CONFIG_LIBVPX 0
#define CONFIG_LIBWAVPACK 0
#define CONFIG_LIBWEBP 0
#define CONFIG_LIBXML2 0
#define CONFIG_LIBZIMG 0
#define CONFIG_LIBZMQ 0
#define CONFIG_LIBZVBI 0
#define CONFIG_LV2 0
#define CONFIG_MEDIACODEC 0
#define CONFIG_OPENAL 0
#define CONFIG_OPENGL 0
#define CONFIG_POCKETSPHINX 0
#define CONFIG_VAPOURSYNTH 0
#define CONFIG_ALSA 0
#define CONFIG_APPKIT 0
#define CONFIG_AVFOUNDATION 0
#define CONFIG_BZLIB 0
#define CONFIG_COREIMAGE 0
#define CONFIG_ICONV 1
#define CONFIG_LIBXCB 0
#define CONFIG_LIBXCB_SHM 0
#define CONFIG_LIBXCB_SHAPE 0
#define CONFIG_LIBXCB_XFIXES 0
#define CONFIG_LZMA 0
#define CONFIG_MEDIAFOUNDATION 0
#define CONFIG_SCHANNEL 0
#define CONFIG_SDL2 1
#define CONFIG_SECURETRANSPORT 0
#define CONFIG_SNDIO 0
#define CONFIG_XLIB 0
#define CONFIG_ZLIB 0
#define CONFIG_CUDA_NVCC 0
#define CONFIG_CUDA_SDK 0
#define CONFIG_LIBNPP 0
#define CONFIG_LIBMFX 0
#define CONFIG_MMAL 0
#define CONFIG_OMX 0
#define CONFIG_OPENCL 0
#define CONFIG_VULKAN 0
#define CONFIG_AMF 0
#define CONFIG_AUDIOTOOLBOX 0
#define CONFIG_CRYSTALHD 0
#define CONFIG_CUDA 0
#define CONFIG_CUDA_LLVM 0
#define CONFIG_CUVID 0
#define CONFIG_D3D11VA 0
#define CONFIG_DXVA2 0
#define CONFIG_FFNVCODEC 0
#define CONFIG_NVDEC 0
#define CONFIG_NVENC 0
#define CONFIG_VAAPI 0
#define CONFIG_VDPAU 0
#define CONFIG_VIDEOTOOLBOX 0
#define CONFIG_V4L2_M2M 0
#define CONFIG_XVMC 0
#define CONFIG_FTRAPV 0
#define CONFIG_GRAY 0
#define CONFIG_HARDCODED_TABLES 0
#define CONFIG_OMX_RPI 0
#define CONFIG_RUNTIME_CPUDETECT 1
#define CONFIG_SAFE_BITSTREAM_READER 1
#define CONFIG_SHARED 0
#define CONFIG_SMALL 0
#define CONFIG_STATIC 1
#define CONFIG_SWSCALE_ALPHA 1
#define CONFIG_GPL 0
#define CONFIG_NONFREE 0
#define CONFIG_VERSION3 0
#define CONFIG_AVDEVICE 1
#define CONFIG_AVFILTER 1
#define CONFIG_SWSCALE 1
#define CONFIG_POSTPROC 0
#define CONFIG_AVFORMAT 1
#define CONFIG_AVCODEC 1
#define CONFIG_SWRESAMPLE 1
#define CONFIG_AVRESAMPLE 0
#define CONFIG_AVUTIL 1
#define CONFIG_FFPLAY 1
#define CONFIG_FFPROBE 0
#define CONFIG_FFMPEG 1
#define CONFIG_DCT 1
#define CONFIG_DWT 1
#define CONFIG_ERROR_RESILIENCE 1
#define CONFIG_FAAN 1
#define CONFIG_FAST_UNALIGNED 1
#define CONFIG_FFT 1
#define CONFIG_LSP 1
#define CONFIG_LZO 1
#define CONFIG_MDCT 1
#define CONFIG_PIXELUTILS 1
#define CONFIG_NETWORK 1
#define CONFIG_RDFT 1
#define CONFIG_AUTODETECT 0
#define CONFIG_FONTCONFIG 0
#define CONFIG_LARGE_TESTS 1
#define CONFIG_LINUX_PERF 0
#define CONFIG_MEMORY_POISONING 0
#define CONFIG_NEON_CLOBBER_TEST 0
#define CONFIG_OSSFUZZ 0
#define CONFIG_PIC 1
#define CONFIG_THUMB 0
#define CONFIG_VALGRIND_BACKTRACE 0
#define CONFIG_XMM_CLOBBER_TEST 0
#define CONFIG_BSFS 1
#define CONFIG_DECODERS 1
#define CONFIG_ENCODERS 1
#define CONFIG_HWACCELS 0
#define CONFIG_PARSERS 1
#define CONFIG_INDEVS 1
#define CONFIG_OUTDEVS 1
#define CONFIG_FILTERS 1
#define CONFIG_DEMUXERS 1
#define CONFIG_MUXERS 1
#define CONFIG_PROTOCOLS 1
#define CONFIG_AANDCTTABLES 1
#define CONFIG_AC3DSP 1
#define CONFIG_ADTS_HEADER 1
#define CONFIG_AUDIO_FRAME_QUEUE 1
#define CONFIG_AUDIODSP 1
#define CONFIG_BLOCKDSP 1
#define CONFIG_BSWAPDSP 1
#define CONFIG_CABAC 1
#define CONFIG_CBS 1
#define CONFIG_CBS_AV1 1
#define CONFIG_CBS_H264 1
#define CONFIG_CBS_H265 1
#define CONFIG_CBS_JPEG 0
#define CONFIG_CBS_MPEG2 1
#define CONFIG_CBS_VP9 1
#define CONFIG_DIRAC_PARSE 1
#define CONFIG_DNN 1
#define CONFIG_DVPROFILE 1
#define CONFIG_EXIF 1
#define CONFIG_FAANDCT 1
#define CONFIG_FAANIDCT 1
#define CONFIG_FDCTDSP 1
#define CONFIG_FLACDSP 1
#define CONFIG_FMTCONVERT 1
#define CONFIG_FRAME_THREAD_ENCODER 0
#define CONFIG_G722DSP 1
#define CONFIG_GOLOMB 1
#define CONFIG_GPLV3 0
#define CONFIG_H263DSP 1
#define CONFIG_H264CHROMA 1
#define CONFIG_H264DSP 1
#define CONFIG_H264PARSE 1
#define CONFIG_H264PRED 1
#define CONFIG_H264QPEL 1
#define CONFIG_HEVCPARSE 1
#define CONFIG_HPELDSP 1
#define CONFIG_HUFFMAN 1
#define CONFIG_HUFFYUVDSP 1
#define CONFIG_HUFFYUVENCDSP 1
#define CONFIG_IDCTDSP 1
#define CONFIG_IIRFILTER 1
#define CONFIG_MDCT15 1
#define CONFIG_INTRAX8 1
#define CONFIG_ISO_MEDIA 1
#define CONFIG_IVIDSP 1
#define CONFIG_JPEGTABLES 1
#define CONFIG_LGPLV3 0
#define CONFIG_LIBX262 0
#define CONFIG_LLAUDDSP 1
#define CONFIG_LLVIDDSP 1
#define CONFIG_LLVIDENCDSP 1
#define CONFIG_LPC 1
#define CONFIG_LZF 1
#define CONFIG_ME_CMP 1
#define CONFIG_MPEG_ER 1
#define CONFIG_MPEGAUDIO 1
#define CONFIG_MPEGAUDIODSP 1
#define CONFIG_MPEGAUDIOHEADER 1
#define CONFIG_MPEGVIDEO 1
#define CONFIG_MPEGVIDEOENC 1
#define CONFIG_MSS34DSP 1
#define CONFIG_PIXBLOCKDSP 1
#define CONFIG_QPELDSP 1
#define CONFIG_QSV 0
#define CONFIG_QSVDEC 0
#define CONFIG_QSVENC 0
#define CONFIG_QSVVPP 0
#define CONFIG_RANGECODER 1
#define CONFIG_RIFFDEC 1
#define CONFIG_RIFFENC 1
#define CONFIG_RTPDEC 1
#define CONFIG_RTPENC_CHAIN 1
#define CONFIG_RV34DSP 1
#define CONFIG_SCENE_SAD 1
#define CONFIG_SINEWIN 1
#define CONFIG_SNAPPY 1
#define CONFIG_SRTP 1
#define CONFIG_STARTCODE 1
#define CONFIG_TEXTUREDSP 1
#define CONFIG_TEXTUREDSPENC 0
#define CONFIG_TPELDSP 1
#define CONFIG_VAAPI_1 0
#define CONFIG_VAAPI_ENCODE 0
#define CONFIG_VC1DSP 1
#define CONFIG_VIDEODSP 1
#define CONFIG_VP3DSP 1
#define CONFIG_VP56DSP 1
#define CONFIG_VP8DSP 1
#define CONFIG_WMA_FREQS 1
#define CONFIG_WMV2DSP 1
#define CONFIG_AAC_ADTSTOASC_BSF 1
#define CONFIG_AV1_FRAME_MERGE_BSF 1
#define CONFIG_AV1_FRAME_SPLIT_BSF 1
#define CONFIG_AV1_METADATA_BSF 1
#define CONFIG_CHOMP_BSF 1
#define CONFIG_DUMP_EXTRADATA_BSF 1
#define CONFIG_DCA_CORE_BSF 1
#define CONFIG_EAC3_CORE_BSF 1
#define CONFIG_EXTRACT_EXTRADATA_BSF 1
#define CONFIG_FILTER_UNITS_BSF 1
#define CONFIG_H264_METADATA_BSF 1
#define CONFIG_H264_MP4TOANNEXB_BSF 1
#define CONFIG_H264_REDUNDANT_PPS_BSF 1
#define CONFIG_HAPQA_EXTRACT_BSF 1
#define CONFIG_HEVC_METADATA_BSF 1
#define CONFIG_HEVC_MP4TOANNEXB_BSF 1
#define CONFIG_IMX_DUMP_HEADER_BSF 1
#define CONFIG_MJPEG2JPEG_BSF 1
#define CONFIG_MJPEGA_DUMP_HEADER_BSF 1
#define CONFIG_MP3_HEADER_DECOMPRESS_BSF 1
#define CONFIG_MPEG2_METADATA_BSF 1
#define CONFIG_MPEG4_UNPACK_BFRAMES_BSF 1
#define CONFIG_MOV2TEXTSUB_BSF 1
#define CONFIG_NOISE_BSF 1
#define CONFIG_NULL_BSF 1
#define CONFIG_OPUS_METADATA_BSF 1
#define CONFIG_PCM_RECHUNK_BSF 1
#define CONFIG_PRORES_METADATA_BSF 1
#define CONFIG_REMOVE_EXTRADATA_BSF 1
#define CONFIG_TEXT2MOVSUB_BSF 1
#define CONFIG_TRACE_HEADERS_BSF 1
#define CONFIG_TRUEHD_CORE_BSF 1
#define CONFIG_VP9_METADATA_BSF 1
#define CONFIG_VP9_RAW_REORDER_BSF 1
#define CONFIG_VP9_SUPERFRAME_BSF 1
#define CONFIG_VP9_SUPERFRAME_SPLIT_BSF 1
#define CONFIG_AASC_DECODER 1
#define CONFIG_AIC_DECODER 1
#define CONFIG_ALIAS_PIX_DECODER 1
#define CONFIG_AGM_DECODER 1
#define CONFIG_AMV_DECODER 1
#define CONFIG_ANM_DECODER 1
#define CONFIG_ANSI_DECODER 1
#define CONFIG_APNG_DECODER 0
#define CONFIG_ARBC_DECODER 1
#define CONFIG_ASV1_DECODER 1
#define CONFIG_ASV2_DECODER 1
#define CONFIG_AURA_DECODER 1
#define CONFIG_AURA2_DECODER 1
#define CONFIG_AVRP_DECODER 1
#define CONFIG_AVRN_DECODER 1
#define CONFIG_AVS_DECODER 1
#define CONFIG_AVUI_DECODER 1
#define CONFIG_AYUV_DECODER 1
#define CONFIG_BETHSOFTVID_DECODER 1
#define CONFIG_BFI_DECODER 1
#define CONFIG_BINK_DECODER 1
#define CONFIG_BITPACKED_DECODER 1
#define CONFIG_BMP_DECODER 1
#define CONFIG_BMV_VIDEO_DECODER 1
#define CONFIG_BRENDER_PIX_DECODER 1
#define CONFIG_C93_DECODER 1
#define CONFIG_CAVS_DECODER 1
#define CONFIG_CDGRAPHICS_DECODER 1
#define CONFIG_CDTOONS_DECODER 1
#define CONFIG_CDXL_DECODER 1
#define CONFIG_CFHD_DECODER 1
#define CONFIG_CINEPAK_DECODER 1
#define CONFIG_CLEARVIDEO_DECODER 1
#define CONFIG_CLJR_DECODER 1
#define CONFIG_CLLC_DECODER 1
#define CONFIG_COMFORTNOISE_DECODER 1
#define CONFIG_CPIA_DECODER 1
#define CONFIG_CSCD_DECODER 1
#define CONFIG_CYUV_DECODER 1
#define CONFIG_DDS_DECODER 1
#define CONFIG_DFA_DECODER 1
#define CONFIG_DIRAC_DECODER 1
#define CONFIG_DNXHD_DECODER 1
#define CONFIG_DPX_DECODER 1
#define CONFIG_DSICINVIDEO_DECODER 1
#define CONFIG_DVAUDIO_DECODER 1
#define CONFIG_DVVIDEO_DECODER 1
#define CONFIG_DXA_DECODER 0
#define CONFIG_DXTORY_DECODER 1
#define CONFIG_DXV_DECODER 1
#define CONFIG_EACMV_DECODER 1
#define CONFIG_EAMAD_DECODER 1
#define CONFIG_EATGQ_DECODER 1
#define CONFIG_EATGV_DECODER 1
#define CONFIG_EATQI_DECODER 1
#define CONFIG_EIGHTBPS_DECODER 1
#define CONFIG_EIGHTSVX_EXP_DECODER 1
#define CONFIG_EIGHTSVX_FIB_DECODER 1
#define CONFIG_ESCAPE124_DECODER 1
#define CONFIG_ESCAPE130_DECODER 1
#define CONFIG_EXR_DECODER 0
#define CONFIG_FFV1_DECODER 1
#define CONFIG_FFVHUFF_DECODER 1
#define CONFIG_FIC_DECODER 1
#define CONFIG_FITS_DECODER 1
#define CONFIG_FLASHSV_DECODER 0
#define CONFIG_FLASHSV2_DECODER 0
#define CONFIG_FLIC_DECODER 1
#define CONFIG_FLV_DECODER 1
#define CONFIG_FMVC_DECODER 1
#define CONFIG_FOURXM_DECODER 1
#define CONFIG_FRAPS_DECODER 1
#define CONFIG_FRWU_DECODER 1
#define CONFIG_G2M_DECODER 0
#define CONFIG_GDV_DECODER 1
#define CONFIG_GIF_DECODER 1
#define CONFIG_H261_DECODER 1
#define CONFIG_H263_DECODER 1
#define CONFIG_H263I_DECODER 1
#define CONFIG_H263P_DECODER 1
#define CONFIG_H263_V4L2M2M_DECODER 0
#define CONFIG_H264_DECODER 1
#define CONFIG_H264_CRYSTALHD_DECODER 0
#define CONFIG_H264_V4L2M2M_DECODER 0
#define CONFIG_H264_MEDIACODEC_DECODER 0
#define CONFIG_H264_MMAL_DECODER 0
#define CONFIG_H264_QSV_DECODER 0
#define CONFIG_H264_RKMPP_DECODER 0
#define CONFIG_HAP_DECODER 1
#define CONFIG_HEVC_DECODER 1
#define CONFIG_HEVC_QSV_DECODER 0
#define CONFIG_HEVC_RKMPP_DECODER 0
#define CONFIG_HEVC_V4L2M2M_DECODER 0
#define CONFIG_HNM4_VIDEO_DECODER 1
#define CONFIG_HQ_HQA_DECODER 1
#define CONFIG_HQX_DECODER 1
#define CONFIG_HUFFYUV_DECODER 1
#define CONFIG_HYMT_DECODER 1
#define CONFIG_IDCIN_DECODER 1
#define CONFIG_IFF_ILBM_DECODER 1
#define CONFIG_IMM4_DECODER 1
#define CONFIG_IMM5_DECODER 1
#define CONFIG_INDEO2_DECODER 1
#define CONFIG_INDEO3_DECODER 1
#define CONFIG_INDEO4_DECODER 1
#define CONFIG_INDEO5_DECODER 1
#define CONFIG_INTERPLAY_VIDEO_DECODER 1
#define CONFIG_JPEG2000_DECODER 1
#define CONFIG_JPEGLS_DECODER 1
#define CONFIG_JV_DECODER 1
#define CONFIG_KGV1_DECODER 1
#define CONFIG_KMVC_DECODER 1
#define CONFIG_LAGARITH_DECODER 1
#define CONFIG_LOCO_DECODER 1
#define CONFIG_LSCR_DECODER 0
#define CONFIG_M101_DECODER 1
#define CONFIG_MAGICYUV_DECODER 1
#define CONFIG_MDEC_DECODER 1
#define CONFIG_MIMIC_DECODER 1
#define CONFIG_MJPEG_DECODER 1
#define CONFIG_MJPEGB_DECODER 1
#define CONFIG_MMVIDEO_DECODER 1
#define CONFIG_MOTIONPIXELS_DECODER 1
#define CONFIG_MPEG1VIDEO_DECODER 1
#define CONFIG_MPEG2VIDEO_DECODER 1
#define CONFIG_MPEG4_DECODER 1
#define CONFIG_MPEG4_CRYSTALHD_DECODER 0
#define CONFIG_MPEG4_V4L2M2M_DECODER 0
#define CONFIG_MPEG4_MMAL_DECODER 0
#define CONFIG_MPEGVIDEO_DECODER 1
#define CONFIG_MPEG1_V4L2M2M_DECODER 0
#define CONFIG_MPEG2_MMAL_DECODER 0
#define CONFIG_MPEG2_CRYSTALHD_DECODER 0
#define CONFIG_MPEG2_V4L2M2M_DECODER 0
#define CONFIG_MPEG2_QSV_DECODER 0
#define CONFIG_MPEG2_MEDIACODEC_DECODER 0
#define CONFIG_MSA1_DECODER 1
#define CONFIG_MSCC_DECODER 0
#define CONFIG_MSMPEG4V1_DECODER 1
#define CONFIG_MSMPEG4V2_DECODER 1
#define CONFIG_MSMPEG4V3_DECODER 1
#define CONFIG_MSMPEG4_CRYSTALHD_DECODER 0
#define CONFIG_MSRLE_DECODER 1
#define CONFIG_MSS1_DECODER 1
#define CONFIG_MSS2_DECODER 1
#define CONFIG_MSVIDEO1_DECODER 1
#define CONFIG_MSZH_DECODER 1
#define CONFIG_MTS2_DECODER 1
#define CONFIG_MV30_DECODER 1
#define CONFIG_MVC1_DECODER 1
#define CONFIG_MVC2_DECODER 1
#define CONFIG_MVDV_DECODER 1
#define CONFIG_MVHA_DECODER 0
#define CONFIG_MWSC_DECODER 0
#define CONFIG_MXPEG_DECODER 1
#define CONFIG_NOTCHLC_DECODER 1
#define CONFIG_NUV_DECODER 1
#define CONFIG_PAF_VIDEO_DECODER 1
#define CONFIG_PAM_DECODER 1
#define CONFIG_PBM_DECODER 1
#define CONFIG_PCX_DECODER 1
#define CONFIG_PFM_DECODER 1
#define CONFIG_PGM_DECODER 1
#define CONFIG_PGMYUV_DECODER 1
#define CONFIG_PICTOR_DECODER 1
#define CONFIG_PIXLET_DECODER 1
#define CONFIG_PNG_DECODER 0
#define CONFIG_PPM_DECODER 1
#define CONFIG_PRORES_DECODER 1
#define CONFIG_PROSUMER_DECODER 1
#define CONFIG_PSD_DECODER 1
#define CONFIG_PTX_DECODER 1
#define CONFIG_QDRAW_DECODER 1
#define CONFIG_QPEG_DECODER 1
#define CONFIG_QTRLE_DECODER 1
#define CONFIG_R10K_DECODER 1
#define CONFIG_R210_DECODER 1
#define CONFIG_RASC_DECODER 0
#define CONFIG_RAWVIDEO_DECODER 1
#define CONFIG_RL2_DECODER 1
#define CONFIG_ROQ_DECODER 1
#define CONFIG_RPZA_DECODER 1
#define CONFIG_RSCC_DECODER 0
#define CONFIG_RV10_DECODER 1
#define CONFIG_RV20_DECODER 1
#define CONFIG_RV30_DECODER 1
#define CONFIG_RV40_DECODER 1
#define CONFIG_S302M_DECODER 1
#define CONFIG_SANM_DECODER 1
#define CONFIG_SCPR_DECODER 1
#define CONFIG_SCREENPRESSO_DECODER 0
#define CONFIG_SGI_DECODER 1
#define CONFIG_SGIRLE_DECODER 1
#define CONFIG_SHEERVIDEO_DECODER 1
#define CONFIG_SMACKER_DECODER 1
#define CONFIG_SMC_DECODER 1
#define CONFIG_SMVJPEG_DECODER 1
#define CONFIG_SNOW_DECODER 1
#define CONFIG_SP5X_DECODER 1
#define CONFIG_SPEEDHQ_DECODER 1
#define CONFIG_SRGC_DECODER 0
#define CONFIG_SUNRAST_DECODER 1
#define CONFIG_SVQ1_DECODER 1
#define CONFIG_SVQ3_DECODER 1
#define CONFIG_TARGA_DECODER 1
#define CONFIG_TARGA_Y216_DECODER 1
#define CONFIG_TDSC_DECODER 0
#define CONFIG_THEORA_DECODER 1
#define CONFIG_THP_DECODER 1
#define CONFIG_TIERTEXSEQVIDEO_DECODER 1
#define CONFIG_TIFF_DECODER 1
#define CONFIG_TMV_DECODER 1
#define CONFIG_TRUEMOTION1_DECODER 1
#define CONFIG_TRUEMOTION2_DECODER 1
#define CONFIG_TRUEMOTION2RT_DECODER 1
#define CONFIG_TSCC_DECODER 0
#define CONFIG_TSCC2_DECODER 1
#define CONFIG_TXD_DECODER 1
#define CONFIG_ULTI_DECODER 1
#define CONFIG_UTVIDEO_DECODER 1
#define CONFIG_V210_DECODER 1
#define CONFIG_V210X_DECODER 1
#define CONFIG_V308_DECODER 1
#define CONFIG_V408_DECODER 1
#define CONFIG_V410_DECODER 1
#define CONFIG_VB_DECODER 1
#define CONFIG_VBLE_DECODER 1
#define CONFIG_VC1_DECODER 1
#define CONFIG_VC1_CRYSTALHD_DECODER 0
#define CONFIG_VC1IMAGE_DECODER 1
#define CONFIG_VC1_MMAL_DECODER 0
#define CONFIG_VC1_QSV_DECODER 0
#define CONFIG_VC1_V4L2M2M_DECODER 0
#define CONFIG_VCR1_DECODER 1
#define CONFIG_VMDVIDEO_DECODER 1
#define CONFIG_VMNC_DECODER 1
#define CONFIG_VP3_DECODER 1
#define CONFIG_VP4_DECODER 1
#define CONFIG_VP5_DECODER 1
#define CONFIG_VP6_DECODER 1
#define CONFIG_VP6A_DECODER 1
#define CONFIG_VP6F_DECODER 1
#define CONFIG_VP7_DECODER 1
#define CONFIG_VP8_DECODER 1
#define CONFIG_VP8_RKMPP_DECODER 0
#define CONFIG_VP8_V4L2M2M_DECODER 0
#define CONFIG_VP9_DECODER 1
#define CONFIG_VP9_RKMPP_DECODER 0
#define CONFIG_VP9_V4L2M2M_DECODER 0
#define CONFIG_VQA_DECODER 1
#define CONFIG_WEBP_DECODER 1
#define CONFIG_WCMV_DECODER 0
#define CONFIG_WRAPPED_AVFRAME_DECODER 1
#define CONFIG_WMV1_DECODER 1
#define CONFIG_WMV2_DECODER 1
#define CONFIG_WMV3_DECODER 1
#define CONFIG_WMV3_CRYSTALHD_DECODER 0
#define CONFIG_WMV3IMAGE_DECODER 1
#define CONFIG_WNV1_DECODER 1
#define CONFIG_XAN_WC3_DECODER 1
#define CONFIG_XAN_WC4_DECODER 1
#define CONFIG_XBM_DECODER 1
#define CONFIG_XFACE_DECODER 1
#define CONFIG_XL_DECODER 1
#define CONFIG_XPM_DECODER 1
#define CONFIG_XWD_DECODER 1
#define CONFIG_Y41P_DECODER 1
#define CONFIG_YLC_DECODER 1
#define CONFIG_YOP_DECODER 1
#define CONFIG_YUV4_DECODER 1
#define CONFIG_ZERO12V_DECODER 1
#define CONFIG_ZEROCODEC_DECODER 0
#define CONFIG_ZLIB_DECODER 0
#define CONFIG_ZMBV_DECODER 0
#define CONFIG_AAC_DECODER 1
#define CONFIG_AAC_FIXED_DECODER 1
#define CONFIG_AAC_LATM_DECODER 1
#define CONFIG_AC3_DECODER 1
#define CONFIG_AC3_FIXED_DECODER 1
#define CONFIG_ACELP_KELVIN_DECODER 1
#define CONFIG_ALAC_DECODER 1
#define CONFIG_ALS_DECODER 1
#define CONFIG_AMRNB_DECODER 1
#define CONFIG_AMRWB_DECODER 1
#define CONFIG_APE_DECODER 1
#define CONFIG_APTX_DECODER 1
#define CONFIG_APTX_HD_DECODER 1
#define CONFIG_ATRAC1_DECODER 1
#define CONFIG_ATRAC3_DECODER 1
#define CONFIG_ATRAC3AL_DECODER 1
#define CONFIG_ATRAC3P_DECODER 1
#define CONFIG_ATRAC3PAL_DECODER 1
#define CONFIG_ATRAC9_DECODER 1
#define CONFIG_BINKAUDIO_DCT_DECODER 1
#define CONFIG_BINKAUDIO_RDFT_DECODER 1
#define CONFIG_BMV_AUDIO_DECODER 1
#define CONFIG_COOK_DECODER 1
#define CONFIG_DCA_DECODER 1
#define CONFIG_DOLBY_E_DECODER 1
#define CONFIG_DSD_LSBF_DECODER 1
#define CONFIG_DSD_MSBF_DECODER 1
#define CONFIG_DSD_LSBF_PLANAR_DECODER 1
#define CONFIG_DSD_MSBF_PLANAR_DECODER 1
#define CONFIG_DSICINAUDIO_DECODER 1
#define CONFIG_DSS_SP_DECODER 1
#define CONFIG_DST_DECODER 1
#define CONFIG_EAC3_DECODER 1
#define CONFIG_EVRC_DECODER 1
#define CONFIG_FFWAVESYNTH_DECODER 1
#define CONFIG_FLAC_DECODER 1
#define CONFIG_G723_1_DECODER 1
#define CONFIG_G729_DECODER 1
#define CONFIG_GSM_DECODER 1
#define CONFIG_GSM_MS_DECODER 1
#define CONFIG_HCA_DECODER 1
#define CONFIG_HCOM_DECODER 1
#define CONFIG_IAC_DECODER 1
#define CONFIG_ILBC_DECODER 1
#define CONFIG_IMC_DECODER 1
#define CONFIG_INTERPLAY_ACM_DECODER 1
#define CONFIG_MACE3_DECODER 1
#define CONFIG_MACE6_DECODER 1
#define CONFIG_METASOUND_DECODER 1
#define CONFIG_MLP_DECODER 1
#define CONFIG_MP1_DECODER 1
#define CONFIG_MP1FLOAT_DECODER 1
#define CONFIG_MP2_DECODER 1
#define CONFIG_MP2FLOAT_DECODER 1
#define CONFIG_MP3FLOAT_DECODER 1
#define CONFIG_MP3_DECODER 1
#define CONFIG_MP3ADUFLOAT_DECODER 1
#define CONFIG_MP3ADU_DECODER 1
#define CONFIG_MP3ON4FLOAT_DECODER 1
#define CONFIG_MP3ON4_DECODER 1
#define CONFIG_MPC7_DECODER 1
#define CONFIG_MPC8_DECODER 1
#define CONFIG_NELLYMOSER_DECODER 1
#define CONFIG_ON2AVC_DECODER 1
#define CONFIG_OPUS_DECODER 1
#define CONFIG_PAF_AUDIO_DECODER 1
#define CONFIG_QCELP_DECODER 1
#define CONFIG_QDM2_DECODER 1
#define CONFIG_QDMC_DECODER 1
#define CONFIG_RA_144_DECODER 1
#define CONFIG_RA_288_DECODER 1
#define CONFIG_RALF_DECODER 1
#define CONFIG_SBC_DECODER 1
#define CONFIG_SHORTEN_DECODER 1
#define CONFIG_SIPR_DECODER 1
#define CONFIG_SIREN_DECODER 1
#define CONFIG_SMACKAUD_DECODER 1
#define CONFIG_SONIC_DECODER 1
#define CONFIG_TAK_DECODER 1
#define CONFIG_TRUEHD_DECODER 1
#define CONFIG_TRUESPEECH_DECODER 1
#define CONFIG_TTA_DECODER 1
#define CONFIG_TWINVQ_DECODER 1
#define CONFIG_VMDAUDIO_DECODER 1
#define CONFIG_VORBIS_DECODER 1
#define CONFIG_WAVPACK_DECODER 1
#define CONFIG_WMALOSSLESS_DECODER 1
#define CONFIG_WMAPRO_DECODER 1
#define CONFIG_WMAV1_DECODER 1
#define CONFIG_WMAV2_DECODER 1
#define CONFIG_WMAVOICE_DECODER 1
#define CONFIG_WS_SND1_DECODER 1
#define CONFIG_XMA1_DECODER 1
#define CONFIG_XMA2_DECODER 1
#define CONFIG_PCM_ALAW_DECODER 1
#define CONFIG_PCM_BLURAY_DECODER 1
#define CONFIG_PCM_DVD_DECODER 1
#define CONFIG_PCM_F16LE_DECODER 1
#define CONFIG_PCM_F24LE_DECODER 1
#define CONFIG_PCM_F32BE_DECODER 1
#define CONFIG_PCM_F32LE_DECODER 1
#define CONFIG_PCM_F64BE_DECODER 1
#define CONFIG_PCM_F64LE_DECODER 1
#define CONFIG_PCM_LXF_DECODER 1
#define CONFIG_PCM_MULAW_DECODER 1
#define CONFIG_PCM_S8_DECODER 1
#define CONFIG_PCM_S8_PLANAR_DECODER 1
#define CONFIG_PCM_S16BE_DECODER 1
#define CONFIG_PCM_S16BE_PLANAR_DECODER 1
#define CONFIG_PCM_S16LE_DECODER 1
#define CONFIG_PCM_S16LE_PLANAR_DECODER 1
#define CONFIG_PCM_S24BE_DECODER 1
#define CONFIG_PCM_S24DAUD_DECODER 1
#define CONFIG_PCM_S24LE_DECODER 1
#define CONFIG_PCM_S24LE_PLANAR_DECODER 1
#define CONFIG_PCM_S32BE_DECODER 1
#define CONFIG_PCM_S32LE_DECODER 1
#define CONFIG_PCM_S32LE_PLANAR_DECODER 1
#define CONFIG_PCM_S64BE_DECODER 1
#define CONFIG_PCM_S64LE_DECODER 1
#define CONFIG_PCM_U8_DECODER 1
#define CONFIG_PCM_U16BE_DECODER 1
#define CONFIG_PCM_U16LE_DECODER 1
#define CONFIG_PCM_U24BE_DECODER 1
#define CONFIG_PCM_U24LE_DECODER 1
#define CONFIG_PCM_U32BE_DECODER 1
#define CONFIG_PCM_U32LE_DECODER 1
#define CONFIG_PCM_VIDC_DECODER 1
#define CONFIG_DERF_DPCM_DECODER 1
#define CONFIG_GREMLIN_DPCM_DECODER 1
#define CONFIG_INTERPLAY_DPCM_DECODER 1
#define CONFIG_ROQ_DPCM_DECODER 1
#define CONFIG_SDX2_DPCM_DECODER 1
#define CONFIG_SOL_DPCM_DECODER 1
#define CONFIG_XAN_DPCM_DECODER 1
#define CONFIG_ADPCM_4XM_DECODER 1
#define CONFIG_ADPCM_ADX_DECODER 1
#define CONFIG_ADPCM_AFC_DECODER 1
#define CONFIG_ADPCM_AGM_DECODER 1
#define CONFIG_ADPCM_AICA_DECODER 1
#define CONFIG_ADPCM_ARGO_DECODER 1
#define CONFIG_ADPCM_CT_DECODER 1
#define CONFIG_ADPCM_DTK_DECODER 1
#define CONFIG_ADPCM_EA_DECODER 1
#define CONFIG_ADPCM_EA_MAXIS_XA_DECODER 1
#define CONFIG_ADPCM_EA_R1_DECODER 1
#define CONFIG_ADPCM_EA_R2_DECODER 1
#define CONFIG_ADPCM_EA_R3_DECODER 1
#define CONFIG_ADPCM_EA_XAS_DECODER 1
#define CONFIG_ADPCM_G722_DECODER 1
#define CONFIG_ADPCM_G726_DECODER 1
#define CONFIG_ADPCM_G726LE_DECODER 1
#define CONFIG_ADPCM_IMA_AMV_DECODER 1
#define CONFIG_ADPCM_IMA_ALP_DECODER 1
#define CONFIG_ADPCM_IMA_APC_DECODER 1
#define CONFIG_ADPCM_IMA_APM_DECODER 1
#define CONFIG_ADPCM_IMA_CUNNING_DECODER 1
#define CONFIG_ADPCM_IMA_DAT4_DECODER 1
#define CONFIG_ADPCM_IMA_DK3_DECODER 1
#define CONFIG_ADPCM_IMA_DK4_DECODER 1
#define CONFIG_ADPCM_IMA_EA_EACS_DECODER 1
#define CONFIG_ADPCM_IMA_EA_SEAD_DECODER 1
#define CONFIG_ADPCM_IMA_ISS_DECODER 1
#define CONFIG_ADPCM_IMA_MTF_DECODER 1
#define CONFIG_ADPCM_IMA_OKI_DECODER 1
#define CONFIG_ADPCM_IMA_QT_DECODER 1
#define CONFIG_ADPCM_IMA_RAD_DECODER 1
#define CONFIG_ADPCM_IMA_SSI_DECODER 1
#define CONFIG_ADPCM_IMA_SMJPEG_DECODER 1
#define CONFIG_ADPCM_IMA_WAV_DECODER 1
#define CONFIG_ADPCM_IMA_WS_DECODER 1
#define CONFIG_ADPCM_MS_DECODER 1
#define CONFIG_ADPCM_MTAF_DECODER 1
#define CONFIG_ADPCM_PSX_DECODER 1
#define CONFIG_ADPCM_SBPRO_2_DECODER 1
#define CONFIG_ADPCM_SBPRO_3_DECODER 1
#define CONFIG_ADPCM_SBPRO_4_DECODER 1
#define CONFIG_ADPCM_SWF_DECODER 1
#define CONFIG_ADPCM_THP_DECODER 1
#define CONFIG_ADPCM_THP_LE_DECODER 1
#define CONFIG_ADPCM_VIMA_DECODER 1
#define CONFIG_ADPCM_XA_DECODER 1
#define CONFIG_ADPCM_YAMAHA_DECODER 1
#define CONFIG_ADPCM_ZORK_DECODER 1
#define CONFIG_SSA_DECODER 1
#define CONFIG_ASS_DECODER 1
#define CONFIG_CCAPTION_DECODER 1
#define CONFIG_DVBSUB_DECODER 1
#define CONFIG_DVDSUB_DECODER 1
#define CONFIG_JACOSUB_DECODER 1
#define CONFIG_MICRODVD_DECODER 1
#define CONFIG_MOVTEXT_DECODER 1
#define CONFIG_MPL2_DECODER 1
#define CONFIG_PGSSUB_DECODER 1
#define CONFIG_PJS_DECODER 1
#define CONFIG_REALTEXT_DECODER 1
#define CONFIG_SAMI_DECODER 1
#define CONFIG_SRT_DECODER 1
#define CONFIG_STL_DECODER 1
#define CONFIG_SUBRIP_DECODER 1
#define CONFIG_SUBVIEWER_DECODER 1
#define CONFIG_SUBVIEWER1_DECODER 1
#define CONFIG_TEXT_DECODER 1
#define CONFIG_VPLAYER_DECODER 1
#define CONFIG_WEBVTT_DECODER 1
#define CONFIG_XSUB_DECODER 1
#define CONFIG_AAC_AT_DECODER 0
#define CONFIG_AC3_AT_DECODER 0
#define CONFIG_ADPCM_IMA_QT_AT_DECODER 0
#define CONFIG_ALAC_AT_DECODER 0
#define CONFIG_AMR_NB_AT_DECODER 0
#define CONFIG_EAC3_AT_DECODER 0
#define CONFIG_GSM_MS_AT_DECODER 0
#define CONFIG_ILBC_AT_DECODER 0
#define CONFIG_MP1_AT_DECODER 0
#define CONFIG_MP2_AT_DECODER 0
#define CONFIG_MP3_AT_DECODER 0
#define CONFIG_PCM_ALAW_AT_DECODER 0
#define CONFIG_PCM_MULAW_AT_DECODER 0
#define CONFIG_QDMC_AT_DECODER 0
#define CONFIG_QDM2_AT_DECODER 0
#define CONFIG_LIBARIBB24_DECODER 0
#define CONFIG_LIBCELT_DECODER 0
#define CONFIG_LIBCODEC2_DECODER 0
#define CONFIG_LIBDAV1D_DECODER 0
#define CONFIG_LIBDAVS2_DECODER 0
#define CONFIG_LIBFDK_AAC_DECODER 0
#define CONFIG_LIBGSM_DECODER 0
#define CONFIG_LIBGSM_MS_DECODER 0
#define CONFIG_LIBILBC_DECODER 0
#define CONFIG_LIBOPENCORE_AMRNB_DECODER 0
#define CONFIG_LIBOPENCORE_AMRWB_DECODER 0
#define CONFIG_LIBOPENJPEG_DECODER 0
#define CONFIG_LIBOPUS_DECODER 0
#define CONFIG_LIBRSVG_DECODER 0
#define CONFIG_LIBSPEEX_DECODER 0
#define CONFIG_LIBVORBIS_DECODER 0
#define CONFIG_LIBVPX_VP8_DECODER 0
#define CONFIG_LIBVPX_VP9_DECODER 0
#define CONFIG_LIBZVBI_TELETEXT_DECODER 0
#define CONFIG_BINTEXT_DECODER 1
#define CONFIG_XBIN_DECODER 1
#define CONFIG_IDF_DECODER 1
#define CONFIG_LIBAOM_AV1_DECODER 0
#define CONFIG_LIBOPENH264_DECODER 0
#define CONFIG_H264_CUVID_DECODER 0
#define CONFIG_HEVC_CUVID_DECODER 0
#define CONFIG_HEVC_MEDIACODEC_DECODER 0
#define CONFIG_MJPEG_CUVID_DECODER 0
#define CONFIG_MJPEG_QSV_DECODER 0
#define CONFIG_MPEG1_CUVID_DECODER 0
#define CONFIG_MPEG2_CUVID_DECODER 0
#define CONFIG_MPEG4_CUVID_DECODER 0
#define CONFIG_MPEG4_MEDIACODEC_DECODER 0
#define CONFIG_VC1_CUVID_DECODER 0
#define CONFIG_VP8_CUVID_DECODER 0
#define CONFIG_VP8_MEDIACODEC_DECODER 0
#define CONFIG_VP8_QSV_DECODER 0
#define CONFIG_VP9_CUVID_DECODER 0
#define CONFIG_VP9_MEDIACODEC_DECODER 0
#define CONFIG_VP9_QSV_DECODER 0
#define CONFIG_A64MULTI_ENCODER 1
#define CONFIG_A64MULTI5_ENCODER 1
#define CONFIG_ALIAS_PIX_ENCODER 1
#define CONFIG_AMV_ENCODER 1
#define CONFIG_APNG_ENCODER 0
#define CONFIG_ASV1_ENCODER 1
#define CONFIG_ASV2_ENCODER 1
#define CONFIG_AVRP_ENCODER 1
#define CONFIG_AVUI_ENCODER 1
#define CONFIG_AYUV_ENCODER 1
#define CONFIG_BMP_ENCODER 1
#define CONFIG_CINEPAK_ENCODER 1
#define CONFIG_CLJR_ENCODER 1
#define CONFIG_COMFORTNOISE_ENCODER 1
#define CONFIG_DNXHD_ENCODER 1
#define CONFIG_DPX_ENCODER 1
#define CONFIG_DVVIDEO_ENCODER 1
#define CONFIG_FFV1_ENCODER 1
#define CONFIG_FFVHUFF_ENCODER 1
#define CONFIG_FITS_ENCODER 1
#define CONFIG_FLASHSV_ENCODER 0
#define CONFIG_FLASHSV2_ENCODER 0
#define CONFIG_FLV_ENCODER 1
#define CONFIG_GIF_ENCODER 1
#define CONFIG_H261_ENCODER 1
#define CONFIG_H263_ENCODER 1
#define CONFIG_H263P_ENCODER 1
#define CONFIG_HAP_ENCODER 0
#define CONFIG_HUFFYUV_ENCODER 1
#define CONFIG_JPEG2000_ENCODER 1
#define CONFIG_JPEGLS_ENCODER 1
#define CONFIG_LJPEG_ENCODER 1
#define CONFIG_MAGICYUV_ENCODER 1
#define CONFIG_MJPEG_ENCODER 1
#define CONFIG_MPEG1VIDEO_ENCODER 1
#define CONFIG_MPEG2VIDEO_ENCODER 1
#define CONFIG_MPEG4_ENCODER 1
#define CONFIG_MSMPEG4V2_ENCODER 1
#define CONFIG_MSMPEG4V3_ENCODER 1
#define CONFIG_MSVIDEO1_ENCODER 1
#define CONFIG_PAM_ENCODER 1
#define CONFIG_PBM_ENCODER 1
#define CONFIG_PCX_ENCODER 1
#define CONFIG_PGM_ENCODER 1
#define CONFIG_PGMYUV_ENCODER 1
#define CONFIG_PNG_ENCODER 0
#define CONFIG_PPM_ENCODER 1
#define CONFIG_PRORES_ENCODER 1
#define CONFIG_PRORES_AW_ENCODER 1
#define CONFIG_PRORES_KS_ENCODER 1
#define CONFIG_QTRLE_ENCODER 1
#define CONFIG_R10K_ENCODER 1
#define CONFIG_R210_ENCODER 1
#define CONFIG_RAWVIDEO_ENCODER 1
#define CONFIG_ROQ_ENCODER 1
#define CONFIG_RV10_ENCODER 1
#define CONFIG_RV20_ENCODER 1
#define CONFIG_S302M_ENCODER 1
#define CONFIG_SGI_ENCODER 1
#define CONFIG_SNOW_ENCODER 1
#define CONFIG_SUNRAST_ENCODER 1
#define CONFIG_SVQ1_ENCODER 1
#define CONFIG_TARGA_ENCODER 1
#define CONFIG_TIFF_ENCODER 1
#define CONFIG_UTVIDEO_ENCODER 1
#define CONFIG_V210_ENCODER 1
#define CONFIG_V308_ENCODER 1
#define CONFIG_V408_ENCODER 1
#define CONFIG_V410_ENCODER 1
#define CONFIG_VC2_ENCODER 1
#define CONFIG_WRAPPED_AVFRAME_ENCODER 1
#define CONFIG_WMV1_ENCODER 1
#define CONFIG_WMV2_ENCODER 1
#define CONFIG_XBM_ENCODER 1
#define CONFIG_XFACE_ENCODER 1
#define CONFIG_XWD_ENCODER 1
#define CONFIG_Y41P_ENCODER 1
#define CONFIG_YUV4_ENCODER 1
#define CONFIG_ZLIB_ENCODER 0
#define CONFIG_ZMBV_ENCODER 0
#define CONFIG_AAC_ENCODER 1
#define CONFIG_AC3_ENCODER 1
#define CONFIG_AC3_FIXED_ENCODER 1
#define CONFIG_ALAC_ENCODER 1
#define CONFIG_APTX_ENCODER 1
#define CONFIG_APTX_HD_ENCODER 1
#define CONFIG_DCA_ENCODER 1
#define CONFIG_EAC3_ENCODER 1
#define CONFIG_FLAC_ENCODER 1
#define CONFIG_G723_1_ENCODER 1
#define CONFIG_MLP_ENCODER 1
#define CONFIG_MP2_ENCODER 1
#define CONFIG_MP2FIXED_ENCODER 1
#define CONFIG_NELLYMOSER_ENCODER 1
#define CONFIG_OPUS_ENCODER 1
#define CONFIG_RA_144_ENCODER 1
#define CONFIG_SBC_ENCODER 1
#define CONFIG_SONIC_ENCODER 1
#define CONFIG_SONIC_LS_ENCODER 1
#define CONFIG_TRUEHD_ENCODER 1
#define CONFIG_TTA_ENCODER 1
#define CONFIG_VORBIS_ENCODER 1
#define CONFIG_WAVPACK_ENCODER 1
#define CONFIG_WMAV1_ENCODER 1
#define CONFIG_WMAV2_ENCODER 1
#define CONFIG_PCM_ALAW_ENCODER 1
#define CONFIG_PCM_DVD_ENCODER 1
#define CONFIG_PCM_F32BE_ENCODER 1
#define CONFIG_PCM_F32LE_ENCODER 1
#define CONFIG_PCM_F64BE_ENCODER 1
#define CONFIG_PCM_F64LE_ENCODER 1
#define CONFIG_PCM_MULAW_ENCODER 1
#define CONFIG_PCM_S8_ENCODER 1
#define CONFIG_PCM_S8_PLANAR_ENCODER 1
#define CONFIG_PCM_S16BE_ENCODER 1
#define CONFIG_PCM_S16BE_PLANAR_ENCODER 1
#define CONFIG_PCM_S16LE_ENCODER 1
#define CONFIG_PCM_S16LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S24BE_ENCODER 1
#define CONFIG_PCM_S24DAUD_ENCODER 1
#define CONFIG_PCM_S24LE_ENCODER 1
#define CONFIG_PCM_S24LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S32BE_ENCODER 1
#define CONFIG_PCM_S32LE_ENCODER 1
#define CONFIG_PCM_S32LE_PLANAR_ENCODER 1
#define CONFIG_PCM_S64BE_ENCODER 1
#define CONFIG_PCM_S64LE_ENCODER 1
#define CONFIG_PCM_U8_ENCODER 1
#define CONFIG_PCM_U16BE_ENCODER 1
#define CONFIG_PCM_U16LE_ENCODER 1
#define CONFIG_PCM_U24BE_ENCODER 1
#define CONFIG_PCM_U24LE_ENCODER 1
#define CONFIG_PCM_U32BE_ENCODER 1
#define CONFIG_PCM_U32LE_ENCODER 1
#define CONFIG_PCM_VIDC_ENCODER 1
#define CONFIG_ROQ_DPCM_ENCODER 1
#define CONFIG_ADPCM_ADX_ENCODER 1
#define CONFIG_ADPCM_G722_ENCODER 1
#define CONFIG_ADPCM_G726_ENCODER 1
#define CONFIG_ADPCM_G726LE_ENCODER 1
#define CONFIG_ADPCM_IMA_QT_ENCODER 1
#define CONFIG_ADPCM_IMA_SSI_ENCODER 1
#define CONFIG_ADPCM_IMA_WAV_ENCODER 1
#define CONFIG_ADPCM_MS_ENCODER 1
#define CONFIG_ADPCM_SWF_ENCODER 1
#define CONFIG_ADPCM_YAMAHA_ENCODER 1
#define CONFIG_SSA_ENCODER 1
#define CONFIG_ASS_ENCODER 1
#define CONFIG_DVBSUB_ENCODER 1
#define CONFIG_DVDSUB_ENCODER 1
#define CONFIG_MOVTEXT_ENCODER 1
#define CONFIG_SRT_ENCODER 1
#define CONFIG_SUBRIP_ENCODER 1
#define CONFIG_TEXT_ENCODER 1
#define CONFIG_WEBVTT_ENCODER 1
#define CONFIG_XSUB_ENCODER 1
#define CONFIG_AAC_AT_ENCODER 0
#define CONFIG_AAC_MF_ENCODER 0
#define CONFIG_AC3_MF_ENCODER 0
#define CONFIG_ALAC_AT_ENCODER 0
#define CONFIG_ILBC_AT_ENCODER 0
#define CONFIG_MP3_MF_ENCODER 0
#define CONFIG_PCM_ALAW_AT_ENCODER 0
#define CONFIG_PCM_MULAW_AT_ENCODER 0
#define CONFIG_LIBAOM_AV1_ENCODER 0
#define CONFIG_LIBCODEC2_ENCODER 0
#define CONFIG_LIBFDK_AAC_ENCODER 0
#define CONFIG_LIBGSM_ENCODER 0
#define CONFIG_LIBGSM_MS_ENCODER 0
#define CONFIG_LIBILBC_ENCODER 0
#define CONFIG_LIBMP3LAME_ENCODER 0
#define CONFIG_LIBOPENCORE_AMRNB_ENCODER 0
#define CONFIG_LIBOPENJPEG_ENCODER 0
#define CONFIG_LIBOPUS_ENCODER 0
#define CONFIG_LIBRAV1E_ENCODER 0
#define CONFIG_LIBSHINE_ENCODER 0
#define CONFIG_LIBSPEEX_ENCODER 0
#define CONFIG_LIBTHEORA_ENCODER 0
#define CONFIG_LIBTWOLAME_ENCODER 0
#define CONFIG_LIBVO_AMRWBENC_ENCODER 0
#define CONFIG_LIBVORBIS_ENCODER 0
#define CONFIG_LIBVPX_VP8_ENCODER 0
#define CONFIG_LIBVPX_VP9_ENCODER 0
#define CONFIG_LIBWAVPACK_ENCODER 0
#define CONFIG_LIBWEBP_ANIM_ENCODER 0
#define CONFIG_LIBWEBP_ENCODER 0
#define CONFIG_LIBX262_ENCODER 0
#define CONFIG_LIBX264_ENCODER 0
#define CONFIG_LIBX264RGB_ENCODER 0
#define CONFIG_LIBX265_ENCODER 0
#define CONFIG_LIBXAVS_ENCODER 0
#define CONFIG_LIBXAVS2_ENCODER 0
#define CONFIG_LIBXVID_ENCODER 0
#define CONFIG_H263_V4L2M2M_ENCODER 0
#define CONFIG_LIBOPENH264_ENCODER 0
#define CONFIG_H264_AMF_ENCODER 0
#define CONFIG_H264_MF_ENCODER 0
#define CONFIG_H264_NVENC_ENCODER 0
#define CONFIG_H264_OMX_ENCODER 0
#define CONFIG_H264_QSV_ENCODER 0
#define CONFIG_H264_V4L2M2M_ENCODER 0
#define CONFIG_H264_VAAPI_ENCODER 0
#define CONFIG_H264_VIDEOTOOLBOX_ENCODER 0
#define CONFIG_NVENC_ENCODER 0
#define CONFIG_NVENC_H264_ENCODER 0
#define CONFIG_NVENC_HEVC_ENCODER 0
#define CONFIG_HEVC_AMF_ENCODER 0
#define CONFIG_HEVC_MF_ENCODER 0
#define CONFIG_HEVC_NVENC_ENCODER 0
#define CONFIG_HEVC_QSV_ENCODER 0
#define CONFIG_HEVC_V4L2M2M_ENCODER 0
#define CONFIG_HEVC_VAAPI_ENCODER 0
#define CONFIG_HEVC_VIDEOTOOLBOX_ENCODER 0
#define CONFIG_LIBKVAZAAR_ENCODER 0
#define CONFIG_MJPEG_QSV_ENCODER 0
#define CONFIG_MJPEG_VAAPI_ENCODER 0
#define CONFIG_MPEG2_QSV_ENCODER 0
#define CONFIG_MPEG2_VAAPI_ENCODER 0
#define CONFIG_MPEG4_OMX_ENCODER 0
#define CONFIG_MPEG4_V4L2M2M_ENCODER 0
#define CONFIG_VP8_V4L2M2M_ENCODER 0
#define CONFIG_VP8_VAAPI_ENCODER 0
#define CONFIG_VP9_VAAPI_ENCODER 0
#define CONFIG_VP9_QSV_ENCODER 0
#define CONFIG_H263_VAAPI_HWACCEL 0
#define CONFIG_H263_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_H264_D3D11VA_HWACCEL 0
#define CONFIG_H264_D3D11VA2_HWACCEL 0
#define CONFIG_H264_DXVA2_HWACCEL 0
#define CONFIG_H264_NVDEC_HWACCEL 0
#define CONFIG_H264_VAAPI_HWACCEL 0
#define CONFIG_H264_VDPAU_HWACCEL 0
#define CONFIG_H264_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_HEVC_D3D11VA_HWACCEL 0
#define CONFIG_HEVC_D3D11VA2_HWACCEL 0
#define CONFIG_HEVC_DXVA2_HWACCEL 0
#define CONFIG_HEVC_NVDEC_HWACCEL 0
#define CONFIG_HEVC_VAAPI_HWACCEL 0
#define CONFIG_HEVC_VDPAU_HWACCEL 0
#define CONFIG_HEVC_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MJPEG_NVDEC_HWACCEL 0
#define CONFIG_MJPEG_VAAPI_HWACCEL 0
#define CONFIG_MPEG1_NVDEC_HWACCEL 0
#define CONFIG_MPEG1_VDPAU_HWACCEL 0
#define CONFIG_MPEG1_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MPEG1_XVMC_HWACCEL 0
#define CONFIG_MPEG2_D3D11VA_HWACCEL 0
#define CONFIG_MPEG2_D3D11VA2_HWACCEL 0
#define CONFIG_MPEG2_NVDEC_HWACCEL 0
#define CONFIG_MPEG2_DXVA2_HWACCEL 0
#define CONFIG_MPEG2_VAAPI_HWACCEL 0
#define CONFIG_MPEG2_VDPAU_HWACCEL 0
#define CONFIG_MPEG2_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_MPEG2_XVMC_HWACCEL 0
#define CONFIG_MPEG4_NVDEC_HWACCEL 0
#define CONFIG_MPEG4_VAAPI_HWACCEL 0
#define CONFIG_MPEG4_VDPAU_HWACCEL 0
#define CONFIG_MPEG4_VIDEOTOOLBOX_HWACCEL 0
#define CONFIG_VC1_D3D11VA_HWACCEL 0
#define CONFIG_VC1_D3D11VA2_HWACCEL 0
#define CONFIG_VC1_DXVA2_HWACCEL 0
#define CONFIG_VC1_NVDEC_HWACCEL 0
#define CONFIG_VC1_VAAPI_HWACCEL 0
#define CONFIG_VC1_VDPAU_HWACCEL 0
#define CONFIG_VP8_NVDEC_HWACCEL 0
#define CONFIG_VP8_VAAPI_HWACCEL 0
#define CONFIG_VP9_D3D11VA_HWACCEL 0
#define CONFIG_VP9_D3D11VA2_HWACCEL 0
#define CONFIG_VP9_DXVA2_HWACCEL 0
#define CONFIG_VP9_NVDEC_HWACCEL 0
#define CONFIG_VP9_VAAPI_HWACCEL 0
#define CONFIG_VP9_VDPAU_HWACCEL 0
#define CONFIG_WMV3_D3D11VA_HWACCEL 0
#define CONFIG_WMV3_D3D11VA2_HWACCEL 0
#define CONFIG_WMV3_DXVA2_HWACCEL 0
#define CONFIG_WMV3_NVDEC_HWACCEL 0
#define CONFIG_WMV3_VAAPI_HWACCEL 0
#define CONFIG_WMV3_VDPAU_HWACCEL 0
#define CONFIG_AAC_PARSER 1
#define CONFIG_AAC_LATM_PARSER 1
#define CONFIG_AC3_PARSER 1
#define CONFIG_ADX_PARSER 1
#define CONFIG_AV1_PARSER 1
#define CONFIG_AVS2_PARSER 1
#define CONFIG_BMP_PARSER 1
#define CONFIG_CAVSVIDEO_PARSER 1
#define CONFIG_COOK_PARSER 1
#define CONFIG_DCA_PARSER 1
#define CONFIG_DIRAC_PARSER 1
#define CONFIG_DNXHD_PARSER 1
#define CONFIG_DPX_PARSER 1
#define CONFIG_DVAUDIO_PARSER 1
#define CONFIG_DVBSUB_PARSER 1
#define CONFIG_DVDSUB_PARSER 1
#define CONFIG_DVD_NAV_PARSER 1
#define CONFIG_FLAC_PARSER 1
#define CONFIG_G723_1_PARSER 1
#define CONFIG_G729_PARSER 1
#define CONFIG_GIF_PARSER 1
#define CONFIG_GSM_PARSER 1
#define CONFIG_H261_PARSER 1
#define CONFIG_H263_PARSER 1
#define CONFIG_H264_PARSER 1
#define CONFIG_HEVC_PARSER 1
#define CONFIG_JPEG2000_PARSER 1
#define CONFIG_MJPEG_PARSER 1
#define CONFIG_MLP_PARSER 1
#define CONFIG_MPEG4VIDEO_PARSER 1
#define CONFIG_MPEGAUDIO_PARSER 1
#define CONFIG_MPEGVIDEO_PARSER 1
#define CONFIG_OPUS_PARSER 1
#define CONFIG_PNG_PARSER 1
#define CONFIG_PNM_PARSER 1
#define CONFIG_RV30_PARSER 1
#define CONFIG_RV40_PARSER 1
#define CONFIG_SBC_PARSER 1
#define CONFIG_SIPR_PARSER 1
#define CONFIG_TAK_PARSER 1
#define CONFIG_VC1_PARSER 1
#define CONFIG_VORBIS_PARSER 1
#define CONFIG_VP3_PARSER 1
#define CONFIG_VP8_PARSER 1
#define CONFIG_VP9_PARSER 1
#define CONFIG_WEBP_PARSER 1
#define CONFIG_XMA_PARSER 1
#define CONFIG_ALSA_INDEV 0
#define CONFIG_ANDROID_CAMERA_INDEV 0
#define CONFIG_AVFOUNDATION_INDEV 0
#define CONFIG_BKTR_INDEV 0
#define CONFIG_DECKLINK_INDEV 0
#define CONFIG_DSHOW_INDEV 0
#define CONFIG_FBDEV_INDEV 0
#define CONFIG_GDIGRAB_INDEV 0
#define CONFIG_IEC61883_INDEV 0
#define CONFIG_JACK_INDEV 0
#define CONFIG_KMSGRAB_INDEV 0
#define CONFIG_LAVFI_INDEV 1
#define CONFIG_OPENAL_INDEV 0
#define CONFIG_OSS_INDEV 0
#define CONFIG_PULSE_INDEV 0
#define CONFIG_SNDIO_INDEV 0
#define CONFIG_V4L2_INDEV 0
#define CONFIG_VFWCAP_INDEV 0
#define CONFIG_XCBGRAB_INDEV 0
#define CONFIG_LIBCDIO_INDEV 0
#define CONFIG_LIBDC1394_INDEV 0
#define CONFIG_ALSA_OUTDEV 0
#define CONFIG_CACA_OUTDEV 0
#define CONFIG_DECKLINK_OUTDEV 0
#define CONFIG_FBDEV_OUTDEV 0
#define CONFIG_OPENGL_OUTDEV 0
#define CONFIG_OSS_OUTDEV 0
#define CONFIG_PULSE_OUTDEV 0
#define CONFIG_SDL2_OUTDEV 1
#define CONFIG_SNDIO_OUTDEV 0
#define CONFIG_V4L2_OUTDEV 0
#define CONFIG_XV_OUTDEV 0
#define CONFIG_ABENCH_FILTER 1
#define CONFIG_ACOMPRESSOR_FILTER 1
#define CONFIG_ACONTRAST_FILTER 1
#define CONFIG_ACOPY_FILTER 1
#define CONFIG_ACUE_FILTER 1
#define CONFIG_ACROSSFADE_FILTER 1
#define CONFIG_ACROSSOVER_FILTER 1
#define CONFIG_ACRUSHER_FILTER 1
#define CONFIG_ADECLICK_FILTER 1
#define CONFIG_ADECLIP_FILTER 1
#define CONFIG_ADELAY_FILTER 1
#define CONFIG_ADERIVATIVE_FILTER 1
#define CONFIG_AECHO_FILTER 1
#define CONFIG_AEMPHASIS_FILTER 1
#define CONFIG_AEVAL_FILTER 1
#define CONFIG_AFADE_FILTER 1
#define CONFIG_AFFTDN_FILTER 1
#define CONFIG_AFFTFILT_FILTER 1
#define CONFIG_AFIR_FILTER 1
#define CONFIG_AFORMAT_FILTER 1
#define CONFIG_AGATE_FILTER 1
#define CONFIG_AIIR_FILTER 1
#define CONFIG_AINTEGRAL_FILTER 1
#define CONFIG_AINTERLEAVE_FILTER 1
#define CONFIG_ALIMITER_FILTER 1
#define CONFIG_ALLPASS_FILTER 1
#define CONFIG_ALOOP_FILTER 1
#define CONFIG_AMERGE_FILTER 1
#define CONFIG_AMETADATA_FILTER 1
#define CONFIG_AMIX_FILTER 1
#define CONFIG_AMULTIPLY_FILTER 1
#define CONFIG_ANEQUALIZER_FILTER 1
#define CONFIG_ANLMDN_FILTER 1
#define CONFIG_ANLMS_FILTER 1
#define CONFIG_ANULL_FILTER 1
#define CONFIG_APAD_FILTER 1
#define CONFIG_APERMS_FILTER 1
#define CONFIG_APHASER_FILTER 1
#define CONFIG_APULSATOR_FILTER 1
#define CONFIG_AREALTIME_FILTER 1
#define CONFIG_ARESAMPLE_FILTER 1
#define CONFIG_AREVERSE_FILTER 1
#define CONFIG_ARNNDN_FILTER 1
#define CONFIG_ASELECT_FILTER 1
#define CONFIG_ASENDCMD_FILTER 1
#define CONFIG_ASETNSAMPLES_FILTER 1
#define CONFIG_ASETPTS_FILTER 1
#define CONFIG_ASETRATE_FILTER 1
#define CONFIG_ASETTB_FILTER 1
#define CONFIG_ASHOWINFO_FILTER 1
#define CONFIG_ASIDEDATA_FILTER 1
#define CONFIG_ASOFTCLIP_FILTER 1
#define CONFIG_ASPLIT_FILTER 1
#define CONFIG_ASR_FILTER 0
#define CONFIG_ASTATS_FILTER 1
#define CONFIG_ASTREAMSELECT_FILTER 1
#define CONFIG_ASUBBOOST_FILTER 1
#define CONFIG_ATEMPO_FILTER 1
#define CONFIG_ATRIM_FILTER 1
#define CONFIG_AXCORRELATE_FILTER 1
#define CONFIG_AZMQ_FILTER 0
#define CONFIG_BANDPASS_FILTER 1
#define CONFIG_BANDREJECT_FILTER 1
#define CONFIG_BASS_FILTER 1
#define CONFIG_BIQUAD_FILTER 1
#define CONFIG_BS2B_FILTER 0
#define CONFIG_CHROMABER_VULKAN_FILTER 0
#define CONFIG_CHANNELMAP_FILTER 1
#define CONFIG_CHANNELSPLIT_FILTER 1
#define CONFIG_CHORUS_FILTER 1
#define CONFIG_COMPAND_FILTER 1
#define CONFIG_COMPENSATIONDELAY_FILTER 1
#define CONFIG_CROSSFEED_FILTER 1
#define CONFIG_CRYSTALIZER_FILTER 1
#define CONFIG_DCSHIFT_FILTER 1
#define CONFIG_DEESSER_FILTER 1
#define CONFIG_DRMETER_FILTER 1
#define CONFIG_DYNAUDNORM_FILTER 1
#define CONFIG_EARWAX_FILTER 1
#define CONFIG_EBUR128_FILTER 1
#define CONFIG_EQUALIZER_FILTER 1
#define CONFIG_EXTRASTEREO_FILTER 1
#define CONFIG_FIREQUALIZER_FILTER 1
#define CONFIG_FLANGER_FILTER 1
#define CONFIG_HAAS_FILTER 1
#define CONFIG_HDCD_FILTER 1
#define CONFIG_HEADPHONE_FILTER 1
#define CONFIG_HIGHPASS_FILTER 1
#define CONFIG_HIGHSHELF_FILTER 1
#define CONFIG_JOIN_FILTER 1
#define CONFIG_LADSPA_FILTER 0
#define CONFIG_LOUDNORM_FILTER 1
#define CONFIG_LOWPASS_FILTER 1
#define CONFIG_LOWSHELF_FILTER 1
#define CONFIG_LV2_FILTER 0
#define CONFIG_MCOMPAND_FILTER 1
#define CONFIG_PAN_FILTER 1
#define CONFIG_REPLAYGAIN_FILTER 1
#define CONFIG_RESAMPLE_FILTER 0
#define CONFIG_RUBBERBAND_FILTER 0
#define CONFIG_SIDECHAINCOMPRESS_FILTER 1
#define CONFIG_SIDECHAINGATE_FILTER 1
#define CONFIG_SILENCEDETECT_FILTER 1
#define CONFIG_SILENCEREMOVE_FILTER 1
#define CONFIG_SOFALIZER_FILTER 0
#define CONFIG_STEREOTOOLS_FILTER 1
#define CONFIG_STEREOWIDEN_FILTER 1
#define CONFIG_SUPEREQUALIZER_FILTER 1
#define CONFIG_SURROUND_FILTER 1
#define CONFIG_TREBLE_FILTER 1
#define CONFIG_TREMOLO_FILTER 1
#define CONFIG_VIBRATO_FILTER 1
#define CONFIG_VOLUME_FILTER 1
#define CONFIG_VOLUMEDETECT_FILTER 1
#define CONFIG_AEVALSRC_FILTER 1
#define CONFIG_AFIRSRC_FILTER 1
#define CONFIG_ANOISESRC_FILTER 1
#define CONFIG_ANULLSRC_FILTER 1
#define CONFIG_FLITE_FILTER 0
#define CONFIG_HILBERT_FILTER 1
#define CONFIG_SINC_FILTER 1
#define CONFIG_SINE_FILTER 1
#define CONFIG_ANULLSINK_FILTER 1
#define CONFIG_ADDROI_FILTER 1
#define CONFIG_ALPHAEXTRACT_FILTER 1
#define CONFIG_ALPHAMERGE_FILTER 1
#define CONFIG_AMPLIFY_FILTER 1
#define CONFIG_ASS_FILTER 0
#define CONFIG_ATADENOISE_FILTER 1
#define CONFIG_AVGBLUR_FILTER 1
#define CONFIG_AVGBLUR_OPENCL_FILTER 0
#define CONFIG_AVGBLUR_VULKAN_FILTER 0
#define CONFIG_BBOX_FILTER 1
#define CONFIG_BENCH_FILTER 1
#define CONFIG_BILATERAL_FILTER 1
#define CONFIG_BITPLANENOISE_FILTER 1
#define CONFIG_BLACKDETECT_FILTER 1
#define CONFIG_BLACKFRAME_FILTER 0
#define CONFIG_BLEND_FILTER 1
#define CONFIG_BM3D_FILTER 1
#define CONFIG_BOXBLUR_FILTER 0
#define CONFIG_BOXBLUR_OPENCL_FILTER 0
#define CONFIG_BWDIF_FILTER 1
#define CONFIG_CAS_FILTER 1
#define CONFIG_CHROMAHOLD_FILTER 1
#define CONFIG_CHROMAKEY_FILTER 1
#define CONFIG_CHROMASHIFT_FILTER 1
#define CONFIG_CIESCOPE_FILTER 1
#define CONFIG_CODECVIEW_FILTER 1
#define CONFIG_COLORBALANCE_FILTER 1
#define CONFIG_COLORCHANNELMIXER_FILTER 1
#define CONFIG_COLORKEY_FILTER 1
#define CONFIG_COLORKEY_OPENCL_FILTER 0
#define CONFIG_COLORHOLD_FILTER 1
#define CONFIG_COLORLEVELS_FILTER 1
#define CONFIG_COLORMATRIX_FILTER 0
#define CONFIG_COLORSPACE_FILTER 1
#define CONFIG_CONVOLUTION_FILTER 1
#define CONFIG_CONVOLUTION_OPENCL_FILTER 0
#define CONFIG_CONVOLVE_FILTER 1
#define CONFIG_COPY_FILTER 1
#define CONFIG_COREIMAGE_FILTER 0
#define CONFIG_COVER_RECT_FILTER 0
#define CONFIG_CROP_FILTER 1
#define CONFIG_CROPDETECT_FILTER 0
#define CONFIG_CUE_FILTER 1
#define CONFIG_CURVES_FILTER 1
#define CONFIG_DATASCOPE_FILTER 1
#define CONFIG_DBLUR_FILTER 1
#define CONFIG_DCTDNOIZ_FILTER 1
#define CONFIG_DEBAND_FILTER 1
#define CONFIG_DEBLOCK_FILTER 1
#define CONFIG_DECIMATE_FILTER 1
#define CONFIG_DECONVOLVE_FILTER 1
#define CONFIG_DEDOT_FILTER 1
#define CONFIG_DEFLATE_FILTER 1
#define CONFIG_DEFLICKER_FILTER 1
#define CONFIG_DEINTERLACE_QSV_FILTER 0
#define CONFIG_DEINTERLACE_VAAPI_FILTER 0
#define CONFIG_DEJUDDER_FILTER 1
#define CONFIG_DELOGO_FILTER 0
#define CONFIG_DENOISE_VAAPI_FILTER 0
#define CONFIG_DERAIN_FILTER 1
#define CONFIG_DESHAKE_FILTER 1
#define CONFIG_DESHAKE_OPENCL_FILTER 0
#define CONFIG_DESPILL_FILTER 1
#define CONFIG_DETELECINE_FILTER 1
#define CONFIG_DILATION_FILTER 1
#define CONFIG_DILATION_OPENCL_FILTER 0
#define CONFIG_DISPLACE_FILTER 1
#define CONFIG_DNN_PROCESSING_FILTER 1
#define CONFIG_DOUBLEWEAVE_FILTER 1
#define CONFIG_DRAWBOX_FILTER 1
#define CONFIG_DRAWGRAPH_FILTER 1
#define CONFIG_DRAWGRID_FILTER 1
#define CONFIG_DRAWTEXT_FILTER 0
#define CONFIG_EDGEDETECT_FILTER 1
#define CONFIG_ELBG_FILTER 1
#define CONFIG_ENTROPY_FILTER 1
#define CONFIG_EQ_FILTER 0
#define CONFIG_EROSION_FILTER 1
#define CONFIG_EROSION_OPENCL_FILTER 0
#define CONFIG_EXTRACTPLANES_FILTER 1
#define CONFIG_FADE_FILTER 1
#define CONFIG_FFTDNOIZ_FILTER 1
#define CONFIG_FFTFILT_FILTER 1
#define CONFIG_FIELD_FILTER 1
#define CONFIG_FIELDHINT_FILTER 1
#define CONFIG_FIELDMATCH_FILTER 1
#define CONFIG_FIELDORDER_FILTER 1
#define CONFIG_FILLBORDERS_FILTER 1
#define CONFIG_FIND_RECT_FILTER 0
#define CONFIG_FLOODFILL_FILTER 1
#define CONFIG_FORMAT_FILTER 1
#define CONFIG_FPS_FILTER 1
#define CONFIG_FRAMEPACK_FILTER 1
#define CONFIG_FRAMERATE_FILTER 1
#define CONFIG_FRAMESTEP_FILTER 1
#define CONFIG_FREEZEDETECT_FILTER 1
#define CONFIG_FREEZEFRAMES_FILTER 1
#define CONFIG_FREI0R_FILTER 0
#define CONFIG_FSPP_FILTER 0
#define CONFIG_GBLUR_FILTER 1
#define CONFIG_GEQ_FILTER 1
#define CONFIG_GRADFUN_FILTER 1
#define CONFIG_GRAPHMONITOR_FILTER 1
#define CONFIG_GREYEDGE_FILTER 1
#define CONFIG_HALDCLUT_FILTER 1
#define CONFIG_HFLIP_FILTER 1
#define CONFIG_HISTEQ_FILTER 0
#define CONFIG_HISTOGRAM_FILTER 1
#define CONFIG_HQDN3D_FILTER 0
#define CONFIG_HQX_FILTER 1
#define CONFIG_HSTACK_FILTER 1
#define CONFIG_HUE_FILTER 1
#define CONFIG_HWDOWNLOAD_FILTER 1
#define CONFIG_HWMAP_FILTER 1
#define CONFIG_HWUPLOAD_FILTER 1
#define CONFIG_HWUPLOAD_CUDA_FILTER 0
#define CONFIG_HYSTERESIS_FILTER 1
#define CONFIG_IDET_FILTER 1
#define CONFIG_IL_FILTER 1
#define CONFIG_INFLATE_FILTER 1
#define CONFIG_INTERLACE_FILTER 0
#define CONFIG_INTERLEAVE_FILTER 1
#define CONFIG_KERNDEINT_FILTER 0
#define CONFIG_LAGFUN_FILTER 1
#define CONFIG_LENSCORRECTION_FILTER 1
#define CONFIG_LENSFUN_FILTER 0
#define CONFIG_LIBVMAF_FILTER 0
#define CONFIG_LIMITER_FILTER 1
#define CONFIG_LOOP_FILTER 1
#define CONFIG_LUMAKEY_FILTER 1
#define CONFIG_LUT_FILTER 1
#define CONFIG_LUT1D_FILTER 1
#define CONFIG_LUT2_FILTER 1
#define CONFIG_LUT3D_FILTER 1
#define CONFIG_LUTRGB_FILTER 1
#define CONFIG_LUTYUV_FILTER 1
#define CONFIG_MASKEDCLAMP_FILTER 1
#define CONFIG_MASKEDMAX_FILTER 1
#define CONFIG_MASKEDMERGE_FILTER 1
#define CONFIG_MASKEDMIN_FILTER 1
#define CONFIG_MASKEDTHRESHOLD_FILTER 1
#define CONFIG_MASKFUN_FILTER 1
#define CONFIG_MCDEINT_FILTER 0
#define CONFIG_MEDIAN_FILTER 1
#define CONFIG_MERGEPLANES_FILTER 1
#define CONFIG_MESTIMATE_FILTER 1
#define CONFIG_METADATA_FILTER 1
#define CONFIG_MIDEQUALIZER_FILTER 1
#define CONFIG_MINTERPOLATE_FILTER 1
#define CONFIG_MIX_FILTER 1
#define CONFIG_MPDECIMATE_FILTER 0
#define CONFIG_NEGATE_FILTER 1
#define CONFIG_NLMEANS_FILTER 1
#define CONFIG_NLMEANS_OPENCL_FILTER 0
#define CONFIG_NNEDI_FILTER 0
#define CONFIG_NOFORMAT_FILTER 1
#define CONFIG_NOISE_FILTER 1
#define CONFIG_NORMALIZE_FILTER 1
#define CONFIG_NULL_FILTER 1
#define CONFIG_OCR_FILTER 0
#define CONFIG_OCV_FILTER 0
#define CONFIG_OSCILLOSCOPE_FILTER 1
#define CONFIG_OVERLAY_FILTER 1
#define CONFIG_OVERLAY_OPENCL_FILTER 0
#define CONFIG_OVERLAY_QSV_FILTER 0
#define CONFIG_OVERLAY_VULKAN_FILTER 0
#define CONFIG_OVERLAY_CUDA_FILTER 0
#define CONFIG_OWDENOISE_FILTER 0
#define CONFIG_PAD_FILTER 1
#define CONFIG_PAD_OPENCL_FILTER 0
#define CONFIG_PALETTEGEN_FILTER 1
#define CONFIG_PALETTEUSE_FILTER 1
#define CONFIG_PERMS_FILTER 1
#define CONFIG_PERSPECTIVE_FILTER 0
#define CONFIG_PHASE_FILTER 0
#define CONFIG_PHOTOSENSITIVITY_FILTER 1
#define CONFIG_PIXDESCTEST_FILTER 1
#define CONFIG_PIXSCOPE_FILTER 1
#define CONFIG_PP_FILTER 0
#define CONFIG_PP7_FILTER 0
#define CONFIG_PREMULTIPLY_FILTER 1
#define CONFIG_PREWITT_FILTER 1
#define CONFIG_PREWITT_OPENCL_FILTER 0
#define CONFIG_PROCAMP_VAAPI_FILTER 0
#define CONFIG_PROGRAM_OPENCL_FILTER 0
#define CONFIG_PSEUDOCOLOR_FILTER 1
#define CONFIG_PSNR_FILTER 1
#define CONFIG_PULLUP_FILTER 0
#define CONFIG_QP_FILTER 1
#define CONFIG_RANDOM_FILTER 1
#define CONFIG_READEIA608_FILTER 1
#define CONFIG_READVITC_FILTER 1
#define CONFIG_REALTIME_FILTER 1
#define CONFIG_REMAP_FILTER 1
#define CONFIG_REMOVEGRAIN_FILTER 1
#define CONFIG_REMOVELOGO_FILTER 1
#define CONFIG_REPEATFIELDS_FILTER 0
#define CONFIG_REVERSE_FILTER 1
#define CONFIG_RGBASHIFT_FILTER 1
#define CONFIG_ROBERTS_FILTER 1
#define CONFIG_ROBERTS_OPENCL_FILTER 0
#define CONFIG_ROTATE_FILTER 1
#define CONFIG_SAB_FILTER 0
#define CONFIG_SCALE_FILTER 1
#define CONFIG_SCALE_CUDA_FILTER 0
#define CONFIG_SCALE_NPP_FILTER 0
#define CONFIG_SCALE_QSV_FILTER 0
#define CONFIG_SCALE_VAAPI_FILTER 0
#define CONFIG_SCALE_VULKAN_FILTER 0
#define CONFIG_SCALE2REF_FILTER 1
#define CONFIG_SCDET_FILTER 1
#define CONFIG_SCROLL_FILTER 1
#define CONFIG_SELECT_FILTER 1
#define CONFIG_SELECTIVECOLOR_FILTER 1
#define CONFIG_SENDCMD_FILTER 1
#define CONFIG_SEPARATEFIELDS_FILTER 1
#define CONFIG_SETDAR_FILTER 1
#define CONFIG_SETFIELD_FILTER 1
#define CONFIG_SETPARAMS_FILTER 1
#define CONFIG_SETPTS_FILTER 1
#define CONFIG_SETRANGE_FILTER 1
#define CONFIG_SETSAR_FILTER 1
#define CONFIG_SETTB_FILTER 1
#define CONFIG_SHARPNESS_VAAPI_FILTER 0
#define CONFIG_SHOWINFO_FILTER 1
#define CONFIG_SHOWPALETTE_FILTER 1
#define CONFIG_SHUFFLEFRAMES_FILTER 1
#define CONFIG_SHUFFLEPLANES_FILTER 1
#define CONFIG_SIDEDATA_FILTER 1
#define CONFIG_SIGNALSTATS_FILTER 1
#define CONFIG_SIGNATURE_FILTER 0
#define CONFIG_SMARTBLUR_FILTER 0
#define CONFIG_SOBEL_FILTER 1
#define CONFIG_SOBEL_OPENCL_FILTER 0
#define CONFIG_SPLIT_FILTER 1
#define CONFIG_SPP_FILTER 0
#define CONFIG_SR_FILTER 1
#define CONFIG_SSIM_FILTER 1
#define CONFIG_STEREO3D_FILTER 0
#define CONFIG_STREAMSELECT_FILTER 1
#define CONFIG_SUBTITLES_FILTER 0
#define CONFIG_SUPER2XSAI_FILTER 0
#define CONFIG_SWAPRECT_FILTER 1
#define CONFIG_SWAPUV_FILTER 1
#define CONFIG_TBLEND_FILTER 1
#define CONFIG_TELECINE_FILTER 1
#define CONFIG_THISTOGRAM_FILTER 1
#define CONFIG_THRESHOLD_FILTER 1
#define CONFIG_THUMBNAIL_FILTER 1
#define CONFIG_THUMBNAIL_CUDA_FILTER 0
#define CONFIG_TILE_FILTER 1
#define CONFIG_TINTERLACE_FILTER 0
#define CONFIG_TLUT2_FILTER 1
#define CONFIG_TMEDIAN_FILTER 1
#define CONFIG_TMIX_FILTER 1
#define CONFIG_TONEMAP_FILTER 1
#define CONFIG_TONEMAP_OPENCL_FILTER 0
#define CONFIG_TONEMAP_VAAPI_FILTER 0
#define CONFIG_TPAD_FILTER 1
#define CONFIG_TRANSPOSE_FILTER 1
#define CONFIG_TRANSPOSE_NPP_FILTER 0
#define CONFIG_TRANSPOSE_OPENCL_FILTER 0
#define CONFIG_TRANSPOSE_VAAPI_FILTER 0
#define CONFIG_TRIM_FILTER 1
#define CONFIG_UNPREMULTIPLY_FILTER 1
#define CONFIG_UNSHARP_FILTER 1
#define CONFIG_UNSHARP_OPENCL_FILTER 0
#define CONFIG_UNTILE_FILTER 1
#define CONFIG_USPP_FILTER 0
#define CONFIG_V360_FILTER 1
#define CONFIG_VAGUEDENOISER_FILTER 0
#define CONFIG_VECTORSCOPE_FILTER 1
#define CONFIG_VFLIP_FILTER 1
#define CONFIG_VFRDET_FILTER 1
#define CONFIG_VIBRANCE_FILTER 1
#define CONFIG_VIDSTABDETECT_FILTER 0
#define CONFIG_VIDSTABTRANSFORM_FILTER 0
#define CONFIG_VIGNETTE_FILTER 1
#define CONFIG_VMAFMOTION_FILTER 1
#define CONFIG_VPP_QSV_FILTER 0
#define CONFIG_VSTACK_FILTER 1
#define CONFIG_W3FDIF_FILTER 1
#define CONFIG_WAVEFORM_FILTER 1
#define CONFIG_WEAVE_FILTER 1
#define CONFIG_XBR_FILTER 1
#define CONFIG_XFADE_FILTER 1
#define CONFIG_XFADE_OPENCL_FILTER 0
#define CONFIG_XMEDIAN_FILTER 1
#define CONFIG_XSTACK_FILTER 1
#define CONFIG_YADIF_FILTER 1
#define CONFIG_YADIF_CUDA_FILTER 0
#define CONFIG_YAEPBLUR_FILTER 1
#define CONFIG_ZMQ_FILTER 0
#define CONFIG_ZOOMPAN_FILTER 1
#define CONFIG_ZSCALE_FILTER 0
#define CONFIG_ALLRGB_FILTER 1
#define CONFIG_ALLYUV_FILTER 1
#define CONFIG_CELLAUTO_FILTER 1
#define CONFIG_COLOR_FILTER 1
#define CONFIG_COREIMAGESRC_FILTER 0
#define CONFIG_FREI0R_SRC_FILTER 0
#define CONFIG_GRADIENTS_FILTER 1
#define CONFIG_HALDCLUTSRC_FILTER 1
#define CONFIG_LIFE_FILTER 1
#define CONFIG_MANDELBROT_FILTER 1
#define CONFIG_MPTESTSRC_FILTER 0
#define CONFIG_NULLSRC_FILTER 1
#define CONFIG_OPENCLSRC_FILTER 0
#define CONFIG_PAL75BARS_FILTER 1
#define CONFIG_PAL100BARS_FILTER 1
#define CONFIG_RGBTESTSRC_FILTER 1
#define CONFIG_SIERPINSKI_FILTER 1
#define CONFIG_SMPTEBARS_FILTER 1
#define CONFIG_SMPTEHDBARS_FILTER 1
#define CONFIG_TESTSRC_FILTER 1
#define CONFIG_TESTSRC2_FILTER 1
#define CONFIG_YUVTESTSRC_FILTER 1
#define CONFIG_NULLSINK_FILTER 1
#define CONFIG_ABITSCOPE_FILTER 1
#define CONFIG_ADRAWGRAPH_FILTER 1
#define CONFIG_AGRAPHMONITOR_FILTER 1
#define CONFIG_AHISTOGRAM_FILTER 1
#define CONFIG_APHASEMETER_FILTER 1
#define CONFIG_AVECTORSCOPE_FILTER 1
#define CONFIG_CONCAT_FILTER 1
#define CONFIG_SHOWCQT_FILTER 1
#define CONFIG_SHOWFREQS_FILTER 1
#define CONFIG_SHOWSPATIAL_FILTER 1
#define CONFIG_SHOWSPECTRUM_FILTER 1
#define CONFIG_SHOWSPECTRUMPIC_FILTER 1
#define CONFIG_SHOWVOLUME_FILTER 1
#define CONFIG_SHOWWAVES_FILTER 1
#define CONFIG_SHOWWAVESPIC_FILTER 1
#define CONFIG_SPECTRUMSYNTH_FILTER 1
#define CONFIG_AMOVIE_FILTER 1
#define CONFIG_MOVIE_FILTER 1
#define CONFIG_AFIFO_FILTER 1
#define CONFIG_FIFO_FILTER 1
#define CONFIG_AA_DEMUXER 1
#define CONFIG_AAC_DEMUXER 1
#define CONFIG_AC3_DEMUXER 1
#define CONFIG_ACM_DEMUXER 1
#define CONFIG_ACT_DEMUXER 1
#define CONFIG_ADF_DEMUXER 1
#define CONFIG_ADP_DEMUXER 1
#define CONFIG_ADS_DEMUXER 1
#define CONFIG_ADX_DEMUXER 1
#define CONFIG_AEA_DEMUXER 1
#define CONFIG_AFC_DEMUXER 1
#define CONFIG_AIFF_DEMUXER 1
#define CONFIG_AIX_DEMUXER 1
#define CONFIG_ALP_DEMUXER 1
#define CONFIG_AMR_DEMUXER 1
#define CONFIG_AMRNB_DEMUXER 1
#define CONFIG_AMRWB_DEMUXER 1
#define CONFIG_ANM_DEMUXER 1
#define CONFIG_APC_DEMUXER 1
#define CONFIG_APE_DEMUXER 1
#define CONFIG_APM_DEMUXER 1
#define CONFIG_APNG_DEMUXER 1
#define CONFIG_APTX_DEMUXER 1
#define CONFIG_APTX_HD_DEMUXER 1
#define CONFIG_AQTITLE_DEMUXER 1
#define CONFIG_ARGO_ASF_DEMUXER 1
#define CONFIG_ASF_DEMUXER 1
#define CONFIG_ASF_O_DEMUXER 1
#define CONFIG_ASS_DEMUXER 1
#define CONFIG_AST_DEMUXER 1
#define CONFIG_AU_DEMUXER 1
#define CONFIG_AV1_DEMUXER 1
#define CONFIG_AVI_DEMUXER 1
#define CONFIG_AVISYNTH_DEMUXER 0
#define CONFIG_AVR_DEMUXER 1
#define CONFIG_AVS_DEMUXER 1
#define CONFIG_AVS2_DEMUXER 1
#define CONFIG_BETHSOFTVID_DEMUXER 1
#define CONFIG_BFI_DEMUXER 1
#define CONFIG_BINTEXT_DEMUXER 1
#define CONFIG_BINK_DEMUXER 1
#define CONFIG_BIT_DEMUXER 1
#define CONFIG_BMV_DEMUXER 1
#define CONFIG_BFSTM_DEMUXER 1
#define CONFIG_BRSTM_DEMUXER 1
#define CONFIG_BOA_DEMUXER 1
#define CONFIG_C93_DEMUXER 1
#define CONFIG_CAF_DEMUXER 1
#define CONFIG_CAVSVIDEO_DEMUXER 1
#define CONFIG_CDG_DEMUXER 1
#define CONFIG_CDXL_DEMUXER 1
#define CONFIG_CINE_DEMUXER 1
#define CONFIG_CODEC2_DEMUXER 1
#define CONFIG_CODEC2RAW_DEMUXER 1
#define CONFIG_CONCAT_DEMUXER 1
#define CONFIG_DASH_DEMUXER 0
#define CONFIG_DATA_DEMUXER 1
#define CONFIG_DAUD_DEMUXER 1
#define CONFIG_DCSTR_DEMUXER 1
#define CONFIG_DERF_DEMUXER 1
#define CONFIG_DFA_DEMUXER 1
#define CONFIG_DHAV_DEMUXER 1
#define CONFIG_DIRAC_DEMUXER 1
#define CONFIG_DNXHD_DEMUXER 1
#define CONFIG_DSF_DEMUXER 1
#define CONFIG_DSICIN_DEMUXER 1
#define CONFIG_DSS_DEMUXER 1
#define CONFIG_DTS_DEMUXER 1
#define CONFIG_DTSHD_DEMUXER 1
#define CONFIG_DV_DEMUXER 1
#define CONFIG_DVBSUB_DEMUXER 1
#define CONFIG_DVBTXT_DEMUXER 1
#define CONFIG_DXA_DEMUXER 1
#define CONFIG_EA_DEMUXER 1
#define CONFIG_EA_CDATA_DEMUXER 1
#define CONFIG_EAC3_DEMUXER 1
#define CONFIG_EPAF_DEMUXER 1
#define CONFIG_FFMETADATA_DEMUXER 1
#define CONFIG_FILMSTRIP_DEMUXER 1
#define CONFIG_FITS_DEMUXER 1
#define CONFIG_FLAC_DEMUXER 1
#define CONFIG_FLIC_DEMUXER 1
#define CONFIG_FLV_DEMUXER 1
#define CONFIG_LIVE_FLV_DEMUXER 1
#define CONFIG_FOURXM_DEMUXER 1
#define CONFIG_FRM_DEMUXER 1
#define CONFIG_FSB_DEMUXER 1
#define CONFIG_FWSE_DEMUXER 1
#define CONFIG_G722_DEMUXER 1
#define CONFIG_G723_1_DEMUXER 1
#define CONFIG_G726_DEMUXER 1
#define CONFIG_G726LE_DEMUXER 1
#define CONFIG_G729_DEMUXER 1
#define CONFIG_GDV_DEMUXER 1
#define CONFIG_GENH_DEMUXER 1
#define CONFIG_GIF_DEMUXER 1
#define CONFIG_GSM_DEMUXER 1
#define CONFIG_GXF_DEMUXER 1
#define CONFIG_H261_DEMUXER 1
#define CONFIG_H263_DEMUXER 1
#define CONFIG_H264_DEMUXER 1
#define CONFIG_HCA_DEMUXER 1
#define CONFIG_HCOM_DEMUXER 1
#define CONFIG_HEVC_DEMUXER 1
#define CONFIG_HLS_DEMUXER 1
#define CONFIG_HNM_DEMUXER 1
#define CONFIG_ICO_DEMUXER 1
#define CONFIG_IDCIN_DEMUXER 1
#define CONFIG_IDF_DEMUXER 1
#define CONFIG_IFF_DEMUXER 1
#define CONFIG_IFV_DEMUXER 1
#define CONFIG_ILBC_DEMUXER 1
#define CONFIG_IMAGE2_DEMUXER 1
#define CONFIG_IMAGE2PIPE_DEMUXER 1
#define CONFIG_IMAGE2_ALIAS_PIX_DEMUXER 1
#define CONFIG_IMAGE2_BRENDER_PIX_DEMUXER 1
#define CONFIG_INGENIENT_DEMUXER 1
#define CONFIG_IPMOVIE_DEMUXER 1
#define CONFIG_IRCAM_DEMUXER 1
#define CONFIG_ISS_DEMUXER 1
#define CONFIG_IV8_DEMUXER 1
#define CONFIG_IVF_DEMUXER 1
#define CONFIG_IVR_DEMUXER 1
#define CONFIG_JACOSUB_DEMUXER 1
#define CONFIG_JV_DEMUXER 1
#define CONFIG_KUX_DEMUXER 1
#define CONFIG_KVAG_DEMUXER 1
#define CONFIG_LMLM4_DEMUXER 1
#define CONFIG_LOAS_DEMUXER 1
#define CONFIG_LRC_DEMUXER 1
#define CONFIG_LVF_DEMUXER 1
#define CONFIG_LXF_DEMUXER 1
#define CONFIG_M4V_DEMUXER 1
#define CONFIG_MATROSKA_DEMUXER 1
#define CONFIG_MGSTS_DEMUXER 1
#define CONFIG_MICRODVD_DEMUXER 1
#define CONFIG_MJPEG_DEMUXER 1
#define CONFIG_MJPEG_2000_DEMUXER 1
#define CONFIG_MLP_DEMUXER 1
#define CONFIG_MLV_DEMUXER 1
#define CONFIG_MM_DEMUXER 1
#define CONFIG_MMF_DEMUXER 1
#define CONFIG_MOV_DEMUXER 1
#define CONFIG_MP3_DEMUXER 1
#define CONFIG_MPC_DEMUXER 1
#define CONFIG_MPC8_DEMUXER 1
#define CONFIG_MPEGPS_DEMUXER 1
#define CONFIG_MPEGTS_DEMUXER 1
#define CONFIG_MPEGTSRAW_DEMUXER 1
#define CONFIG_MPEGVIDEO_DEMUXER 1
#define CONFIG_MPJPEG_DEMUXER 1
#define CONFIG_MPL2_DEMUXER 1
#define CONFIG_MPSUB_DEMUXER 1
#define CONFIG_MSF_DEMUXER 1
#define CONFIG_MSNWC_TCP_DEMUXER 1
#define CONFIG_MTAF_DEMUXER 1
#define CONFIG_MTV_DEMUXER 1
#define CONFIG_MUSX_DEMUXER 1
#define CONFIG_MV_DEMUXER 1
#define CONFIG_MVI_DEMUXER 1
#define CONFIG_MXF_DEMUXER 1
#define CONFIG_MXG_DEMUXER 1
#define CONFIG_NC_DEMUXER 1
#define CONFIG_NISTSPHERE_DEMUXER 1
#define CONFIG_NSP_DEMUXER 1
#define CONFIG_NSV_DEMUXER 1
#define CONFIG_NUT_DEMUXER 1
#define CONFIG_NUV_DEMUXER 1
#define CONFIG_OGG_DEMUXER 1
#define CONFIG_OMA_DEMUXER 1
#define CONFIG_PAF_DEMUXER 1
#define CONFIG_PCM_ALAW_DEMUXER 1
#define CONFIG_PCM_MULAW_DEMUXER 1
#define CONFIG_PCM_VIDC_DEMUXER 1
#define CONFIG_PCM_F64BE_DEMUXER 1
#define CONFIG_PCM_F64LE_DEMUXER 1
#define CONFIG_PCM_F32BE_DEMUXER 1
#define CONFIG_PCM_F32LE_DEMUXER 1
#define CONFIG_PCM_S32BE_DEMUXER 1
#define CONFIG_PCM_S32LE_DEMUXER 1
#define CONFIG_PCM_S24BE_DEMUXER 1
#define CONFIG_PCM_S24LE_DEMUXER 1
#define CONFIG_PCM_S16BE_DEMUXER 1
#define CONFIG_PCM_S16LE_DEMUXER 1
#define CONFIG_PCM_S8_DEMUXER 1
#define CONFIG_PCM_U32BE_DEMUXER 1
#define CONFIG_PCM_U32LE_DEMUXER 1
#define CONFIG_PCM_U24BE_DEMUXER 1
#define CONFIG_PCM_U24LE_DEMUXER 1
#define CONFIG_PCM_U16BE_DEMUXER 1
#define CONFIG_PCM_U16LE_DEMUXER 1
#define CONFIG_PCM_U8_DEMUXER 1
#define CONFIG_PJS_DEMUXER 1
#define CONFIG_PMP_DEMUXER 1
#define CONFIG_PP_BNK_DEMUXER 1
#define CONFIG_PVA_DEMUXER 1
#define CONFIG_PVF_DEMUXER 1
#define CONFIG_QCP_DEMUXER 1
#define CONFIG_R3D_DEMUXER 1
#define CONFIG_RAWVIDEO_DEMUXER 1
#define CONFIG_REALTEXT_DEMUXER 1
#define CONFIG_REDSPARK_DEMUXER 1
#define CONFIG_RL2_DEMUXER 1
#define CONFIG_RM_DEMUXER 1
#define CONFIG_ROQ_DEMUXER 1
#define CONFIG_RPL_DEMUXER 1
#define CONFIG_RSD_DEMUXER 1
#define CONFIG_RSO_DEMUXER 1
#define CONFIG_RTP_DEMUXER 1
#define CONFIG_RTSP_DEMUXER 1
#define CONFIG_S337M_DEMUXER 1
#define CONFIG_SAMI_DEMUXER 1
#define CONFIG_SAP_DEMUXER 1
#define CONFIG_SBC_DEMUXER 1
#define CONFIG_SBG_DEMUXER 1
#define CONFIG_SCC_DEMUXER 1
#define CONFIG_SDP_DEMUXER 1
#define CONFIG_SDR2_DEMUXER 1
#define CONFIG_SDS_DEMUXER 1
#define CONFIG_SDX_DEMUXER 1
#define CONFIG_SEGAFILM_DEMUXER 1
#define CONFIG_SER_DEMUXER 1
#define CONFIG_SHORTEN_DEMUXER 1
#define CONFIG_SIFF_DEMUXER 1
#define CONFIG_SLN_DEMUXER 1
#define CONFIG_SMACKER_DEMUXER 1
#define CONFIG_SMJPEG_DEMUXER 1
#define CONFIG_SMUSH_DEMUXER 1
#define CONFIG_SOL_DEMUXER 1
#define CONFIG_SOX_DEMUXER 1
#define CONFIG_SPDIF_DEMUXER 1
#define CONFIG_SRT_DEMUXER 1
#define CONFIG_STR_DEMUXER 1
#define CONFIG_STL_DEMUXER 1
#define CONFIG_SUBVIEWER1_DEMUXER 1
#define CONFIG_SUBVIEWER_DEMUXER 1
#define CONFIG_SUP_DEMUXER 1
#define CONFIG_SVAG_DEMUXER 1
#define CONFIG_SWF_DEMUXER 1
#define CONFIG_TAK_DEMUXER 1
#define CONFIG_TEDCAPTIONS_DEMUXER 1
#define CONFIG_THP_DEMUXER 1
#define CONFIG_THREEDOSTR_DEMUXER 1
#define CONFIG_TIERTEXSEQ_DEMUXER 1
#define CONFIG_TMV_DEMUXER 1
#define CONFIG_TRUEHD_DEMUXER 1
#define CONFIG_TTA_DEMUXER 1
#define CONFIG_TXD_DEMUXER 1
#define CONFIG_TTY_DEMUXER 1
#define CONFIG_TY_DEMUXER 1
#define CONFIG_V210_DEMUXER 1
#define CONFIG_V210X_DEMUXER 1
#define CONFIG_VAG_DEMUXER 1
#define CONFIG_VC1_DEMUXER 1
#define CONFIG_VC1T_DEMUXER 1
#define CONFIG_VIVIDAS_DEMUXER 1
#define CONFIG_VIVO_DEMUXER 1
#define CONFIG_VMD_DEMUXER 1
#define CONFIG_VOBSUB_DEMUXER 1
#define CONFIG_VOC_DEMUXER 1
#define CONFIG_VPK_DEMUXER 1
#define CONFIG_VPLAYER_DEMUXER 1
#define CONFIG_VQF_DEMUXER 1
#define CONFIG_W64_DEMUXER 1
#define CONFIG_WAV_DEMUXER 1
#define CONFIG_WC3_DEMUXER 1
#define CONFIG_WEBM_DASH_MANIFEST_DEMUXER 1
#define CONFIG_WEBVTT_DEMUXER 1
#define CONFIG_WSAUD_DEMUXER 1
#define CONFIG_WSD_DEMUXER 1
#define CONFIG_WSVQA_DEMUXER 1
#define CONFIG_WTV_DEMUXER 1
#define CONFIG_WVE_DEMUXER 1
#define CONFIG_WV_DEMUXER 1
#define CONFIG_XA_DEMUXER 1
#define CONFIG_XBIN_DEMUXER 1
#define CONFIG_XMV_DEMUXER 1
#define CONFIG_XVAG_DEMUXER 1
#define CONFIG_XWMA_DEMUXER 1
#define CONFIG_YOP_DEMUXER 1
#define CONFIG_YUV4MPEGPIPE_DEMUXER 1
#define CONFIG_IMAGE_BMP_PIPE_DEMUXER 1
#define CONFIG_IMAGE_DDS_PIPE_DEMUXER 1
#define CONFIG_IMAGE_DPX_PIPE_DEMUXER 1
#define CONFIG_IMAGE_EXR_PIPE_DEMUXER 1
#define CONFIG_IMAGE_GIF_PIPE_DEMUXER 1
#define CONFIG_IMAGE_J2K_PIPE_DEMUXER 1
#define CONFIG_IMAGE_JPEG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_JPEGLS_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PAM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PBM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PCX_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PGMYUV_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PGM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PICTOR_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PNG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PPM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_PSD_PIPE_DEMUXER 1
#define CONFIG_IMAGE_QDRAW_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SGI_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SVG_PIPE_DEMUXER 1
#define CONFIG_IMAGE_SUNRAST_PIPE_DEMUXER 1
#define CONFIG_IMAGE_TIFF_PIPE_DEMUXER 1
#define CONFIG_IMAGE_WEBP_PIPE_DEMUXER 1
#define CONFIG_IMAGE_XPM_PIPE_DEMUXER 1
#define CONFIG_IMAGE_XWD_PIPE_DEMUXER 1
#define CONFIG_LIBGME_DEMUXER 0
#define CONFIG_LIBMODPLUG_DEMUXER 0
#define CONFIG_LIBOPENMPT_DEMUXER 0
#define CONFIG_VAPOURSYNTH_DEMUXER 0
#define CONFIG_A64_MUXER 1
#define CONFIG_AC3_MUXER 1
#define CONFIG_ADTS_MUXER 1
#define CONFIG_ADX_MUXER 1
#define CONFIG_AIFF_MUXER 1
#define CONFIG_AMR_MUXER 1
#define CONFIG_APNG_MUXER 1
#define CONFIG_APTX_MUXER 1
#define CONFIG_APTX_HD_MUXER 1
#define CONFIG_ASF_MUXER 1
#define CONFIG_ASS_MUXER 1
#define CONFIG_AST_MUXER 1
#define CONFIG_ASF_STREAM_MUXER 1
#define CONFIG_AU_MUXER 1
#define CONFIG_AVI_MUXER 1
#define CONFIG_AVM2_MUXER 1
#define CONFIG_AVS2_MUXER 1
#define CONFIG_BIT_MUXER 1
#define CONFIG_CAF_MUXER 1
#define CONFIG_CAVSVIDEO_MUXER 1
#define CONFIG_CODEC2_MUXER 1
#define CONFIG_CODEC2RAW_MUXER 1
#define CONFIG_CRC_MUXER 1
#define CONFIG_DASH_MUXER 1
#define CONFIG_DATA_MUXER 1
#define CONFIG_DAUD_MUXER 1
#define CONFIG_DIRAC_MUXER 1
#define CONFIG_DNXHD_MUXER 1
#define CONFIG_DTS_MUXER 1
#define CONFIG_DV_MUXER 1
#define CONFIG_EAC3_MUXER 1
#define CONFIG_F4V_MUXER 1
#define CONFIG_FFMETADATA_MUXER 1
#define CONFIG_FIFO_MUXER 0
#define CONFIG_FIFO_TEST_MUXER 1
#define CONFIG_FILMSTRIP_MUXER 1
#define CONFIG_FITS_MUXER 1
#define CONFIG_FLAC_MUXER 1
#define CONFIG_FLV_MUXER 1
#define CONFIG_FRAMECRC_MUXER 1
#define CONFIG_FRAMEHASH_MUXER 1
#define CONFIG_FRAMEMD5_MUXER 1
#define CONFIG_G722_MUXER 1
#define CONFIG_G723_1_MUXER 1
#define CONFIG_G726_MUXER 1
#define CONFIG_G726LE_MUXER 1
#define CONFIG_GIF_MUXER 1
#define CONFIG_GSM_MUXER 1
#define CONFIG_GXF_MUXER 1
#define CONFIG_H261_MUXER 1
#define CONFIG_H263_MUXER 1
#define CONFIG_H264_MUXER 1
#define CONFIG_HASH_MUXER 1
#define CONFIG_HDS_MUXER 1
#define CONFIG_HEVC_MUXER 1
#define CONFIG_HLS_MUXER 1
#define CONFIG_ICO_MUXER 1
#define CONFIG_ILBC_MUXER 1
#define CONFIG_IMAGE2_MUXER 1
#define CONFIG_IMAGE2PIPE_MUXER 1
#define CONFIG_IPOD_MUXER 1
#define CONFIG_IRCAM_MUXER 1
#define CONFIG_ISMV_MUXER 1
#define CONFIG_IVF_MUXER 1
#define CONFIG_JACOSUB_MUXER 1
#define CONFIG_KVAG_MUXER 1
#define CONFIG_LATM_MUXER 1
#define CONFIG_LRC_MUXER 1
#define CONFIG_M4V_MUXER 1
#define CONFIG_MD5_MUXER 1
#define CONFIG_MATROSKA_MUXER 1
#define CONFIG_MATROSKA_AUDIO_MUXER 1
#define CONFIG_MICRODVD_MUXER 1
#define CONFIG_MJPEG_MUXER 1
#define CONFIG_MLP_MUXER 1
#define CONFIG_MMF_MUXER 1
#define CONFIG_MOV_MUXER 1
#define CONFIG_MP2_MUXER 1
#define CONFIG_MP3_MUXER 1
#define CONFIG_MP4_MUXER 1
#define CONFIG_MPEG1SYSTEM_MUXER 1
#define CONFIG_MPEG1VCD_MUXER 1
#define CONFIG_MPEG1VIDEO_MUXER 1
#define CONFIG_MPEG2DVD_MUXER 1
#define CONFIG_MPEG2SVCD_MUXER 1
#define CONFIG_MPEG2VIDEO_MUXER 1
#define CONFIG_MPEG2VOB_MUXER 1
#define CONFIG_MPEGTS_MUXER 1
#define CONFIG_MPJPEG_MUXER 1
#define CONFIG_MXF_MUXER 1
#define CONFIG_MXF_D10_MUXER 1
#define CONFIG_MXF_OPATOM_MUXER 1
#define CONFIG_NULL_MUXER 1
#define CONFIG_NUT_MUXER 1
#define CONFIG_OGA_MUXER 1
#define CONFIG_OGG_MUXER 1
#define CONFIG_OGV_MUXER 1
#define CONFIG_OMA_MUXER 1
#define CONFIG_OPUS_MUXER 1
#define CONFIG_PCM_ALAW_MUXER 1
#define CONFIG_PCM_MULAW_MUXER 1
#define CONFIG_PCM_VIDC_MUXER 1
#define CONFIG_PCM_F64BE_MUXER 1
#define CONFIG_PCM_F64LE_MUXER 1
#define CONFIG_PCM_F32BE_MUXER 1
#define CONFIG_PCM_F32LE_MUXER 1
#define CONFIG_PCM_S32BE_MUXER 1
#define CONFIG_PCM_S32LE_MUXER 1
#define CONFIG_PCM_S24BE_MUXER 1
#define CONFIG_PCM_S24LE_MUXER 1
#define CONFIG_PCM_S16BE_MUXER 1
#define CONFIG_PCM_S16LE_MUXER 1
#define CONFIG_PCM_S8_MUXER 1
#define CONFIG_PCM_U32BE_MUXER 1
#define CONFIG_PCM_U32LE_MUXER 1
#define CONFIG_PCM_U24BE_MUXER 1
#define CONFIG_PCM_U24LE_MUXER 1
#define CONFIG_PCM_U16BE_MUXER 1
#define CONFIG_PCM_U16LE_MUXER 1
#define CONFIG_PCM_U8_MUXER 1
#define CONFIG_PSP_MUXER 1
#define CONFIG_RAWVIDEO_MUXER 1
#define CONFIG_RM_MUXER 1
#define CONFIG_ROQ_MUXER 1
#define CONFIG_RSO_MUXER 1
#define CONFIG_RTP_MUXER 1
#define CONFIG_RTP_MPEGTS_MUXER 1
#define CONFIG_RTSP_MUXER 1
#define CONFIG_SAP_MUXER 1
#define CONFIG_SBC_MUXER 1
#define CONFIG_SCC_MUXER 1
#define CONFIG_SEGAFILM_MUXER 1
#define CONFIG_SEGMENT_MUXER 1
#define CONFIG_STREAM_SEGMENT_MUXER 1
#define CONFIG_SINGLEJPEG_MUXER 1
#define CONFIG_SMJPEG_MUXER 1
#define CONFIG_SMOOTHSTREAMING_MUXER 1
#define CONFIG_SOX_MUXER 1
#define CONFIG_SPX_MUXER 1
#define CONFIG_SPDIF_MUXER 1
#define CONFIG_SRT_MUXER 1
#define CONFIG_STREAMHASH_MUXER 1
#define CONFIG_SUP_MUXER 1
#define CONFIG_SWF_MUXER 1
#define CONFIG_TEE_MUXER 1
#define CONFIG_TG2_MUXER 1
#define CONFIG_TGP_MUXER 1
#define CONFIG_MKVTIMESTAMP_V2_MUXER 1
#define CONFIG_TRUEHD_MUXER 1
#define CONFIG_TTA_MUXER 1
#define CONFIG_UNCODEDFRAMECRC_MUXER 1
#define CONFIG_VC1_MUXER 1
#define CONFIG_VC1T_MUXER 1
#define CONFIG_VOC_MUXER 1
#define CONFIG_W64_MUXER 1
#define CONFIG_WAV_MUXER 1
#define CONFIG_WEBM_MUXER 1
#define CONFIG_WEBM_DASH_MANIFEST_MUXER 1
#define CONFIG_WEBM_CHUNK_MUXER 1
#define CONFIG_WEBP_MUXER 1
#define CONFIG_WEBVTT_MUXER 1
#define CONFIG_WTV_MUXER 1
#define CONFIG_WV_MUXER 1
#define CONFIG_YUV4MPEGPIPE_MUXER 1
#define CONFIG_CHROMAPRINT_MUXER 0
#define CONFIG_ASYNC_PROTOCOL 0
#define CONFIG_BLURAY_PROTOCOL 0
#define CONFIG_CACHE_PROTOCOL 1
#define CONFIG_CONCAT_PROTOCOL 1
#define CONFIG_CRYPTO_PROTOCOL 1
#define CONFIG_DATA_PROTOCOL 1
#define CONFIG_FFRTMPCRYPT_PROTOCOL 0
#define CONFIG_FFRTMPHTTP_PROTOCOL 1
#define CONFIG_FILE_PROTOCOL 1
#define CONFIG_FTP_PROTOCOL 1
#define CONFIG_GOPHER_PROTOCOL 1
#define CONFIG_HLS_PROTOCOL 1
#define CONFIG_HTTP_PROTOCOL 1
#define CONFIG_HTTPPROXY_PROTOCOL 1
#define CONFIG_HTTPS_PROTOCOL 0
#define CONFIG_ICECAST_PROTOCOL 1
#define CONFIG_MMSH_PROTOCOL 1
#define CONFIG_MMST_PROTOCOL 1
#define CONFIG_MD5_PROTOCOL 1
#define CONFIG_PIPE_PROTOCOL 1
#define CONFIG_PROMPEG_PROTOCOL 1
#define CONFIG_RTMP_PROTOCOL 1
#define CONFIG_RTMPE_PROTOCOL 0
#define CONFIG_RTMPS_PROTOCOL 0
#define CONFIG_RTMPT_PROTOCOL 1
#define CONFIG_RTMPTE_PROTOCOL 0
#define CONFIG_RTMPTS_PROTOCOL 0
#define CONFIG_RTP_PROTOCOL 1
#define CONFIG_SCTP_PROTOCOL 0
#define CONFIG_SRTP_PROTOCOL 1
#define CONFIG_SUBFILE_PROTOCOL 1
#define CONFIG_TEE_PROTOCOL 1
#define CONFIG_TCP_PROTOCOL 1
#define CONFIG_TLS_PROTOCOL 0
#define CONFIG_UDP_PROTOCOL 1
#define CONFIG_UDPLITE_PROTOCOL 1
#define CONFIG_UNIX_PROTOCOL 1
#define CONFIG_LIBAMQP_PROTOCOL 0
#define CONFIG_LIBRTMP_PROTOCOL 0
#define CONFIG_LIBRTMPE_PROTOCOL 0
#define CONFIG_LIBRTMPS_PROTOCOL 0
#define CONFIG_LIBRTMPT_PROTOCOL 0
#define CONFIG_LIBRTMPTE_PROTOCOL 0
#define CONFIG_LIBSRT_PROTOCOL 0
#define CONFIG_LIBSSH_PROTOCOL 0
#define CONFIG_LIBSMBCLIENT_PROTOCOL 0
#define CONFIG_LIBZMQ_PROTOCOL 0
#endif /* FFMPEG_CONFIG_H */

'''
