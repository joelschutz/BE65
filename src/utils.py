
def save_ram(memory, memory_range):
    with open('ram.bin', 'wb') as f:
        byte_list = []
        for address in memory_range:
            byte_list.append(memory[address])
        
        f.write(bytearray(byte_list))

def load_ram(memory, ram_base):
    try:
        with open('ram.bin', 'rb') as f:
            memory.write(start_address=ram_base, bytes=f.read())
    except FileNotFoundError:
        pass

def load_rom(memory, file_name, rom_base):
    with open(file_name, 'rb') as f:
        memory.write(start_address=rom_base, bytes=f.read())

class AddressManager:
    def __init__(self):
        self.write_address_space = {}
        self.read_address_space = {}
    
    def write_address(self, address):
        def wrapper(func):
            self.write_address_space[address] = func
            return func
        return wrapper
    
    def read_address(self, address):
        def wrapper(func):
            self.read_address_space[address] = func
            return func
        return wrapper

