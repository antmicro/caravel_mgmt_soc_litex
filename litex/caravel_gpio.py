from migen import *
from litex.soc.cores.gpio import GPIOTristate
from litex.soc.interconnect.csr_eventmanager import *
from migen.genlib.cdc import MultiReg


class GPIOASIC(GPIOTristate):
    def __init__(self, pads):
        assert isinstance(pads, Signal) or isinstance(pads, Record)
        nbits = len(pads) if isinstance(pads, Signal) else len(pads.out_pad)

        self._mode1  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._mode0  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._ien  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._oe  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._in  = CSRStatus(nbits,  description="GPIO Input(s) Status.")
        self._out = CSRStorage(nbits, description="GPIO Ouptut(s) Control.")

        # # #
        # Tristate inout IOs (For external tristate IO chips or simulation).
        for i in range(nbits):
            self.comb += pads.mode0_pad[i].eq(self._mode0.storage[i])
            self.comb += pads.mode1_pad[i].eq(self._mode1.storage[i])
            self.comb += pads.inenb_pad[i].eq(~self._ien.storage[i])
            self.comb += pads.outenb_pad[i].eq(~self._oe.storage[i])
            self.comb += pads.out_pad[i].eq(self._out.storage[i])
            self.specials += MultiReg(pads.in_pad[i], self._in.status[i])

class GPIOFPGA(GPIOTristate):
    def __init__(self, pads):
        assert isinstance(pads, Signal) or isinstance(pads, Record)
        nbits = len(pads) if isinstance(pads, Signal) else len(pads.out_pad)

        self._mode1  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._mode0  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._ien  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._oe  = CSRStorage(nbits, description="GPIO Tristate(s) Control.")
        self._in  = CSRStatus(nbits,  description="GPIO Input(s) Status.")
        self._out = CSRStorage(nbits, description="GPIO Ouptut(s) Control.")

        # TODO: handle mode1, mode0, ien

        # # #
        # Tristate inout IOs (For internal GPIO).
        if isinstance(pads, Record):
            pads = pads.flatten()
        # Proper inout IOs.
        for i in range(nbits):
            t = TSTriple()
            self.specials += t.get_tristate(pads[i])
            self.comb += t.oe.eq(self._oe.storage[i])
            self.comb += t.o.eq(self._out.storage[i])
            self.specials += MultiReg(t.i, self._in.status[i])


class LogicAnalyzer(GPIOTristate):
    def __init__(self, pads):
        assert isinstance(pads, Signal) or isinstance(pads, Record)
        nbits = len(pads) if isinstance(pads, Signal) else len(pads.output)

        self._ien  = CSRStorage(nbits, description="LA Input Enable")
        self._oe  = CSRStorage(nbits, description="LA Output Enable")
        self._in  = CSRStatus(nbits,  description="LA Input(s) Status.")
        self._out = CSRStorage(nbits, description="LA Ouptut(s) Control.")

        # # #
        # Tristate inout IOs (For external tristate IO chips or simulation).
        for i in range(nbits):
            self.comb += pads.iena[i].eq(~self._ien.storage[i])
            self.comb += pads.oenb[i].eq(~self._oe.storage[i])
            self.comb += pads.output[i].eq(self._out.storage[i])
            self.specials += MultiReg(pads.input[i], self._in.status[i])