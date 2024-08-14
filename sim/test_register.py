# This file is public domain, it can be freely copied without restrictions.
# SPDX-License-Identifier: CC0-1.0

import os
import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.runner import get_runner
from cocotb.triggers import RisingEdge, NextTimeStep, Timer, ReadOnly
from cocotb.types import LogicArray

import debugpy


@cocotb.test()
async def register_simple_test(dut):
    """Test that loads the register with random data"""

    # Set initial input value to prevent it from floating
    dut.d.value = 0
    dut.rst.value = 0
    dut.load_en.value = 1

    clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for updated values

    for i in range(10):
        await NextTimeStep() # wait for the next timestep

        val = random.randint(0, 2**int(dut.SIZE.value) - 1)
        dut.d.value = val  # set random data
        load = random.randint(0, 1) # random load/keep
        dut.load_en.value = load

        dut._log.info("val=%d, load=%d", val, load)

        old_val = dut.q.value

        await RisingEdge(dut.clk)
        await ReadOnly()

        dut._log.info("q=%d", int(dut.q.value))

        assert dut.q.value == (val if load else old_val), f"output q was incorrect on the {i}th cycle"


@cocotb.test()
async def register_reset_test(dut):
    """Test that performs an async reset on the register"""

    # Set initial input value to prevent it from floating
    dut.d.value = 0
    dut.rst.value = 0
    dut.load_en.value = 1

    clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)

    val = random.randint(0, 2**int(dut.SIZE.value) - 1)
    dut.d.value = val  # set random data
    await RisingEdge(dut.clk)
    await NextTimeStep()
    assert dut.q.value == val, f"output q was not set correctly"
    
    delay_ns = random.randint(1,9)

    await Timer(delay_ns, "ns")
    dut.rst.value = 1 # set reset
    await NextTimeStep()
    assert dut.q.value == 0, f"output was not reset correctly: got {dut.q.value}, expected 0"


def test_simple_register_runner():

    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [proj_path / "../src/register.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="register",
        always=True,
        timescale=("1ns","1ps")
    )

    runner.test(hdl_toplevel="register", test_module="test_register,", timescale=("1ns","1ps"))


if __name__ == "__main__":
    test_simple_register_runner()