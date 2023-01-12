from py65.memory import ObservableMemory
import csv

class Memory(ObservableMemory):
    def get_adress_space(self):
        write_dict = self._write_subscribers.copy()
        read_dict = self._read_subscribers.copy()

        addresse_space = [{
            'Address': hex(address), 
            'Object': function[0].__qualname__.__name__, 
            'W/R': 'W'} 
            for address, function in write_dict.items()]
        with open('address_space.csv', 'w') as f:
            writer = csv.DictWriter(
                f = f,
                fieldnames = ['Address', 'Object', 'W/R'])
            
            writer.writeheader()
            writer.writerows(addresse_space)
        