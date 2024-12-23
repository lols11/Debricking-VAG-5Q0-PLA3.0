# Debricking VAG 5Q0 PLA3.0
![License](https://img.shields.io/static/v1?label=license&message=CC-BY-NC-4.0&color=green)

This is a story about trying to debrick a PLA3.0 module



When I tried to flash the 5Q0 (MQB) module with the 7N0 (PQ) firmware, it gave me the silent treatment and left me with zero communication

![image](https://github.com/user-attachments/assets/e4c1b6f5-09e4-42e7-a3d9-83939899047b)

This repository describes the attempt to bring it back to life (still ongoing!).

## JTAG Pinout
![jtag](https://github.com/user-attachments/assets/49b42cec-dd76-44a0-92d1-e65852e6f4d3)


## Watchdog

MCU is powered via LDO Regulator (NCV4263-2C) with Watchdog. WD is reseted by rising edge from pin 10 of MCU, so it's need to be bypassed for JTAG access. According to the datasheet, to disable WD pin 5 (DelayTiming) needs to be lifted (NC). (If you have a better idea, please contact me, as I don't have much experience in this type of thing)


[NCV4263-2C Datasheet](https://www.onsemi.com/download/data-sheet/pdf/ncv4263-2c-d.pdf)

## Overview 

- Module P/N: 5Q0 919 298 C, H08
- MCU used: SPC56AP60L3 (LQFP100, 1 MB Flash)
- [Datasheet](https://www.st.com/en/automotive-microcontrollers/spc56ap60l3.html)

The most important question right now is whether the JTAG interface is unlocked. I haven’t checked that yet.

## License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/lols11/Debricking-VAG-5Q0-PLA3.0">Debricking VAG 5Q0 PLA3.0</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/lols11">lols11</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""></a></p>




