#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM Transmitter
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
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import qtgui

class ofdm_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Transmitter")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM Transmitter")
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm_tx")

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
        self.occupied_carriers0 = occupied_carriers0 = [c for c in range(-carrier_count, carrier_count+1) if c not in pilot_carriers0 and c != 0]
        self.pilot_symbols0 = pilot_symbols0 = (1, 1, 1, -1,)
        self.payload_modulation = payload_modulation = digital.constellation_qpsk()
        self.packet_len_key = packet_len_key = "packet_len"
        self.occupied_carriers = occupied_carriers = (occupied_carriers0,)
        self.header_modulation = header_modulation = digital.constellation_bpsk()
        self.frame_len_key = frame_len_key = "frame_len"
        self.fft_len = fft_len = 64
        self.sync_word2 = sync_word2 = [0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 0, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 0, 0, 0, 0, 0]
        self.sync_word1 = sync_word1 = [0., 0., 0., 0., 0., 0., 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., -1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., -1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 1.41421356, 0., 0., 0., 0., 0., 0.]
        self.samp_rate = samp_rate = int(2e6)
        self.rolloff = rolloff = 0
        self.pilot_symbols = pilot_symbols = (pilot_symbols0,)
        self.pilot_carriers = pilot_carriers = (pilot_carriers0,)
        self.packet_len = packet_len = 96
        self.header_format = header_format = digital.header_format_ofdm(occupied_carriers, n_syms=1, len_key_name=packet_len_key, frame_key_name=frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False)
        self.gain = gain = 80
        self.cp_len = cp_len = fft_len//4
        self.center_freq = center_freq = 2.5e9
        self.bits_per_byte = bits_per_byte = 8

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("name=winslab_3", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # No synchronization enforced.
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Transmitted Signal", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.fft_vxx_0 = fft.fft_vcc(fft_len, False, (), True, 1)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(header_format, packet_len_key)
        self.digital_ofdm_cyclic_prefixer_0 = digital.ofdm_cyclic_prefixer(fft_len, fft_len + cp_len, rolloff, packet_len_key)
        self.digital_ofdm_carrier_allocator_cvc_0 = digital.ofdm_carrier_allocator_cvc( fft_len, occupied_carriers, pilot_carriers, pilot_symbols, (sync_word1, sync_word2,), packet_len_key, True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, packet_len_key, True)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc(payload_modulation.points(), payload_modulation.dimensionality())
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(header_modulation.points(), header_modulation.dimensionality())
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_gr_complex*1, packet_len_key, 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, packet_len_key)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(bits_per_byte, header_modulation.bits_per_symbol(), packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(bits_per_byte, payload_modulation.bits_per_symbol(), packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.05)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/berker/Desktop/ceng513/files/input.txt', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_ofdm_carrier_allocator_cvc_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_ofdm_carrier_allocator_cvc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.digital_ofdm_cyclic_prefixer_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.fft_vxx_0, 0), (self.digital_ofdm_cyclic_prefixer_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_tx")
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

    def get_occupied_carriers0(self):
        return self.occupied_carriers0

    def set_occupied_carriers0(self, occupied_carriers0):
        self.occupied_carriers0 = occupied_carriers0
        self.set_occupied_carriers((self.occupied_carriers0,))

    def get_pilot_symbols0(self):
        return self.pilot_symbols0

    def set_pilot_symbols0(self, pilot_symbols0):
        self.pilot_symbols0 = pilot_symbols0
        self.set_pilot_symbols((self.pilot_symbols0,))

    def get_payload_modulation(self):
        return self.payload_modulation

    def set_payload_modulation(self, payload_modulation):
        self.payload_modulation = payload_modulation

    def get_packet_len_key(self):
        return self.packet_len_key

    def set_packet_len_key(self, packet_len_key):
        self.packet_len_key = packet_len_key
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))

    def get_occupied_carriers(self):
        return self.occupied_carriers

    def set_occupied_carriers(self, occupied_carriers):
        self.occupied_carriers = occupied_carriers
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))

    def get_header_modulation(self):
        return self.header_modulation

    def set_header_modulation(self, header_modulation):
        self.header_modulation = header_modulation

    def get_frame_len_key(self):
        return self.frame_len_key

    def set_frame_len_key(self, frame_len_key):
        self.frame_len_key = frame_len_key
        self.set_header_format(digital.header_format_ofdm(self.occupied_carriers, n_syms=1, len_key_name=self.packet_len_key, frame_key_name=self.frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False))

    def get_fft_len(self):
        return self.fft_len

    def set_fft_len(self, fft_len):
        self.fft_len = fft_len
        self.set_cp_len(self.fft_len//4)

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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_rolloff(self):
        return self.rolloff

    def set_rolloff(self, rolloff):
        self.rolloff = rolloff

    def get_pilot_symbols(self):
        return self.pilot_symbols

    def set_pilot_symbols(self, pilot_symbols):
        self.pilot_symbols = pilot_symbols

    def get_pilot_carriers(self):
        return self.pilot_carriers

    def set_pilot_carriers(self, pilot_carriers):
        self.pilot_carriers = pilot_carriers

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.packet_len)

    def get_header_format(self):
        return self.header_format

    def set_header_format(self, header_format):
        self.header_format = header_format

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(self.center_freq, 0)

    def get_bits_per_byte(self):
        return self.bits_per_byte

    def set_bits_per_byte(self, bits_per_byte):
        self.bits_per_byte = bits_per_byte
        self.blocks_repack_bits_bb_0.set_k_and_l(self.bits_per_byte,payload_modulation.bits_per_symbol())
        self.blocks_repack_bits_bb_1.set_k_and_l(self.bits_per_byte,header_modulation.bits_per_symbol())



def main(top_block_cls=ofdm_tx, options=None):

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
