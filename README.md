# CENG513 - Wireless Communication and Networks

## Requirements
1. Installation of UHD 3.15.0: [Build Dependencies](https://kb.ettus.com/UHD#Build_Dependencies), [Binary Installation](https://files.ettus.com/manual/page_install.html) or [Installation from Source](https://files.ettus.com/manual/page_build_guide.html)
2. Installation of GNU Radio 3.8: [GNU Radio](https://wiki.gnuradio.org/index.php/InstallingGR), alternatively [PyBOMBS](https://github.com/gnuradio/pybombs#pybombs)

## How to run GNU Radio Companion (GRC) modules?
Run GNU Radio Companion through installed application or command line: 
```
gnuradio-companion
gnuradio-companion path/to/grc/file
```

If the GRC model is compiled, there are both grc and python files. GRC model can be run either from GNU Radio Companion application or by running the python3 code. Running the GRC models through command line is better as GRC UI freezes when the model prints to console.

In **audio_txrx** folder, there are GRC models for transmitting and receiving FM modulated sound with using USRPs.

In **file_txrx** folder: 
* ofdm_txrx.grc model contains OFMD Transmitter and Receiver desing which works without USRPs. It simply simulates a file transmission and reception, received bytes are written into a file. It can be run with ```python3 -u ofdm_txrx.py``` in the command shell if the GRC model is compiled.
* ofdm_tx.grc model contains OFDM Transmitter design.
* ofdm_rx.grc model contains OFDM Receiver design.
* usrp_ofdm_txrx.grc model contains OFDM Transmitter and Receiver design.