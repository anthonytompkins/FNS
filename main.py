import os, ConfigParser
from subprocess import *
import Airports, DOD, EN2, NMPC, TechOps
from multiprocessing import Process
import threading, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#Read Config
config = ConfigParser.ConfigParser()
config.readfp(open('NMG.cfg'))

airport_thread = threading.Thread(target=Airports.airport_generator, args= ( config.get('Airports', 'home_url'),
                                                                config.get('Airports', 'username'),
                                                                config.get('Airports', 'password'),
                                                                config.get('Airports', 'notams'),
                                                                config.get('Airports', 'length'),
                                                                config.get('Airports', 'delay'),
                                                                config.get('Airports', 'cancel_rate')))


dod_thread = threading.Thread(target=DOD.dod_generator, args= ( config.get('DOD', 'home_url'),
                                                                config.get('DOD', 'username'),
                                                                config.get('DOD', 'password'),
                                                                config.get('DOD', 'notams'),
                                                                config.get('DOD', 'length'),
                                                                config.get('DOD', 'delay'),
                                                                config.get('DOD', 'cancel_rate')))

en2_thread = threading.Thread(target=EN2.en2_generator, args= ( config.get('EN2', 'home_url'),
                                                                config.get('EN2', 'username'),
                                                                config.get('EN2', 'password'),
                                                                config.get('EN2', 'notams'),
                                                                config.get('EN2', 'length'),
                                                                config.get('EN2', 'delay'),
                                                                config.get('EN2', 'cancel_rate')))

nmpc_thread = threading.Thread(target=NMPC.nmpc_generator, args= ( config.get('NMPC', 'home_url'),
                                                                   config.get('NMPC', 'username'),
                                                                   config.get('NMPC', 'password'),
                                                                   config.get('NMPC', 'project_id'),
                                                                   config.get('NMPC', 'notams'),
                                                                   config.get('NMPC', 'length'),
                                                                   config.get('NMPC', 'delay'),
                                                                   config.get('NMPC', 'cancel_rate')))

techops_thread = threading.Thread(target=TechOps.techops_generator, args= ( config.get('TechOps', 'home_url'),
                                                                            config.get('TechOps', 'username'),
                                                                            config.get('TechOps', 'password'),
                                                                            config.get('TechOps', 'notams'),
                                                                            config.get('TechOps', 'length'),
                                                                            config.get('TechOps', 'delay'),
                                                                            config.get('TechOps', 'cancel_rate')))

airport_thread.start()
dod_thread.start()
en2_thread.start()
nmpc_thread.start()
techops_thread.start()

airport_thread.join()
dod_thread.join()
en2_thread.join()
nmpc_thread.join()
techops_thread.join()
