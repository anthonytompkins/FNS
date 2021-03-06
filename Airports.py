import requests, os, threading, logging
import json, time, datetime, random
from urlparse import urlparse


def airport_generator(_home_url,_username,_password,_notams,_length,_delay,_cancel_rate, _log_file_path):

    #proxies = { 'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
    proxies = None

    #create log file
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

    submitted_airport_notams = 0
    canceled_airpot_notams = 0

    xsrf_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|CCA65B31464BDB27545C23C142FEEEF8|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

    utility_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|478CF164B5FD1D3E43383F3E499124D9|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|"

    # A request session
    session = requests.Session()

    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

    session.headers.update ({'host': urlparse(home_url).netloc})

    session.headers.update ({'Referer': home_url})

    try:
        response = session.get(home_url, verify=False, proxies=proxies)
        if response.status_code != 200:
            print "%s - Error Getting Airport Home URL" %(threading.current_thread().getName())
            time.sleep(30)
            return
    except:
        print "%s - Error Getting Airport Home URL" %(threading.current_thread().getName())
        time.sleep(30)
        exit(1)

    while submitted_airport_notams < notams_to_submit:

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
                print "%s - Error Posting Airport Utility Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting Airport Utility Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        session.cookies.update( { 'JSESSIONIDXSRFH':'317101520124880832' } )


        try:
            response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting Airport XSRF Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting Airport XSRF Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue


        xsrfToken = json.loads ( response.text.lstrip('//OK') )

        login_data = '7|2|9|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + \
                     '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|'+ username +'|' + password + '|1|2|3|4|5|6|4|7|7|7|7|8|9|4|0|'

        try:
            response = session.post(login_url,verify=False,data=login_data, proxies=proxies)

            if response.status_code != 200 or 'Exception' in response.text:
                print "%s - Error Posting Airport Login Data" %(threading.current_thread().getName())
                time.sleep(30)
                os._exit(1)
        except:
            print "%s - Error Posting Airport Login Data" %(threading.current_thread().getName())
            time.sleep(30)
            os._exit(1)


        session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )


        start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=length,minutes=random.randint(1,20)))
        start_time = '%02d%02d' %(start_date.hour, start_date.minute)
        end_time = '%02d%02d' %(end_date.hour, end_date.minute)

        notam_data = {

                'PID_REASON_643' : ['Calibration', 'CALIBRATION_PAEW'],
                'PID_DIR_645' : 'S',
                'PID_FREE_946' : '',
                'IS_DYNAMIC_FORM' : 'true',
                'CONDITION_TEXT' : '',
                'START_DATE' : [start_date.strftime('%m/%d/%Y'), start_date.strftime('%m/%d/%Y')],
                'END_DATE' : [end_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')],
                'USER_ID' : ['7973','LoadTest Anthony'],
                'TRANSACTION_ID' : 'undefined',
                'FEATURE_ID' : '18668',
                'SCENARIO_ID' : '302',
                'AIRPORT_ID' : ['18668','BWI'],
                'START_TIME' : start_time,
                'END_TIME' : end_time,
                'US_FAA' : '!BWI XX/XXX BWI AD AP ALL SFC WIP CLBR WORK S SIDE %s%s-%s%s' %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
                'ICAO' : 'XX/XXX NOTAMN \nQ) ZDC/QFAHW/IV/NBO/A/000/999/3910N07640W005 \n\nA) KBWI \nB) %s%s \nC) %s%s \nE) AD CLBR WORK ALL SFC WIP N SIDE '
                         %(start_date.strftime('%y%m%d'),start_time, end_date.strftime('%y%m%d'), end_time),
                'PLAIN' : ' <table border="0"><tbody><tr><td><b>Issuing Airport:</b></td><td>(BWI) Baltimore/Washington Intl Thurgood Marshall </td></tr>'
                          '<tr><td><b>NOTAM Number:</b></td><td> XX/XXX</td></tr><tr><td colspan="2"><b>Effective Time Frame</b></td></tr>'
                          '<tr><td><b>Beginning:</b></td><td>Monday, March 5, 2018 0200 (UTC)</td></tr>'
                          '<tr><td><b>Ending:</b></td><td>Monday, March 5, 2018 0500 (UTC)</td></tr>'
                          '<tr><td colspan="2"><b>Affected Areas</b></td></tr>'
                          '<tr><td><b>Airport:</b></td><td>BWI</td></tr>'
                          '<tr><td><b> Warning:</b></td><td>Work In Progress -Calibration (all surfaces) on the South side </td></tr>'
                          ' <tr><td><b></b></td></tr><tr></tr></tbody></table>',
                'ACTION' : 'Activate',
                'PPR_RADIO' : '',
                'C_TRANSACTION_ID' : '',
                'ARPT_DSG' : 'BWI',
                'ACCOUNT_DESIGNATOR' : '',
                'ROLE' : 'Tester',
                'COMPLEX_SCHED' : '',
                'FORM_KEY' : '1520215108332',
                'ON_CLICK_NEW_BTN_TIME' : '1520232960000',
                'END_DATE_OPTIONAL' : 'NO',
                'NOTES' : '',
                'NOTAM_R_NUMBER' : '04%2F001',
                'USER_TYPE' : 'AIRPORT',
                'RMLS_LOG_ID' : '',
                'xsrfToken' : xsrfToken[2][1]
        }

        submission_time = datetime.datetime.utcnow()

        try:
            response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting Airport NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting Airport NOTAM" %(threading.current_thread().getName())
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
            submitted_airport_notams += 1

        submission_time = (datetime.datetime.utcnow() - submission_time).total_seconds()

        submitted_notams.append({'notamNumber':submission_response['notamNumber'], 'transactionId':submission_response['transactionId'], 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %d, %Y %X'), 'responsetime':str(submission_time)})

        print "%s - Airport NOTAM %d Submitted: NOTAM Number = %s Response Time = %d seconds" %(threading.current_thread().getName(), submitted_airport_notams, submission_response['notamNumber'], submission_time)

        time.sleep(delay)

        if (submitted_airport_notams % cancel_rate) == 0:

            time.sleep(60)

            session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

            for notams in submitted_notams:
                log_message = 'SUBMIT - '
                for k,v in notams.items():
                    log_message += '%s=%s    ' %(k, v)
                logger.info(log_message)

            item = submitted_notams.pop(0)

            del submitted_notams[:]

            cancel_data = '7|2|74|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|' \
                  'com.google.gwt.user.client.rpc.XsrfToken/4254043109|7BD738F38104A4011DC17A5B8F3804D0|' \
                  'gov.faa.aim.dnotam.ui.client.AirportInformationService|cancelNotam|java.lang.String/2004016611|' \
                  'gov.faa.aim.dnotam.ui.dto.UserTO/1159427881|'+ item['transactionId'] +'||[[Ljava.lang.String;/4182515373|[Ljava.lang.String;/2600011424|' \
                  '1|0|Keyword-All|2|Aerodrome|20|AD|3|Apron|31|APRON|6|Obstruction|OBST|7|Runway|RWY|9|Taxiway|30|TWY|18668|' \
                  'BWI-Baltimore/Washington Intl Thurgood Marshall|15709|IAD-Washington Dulles Intl|6384|JFK-John F Kennedy Intl|' \
                  'http://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/index.html|7031112222|java.util.Date/3385151746|LoadTest|' \
                  'http://notamdemo.aim.nas.faa.gov/fnshelp/help.html|172.26.22.194|Tester|Anthony|Success|' \
                  'load.test@airports.com|Password123!|java.util.ArrayList/4159755760|gov.faa.aim.dnotam.ui.dto.UserPreference/1057420195' \
                  '|EXPIRY_NOTIFICATION_HRS|48|SHOWPAGINATION|YES|SHOWMAP|NO|ROWLIMIT|50|CANCEL_DAYS' \
                  '|gov.faa.aim.dnotam.ui.dto.UserRole/1873077557|BWI|AIRPORT|ZDC|Baltimore/Washington Intl Thurgood Marshall|IAD|Washington Dulles Intl|JFK|ZNY|' \
                  'John F Kennedy Intl|311da27196d4c03364906e963921|Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0|7973|' \
                  '1|2|3|4|5|6|3|7|8|7|9|8|0|10|10|0|0|0|11|6|12|8|13|14|15|14|14|0|15|0|12|8|16|13|17|14|18|19|17|0|12|8|20|13|21|14|22|23|21|0|12|8|24|13|25|14' \
                  '|14|26|25|0|12|8|27|13|28|14|14|29|28|0|12|8|30|13|31|14|32|33|31|0|11|3|12|2|34|35|12|2|36|37|12|2|38|39|10|0|40|10|10|0|41|0|42|WKjEd2u|8|10' \
                  '|0|43|44|2|45|46|47|0|34|0|48|49|0|24|3|0|0|10|50|0|0|90|51|5|52|53|54|52|55|56|52|57|58|52|59|60|52|61|16|10|0|0|32|0|51|3|62|63|65|0|64|0|65|0|63' \
                  '|18668|66|0|0|0|0|0|0|0|62|67|65|0|64|0|65|0|67|15709|68|0|0|0|0|0|0|0|62|69|65|0|64|0|70|0|69|6384|71|0|0|0|0|0|0|0|39|72|0|0|0|10|0|10|10|0' \
                  '|WKjEd2u|73|74|64|42|WKjEd2u|0|4|2018|10|10|'

            cancel_time = datetime.datetime.utcnow()

            try:
                response = session.post(cancel_url,verify=False,data=cancel_data, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Error Canceling Airport NOTAM: %s" %(threading.current_thread().getName(), item['notamNumber'])
                    time.sleep(30)
                    continue
            except:
                print "%s - Error Canceling Airport NOTAM: %s" %(threading.current_thread().getName(), item['notamNumber'])
                time.sleep(30)
                continue

            cancel_time = (datetime.datetime.utcnow() - cancel_time).total_seconds()

            canceled_airpot_notams += 1

            print "%s - Airport NOTAM %d Canceled: NOTAM Number = %s Response Time = %d seconds" %(threading.current_thread().getName(), canceled_airpot_notams,item['notamNumber'], cancel_time)

            log_message = 'CANCEL - notamNumber=%s    responsetime=%d seconds' %(item['notamNumber'], cancel_time)
            logger.info(log_message)

