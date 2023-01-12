from abc import ABCMeta, abstractproperty
from py65.memory import ObservableMemory
import csv

class Component:
    __metaclass__ = ABCMeta
    class_property = None

    @abstractproperty
    def name(self):
       return self.__class__.__name__

    def __init__(self, address_range, memory: ObservableMemory, cpu):
        self.addresses = address_range
        self.memory = memory
        self.cpu = cpu
        self.memory.subscribe_to_write(self.addresses, self.write_handler)
        self.memory.subscribe_to_read(self.addresses, self.read_handler)

    def write_handler(self, address, value):
        if not address in self.addresses:
            raise ValueError(f'Component not connected to address {address}')

        try:
            self.am.write_address_space[address](self, value)
        except KeyError:
            print("Address not used")
        except AttributeError:
            raise NotImplementedError('Must implement write_adress_space in child class')
    
    def read_handler(self, address):
        if not address in self.addresses:
            raise ValueError(f'Component not connected to address {hex(address)}')

        try:
            return self.am.read_address_space[address](self)
        except KeyError:
            print(f"Address not used: {hex(address)}")
        except AttributeError:
            raise NotImplementedError('Must implement read_adress_space in child class')
    
    def get_address_space(self):
        address_space = []
        for address in self.addresses:
            write_function = self.am.write_address_space.get(address, None)
            read_function = self.am.read_address_space.get(address, None)
            address_space.append({
                'Address' : hex(address), 
                'Write Function' : write_function.__name__ if write_function else 'Not Used', 
                'Read Function' : read_function.__name__ if read_function else 'Not Used'
            })
        return(address_space)
    
    def save_address_space(self):
        with open(f'{self.name}_address_space.csv', 'w') as f:
            writer = csv.DictWriter(
                f = f,
                fieldnames = ['Address', 'Write Function', 'Read Function'])
            
            writer.writeheader()
            writer.writerows(self.get_address_space())

