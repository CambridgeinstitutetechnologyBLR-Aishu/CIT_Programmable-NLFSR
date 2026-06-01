# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 1. Setup Clock (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # 2. Reset the NLFSR
    dut._log.info("Resetting NLFSR")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1) # Wait for reset to settle

    # 3. Test Mode 0 (Function A)
    dut._log.info("Testing Mode 0...")
    dut.ui_in.value = 0 
    
    # Grab the first output after reset (should be high byte of our seed 0xACE1)
    # 0xAC is 172 in decimal
    val_a = int(dut.uo_out.value)
    dut._log.info(f"Mode 0 initial output: {hex(val_a)}")
    
    # Let it run for a few cycles
    await ClockCycles(dut.clk, 5)
    state_a_later = int(dut.uo_out.value)

    # 4. Reset and Test Mode 1 (Function B / Chaotic)
    dut._log.info("Switching to Mode 1 (Chaotic)...")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 1)
    
    dut.ui_in.value = 1 # Enable the second non-linear function
    
    # Let it run for the same 5 cycles
    await ClockCycles(dut.clk, 5)
    state_b_later = int(dut.uo_out.value)

    # 5. Assertions
    # If the modes are different, the state after 5 cycles should not be the same
    dut._log.info(f"Mode 0 after 5 cycles: {hex(state_a_later)}")
    dut._log.info(f"Mode 1 after 5 cycles: {hex(state_b_later)}")
    
    assert state_a_later != state_b_later, "CRITICAL FAILURE: Both modes produced the same output!"
    dut._log.info("SUCCESS: Programmable logic verified.")
