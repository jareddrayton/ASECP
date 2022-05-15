import configparser

config = configparser.ConfigParser()
config.read('asecp_configuration.ini')

print(config.sections())
import pdb;pdb.set_trace()
