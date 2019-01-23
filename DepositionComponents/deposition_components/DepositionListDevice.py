# See LICENSE file in root directory for this package
import logging
import csv
from ophyd.device import Device
logger = logging.getLogger(__name__)

class DepositionListDevice(Device):
    '''
    Generic device type for our project
    '''

    def __init__(self, *args, instance_number=0, config_file="", **kwargs):
        self.prefix = args[0]
        self.instance_number = instance_number
        self.instance_letter = chr(instance_number + 64)
        # print ("kwargs %s" % kwargs)
        super(DepositionListDevice, self).__init__(*args, **kwargs)
            
    def loadListFile(self):
        configuration = {}
        with open(self.config_file, 'r') as config:
            config_reader = csv.DictReader(config)
            numAttr = 0
            for row in config_reader:
                if row['object'] == self.__class__.__name__:
                    configuration[numAttr] = row
                    numAttr += 1
        logger.debug ("\nconfiguration %s\n" % configuration)

        return configuration
        
