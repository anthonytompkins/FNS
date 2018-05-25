import os, ConfigParser
from datetime import datetime
import Airports, DOD, EN2, NMPC, TechOps
import threading, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if not os.path.exists('Logs'):
    os.mkdir('Logs')


#Read Config
config = ConfigParser.ConfigParser({'Threads':'1'})
config.readfp(open('config.cfg'))

log_dir_timestamp = datetime.utcnow().strftime('%m%d%y-%H%M%S')

airport_log_path = 'Logs/Airport/' + log_dir_timestamp
dod_log_path = 'Logs/DOD/' + log_dir_timestamp
en2_log_path = 'Logs/EN2/' + log_dir_timestamp
nmpc_log_path = 'Logs/NMPC/' + log_dir_timestamp
techops_log_path = 'Logs/TECHOPS/' + log_dir_timestamp

os.makedirs(airport_log_path)
os.makedirs(dod_log_path)
os.makedirs(en2_log_path)
os.makedirs(nmpc_log_path)
os.makedirs(techops_log_path)

airport_threads = [threading.Thread(name='Airport_Thread_%d' %(i), target=Airports.airport_generator, args= ( config.get('Airports', 'home_url'),
                                                                                                              config.get('Airports', 'username'),
                                                                                                              config.get('Airports', 'password'),
                                                                                                              config.get('Airports', 'notams'),
                                                                                                              config.get('Airports', 'length'),
                                                                                                              config.get('Airports', 'delay'),
                                                                                                              config.get('Airports', 'cancel_rate'),
                                                                                                              airport_log_path)) for i in range(int(config.get('Airports', 'Threads')))]



dod_threads = [threading.Thread(name='DOD_Thread:%d' %(i), target=DOD.dod_generator, args= ( config.get('DOD', 'home_url'),
                                                                                             config.get('DOD', 'username'),
                                                                                             config.get('DOD', 'password'),
                                                                                             config.get('DOD', 'notams'),
                                                                                             config.get('DOD', 'length'),
                                                                                             config.get('DOD', 'delay'),
                                                                                             config.get('DOD', 'cancel_rate'),
                                                                                             dod_log_path)) for i in range(int(config.get('DOD', 'Threads')))]

en2_threads = [threading.Thread(name='EN2_Thread:%d' %(i), target=EN2.en2_generator, args= ( config.get('EN2', 'home_url'),
                                                                                             config.get('EN2', 'username'),
                                                                                             config.get('EN2', 'password'),
                                                                                             config.get('EN2', 'notams'),
                                                                                             config.get('EN2', 'length'),
                                                                                             config.get('EN2', 'delay'),
                                                                                             config.get('EN2', 'cancel_rate'),
                                                                                             en2_log_path)) for i in range(int(config.get('EN2', 'Threads')))]

nmpc_threads = [threading.Thread(name='NMPC_Thread:%d' %(i), target=NMPC.nmpc_generator, args= ( config.get('NMPC', 'home_url'),
                                                                                                 config.get('NMPC', 'username'),
                                                                                                 config.get('NMPC', 'password'),
                                                                                                 config.get('NMPC', 'project_id'),
                                                                                                 config.get('NMPC', 'notams'),
                                                                                                 config.get('NMPC', 'length'),
                                                                                                 config.get('NMPC', 'delay'),
                                                                                                 config.get('NMPC', 'cancel_rate'),
                                                                                                 nmpc_log_path)) for i in range(int(config.get('NMPC','Threads')))]

techops_thread = [threading.Thread(name='TechOps_Thread:%d' %(i), target=TechOps.techops_generator, args= ( config.get('TechOps', 'home_url'),
                                                                                                            config.get('TechOps', 'username'),
                                                                                                            config.get('TechOps', 'password'),
                                                                                                            config.get('TechOps', 'notams'),
                                                                                                            config.get('TechOps', 'length'),
                                                                                                            config.get('TechOps', 'delay'),
                                                                                                            config.get('TechOps', 'cancel_rate'),
                                                                                                            techops_log_path)) for i in range(int(config.get('TechOps', 'Threads')))]



for t in airport_threads:
    t.start()

for t in dod_threads:
    t.start()

for t in en2_threads:
    t.start()

for t in nmpc_threads:
    t.start()

for t in techops_thread:
    t.start()



for t in airport_threads:
    t.join()

for t in dod_threads:
    t.join()

for t in en2_threads:
    t.join()

for t in nmpc_threads:
    t.join()

for t in techops_thread:
    t.join()
