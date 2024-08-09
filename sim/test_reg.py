# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray


@cocotb.test()
async def dff_simple_test(dut):
    """Test that d propagates to q"""

    # Set initial input value to prevent it from floating
    dut.d.value = 0
    dut.rst.value = 0

    clock = Clock(dut.clk, 10, units="us")  # Create a 10us period clock on port clk
    # Start the clock. Start it low to avoid issues on the first RisingEdge
    cocotb.start_soon(clock.start(start_high=False))

    # Synchronize with the clock. This will regisiter the initial `d` value
    await RisingEdge(dut.clk)
    expected_val = 0  # Matches initial input value
    for i in range(10):
        val = random.randint(0, 2**int(dut.SIZE.value) - 1)
        dut.d.value = val  # Assign the random value val to the input port d
        await RisingEdge(dut.clk)
        assert dut.q.value == expected_val, f"output q was incorrect on the {i}th cycle"
        expected_val = val  # Save random value for next RisingEdge

    # Check the final input on the next clock
    await RisingEdge(dut.clk)
    assert dut.q.value == expected_val, "output q was incorrect on the last cycle"


def test_simple_dff_runner():

    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [proj_path / "../src/reg.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="register",
        always=True,
    )

    runner.test(hdl_toplevel="register", test_module="test_reg,")


if __name__ == "__main__":
    test_simple_dff_runner()