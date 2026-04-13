#!/usr/bin/env python3
"""
AppChk v1 — application checksum tool for 7N0 PLA firmware (SPC56AP60L3).
<!--                                  -->
<!--    https://github.com/lols11/    -->
<!--              lols11              -->
<!--                                  -->
<!--  ███████████████████████████	  -->
<!--  ███████▀▀▀░░░░░░░▀▀▀███████     -->
<!--  ████▀░░░░░░░░░░░░░░░░░▀████     -->
<!--  ███│░░░░░░░░░░░░░░░░░░░│███     -->
<!--  ██▌│░░░░░░░░░░░░░░░░░░░│▐██     -->
<!--  ██░└┐░░░░░░░░░░░░░░░░░┌┘░██     -->
<!--  ██░░└┐░░░░░░░░░░░░░░░┌┘░░██     -->
<!--  ██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██     -->
<!--  ██▌░│██████▌░░░▐██████│░▐██     -->
<!--  ███░│▐███▀▀░░▄░░▀▀███▌│░███     -->
<!--  ██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██     -->
<!--  ██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██     -->
<!--  ████▄─┘██▌░░░░░░░▐██└─▄████     -->
<!--  █████░░▐█─┬┬┬┬┬┬┬─█▌░░█████     -->
<!--  ████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████     -->
<!--  █████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████     -->
<!--  ███████▄░░░░░░░░░░░▄███████     -->
<!--  ██████████▄▄▄▄▄▄▄██████████     -->
<!--  ███████████████████████████     -->
<!--                                  -->
<!--    https://github.com/lols11/    -->
<!--                                  -->	
<!--           THX PQISA              -->	

Usage:
    python3 appchk_compute.py <firmware.bin>
        [--base 0x00000000]
        [--start 0x00010000] [--end 0x000FFFF8]
        [--slot 0x000FFFF4]
        [-r]

Reproduces the algorithm implemented by AppChk_StepTick @ 0x000B3580:
  - 32-bit big-endian word-wise additive sum, modulo 2**32
  - region table @ 0x000E2214: count=1, start=0x00010000, end=0x000FFFF8
  - last summed word lives at 0x000FFFF4 (AppChk_StoredSum)
  - pass condition: running sum == 0xFFFFFFFF

<firmware.bin> must be a flat CFlash dump or unpacked ODX converted to raw bytes with correct regions set;
--base is the address of byte 0 in the file (default 0). --end is exclusive, matching the on-target formula
(end + 1 - ptr) >> 2 with end aligned to the last byte of the final word.
Use -r to automatically write the corrected checksum back to the file and verify.

"""

import argparse
import struct
import sys

REGION_START = 0x00010000
REGION_END   = 0x000FFFF8  # exclusive
SLOT_ADDR    = 0x000FFFF4  # AppChk_StoredSum
TARGET_SUM   = 0xFFFFFFFF
MASK32       = 0xFFFFFFFF


def load_window(path, base, start, end):
    with open(path, "rb") as f:
        blob = f.read()
    lo = start - base
    hi = end   - base
    if lo < 0 or hi > len(blob):
        sys.exit(f"range 0x{start:08X}..0x{end:08X} outside file "
                 f"(base=0x{base:08X}, size=0x{len(blob):X})")
    if (hi - lo) % 4:
        sys.exit(f"range length 0x{hi-lo:X} is not a multiple of 4")
    return blob[lo:hi]


def sum32_be(window):
    s = 0
    for (w,) in struct.iter_unpack(">I", window):
        s = (s + w) & MASK32
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("firmware")
    ap.add_argument("--base",  type=lambda x: int(x, 0), default=0x00000000)
    ap.add_argument("--start", type=lambda x: int(x, 0), default=REGION_START)
    ap.add_argument("--end",   type=lambda x: int(x, 0), default=REGION_END)
    ap.add_argument("--slot",  type=lambda x: int(x, 0), default=SLOT_ADDR)
    ap.add_argument("-r", "--repair", action="store_true", help="Write correct checksum to file and verify")
    args = ap.parse_args()

    window = load_window(args.firmware, args.base, args.start, args.end)
    total  = sum32_be(window)

    slot_off = args.slot - args.start
    stored,  = struct.unpack_from(">I", window, slot_off)

    # sum with the stored word excluded -> the "payload" sum
    payload = (total - stored) & MASK32
    # balancing word that would make payload + X == TARGET_SUM
    needed  = (TARGET_SUM - payload) & MASK32

    status = "PASS" if total == TARGET_SUM else "FAIL"
    print(f"--------------------------------------------------------")
    print(f"------------  Checksum tool for 7N0 PLA FW -------------")
    print(f"-------------  https://github.com/lols11  --------------")
    print(f"----------------------  by lols11  ---------------------")
    print(f"------------------  Thanks to PQISA  -------------------")
    print(f"-------------------  FREE FOR ALL!!  -------------------")
    print(f"--------------------------------------------------------")
    print(f"")
    print(f"region         : 0x{args.start:08X} .. 0x{args.end:08X} "
          f"({(args.end - args.start) // 4} words)")
    print(f"stored CS      : 0x{args.slot:08X} = 0x{stored:08X}")
    print(f"payload sum    : 0x{payload:08X}  (region sum excl. slot)")
    print(f"full sum       : 0x{total:08X}  (region sum incl. slot)")
    print(f"target         : 0x{TARGET_SUM:08X}")
    print(f"required CS    : 0x{needed:08X}")
    print(f"status         : {status}")

    if args.repair and status == "FAIL":
        print("\n--- Applying Fix ---")
        print(f"old CS         : 0x{stored:08X}")
        print(f"new CS         : 0x{needed:08X}")
        
        file_offset = args.slot - args.base
        with open(args.firmware, "r+b") as f:
            f.seek(file_offset)
            f.write(struct.pack(">I", needed))
        
        print("\n--- Verification Pass ---")
        window2 = load_window(args.firmware, args.base, args.start, args.end)
        total2 = sum32_be(window2)
        status2 = "PASS" if total2 == TARGET_SUM else "FAIL"
        
        print(f"full sum       : 0x{total2:08X}")
        print(f"status         : {status2}")
        
        return 0 if status2 == "PASS" else 1

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
