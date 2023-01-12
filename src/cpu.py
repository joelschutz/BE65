from py65.devices.mpu6502 import MPU


class CPU(MPU):

    def reset(self):
        super().reset()
        self.pc = self.WordAt(self.RESET)
    
    def irq(self):
        # triggers a normal IRQ
        # this is very similar to the BRK instruction
        if self.p & self.INTERRUPT:
            return
        self.stPushWord(self.pc)
        self.p &= ~self.BREAK
        self.stPush(self.p | self.UNUSED)
        self.p |= self.INTERRUPT
        self.pc = self.WordAt(self.IRQ)
        self.processorCycles += 7

    def nmi(self):
        # triggers a NMI IRQ in the processor
        # this is very similar to the BRK instruction
        self.stPushWord(self.pc)
        self.p &= ~self.BREAK
        self.stPush(self.p | self.UNUSED)
        self.p |= self.INTERRUPT
        self.pc = self.WordAt(self.NMI)
        self.processorCycles += 7