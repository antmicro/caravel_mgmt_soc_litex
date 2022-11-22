#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2020 Piotr Esden-Tempski <piotr@esden.net>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform
from litex.build.openocd import OpenOCD


# IOs ----------------------------------------------------------------------------------------------
_io = [
    ("core_clk", 0, Pins("E3"), IOStandard("LVCMOS33")),
    # ("core_rst", 0, Pins(1)),
    ("core_rstn", 0, Pins("C2"), IOStandard("LVCMOS33")),

    # # pass-thru pins for clock and reset
    # # TODO: user project
    # ("clk_in", 0, Pins(1)),
    # ("clk_out", 0, Pins(1)),
    # ("resetn_in", 0, Pins(1)),
    # ("resetn_out", 0, Pins(1)),

    # # TODO: buffered signals
    # ("serial_load_in", 0, Pins(1)),
    # ("serial_load_out", 0, Pins(1)),
    # ("serial_data_2_in", 0, Pins(1)),
    # ("serial_data_2_out", 0, Pins(1)),
    # ("serial_resetn_in", 0, Pins(1)),
    # ("serial_resetn_out", 0, Pins(1)),
    # ("serial_clock_in", 0, Pins(1)),
    # ("serial_clock_out", 0, Pins(1)),
    # ("rstb_l_in", 0, Pins(1)),
    # ("rstb_l_out", 0, Pins(1)),
    # ("por_l_in", 0, Pins(1)),
    # ("por_l_out", 0, Pins(1)),
    # ("porb_h_in", 0, Pins(1)),
    # ("porb_h_out", 0, Pins(1)),

    # GPIO mgmt
    ("gpio", 0, Pins("N15"), IOStandard("LVCMOS33")), #io_8

    # # Logic analyzer
    # # TODO: user project
    # ("la", 0,
    #  Subsignal("output", Pins(128)),
    #  Subsignal("input", Pins(128)),
    #  Subsignal("oenb", Pins(128)),
    #  Subsignal("iena", Pins(128)),
    #  ),

    # Flash memory controller (SPI master)
    ("flash", 0,
     Subsignal("cs_n", Pins("L13")),
     Subsignal("clk",  Pins("L16")),
     Subsignal("dq",   Pins("K17 K18 L14 M14")),
     IOStandard("LVCMOS33")
     ),

    # # Exported wishbone bus
    # # TODO: user project
    # ("mprj", 0,
    #  Subsignal("wb_iena", Pins(1)),  # enable for the user wishbone return signals
    #  Subsignal("cyc_o", Pins(1)),
    #  Subsignal("stb_o", Pins(1)),
    #  Subsignal("we_o", Pins(1)),
    #  Subsignal("sel_o", Pins(4)),
    #  Subsignal("adr_o", Pins(32)),
    #  Subsignal("dat_o", Pins(32)),
    #  Subsignal("dat_i", Pins(32)),
    #  Subsignal("ack_i", Pins(1)),
    #  ),

    # # Housekeeping
    # # TODO: housekeeping
    # ("hk", 0,
    #  Subsignal("dat_i", Pins(32)),
    #  Subsignal("stb_o", Pins(1)),
    #  Subsignal("cyc_o", Pins(1)),
    #  Subsignal("ack_i", Pins(1)),
    #  ),

    # # IRQ
    # # TODO: user project
    # ("user_irq", 0, Pins(6)),
    # ("user_irq_ena", 0, Pins(3)),

    # Module status
    # TODO: housekeeping
    #("qspi_enabled", 0, Pins(1)),
    ("uart_enabled", 0, Pins("G6"), IOStandard("LVCMOS33")), #LD0 r
    ("spi_enabled", 0, Pins("F6"), IOStandard("LVCMOS33")), #LD0 g
    ("debug_mode", 0, Pins("E1"), IOStandard("LVCMOS33")), #LD0 b

    # Serial UART
    # muxed output between system and debug uarts
    ("serial", 0,
     Subsignal("tx", Pins("D10")),
     Subsignal("rx", Pins("A9")),
     IOStandard("LVCMOS33")
     ),

    # Debug interface -- only debug_in is used
    # TODO: housekeeping
    ("debug", 0,
     Subsignal("in", Pins("A8")), #SW0
     #Subsignal("out", None),
     Subsignal("oeb", Pins("T10")), #LD7
     IOStandard("LVCMOS33")
     ),

    # SPI master Controller
    ("spi", 0,
        Subsignal("clk",  Pins("F1")),
        Subsignal("cs_n", Pins("C1")),
        Subsignal("mosi", Pins("H1")),
        Subsignal("miso", Pins("G1")),
        IOStandard("LVCMOS33"),
        #Subsignal("sdoenb", Pins(1)),
    ),

    # SRAM read-only access from housekeeping
    # ("sram_ro", 0,
    #  Subsignal("clk", Pins(1)),
    #  Subsignal("csb", Pins(1)),
    #  Subsignal("addr", Pins(8)),
    #  Subsignal("data", Pins(32)),
    #  ),

    ("trap", 0, Pins("J5"), IOStandard("LVCMOS33")), #LD5

    # Memory Interface
    # ("mem", 0,
    #  Subsignal("ena", Pins(1)),
    #  Subsignal("wen", Pins(4)),
    #  Subsignal("addr", Pins(8)),
    #  Subsignal("wdata", Pins(32)),
    #  Subsignal("rdata", Pins(32)),
    #  ),
    # ("mgmt_soc_dff", 0,
    #  Subsignal("EN", Pins(1)),
    #  Subsignal("WE", Pins(4)),
    #  Subsignal("A", Pins(8)),
    #  Subsignal("Di", Pins(32)),
    #  Subsignal("Do", Pins(32)),
    #  ),
]


# Platform -----------------------------------------------------------------------------------------

class ArtyPlatform(XilinxPlatform):
    default_clk_name   = "clk100"
    default_clk_period = 1e9/100e6

    def __init__(self, vname="", variant="a7-35", toolchain="vivado"):
        device = {
            "a7-35":  "xc7a35ticsg324-1L",
            "a7-100": "xc7a100tcsg324-1"
        }[variant]
        XilinxPlatform.__init__(self, device, _io, toolchain=toolchain)
        self.toolchain.bitstream_commands = \
            ["set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]"]
        self.toolchain.additional_commands = \
            ["write_cfgmem -force -format bin -interface spix4 -size 16 "
             "-loadbit \"up 0x0 {build_name}.bit\" -file {build_name}.bin"]
        self.add_platform_command("set_property INTERNAL_VREF 0.675 [get_iobanks 34]")

    def create_programmer(self):
        bscan_spi = "bscan_spi_xc7a100t.bit" if "xc7a100t" in self.device else "bscan_spi_xc7a35t.bit"
        return OpenOCD("openocd_xc7_ft2232.cfg", bscan_spi)

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/100e6)
