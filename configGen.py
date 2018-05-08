import ConfigParser, os

config = ConfigParser.RawConfigParser()

# Default Configuration file generator
config.add_section('Global')
config.set('Global', 'domain', 'notamdemo.aim.nas.faa.gov')

#Airport
config.add_section('Airports')
config.set('Airports', 'Home_url', 'https://notamdemo.aim.nas.faa.gov/dnotamtest/')
config.set('Airports', 'Username', 'load.test@airports.com')
config.set('Airports', 'Password', 'Password123!')
#Amount of Airport NOTAMS to submit
config.set('Airports', 'NOTAMS', '1000')
#Time, in seconds, between NOTAM submission
config.set('Airports', 'Delay', '30')
#Duration, in hours, of NOTAMS
config.set('Airports', 'Length', '2')
#Amount of NOTAMS to submit before canceling one NOTAM
config.set('Airports', 'Cancel_Rate', '10')

#DOD
config.add_section('DOD')
config.set('DOD', 'Home_url', 'https://notamdemo.aim.nas.faa.gov/dnotamtest/')
config.set('DOD', 'Username', 'nmdod.test@faa.gov')
config.set('DOD', 'Password', 'Test123!')
#Amount of DOD NOTAMS to submit
config.set('DOD', 'NOTAMS', '1000')
#Time, in seconds, between NOTAM submission
config.set('DOD', 'Delay', '30')
#Duration, in hours, of NOTAMS
config.set('DOD', 'Length', '2')
#Amount of NOTAMS to submit before canceling one NOTAM
config.set('DOD', 'Cancel_Rate', '10')

#EN2
config.add_section('EN2')
config.set('EN2', 'Home_url', 'https://notamdemo.aim.nas.faa.gov/en2plus/')
config.set('EN2', 'Username', 'en2.test@faa.gov')
config.set('EN2', 'Password', 'Test123!')
#Amount of EN2 NOTAMS to submit
config.set('EN2', 'NOTAMS', '1000')
#Time, in seconds, between NOTAM submission
config.set('EN2', 'Delay', '30')
#Duration, in hours, of NOTAMS
config.set('EN2', 'Length', '2')
#Amount of NOTAMS to submit before canceling one NOTAM
config.set('EN2', 'Cancel_Rate', '10')

#NMPC
config.add_section('NMPC')
config.set('NMPC', 'Home_url', 'https://notamdemo.aim.nas.faa.gov/nmpc/')
config.set('NMPC', 'Username', 'nmpc.test@faa.gov')
config.set('NMPC', 'Password', 'Test123!')
#NMPC ProgectId, the project must be created prior starting the NOTAM Generator
config.set('NMPC', 'Project_Id', '697')
#Amount of NMPC NOTAMS to submit
config.set('NMPC', 'NOTAMS', '1000')
#Time, in seconds, between NOTAM submission
config.set('NMPC', 'Delay', '30')
#Duration, in hours, of NOTAMS
config.set('NMPC', 'Length', '2')
#Amount of NOTAMS to submit before canceling one NOTAM
config.set('NMPC', 'Cancel_Rate', '10')

#TechOps
config.add_section('TechOps')
config.set('TechOps', 'Home_url', 'https://notamdemo.aim.nas.faa.gov/dnotamtest/')
config.set('TechOps', 'Username', 'nmtech.test@faa.gov')
config.set('TechOps', 'Password', 'Test123!')
#Amount of NMPC NOTAMS to submit
config.set('TechOps', 'NOTAMS', '1000')
#Time, in seconds, between NOTAM submission
config.set('TechOps', 'Delay', '30')
#Duration, in hours, of NOTAMS
config.set('TechOps', 'Length', '2')
#Amount of NOTAMS to submit before canceling one NOTAM
config.set('TechOps', 'Cancel_Rate', '10')


# Writing our configuration file to 'example.cfg'
with open('NMG.cfg', 'wb') as configfile:
    config.write(configfile)