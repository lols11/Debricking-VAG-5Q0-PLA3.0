# Debricking VAG 5Q0 PLA3.0
![License](https://img.shields.io/static/v1?label=license&message=CC-BY-NC-4.0&color=green)

This is a story about trying to debrick a PLA3.0 module



When I tried to flash the 5Q0 (MQB) module with the 7N0 (PQ) firmware, it gave me the silent treatment and left me with zero communication

![image](https://github.com/user-attachments/assets/e4c1b6f5-09e4-42e7-a3d9-83939899047b)

This repository describes the attempt to bring it back to life (still ongoing!).

## JTAG 
![jtag](https://github.com/user-attachments/assets/ec61c51c-9507-4ce5-855a-0019baa4c944)



**JTAG is fully unlocked**

I used the uLink-NT programmer to read the MCU, but the RESET pin from the programmer had to be disconnected (with it connected, there were some reading errors).
***The MCU must be powered directly.*** I achieved error-free memory readings at a voltage of 3.3V. Reading was unsuccessful when using a 12V VIN power supply or directly supplying 5V (the default operating voltage).

```
onCE JTAG ID 	0x07E2C01D
MCU ID    56A6   Version 0.1
SSCM STATUS    0870   NexusStatus = 1 
SSCM MEMCONFIG 8923   JPIN = 0x224
MCR C3F88000  Value= 03700600 
MCR C3F88000  Value= 03700600 
MCR C3F8C000  Value= 06670600 
Found Address= 00000000 Code Flash
Found Address= 00800000 Data Flash
```

## Watchdog

~~We probably don't have to worry about the watchdog as we power the MCU directly~~

MCU is powered via LDO Regulator (NCV4263-2C) with Watchdog. WD is reseted by rising edge from pin 10 of MCU, so it's need to be bypassed for JTAG access. 

According to the datasheet, to disable WD pin 5 (DelayTiming) needs to be lifted (NC). By unofficial method, WatchDog can also be disabled by pulling DelayTiming to VCC


[NCV4263-2C Datasheet](https://www.onsemi.com/download/data-sheet/pdf/ncv4263-2c-d.pdf)

## Overview 

- Module P/N: 5Q0 919 298 C, H08
- MCU used: SPC56AP60L3 (LQFP100, 1 MB Flash)
- [Datasheet](https://www.st.com/en/automotive-microcontrollers/spc56ap60l3.html)


## License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/lols11/Debricking-VAG-5Q0-PLA3.0">Debricking VAG 5Q0 PLA3.0</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/lols11">lols11</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""></a></p>




