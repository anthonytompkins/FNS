# FNS NOTAM Manager Load Tool

Description

    The NOTAM Manager Load Tool is a collection of python scripts that use the requests module to automate NOTAM submissions for the following NOTAM Manager user types:

        · Airport
        · EN2
        · TechOps
        · DOD
        · NMPC

    The tool uses a template of a NOTAM manager scenario for each user type. The tool changes the start and stop date of each NOTAM to avoid submitting duplicate NOTAMS. The tool also cancels a configurable amount of the NOTAMs it submitted.

Installation

    Ubuntu

        1. Execute the following command to switch to the root user

            sudo su –

        2. Execute the following command to update system repositories

            apt update

        3. Execute the following command to install the python 2.7 distribution

            apt install python-minimal

        4. Execute the following commands to install the required python modules

            apt install python-pip
            pip install requests urllib3

        5. Execute the following command to install GIT, a software version control tool

            apt install git

        6. Use the exit command to switch to a non-root account

        7. Execute the following command to change the current working directory

            cd /opt/

        8. Execute the following command to clone the NOTAM Manager Load tool repository

            git clone https://github.com/anthonytompkins/FNS.git

    RedHat/Fedora

        1. Execute the following command to switch to the root user

            yum su –

        2. Execute the following command to update system repositories

            yum update

        3. Execute the following command to install the python 2.7 distribution

            yum install python-minimal

        4. Execute the following commands to install the required python modules

            yum install python-pip
            pip install requests urllib3

        5. Execute the following command to install GIT, a software version control tool

            yum install git

        6. Use the exit command to switch to a non-root account

        7. Execute the following command to change the current working directory

            cd /opt/

        7. Execute the following command to clone the NOTAM Manager Load tool repository

            git clone https://github.com/anthonytompkins/FNS.git

Configuration

    The tool uses a configuration file, config.cfg, that contains the following parameters for each user type.

        · Threads - Amount of instances of this user type
        · Home_url – URL of the login page for the user type
        · Username – Username for the user type account
        · Password – Password for the user type account
        · Notams - Amount of NOTAMS to submit per thread
        · Delay - Time, in seconds, between NOTAM submission attempts
        · Length - Duration, in hours, each NOTAM is active
        · Cancel_rate - Amount of NOTAMS to submit before canceling a previously submitted NOTAM

    The NMPC user type has an additional parameter, ProjectId, which represents an existing project associated with the NMPC user account. You must login as the NMPC user, create a project, and retrieve the ProjectId before configuring the tool.

    To configure the tool, navigate to the /opt/FNS/ directory and use vi or nano to edit the config.cfg file.

    If you encounter a issue with the config file, execute the following command from the /opt/FNS/ directory to create a new default config file.

        python configGen.py

Execution

    The tool is multithreaded and creates a thread to simulate each user type. Multiple threads can be created for the same user type, i.e., simulate multiple airport users. Each thread displays the following information for each successfully submitted NOTAM in the console window.

        · Total Number of NOTAMS submitted by the thread
        · NOTAM Number of the last NOTAM successfully submitted
        · NOTAM Manager response time, i.e., time between submitting a NOTAM and receiving a response from the NOTAM Manager system

    The tool execution starts in the main.py file located in the /opt/FNS/ directory.

    To start the tool, navigate to the /opt/FNS/ directory and execute the following command.

          python main.py

    To run the tool in the background, execute the following command.

          python main.py &

Logging

    The tool creates a directory for each user type in the /opt/FNS/Logs/ directory. Each time the tool executes, the tool creates a timestamp titled directory within each user type's logs directory, e.g., /opt/FNS.Logs/Airport/052418-220511. Each user type thread logs the following information for each successfully submitted NOTAM in a self-titled log file, e.g., Airport_Thread:1.log.

        · NOTAM Number
        · Transaction ID
        · NOTAM Manager response time, i.e., the time between submitting a NOTAM and receiving a response from the NOTAM Manager system
        · Time stamp, the date and time when the NOTAM was submitted
