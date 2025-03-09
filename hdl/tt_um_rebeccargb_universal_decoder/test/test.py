# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    async def test_ubcd(rbi, bi, lt, al, version, extras, value, data, rbo):
        dut.uio_in.value = extras | (lt << 3) | (bi << 4) | (al << 5)
        dut.ui_in.value = value | (version << 4) | (rbi << 7)
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == data | (rbo << 7)

    # BCD RCA/blanking version
    await test_ubcd(1, 1, 1, 1, 0, 0, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0, 14, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0, 13, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0, 12, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0, 11, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0, 10, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  9, 0x67, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  7, 0x07, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  6, 0x7C, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 0, 0,  0, 0x3F, 1)

    # BCD TI version
    await test_ubcd(1, 1, 1, 1, 1, 1, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1, 14, 0x78, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1, 13, 0x69, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1, 12, 0x62, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1, 11, 0x4C, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1, 10, 0x58, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  9, 0x67, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  7, 0x07, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  6, 0x7D, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 1, 1,  0, 0x3F, 1)

    # BCD NatSemi version
    await test_ubcd(1, 1, 1, 1, 2, 2, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2, 14, 0x08, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2, 13, 0x40, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2, 12, 0x01, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2, 11, 0x63, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2, 10, 0x5C, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  9, 0x67, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  7, 0x27, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  6, 0x7C, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 2, 2,  0, 0x3F, 1)

    # BCD Toshiba version
    await test_ubcd(1, 1, 1, 1, 3, 3, 15, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3, 14, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3, 13, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3, 12, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3, 11, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3, 10, 0x3F, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  9, 0x67, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  7, 0x27, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  6, 0x7D, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 3, 3,  0, 0x3F, 1)

    # BCD lines version
    await test_ubcd(1, 1, 1, 1, 4, 4, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4, 14, 0x01, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4, 13, 0x41, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4, 12, 0x49, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4, 11, 0x48, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4, 10, 0x08, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  9, 0x6F, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  7, 0x07, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  6, 0x7C, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 4, 4,  0, 0x3F, 1)

    # BCD Electronika version
    await test_ubcd(1, 1, 1, 1, 5, 5, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5, 14, 0x79, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5, 13, 0x31, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5, 12, 0x39, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5, 11, 0x38, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5, 10, 0x40, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  9, 0x6F, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  7, 0x07, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  6, 0x7D, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 5, 5,  0, 0x3F, 1)

    # BCD Code B version
    await test_ubcd(1, 1, 1, 1, 6, 6, 15, 0x00, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6, 14, 0x73, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6, 13, 0x38, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6, 12, 0x76, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6, 11, 0x79, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6, 10, 0x40, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  9, 0x6F, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  7, 0x27, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  6, 0x7C, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 6, 6,  0, 0x3F, 1)

    # BCD hexadecimal version
    await test_ubcd(1, 1, 1, 1, 7, 7, 15, 0x71, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7, 14, 0x79, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7, 13, 0x5E, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7, 12, 0x39, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7, 11, 0x7C, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7, 10, 0x77, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  9, 0x6F, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  8, 0x7F, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  7, 0x27, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  6, 0x7D, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  5, 0x6D, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  4, 0x66, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  3, 0x4F, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  2, 0x5B, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  1, 0x06, 1)
    await test_ubcd(1, 1, 1, 1, 7, 7,  0, 0x3F, 1)

    # BCD ripple blanking input
    await test_ubcd(0, 1, 1, 1, 7, 7, 15, 0x71, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7, 14, 0x79, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7, 13, 0x5E, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7, 12, 0x39, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7, 11, 0x7C, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7, 10, 0x77, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  9, 0x6F, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  8, 0x7F, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  7, 0x27, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  6, 0x7D, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  5, 0x6D, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  4, 0x66, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  3, 0x4F, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  2, 0x5B, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  1, 0x06, 1)
    await test_ubcd(0, 1, 1, 1, 7, 7,  0, 0x00, 0)

    # BCD RBI, BI, LT, AL lines
    await test_ubcd(1, 1, 1, 1, 7, 7, 1, 0x06, 1)
    await test_ubcd(1, 1, 0, 1, 7, 7, 1, 0x7F, 1)
    await test_ubcd(1, 1, 0, 0, 7, 7, 1, 0x00, 1)
    await test_ubcd(1, 0, 0, 0, 7, 7, 1, 0x7F, 0)

    # BCD RBI, BI, LT, AL lines
    await test_ubcd(0, 1, 1, 1, 7, 7, 1, 0x06, 1)
    await test_ubcd(0, 1, 0, 1, 7, 7, 1, 0x7F, 1)
    await test_ubcd(0, 1, 0, 0, 7, 7, 1, 0x00, 1)
    await test_ubcd(0, 0, 0, 0, 7, 7, 1, 0x7F, 0)

    async def test_ascii(bi, al, lc, fs, extras, value, data, ltr):
        dut.uio_in.value = extras | (fs << 3) | (bi << 4) | (al << 5) | (1 << 6)
        dut.ui_in.value = value | (lc << 7)
        await ClockCycles(dut.clk, 1)
        assert dut.uo_out.value == data | (ltr << 7)

    # ASCII font 0
    await test_ascii(1, 1, 1, 0, 7, 0x20, 0x00, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x21, 0x0A, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x22, 0x22, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x23, 0x36, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x24, 0x2D, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x25, 0x24, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x26, 0x78, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x27, 0x42, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x28, 0x39, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x29, 0x0F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2A, 0x63, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2B, 0x46, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2C, 0x0C, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2D, 0x40, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2E, 0x08, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x2F, 0x52, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x30, 0x3F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x31, 0x06, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x32, 0x5B, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x33, 0x4F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x34, 0x66, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x35, 0x6D, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x36, 0x7D, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x37, 0x27, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x38, 0x7F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x39, 0x6F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3A, 0x09, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3B, 0x0D, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3C, 0x46, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3D, 0x48, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3E, 0x70, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x3F, 0x53, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x40, 0x7B, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x41, 0x77, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x42, 0x7C, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x43, 0x39, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x44, 0x5E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x45, 0x79, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x46, 0x71, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x47, 0x3D, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x48, 0x76, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x49, 0x06, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4A, 0x1E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4B, 0x75, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4C, 0x38, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4D, 0x2B, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4E, 0x37, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x4F, 0x3F, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x50, 0x73, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x51, 0x67, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x52, 0x31, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x53, 0x6D, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x54, 0x07, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x55, 0x3E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x56, 0x6A, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x57, 0x7E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x58, 0x49, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x59, 0x6E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x5A, 0x5B, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x5B, 0x39, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x5C, 0x64, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x5D, 0x0F, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x5E, 0x23, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x5F, 0x08, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x60, 0x60, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x61, 0x5F, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x62, 0x7C, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x63, 0x58, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x64, 0x5E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x65, 0x7B, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x66, 0x71, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x67, 0x6F, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x68, 0x74, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x69, 0x05, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6A, 0x0E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6B, 0x75, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6C, 0x06, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6D, 0x55, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6E, 0x54, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x6F, 0x5C, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x70, 0x73, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x71, 0x67, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x72, 0x50, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x73, 0x6D, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x74, 0x78, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x75, 0x1C, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x76, 0x1D, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x77, 0x7E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x78, 0x48, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x79, 0x6E, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x7A, 0x5B, 0)
    await test_ascii(1, 1, 1, 0, 7, 0x7B, 0x46, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x7C, 0x30, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x7D, 0x70, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x7E, 0x01, 1)
    await test_ascii(1, 1, 1, 0, 7, 0x7F, 0x00, 1)

    # ASCII font 1
    await test_ascii(1, 1, 1, 1, 0, 0x20, 0x00, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x21, 0x0A, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x22, 0x22, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x23, 0x36, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x24, 0x12, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x25, 0x24, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x26, 0x78, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x27, 0x42, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x28, 0x58, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x29, 0x4C, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2A, 0x63, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2B, 0x46, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2C, 0x0C, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2D, 0x40, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2E, 0x10, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x2F, 0x52, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x30, 0x3F, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x31, 0x06, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x32, 0x5B, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x33, 0x4F, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x34, 0x66, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x35, 0x6D, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x36, 0x7C, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x37, 0x07, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x38, 0x7F, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x39, 0x67, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3A, 0x09, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3B, 0x0D, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3C, 0x61, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3D, 0x41, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3E, 0x43, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x3F, 0x53, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x40, 0x7B, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x41, 0x77, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x42, 0x7C, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x43, 0x39, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x44, 0x5E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x45, 0x79, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x46, 0x71, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x47, 0x3D, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x48, 0x76, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x49, 0x05, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4A, 0x1E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4B, 0x75, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4C, 0x38, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4D, 0x2B, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4E, 0x37, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x4F, 0x6B, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x50, 0x73, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x51, 0x67, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x52, 0x31, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x53, 0x2D, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x54, 0x07, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x55, 0x3E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x56, 0x6A, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x57, 0x7E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x58, 0x49, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x59, 0x6E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x5A, 0x1B, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x5B, 0x59, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x5C, 0x64, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x5D, 0x4D, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x5E, 0x23, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x5F, 0x08, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x60, 0x60, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x61, 0x44, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x62, 0x7C, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x63, 0x58, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x64, 0x5E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x65, 0x18, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x66, 0x33, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x67, 0x2F, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x68, 0x74, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x69, 0x05, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6A, 0x0E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6B, 0x75, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6C, 0x3C, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6D, 0x55, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6E, 0x54, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x6F, 0x5C, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x70, 0x73, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x71, 0x67, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x72, 0x50, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x73, 0x2D, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x74, 0x70, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x75, 0x1C, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x76, 0x1D, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x77, 0x7E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x78, 0x48, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x79, 0x6E, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x7A, 0x1B, 0)
    await test_ascii(1, 1, 1, 1, 0, 0x7B, 0x69, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x7C, 0x30, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x7D, 0x4B, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x7E, 0x01, 1)
    await test_ascii(1, 1, 1, 1, 0, 0x7F, 0x00, 1)

    # ASCII font 0, uppercase only
    await test_ascii(1, 1, 0, 0, 7, 0x20, 0x00, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x21, 0x0A, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x22, 0x22, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x23, 0x36, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x24, 0x2D, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x25, 0x24, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x26, 0x78, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x27, 0x42, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x28, 0x39, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x29, 0x0F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2A, 0x63, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2B, 0x46, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2C, 0x0C, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2D, 0x40, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2E, 0x08, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x2F, 0x52, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x30, 0x3F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x31, 0x06, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x32, 0x5B, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x33, 0x4F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x34, 0x66, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x35, 0x6D, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x36, 0x7D, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x37, 0x27, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x38, 0x7F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x39, 0x6F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3A, 0x09, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3B, 0x0D, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3C, 0x46, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3D, 0x48, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3E, 0x70, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x3F, 0x53, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x40, 0x7B, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x41, 0x77, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x42, 0x7C, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x43, 0x39, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x44, 0x5E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x45, 0x79, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x46, 0x71, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x47, 0x3D, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x48, 0x76, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x49, 0x06, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4A, 0x1E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4B, 0x75, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4C, 0x38, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4D, 0x2B, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4E, 0x37, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x4F, 0x3F, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x50, 0x73, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x51, 0x67, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x52, 0x31, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x53, 0x6D, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x54, 0x07, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x55, 0x3E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x56, 0x6A, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x57, 0x7E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x58, 0x49, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x59, 0x6E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x5A, 0x5B, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x5B, 0x39, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x5C, 0x64, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x5D, 0x0F, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x5E, 0x23, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x5F, 0x08, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x60, 0x60, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x61, 0x77, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x62, 0x7C, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x63, 0x39, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x64, 0x5E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x65, 0x79, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x66, 0x71, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x67, 0x3D, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x68, 0x76, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x69, 0x06, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6A, 0x1E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6B, 0x75, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6C, 0x38, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6D, 0x2B, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6E, 0x37, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x6F, 0x3F, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x70, 0x73, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x71, 0x67, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x72, 0x31, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x73, 0x6D, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x74, 0x07, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x75, 0x3E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x76, 0x6A, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x77, 0x7E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x78, 0x49, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x79, 0x6E, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x7A, 0x5B, 0)
    await test_ascii(1, 1, 0, 0, 7, 0x7B, 0x46, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x7C, 0x30, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x7D, 0x70, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x7E, 0x01, 1)
    await test_ascii(1, 1, 0, 0, 7, 0x7F, 0x00, 1)

    # ASCII font 1, uppercase only
    await test_ascii(1, 1, 0, 1, 0, 0x20, 0x00, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x21, 0x0A, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x22, 0x22, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x23, 0x36, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x24, 0x12, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x25, 0x24, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x26, 0x78, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x27, 0x42, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x28, 0x58, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x29, 0x4C, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2A, 0x63, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2B, 0x46, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2C, 0x0C, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2D, 0x40, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2E, 0x10, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x2F, 0x52, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x30, 0x3F, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x31, 0x06, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x32, 0x5B, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x33, 0x4F, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x34, 0x66, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x35, 0x6D, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x36, 0x7C, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x37, 0x07, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x38, 0x7F, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x39, 0x67, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3A, 0x09, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3B, 0x0D, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3C, 0x61, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3D, 0x41, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3E, 0x43, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x3F, 0x53, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x40, 0x7B, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x41, 0x77, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x42, 0x7C, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x43, 0x39, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x44, 0x5E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x45, 0x79, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x46, 0x71, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x47, 0x3D, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x48, 0x76, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x49, 0x05, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4A, 0x1E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4B, 0x75, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4C, 0x38, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4D, 0x2B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4E, 0x37, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x4F, 0x6B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x50, 0x73, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x51, 0x67, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x52, 0x31, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x53, 0x2D, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x54, 0x07, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x55, 0x3E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x56, 0x6A, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x57, 0x7E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x58, 0x49, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x59, 0x6E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x5A, 0x1B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x5B, 0x59, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x5C, 0x64, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x5D, 0x4D, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x5E, 0x23, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x5F, 0x08, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x60, 0x60, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x61, 0x77, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x62, 0x7C, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x63, 0x39, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x64, 0x5E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x65, 0x79, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x66, 0x71, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x67, 0x3D, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x68, 0x76, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x69, 0x05, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6A, 0x1E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6B, 0x75, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6C, 0x38, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6D, 0x2B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6E, 0x37, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x6F, 0x6B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x70, 0x73, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x71, 0x67, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x72, 0x31, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x73, 0x2D, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x74, 0x07, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x75, 0x3E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x76, 0x6A, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x77, 0x7E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x78, 0x49, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x79, 0x6E, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x7A, 0x1B, 0)
    await test_ascii(1, 1, 0, 1, 0, 0x7B, 0x69, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x7C, 0x30, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x7D, 0x4B, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x7E, 0x01, 1)
    await test_ascii(1, 1, 0, 1, 0, 0x7F, 0x00, 1)

    # ASCII BI and AL lines
    await test_ascii(1, 1, 1, 1, 1, 0x31, 0x06, 1)
    await test_ascii(1, 0, 1, 1, 1, 0x31, 0x79, 1)
    await test_ascii(0, 0, 1, 1, 1, 0x31, 0x7F, 1)
    await test_ascii(0, 1, 1, 1, 1, 0x31, 0x00, 1)

    async def test_cistercian(bi, al, lt1, lt2, value1, value2, u1, v1, w1, x1, y1, u2, v2, w2, x2, y2):
        dut.uio_in.value = (lt1 << 2) | (lt2 << 3) | (bi << 4) | (al << 5) | (1 << 7)
        dut.ui_in.value = value1 | (value2 << 4)
        await ClockCycles(dut.clk, 1)
        assert dut.uio_out.value == y1 | (y2 << 1)
        assert dut.uo_out.value == u1 | (u2 << 1) | (v1 << 2) | (v2 << 3) | (w1 << 4) | (w2 << 5) | (x1 << 6) | (x2 << 7)

    # Cistercian
    await test_cistercian(1, 1, 1, 1,  0, 15, 0,0,0,0,0, 0,1,1,1,1)
    await test_cistercian(1, 1, 1, 1,  1, 14, 1,0,0,0,0, 1,0,1,1,1)
    await test_cistercian(1, 1, 1, 1,  2, 13, 0,1,0,0,0, 1,1,0,1,1)
    await test_cistercian(1, 1, 1, 1,  3, 12, 0,0,1,0,0, 1,1,1,0,1)
    await test_cistercian(1, 1, 1, 1,  4, 11, 0,0,0,1,0, 1,0,0,1,1)
    await test_cistercian(1, 1, 1, 1,  5, 10, 1,0,0,1,0, 1,1,1,1,0)
    await test_cistercian(1, 1, 1, 1,  6,  9, 0,0,0,0,1, 1,1,0,0,1)
    await test_cistercian(1, 1, 1, 1,  7,  8, 1,0,0,0,1, 0,1,0,0,1)
    await test_cistercian(1, 1, 1, 1,  8,  7, 0,1,0,0,1, 1,0,0,0,1)
    await test_cistercian(1, 1, 1, 1,  9,  6, 1,1,0,0,1, 0,0,0,0,1)
    await test_cistercian(1, 1, 1, 1, 10,  5, 1,1,1,1,0, 1,0,0,1,0)
    await test_cistercian(1, 1, 1, 1, 11,  4, 1,0,0,1,1, 0,0,0,1,0)
    await test_cistercian(1, 1, 1, 1, 12,  3, 1,1,1,0,1, 0,0,1,0,0)
    await test_cistercian(1, 1, 1, 1, 13,  2, 1,1,0,1,1, 0,1,0,0,0)
    await test_cistercian(1, 1, 1, 1, 14,  1, 1,0,1,1,1, 1,0,0,0,0)
    await test_cistercian(1, 1, 1, 1, 15,  0, 0,1,1,1,1, 0,0,0,0,0)

    # Cistercian AL, BI, LT lines
    await test_cistercian(1, 1, 0, 1, 7, 7, 1,1,1,1,1, 1,0,0,0,1)
    await test_cistercian(1, 1, 1, 0, 7, 7, 1,0,0,0,1, 1,1,1,1,1)
    await test_cistercian(1, 1, 0, 0, 7, 7, 1,1,1,1,1, 1,1,1,1,1)
    await test_cistercian(1, 0, 0, 0, 7, 7, 0,0,0,0,0, 0,0,0,0,0)
    await test_cistercian(0, 0, 0, 0, 7, 7, 1,1,1,1,1, 1,1,1,1,1)

    async def test_kaktovik(rbi, bi, lt, al, vbi, value, data, rbo, v):
        dut.uio_in.value = (lt << 3) | (bi << 4) | (al << 5) | (3 << 6)
        dut.ui_in.value = value | (vbi << 6) | (rbi << 7)
        await ClockCycles(dut.clk, 1)
        assert dut.uio_out.value == (data >> 7) | (v << 1)
        assert dut.uo_out.value == (data & 0x7F) | (rbo << 7)

    # Kaktovik
    await test_kaktovik(1, 1, 1, 1, 1,  0, 0b00000100, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  1, 0b00000001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  2, 0b00000111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  3, 0b00001111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  4, 0b00011111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  5, 0b00100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  6, 0b00100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  7, 0b00100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  8, 0b00101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1,  9, 0b00111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 10, 0b01100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 11, 0b01100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 12, 0b01100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 13, 0b01101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 14, 0b01111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 15, 0b11100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 16, 0b11100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 17, 0b11100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 18, 0b11101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 19, 0b11111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 20, 0b11000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 21, 0b11000001, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 22, 0b11000111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 23, 0b11001111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 24, 0b11011111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 25, 0b10100000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 26, 0b10100001, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 27, 0b10100111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 28, 0b10101111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 29, 0b10111111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 30, 0b11111111, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 1, 31, 0b00000000, 1, 1)

    # Kaktovik ripple blanking input
    await test_kaktovik(0, 1, 1, 1, 1,  0, 0b00000000, 0, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  1, 0b00000001, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  2, 0b00000111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  3, 0b00001111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  4, 0b00011111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  5, 0b00100000, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  6, 0b00100001, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  7, 0b00100111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  8, 0b00101111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1,  9, 0b00111111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 10, 0b01100000, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 11, 0b01100001, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 12, 0b01100111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 13, 0b01101111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 14, 0b01111111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 15, 0b11100000, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 16, 0b11100001, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 17, 0b11100111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 18, 0b11101111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 19, 0b11111111, 1, 0)
    await test_kaktovik(0, 1, 1, 1, 1, 20, 0b11000000, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 21, 0b11000001, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 22, 0b11000111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 23, 0b11001111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 24, 0b11011111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 25, 0b10100000, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 26, 0b10100001, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 27, 0b10100111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 28, 0b10101111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 29, 0b10111111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 30, 0b11111111, 1, 1)
    await test_kaktovik(0, 1, 1, 1, 1, 31, 0b00000000, 1, 1)

    # Kaktovik overflow blanking input
    await test_kaktovik(1, 1, 1, 1, 0,  0, 0b00000100, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  1, 0b00000001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  2, 0b00000111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  3, 0b00001111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  4, 0b00011111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  5, 0b00100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  6, 0b00100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  7, 0b00100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  8, 0b00101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0,  9, 0b00111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 10, 0b01100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 11, 0b01100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 12, 0b01100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 13, 0b01101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 14, 0b01111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 15, 0b11100000, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 16, 0b11100001, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 17, 0b11100111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 18, 0b11101111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 19, 0b11111111, 1, 0)
    await test_kaktovik(1, 1, 1, 1, 0, 20, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 21, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 22, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 23, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 24, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 25, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 26, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 27, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 28, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 29, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 30, 0b00000000, 1, 1)
    await test_kaktovik(1, 1, 1, 1, 0, 31, 0b00000000, 1, 1)

    # Kaktovik RBI, BI, LT, AT lines
    await test_kaktovik(0, 1, 1, 1, 1, 17, 0b11100111, 1, 0)
    await test_kaktovik(0, 1, 0, 1, 1, 17, 0b11111111, 1, 0)
    await test_kaktovik(0, 1, 0, 0, 1, 17, 0b00000000, 1, 0)
    await test_kaktovik(0, 0, 0, 0, 1, 17, 0b11111111, 0, 0)
    await test_kaktovik(1, 1, 1, 1, 1, 17, 0b11100111, 1, 0)
    await test_kaktovik(1, 1, 0, 1, 1, 17, 0b11111111, 1, 0)
    await test_kaktovik(1, 1, 0, 0, 1, 17, 0b00000000, 1, 0)
    await test_kaktovik(1, 0, 0, 0, 1, 17, 0b11111111, 0, 0)
