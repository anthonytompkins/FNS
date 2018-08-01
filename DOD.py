import requests, os, threading, logging
import json, time, datetime, random
from urlparse import urlparse


def dod_generator(_home_url,_username,_password,_notams,_length,_delay,_cancel_rate, _log_file_path):


    #proxies = { 'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
    proxies = None

    # create log file
    log_file_path = _log_file_path + '/' + threading.current_thread().getName() + '.log'
    logger = logging.getLogger(threading.current_thread().getName())
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file_path)
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    # URLs
    if _home_url[-1] != '/':
        _home_url += '/'

    home_url = _home_url
    xsrf_url = home_url + "dnotam/xsrf"
    login_url = home_url + "dnotam/airportInfoService"
    form_url = home_url + "dnotam/dnotamFormHandler"
    utility_url = home_url + "dnotam/utilityService"
    cancel_url = home_url + "dnotam/airportInfoService"

    # login email
    username = _username
    # password
    password = _password

    notams_to_submit = int(_notams)
    length = int(_length)
    delay = int(_delay)
    cancel_rate = int(_cancel_rate)

    submitted_notams = []
    canceled_notams = []

    submitted_dod_notams = 0
    canceled_dod_notams = 0

    xsrf_data = "7|0|4|https://155.178.63.75/dnotam2/dnotam/|CCA65B31464BDB27545C23C142FEEEF8|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

    utility_data = '7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|478CF164B5FD1D3E43383F3E499124D9|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'

    # A request session
    session = requests.Session()

    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

    session.headers.update ({'host': urlparse(home_url).netloc})

    session.headers.update ({'Referer': home_url})

    try:
        response = session.get(home_url, verify=False, proxies=proxies)

        if response.status_code != 200:
            print "%s - Error Getting DOD Home URL" %(threading.current_thread().getName())
            time.sleep(30)
            exit(1)
    except:
        print "%s - Error Getting DOD Home URL"
        time.sleep(30)
        exit(1)

    index = 0
    while index < notams_to_submit:

        session.headers.update(
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Content-Type': 'text/x-gwt-rpc; charset=utf-8',
             'X-GWT-Permutation': '91DAC5113A41AD9FACB523FF735B4CB6',
             'X-GWT-Module-Base': 'https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/',
             'Referer': 'https://notamdemo.aim.nas.faa.gov/dnotamtest/'
             }
        )

        try:
            response = session.post(utility_url, data=utility_data, verify=False, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting DOD Utility Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting DOD Utility Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        session.cookies.update( { 'JSESSIONIDXSRFH':'347311533141375717' } )

        try:
            response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting DOD XSRF Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting DOD XSRF Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        xsrfToken = json.loads ( response.text.lstrip('//OK') )

        login_data = '7|2|9|https://155.178.63.75/dnotam2/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|com.google.gwt.user.client.rpc.XsrfToken/4254043109' \
                     '|'+xsrfToken[2][1] + '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611' \
                     '|' + username + '|' + password + '|1|2|3|4|5|6|4|7|7|7|7|8|9|4|0|'

        try:
            response = session.post(login_url,verify=False,data=login_data, proxies=proxies)

            if response.status_code != 200 or 'Exception' in response.text:
                print "%s - Error Posting DOD Login Data" %(threading.current_thread().getName())
                time.sleep(30)
                os._exit(1)
        except:
            print "%s - Error Posting DOD Login Data" %(threading.current_thread().getName())
            time.sleep(30)
            os._exit(1)

        session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )

        start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=length,minutes=random.randint(1,20)))
        start_time = '%02d%02d' %(start_date.hour, start_date.minute)
        end_time = '%02d%02d' %(end_date.hour, end_date.minute)

        notam_data = {
            'PID_TYPE_7439' : 'TACAN',
            'PID_NAVSTATUS_7440' : 'DECOMMISSIONED',
            'PID_FREQ_7441' : '',
            'PID_CHAN_7442' : '',
            'PID_STANGLE_7444' : '',
            'PID_ENDANGLE_7445' : '',
            'PID_BEYOND_7446' : '',
            'PID_BELOW_7447' : '',
            'PID_DODFREE_8230' : 'Test',
            'IS_DYNAMIC_FORM' : 'true',
            'CONDITION_TEXT' : '',
            'START_DATE' : [start_date.strftime('%m/%d/%Y'), start_date.strftime('%m/%d/%Y')],
            'END_DATE' : [end_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')],
            'USER_ID' : ['24015','Niru Venreddy'],
            'TRANSACTION_ID' : 'undefined',
            'FEATURE_ID' : '20089',
            'SCENARIO_ID' : '602',
            'AIRPORT_ID' : ['36202','KADW'],
            'START_TIME' : start_time,
            'END_TIME' : end_time,
            'US_FAA' : '!KADW XX/XXX ADW NAV TACAN DECOMMISSIONED TEST %s%s-%s%s' %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'ICAO' : 'XX/XXX NOTAMN\nQ) ZDC/QNBXX/IV/NBO/AE/000/999/3848N07652W005 \nA) KADW \nB) %s%s \nC) %s%s \nE) \nNAVAID ADW TACAN DECOMMISSIONED TEST\n'
                     %(start_date.strftime('%y%m%d'),start_time, end_date.strftime('%y%m%d'), end_time),

            'PLAIN' : '<table border="0"><tbody><tr><td><b>Issuing Airport:</b></td><td>(ADW) Joint Base Andrews </td></tr><tr><td><b>NOTAM Number:</b></td><td> XX/XXX</td></tr>'
                      '<tr><td colspan="2"><b>Effective Time Frame</b></td></tr><tr><td><b>Beginning:</b></td><td>Friday, April 13, 2018 0200 (UTC)</td></tr>'
                      '<tr><td><b>Ending:</b></td><td>Friday, April 13, 2018 0500 (UTC)</td></tr><tr><td colspan="2"><b>Affected Areas</b></td></tr>'
                      '<tr><td><b>Airport:</b></td><td>ADW</td></tr><tr><td><b> Type:</b></td><td>Tactical Air Navigation Beacon (TACAN) </td></tr>'
                      '<tr><td><b> Status:</b></td><td>Decommissioned </td></tr><tr><td><b> Additional Text:</b></td><td> TEST </td></tr><tr><td><b></b></td></tr>'
                      '<tr></tr></tbody></table>',
            'ACTION' : 'Activate',
            'PPR_RADIO' : '',
            'C_TRANSACTION_ID' : '',
            'ARPT_DSG' : 'KADW',
            'ACCOUNT_DESIGNATOR' : '',
            'ROLE' : 'QA Analyst',
            'COMPLEX_SCHED' : '',
            'FORM_KEY' : '1533150574583',
            'ON_CLICK_NEW_BTN_TIME' : 'undefined',
            'END_DATE_OPTIONAL' : 'NO',
            'NOTES' : '',
            'NOTAM_R_NUMBER' : 'undefined',
            'USER_TYPE' : 'DOD',
            'RMLS_LOG_ID' : '',
            'xsrfToken' : xsrfToken[2][1]

        }

        submission_time = datetime.datetime.utcnow()

        try:
            response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting DOD NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting DOD NOTAM" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        notam_response = response.text.encode('ascii','ignore')

        notam_response = notam_response.lstrip("MessageTO").replace('[','').replace(']','')

        items = [i.strip() for i in notam_response.split('~')]
        items = [i.split('=') for i in items]

        submission_response = {}

        for item in items:
            if item.__len__() == 2:
                submission_response[item[0]] = item[1]

        if submission_response['errorCode'] != '0':
            print '%s - %s' %(threading.current_thread().getName(), response.text)
            continue
        else:
            submitted_dod_notams += 1
            index += 1

        submission_time = (datetime.datetime.utcnow() - submission_time).total_seconds()

        print "%s - DOD NOTAM %d Submitted: NOTAM Number = %s Response Time = %d seconds" % (threading.current_thread().getName(), submitted_dod_notams, submission_response['notamNumber'], submission_time)

        submitted_notams.append({'notamNumber':submission_response['notamNumber'],
                                 'transactionId':submission_response['transactionId'],
                                 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R'),
                                 'responsetime':submission_time})

        time.sleep(delay)

        if (submitted_dod_notams % cancel_rate) == 0:

            time.sleep(60)

            session.headers.update({'Content-Type': 'text/x-gwt-rpc; charset=utf-8'})

            for notams in submitted_notams:
                log_message = 'SUBMIT - '
                for k,v in notams.items():
                    log_message += '%s=%s    ' %(k, v)
                logger.info(log_message)

            item = submitted_notams.pop(0)

            del submitted_notams [:]

            id = item['transactionId']

            cancel_data = '7|0|97|https://155.178.63.75/dnotam2/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F' \
                          '|gov.faa.aim.dnotam.ui.client.AirportInformationService|cancelNotam|java.lang.String/2004016611' \
                          '|gov.faa.aim.dnotam.ui.dto.UserTO/1159427881|' + id + '||[[Ljava.lang.String;/4182515373' \
                          '|[Ljava.lang.String;/2600011424|17|0|Classification|-1|18|Aerodrome|6|20|Apron|7|21|Runway' \
                          '|8|22|Taxiway|9|35|Obstruction|37|OBST|36202|KADW-JOINT BASE ANDREWS|36226|KBTL-W K KELLOGG' \
                          '|36265|KEGI-DUKE FIELD,(EGLIN AF AUX NR 3)|36857|OPIS-Islamabad int airport|36586' \
                          '|ORAA-AL ASAD|36725|ORBD-Balad Airbase|36660|RJTR-ZAMA/KASTNER|36667|RKRR-INCHEON ACC' \
                          '|36674|RODN-KADENA AB|http://155.178.63.75:9081/dnotam2/dnotam/index.html|9090090099' \
                          '|java.util.Date/3385151746|Niru|http://notams.aim.faa.gov/nmdoduserguide.pdf|10.182.199.52' \
                          '|QA Analyst|Venreddy|Success|niru.venreddy@dod.gov|Passwd1#|java.util.ArrayList/4159755760' \
                          '|gov.faa.aim.dnotam.ui.dto.UserPreference/1057420195|EXPIRY_NOTIFICATION_HRS|24' \
                          '|SHOWPAGINATION|YES|SHOWMAP|NO|ROWLIMIT|50|CANCEL_DAYS|2|gov.faa.aim.dnotam.ui.dto.UserRole/1873077557' \
                          '|KADW|DOD|JOINT BASE ANDREWS|KBTL|W K KELLOGG|KEGI|DUKE FIELD,(EGLIN AF AUX NR 3)|OPIS' \
                          '|Islamabad int airport|ORAA|AL ASAD|ORBD|Balad Airbase|RJTR|ZAMA/KASTNER|RKRR|INCHEON ACC' \
                          '|RODN|KADENA AB|EyYKudjpU6uQK1oqFvUhrhj|2117' \
                          '|Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0|24015' \
                          '|7540E370BE4864102A9160A96B2E70BA|.Hazard no longer exists.|1|2|3|4|3|5|6|5|7|6|0|8' \
                          '|8|0|0|0|9|6|10|8|11|12|13|12|12|0|13|14|10|8|15|11|16|12|12|0|16|17|10|8|18|11|19|12|12|0' \
                          '|19|20|10|8|21|11|22|12|12|0|22|23|10|8|24|11|25|12|12|0|25|26|10|8|27|11|28|29|12|30|28' \
                          '|15|9|9|10|2|31|32|10|2|33|34|10|2|35|36|10|2|37|38|10|2|39|40|10|2|41|42|10|2|43|44|10|2' \
                          '|45|46|10|2|47|48|8|0|49|8|8|0|50|0|51|WT2nt7A|1|8|0|52|53|17|54|55|56|0|31|0|57|58|0' \
                          '|52|7|0|0|8|59|0|0|90|60|5|61|62|63|61|64|65|61|66|67|61|68|69|61|70|71|8|0|0|32|0' \
                          '|60|9|72|73|65|0|74|0|73|0|73|36202|75|1|0|0|0|0|0|0|72|73|65|0|74|0|73|0|76|36226|77' \
                          '|0|0|0|0|0|0|0|72|73|65|0|74|0|73|0|78|36265|79|0|0|0|0|0|0|0|72|73|65|0|74|0|73|0|80' \
                          '|36857|81|0|0|0|0|0|0|0|72|73|65|0|74|0|73|0|82|36586|83|0|0|0|0|0|0|0|72|73|65|0|74' \
                          '|0|73|0|84|36725|85|0|0|0|0|0|0|0|72|73|65|0|74|0|73|0|86|36660|87|0|0|0|0|0|0|0|72' \
                          '|73|65|0|74|0|73|0|88|36667|89|0|0|0|0|0|0|0|72|73|65|0|74|0|73|0|90|36674|91|0|0|0|0|0|0|0' \
                          '|44|92|93|1|0|8|0|8|8|0|WT2nt7A|94|95|74|51|WT2nt7A|0|96|2018|8|97|'

            cancel_time = datetime.datetime.utcnow()

            try:
                response = session.post(cancel_url,verify=False,data=cancel_data, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Erorr Canceling DOD NOTAM" %(threading.current_thread().getName())
                    time.sleep(30)
                    continue
            except:
                print "%s - Erorr Canceling DOD NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue


            cancel_time = (datetime.datetime.utcnow() - cancel_time).total_seconds()

            canceled_dod_notams += 1

            print "%s - DOD NOTAM %d Canceled: NOTAM Number = %s Response Time = %d seconds" %(threading.current_thread().getName(), canceled_dod_notams,item['notamNumber'], cancel_time)

            log_message = 'CANCEL - notamNumber=%s    responsetime=%d seconds' %(item['notamNumber'], cancel_time)
            logger.info(log_message)

