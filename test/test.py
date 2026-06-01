import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

@cocotb.test()
async def test_project(dut):
    # Standard Clock Setup
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # --- TEST MODE 0 ---
    dut._log.info("Testing Mode 0...")
    dut.ena.value = 1
    dut.ui_in.value = 0  # Mode 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    # Let it run for 30 cycles to ensure the feedback logic diverges
    await ClockCycles(dut.clk, 30)
    await FallingEdge(dut.clk) 
    val_a = int(dut.uo_out.value)

    # --- TEST MODE 1 ---
    dut._log.info("Testing Mode 1...")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    
    dut.ui_in.value = 1  # Mode 1
    
    # Let it run for the same 30 cycles
    await ClockCycles(dut.clk, 30)
    await FallingEdge(dut.clk)
    val_b = int(dut.uo_out.value)

    dut._log.info(f"Final Comparison -> Mode 0: {hex(val_a)}, Mode 1: {hex(val_b)}")
    
    # This should now pass because 30 cycles is plenty of time for chaos to happen
    assert val_a != val_b, f"Chaos Failure: Both modes resulted in {hex(val_a)} after 30 cycles"
