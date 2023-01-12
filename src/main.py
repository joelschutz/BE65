from utils import load_ram, load_rom
from cpu import CPU
from memory import Memory
from components.essencials import ACIA, Drive

memory = Memory()
load_ram(memory=memory, ram_base=0x0000)
load_rom(memory=memory, file_name='basic.out', rom_base=0xc000)

cpu = CPU(memory=memory)
terminal = ACIA(address_range=range(0xf000, 0xf00a), memory=memory, cpu=cpu)
drive = Drive(address_range=range(0xf010, 0xf01a), memory=memory, cpu=cpu, folder_name='examples')

while True:
    cpu.step()
    terminal.update()
