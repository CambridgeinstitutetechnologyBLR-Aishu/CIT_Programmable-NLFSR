import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 100 KHz clock
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
    
    # Wait for the first falling edge after reset to ensure stability
    await FallingEdge(dut.clk)

    # --- Mode 0 Capture ---
    dut._log.info("Testing Mode 0 (Function A)")
    dut.ui_in.value = 0 
    
    # We wait for 5 cycles. 
    # CRITICAL: Always read values on the FALLING edge in GL tests.
    # This gives the gates 1/2 clock cycle to settle.
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk) 
    state_a = int(dut.uo_out.value)

    # --- Reset for Mode 1 ---
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1
    await FallingEdge(dut.clk)

    # --- Mode 1 Capture ---
    dut._log.info("Testing Mode 1 (Function B)")
    dut.ui_in.value = 1 
    
    await ClockCycles(dut.clk, 5)
    await FallingEdge(dut.clk)
    state_b = int(dut.uo_out.value)

    dut._log.info(f"Mode 0 Result: {hex(state_a)}")
    dut._log.info(f"Mode 1 Result: {hex(state_b)}")
    
    # Comparison
    assert state_a != state_b, f"Error: Mode 0 and Mode 1 both produced {hex(state_a)}. Logic switch failed!"
    
    dut._log.info("SUCCESS: Programmable NLFSR Verified at Gate Level.")
