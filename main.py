import os, ConfigParser
from subprocess import *
import Airports
from multiprocessing import Process




#run child script 1
#p = Popen([r'python Airports.py', "ArcView"], shell=True, stdin=PIPE, stdout=PIPE)
#output = p.communicate()
#print output[0]

#run child script 2
#p = Popen([r'python EN2.py', "ArcEditor"], shell=True, stdin=PIPE, stdout=PIPE)
#output = p.communicate()
#print output[0]

#exit(0)

#Read Config
config = ConfigParser.ConfigParser()
config.readfp(open('NMG.cfg'))



p1 = Process(target=Airports.airport_generator,args=( config.get('Airports', 'home_url'),
                                                      config.get('Airports', 'username'),
                                                      config.get('Airports', 'password'),
                                                      config.get('Airports', 'notams'),
                                                      config.get('Airports', 'length'),
                                                      config.get('Airports', 'delay'),
                                                      config.get('Airports', 'cancel_rate')))

p2 = Process(target=Airports.airport_generator,args=( config.get('Airports', 'home_url'),
                                                      config.get('Airports', 'username'),
                                                      config.get('Airports', 'password'),
                                                      config.get('Airports', 'notams'),
                                                      config.get('Airports', 'length'),
                                                      config.get('Airports', 'delay'),
                                                      config.get('Airports', 'cancel_rate')))

p1.start()
p2.start()
#p1.join()

exit(0)

os.system('python Airports.py')
os.system('python DOD.py')
os.system('python EN2.py')
os.system('python NMPC.py')
os.system('python TechOps.py')