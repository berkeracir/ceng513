#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM Transmitter and Receiver (Without using USRPs)
# Author: Berker
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
from gnuradio import fec
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui

class ofdm_txrx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Transmitter and Receiver (Without using USRPs)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM Transmitter and Receiver (Without using USRPs)")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ofdm_txrx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.pilot_carriers0 = pilot_carriers0 = (-21, -7, 7, 21,)
        self.carrier_count = carrier_count = 26
        self.pilot_symbols0 = pilot_symbols0 = (1, 1, 1, -1,)
        self.occupied_carriers0 = occupied_carriers0 = [c for c in range(-carrier_count, carrier_count+1) if c not in pilot_carriers0 and c != 0]
        self.pilot_symbols = pilot_symbols = (pilot_symbols0,)
        self.pilot_carriers = pilot_carriers = (pilot_carriers0,)
        self.payload_modulation = payload_modulation = digital.constellation_qpsk()
        self.packet_len_key = packet_len_key = "packet_len"
        self.occupied_carriers = occupied_carriers = (occupied_carriers0,)
        self.header_modulation = header_modulation = digital.constellation_bpsk()
        self.frame_len_key = frame_len_key = "frame_len"
        self.fft_len = fft_len = 64
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.samp_rate = samp_rate = int(10e6)
        self.rolloff = rolloff = 0
        self.payload_equalizer = payload_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, payload_modulation.base(), occupied_carriers, pilot_carriers, pilot_symbols, 1)
        self.packet_len = packet_len = 96
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, n_syms=1, len_tag_key=packet_len_key, frame_len_tag_key=frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False)
        self.header_format = header_format = digital.header_format_ofdm(occupied_carriers, n_syms=1, len_key_name=packet_len_key, frame_key_name=frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False)
        self.header_equalizer = header_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, header_modulation.base(), occupied_carriers, pilot_carriers, pilot_symbols)
        self.cp_len = cp_len = fft_len//4
        self.bits_per_byte = bits_per_byte = 8

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.fft_vxx_1_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_1 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(header_format, packet_len_key)
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_ofdm_sync_sc_cfb_0 = digital.ofdm_sync_sc_cfb(fft_len, cp_len, False, 0.9)
        self.digital_ofdm_serializer_vcc_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, frame_len_key, packet_len_key, 1, '', True)
        self.digital_ofdm_serializer_vcc_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, frame_len_key, '', 0, '', True)
        self.digital_ofdm_frame_equalizer_vcvc_0_0 = digital.ofdm_frame_equalizer_vcvc(payload_equalizer.base(), cp_len, frame_len_key, True, 0)
        self.digital_ofdm_frame_equalizer_vcvc_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer.base(), cp_len, frame_len_key, True, 1)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len + cp_len, rolloff, packet_len_key)
        self.digital_ofdm_chanest_vcvc_0 = digital.ofdm_chanest_vcvc(sync_word1, sync_word2, 1, 0, 3, False)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2,), packet_len_key, True)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            3,
            fft_len,
            cp_len,
            frame_len_key,
            "",
            True,
            gr.sizeof_gr_complex,
            "rx_time",
            samp_rate,
            (),
            0)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, packet_len_key, True)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(payload_modulation.base())
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(header_modulation.base())
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_modulation.points(), payload_modulation.dimensionality())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_modulation.points(), header_modulation.dimensionality())
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=0.1,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0 + 1.0j],
            noise_seed=0,
            block_tags=True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, packet_len_key, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, packet_len_key)
        self.blocks_repack_bits_bb_2 = blocks.repack_bits_bb(payload_modulation.bits_per_symbol(), bits_per_byte, packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(bits_per_byte, header_modulation.bits_per_symbol(), packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(bits_per_byte, payload_modulation.bits_per_symbol(), packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.05)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/berker/Desktop/ceng513/files/input.txt', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, fft_len + cp_len)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(-2.0/fft_len)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_2, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_ofdm_sync_sc_cfb_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_repack_bits_bb_2, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.fft_vxx_1, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.fft_vxx_1_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0, 0), (self.digital_ofdm_serializer_vcc_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0_0, 0), (self.digital_ofdm_serializer_vcc_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 1), (self.digital_header_payload_demux_0, 1))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.digital_ofdm_chanest_vcvc_0, 0))
        self.connect((self.fft_vxx_1_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_txrx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_pilot_carriers0(self):
        return self.pilot_carriers0

    def set_pilot_carriers0(self, pilot_carriers0):
        self.pilot_carriers0 = pilot_carriers0
        self.set_occupied_carriers0([c for c in range(-self.carrier_count, self.carrier_count+1) if c not in self.pilot_carriers0 and c != 0])
        self.set_pilot_carriers((self.pilot_carriers0,))

    def get_carrier_count(self):
        return self.carrier_count

    def set_carrier_count(self, carrier_count):
        self.carrier_count = carrier_count
        self.set_occupied_carriers0([c for c in range(-self.carrier_count, self.carrier_count+1) if c not in self.pilot_carriers0 and c != 0])

    def get_pilot_symbols0(self):
        return self.pilot_symbols0

    def set_pilot_symbols0(self, pilot_symbols0):
        self.pilot_symbols0 = pilot_symbols0
        self.set_pilot_symbols((self.pilot_symbols0,))

    def get_occupied_carriers0(self):
        return self.occupied_carriers0

    def set_occupied_carriers0(self, occupied_carriers0):
        self.occupied_carriers0 = occupied_carriers0
        self.set_occupied_carriers((self.occupied_carriers0,))

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_payload_modulation(self):
        return self.payload_modulation

    def set_payload_modulation(self, payload_modulation):
        self.payload_modulation = payload_modulation

    def get_packet_len_key(self):
        return self.packet_len_key

    def set_packet_len_key(self, packet_len_key):
        self.packet_len_key = packet_len_key
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_len_key, frame_len_tag_key=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_len_key, frame_len_tag_key=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))

    def get_header_modulation(self):
        return self.header_modulation

    def set_header_modulation(self, header_modulation):
        self.header_modulation = header_modulation

    def get_frame_len_key(self):
        return self.frame_len_key

    def set_frame_len_key(self, frame_len_key):
        self.frame_len_key = frame_len_key
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))
        self.set_header_formatter(digital.packet_header_ofdm(self.occupied_carriers, n_syms=1, len_tag_key=self.packet_len_key, frame_len_tag_key=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_cp_len(self.fft_len//4)
        self.set_header_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, header_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols))
        self.set_payload_equalizer(digital.ofdm_equalizer_simpledfe(self.fft_len, payload_modulation.base(), self.occupied_carriers, self.pilot_carriers, self.pilot_symbols, 1))
        self.analog_frequency_modulator_fc_0.set_sensitivity(-2.0/self.fft_len)
        self.blocks_delay_0.set_dly(self.fft_len + self.cp_len)

    def get_sync_word2(self):
        return self.sync_word2

    def set_sync_word2(self, sync_word2):
        self.sync_word2 = sync_word2

    def get_sync_word1(self):
        return self.sync_word1

    def set_sync_word1(self, sync_word1):
        self.sync_word1 = sync_word1

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_payload_equalizer(self):
        return self.payload_equalizer

    def set_payload_equalizer(self, payload_equalizer):
        self.payload_equalizer = payload_equalizer

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_header_formatter(self):
        return self.header_formatter

    def set_header_formatter(self, header_formatter):
        self.header_formatter = header_formatter

    def get_header_format(self):
        return self.header_format

    def set_header_format(self, header_format):
        self.header_format = header_format

    def get_header_equalizer(self):
        return self.header_equalizer

    def set_header_equalizer(self, header_equalizer):
        self.header_equalizer = header_equalizer

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.blocks_delay_0.set_dly(self.fft_len + self.cp_len)

    def get_bits_per_byte(self):
        return self.bits_per_byte

    def set_bits_per_byte(self, bits_per_byte):
        self.bits_per_byte = bits_per_byte
        self.blocks_repack_bits_bb_0.set_k_and_l(self.bits_per_byte,payload_modulation.bits_per_symbol())
        self.blocks_repack_bits_bb_1.set_k_and_l(self.bits_per_byte,header_modulation.bits_per_symbol())
        self.blocks_repack_bits_bb_2.set_k_and_l(payload_modulation.bits_per_symbol(),self.bits_per_byte)



def main(top_block_cls=ofdm_txrx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
