#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: OFDM Receiver
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
from gnuradio import analog
from gnuradio import blocks
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

class ofdm_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "OFDM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("OFDM Receiver")
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

        self.settings = Qt.QSettings("GNU Radio", "ofdm_rx")

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
        self.samp_rate = samp_rate = int(2e6)
        self.rolloff = rolloff = 0
        self.payload_equalizer = payload_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, payload_modulation.base(), occupied_carriers, pilot_carriers, pilot_symbols, 1)
        self.packet_len = packet_len = 96
        self.header_formatter = header_formatter = digital.packet_header_ofdm(occupied_carriers, n_syms=1, len_tag_key=packet_len_key, frame_len_tag_key=frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False)
        self.header_format = header_format = digital.header_format_ofdm(occupied_carriers, n_syms=1, len_key_name=packet_len_key, frame_key_name=frame_len_key, bits_per_header_sym=header_modulation.bits_per_symbol(), bits_per_payload_sym=payload_modulation.bits_per_symbol(), scramble_header=False)
        self.header_equalizer = header_equalizer = digital.ofdm_equalizer_simpledfe(fft_len, header_modulation.base(), occupied_carriers, pilot_carriers, pilot_symbols)
        self.gain = gain = 20
        self.cp_len = cp_len = fft_len//4
        self.center_freq = center_freq = 2.5e9
        self.bits_per_byte = bits_per_byte = 8

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("name=winslab_8", "")),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_center_freq(center_freq, 0)
        self.uhd_usrp_source_0.set_gain(15, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_KAISER, #wintype
            center_freq, #fc
            samp_rate, #bw
            "Received Signal", #name
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
        self.fft_vxx_1_0 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.fft_vxx_1 = fft.fft_vcc(fft_len, True, (), True, 1)
        self.digital_packet_headerparser_b_0 = digital.packet_headerparser_b(header_formatter.base())
        self.digital_ofdm_sync_sc_cfb_0 = digital.ofdm_sync_sc_cfb(fft_len, cp_len, False, 0.9)
        self.digital_ofdm_serializer_vcc_0_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, frame_len_key, packet_len_key, 1, '', True)
        self.digital_ofdm_serializer_vcc_0 = digital.ofdm_serializer_vcc(fft_len, occupied_carriers, frame_len_key, '', 0, '', True)
        self.digital_ofdm_frame_equalizer_vcvc_0_0 = digital.ofdm_frame_equalizer_vcvc(payload_equalizer.base(), cp_len, frame_len_key, True, 0)
        self.digital_ofdm_frame_equalizer_vcvc_0 = digital.ofdm_frame_equalizer_vcvc(header_equalizer.base(), cp_len, frame_len_key, True, 1)
        self.digital_ofdm_chanest_vcvc_0 = digital.ofdm_chanest_vcvc(sync_word1, sync_word2, 1, 0, 3, False)
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
        self.digital_crc32_bb_1 = digital.crc32_bb(True, packet_len_key, True)
        self.digital_constellation_decoder_cb_0_0 = digital.constellation_decoder_cb(payload_modulation.base())
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(header_modulation.base())
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, packet_len_key)
        self.blocks_repack_bits_bb_2 = blocks.repack_bits_bb(payload_modulation.bits_per_symbol(), bits_per_byte, packet_len_key, False, gr.GR_LSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/berker/Desktop/ceng513/files/iq.txt', False)
        self.blocks_file_sink_1.set_unbuffered(True)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, fft_len + cp_len)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(-2.0/fft_len)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.digital_packet_headerparser_b_0, 'header_data'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_repack_bits_bb_2, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_packet_headerparser_b_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0_0, 0), (self.blocks_repack_bits_bb_2, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.fft_vxx_1, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.fft_vxx_1_0, 0))
        self.connect((self.digital_ofdm_chanest_vcvc_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0, 0), (self.digital_ofdm_serializer_vcc_0, 0))
        self.connect((self.digital_ofdm_frame_equalizer_vcvc_0_0, 0), (self.digital_ofdm_serializer_vcc_0_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_ofdm_serializer_vcc_0_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.digital_ofdm_serializer_vcc_0_0, 0), (self.digital_constellation_decoder_cb_0_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.digital_ofdm_sync_sc_cfb_0, 1), (self.digital_header_payload_demux_0, 1))
        self.connect((self.fft_vxx_1, 0), (self.digital_ofdm_chanest_vcvc_0, 0))
        self.connect((self.fft_vxx_1_0, 0), (self.digital_ofdm_frame_equalizer_vcvc_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.digital_ofdm_sync_sc_cfb_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ofdm_rx")
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
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

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

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain

    def get_cp_len(self):
        return self.cp_len

    def set_cp_len(self, cp_len):
        self.cp_len = cp_len
        self.blocks_delay_0.set_dly(self.fft_len + self.cp_len)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_center_freq(self.center_freq, 0)

    def get_bits_per_byte(self):
        return self.bits_per_byte

    def set_bits_per_byte(self, bits_per_byte):
        self.bits_per_byte = bits_per_byte
        self.blocks_repack_bits_bb_2.set_k_and_l(payload_modulation.bits_per_symbol(),self.bits_per_byte)



def main(top_block_cls=ofdm_rx, options=None):

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
