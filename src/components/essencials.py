from py65.memory import ObservableMemory
from utils import AddressManager, save_ram
from components import Component
from cpu import CPU
import pygame
import sys

class ACIA(Component):
    am = AddressManager()

    def __init__(self, address_range, memory:ObservableMemory , cpu:CPU):
        super().__init__(address_range, memory, cpu)
        pygame.init()
        pygame.font.init()

        self.buffer = [""]
        self.line_counter = 0
        self.input = 0

        self.size = (800, 600)

        self.width = self.size[0]
        self.height = self.size[1]

        self.background_color = (0, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('ubuntumono', 20)

        self.screen = pygame.display.set_mode(self.size)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_ram(self.memory, range(0x0000, 0xc000))
                    sys.exit()
                self.input = event.key

    @property
    def ascii_commands(self) -> dict:
        return {
            13: lambda: None,
            10: self.new_line,
            12: self.clean_buffer,
            8: self.backspace
        }

    def new_line(self):
        self.buffer.append('')
        self.line_counter += 1
        if self.line_counter > 19:
            self.line_counter = 19
            self.buffer.pop(0)

    def backspace(self):
        original = self.buffer[self.line_counter]
        self.buffer[self.line_counter] = original[:-1]

    def clean_buffer(self, value=None):
        self.buffer = ['']
        self.line_counter = 0

    def print_buffer(self):
        self.screen.fill(self.background_color)
        for index, line in enumerate(self.buffer):
            cursor = '_' if self.line_counter == index else ''
            textsurface = self.font.render(f' {line}{cursor}', True, self.text_color)
            self.screen.blit(textsurface,(0,index*30))
        pygame.display.update()

    @am.write_address(address=0xf001)
    def adds_to_buffer(self, value):
        print(value, chr(value))
        if value:
            if value in self.ascii_commands.keys():
                self.ascii_commands[value]()
            else:
                self.buffer[self.line_counter] += chr(value)
            self.print_buffer()
    
    @am.read_address(address=0xf004)
    def send_input(self):
        value = self.input
        if value in range(97, 123):
            value -= 32
        if value == 39:
            value = 34
        self.input = 0
        return value
    
    @am.write_address(address=0xf002)
    def change_background_color(self, value):
        red_mask = 0b00110000
        green_mask = 0b00001100
        blue_mask = 0b00000011

        red_value = (value & red_mask) * 5.3125
        green_value = (value & green_mask) * 21.25
        blue_value = (value & blue_mask) * 85

        self.background_color = (red_value, green_value, blue_value)
    
    @am.write_address(address=0xf003)
    def change_text_color(self, value):
        red_mask = 0b00110000
        green_mask = 0b00001100
        blue_mask = 0b00000011

        red_value = (value & red_mask) * 5.3125
        green_value = (value & green_mask) * 21.25
        blue_value = (value & blue_mask) * 85

        self.text_color = (red_value, green_value, blue_value)



class Drive(Component):
    am = AddressManager()

    def __init__(self, address_range, memory, cpu, folder_name="drive"):
        super().__init__(address_range, memory, cpu)
        self.file_name = ''
        self.file_data = []
        self.folder_name = folder_name

    @am.write_address(address=0xf011)
    def get_file_name(self, value):
        print("Parameter", value, chr(value))
        self.file_name += chr(value)
       
    @am.write_address(address=0xf012)
    def store_file_data(self, value):
        print("Program", value, chr(value))
        self.file_data.append(value)
    
    @am.read_address(address=0xf012)
    def get_file_data(self):
        try:
            return self.file_data.pop(0)
        except IndexError:
            return 0x00

    @am.write_address(address=0xf013)
    def get_drive_command(self, value):
        print("Command", value, chr(value))
        commands = {
            0x00: self.reset_drive,
            0x01: self.save_file,
            0x02: self.load_file
            }
        commands[value]()

    def reset_drive(self):
        print('reseting drive')
        self.file_name = ''
        self.file_data = []
    
    def save_file(self):
        print('saving file')
        with open(f'{self.folder_name}/{self.file_name}', 'wb') as f:
            f.write(bytearray(self.file_data))
    
    def load_file(self):
        print('saving file')
        with open(f'{self.folder_name}/{self.file_name}', 'rb') as f:
            for byte in f.read():
                self.file_data.append(int(byte))