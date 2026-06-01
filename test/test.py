import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Resetting...")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    # GL TEST FIX: Wait a few extra nanoseconds for the gates to settle
    await Timer(100, units="ns") 
    await ClockCycles(dut.clk, 1)

    dut._log.info("Testing Mode 0")
    dut.ui_in.value = 0 
    await ClockCycles(dut.clk, 5)
    state_a = int(dut.uo_out.value)

    # Reset for Mode 1
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await Timer(100, units="ns") # Settlement delay
    await ClockCycles(dut.clk, 1)
    
    dut._log.info("Testing Mode 1")
    dut.ui_in.value = 1 # Switch feedback function
    await ClockCycles(dut.clk, 5)
    state_b = int(dut.uo_out.value)

    dut._log.info(f"Mode 0: {hex(state_a)} | Mode 1: {hex(state_b)}")
    
    # Check that they are different
    assert state_a != state_b, f"Redundant outputs detected: {hex(state_a)}"
    dut._log.info("SUCCESS: Chaos confirmed!")
