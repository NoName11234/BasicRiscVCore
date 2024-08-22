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
async def counter_preload_test(dut):
    """Tests counter preload"""

    # Set initial input value to prevent it from floating
    dut.d.value = 130
    dut.rst.value = 0
    dut.load_en.value = 1

    clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for updated values

    assert dut.q.value == 130, "preset failed"


@cocotb.test()
async def counter_increment_test(dut):
    """
    Tests the counter increment
    """
    dut.d.value = 0
    dut.rst.value = 0
    dut.load_en.value = 1
    dut.count_en.value = 0
    
    clock = Clock(dut.clk, 10, units="ns")  # Create a 10us period clock on port clk
    cocotb.start_soon(clock.start(start_high=False))

    # preset counter to 0
    await RisingEdge(dut.clk)
    
    #increment counter
    dut.load_en.value = 0
    dut.count_en.value = 1
    await RisingEdge(dut.clk)
    await ReadOnly()

    assert dut.q.value == 1, "increment failed. Expected 1"


@cocotb.test()
async def counter_reset_test(dut):
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


def test_simple_counter_runner():

    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent
    verilog_sources = [proj_path / "../src/counter.sv"]

    runner = get_runner(sim)
    runner.build(
        verilog_sources=verilog_sources,
        hdl_toplevel="counter",
        always=True,
        timescale=("1ns","1ps")
    )

    runner.test(hdl_toplevel="counter", test_module="test_counter,", timescale=("1ns","1ps"))


if __name__ == "__main__":
    test_simple_counter_runner()