import requests, os, threading, logging
import json, time, datetime, random
from urlparse import urlparse

def techops_generator(_home_url,_username,_password,_notams,_length,_delay,_cancel_rate, _log_file_path):

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

    submitted_techops_notams = 0
    canceled_techops_notams = 0

    xsrf_data = "7|0|4|https://155.178.63.75/dnotam2/dnotam/|CCA65B31464BDB27545C23C142FEEEF8|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

    utility_data = '7|0|4|https://155.178.63.75/dnotam2/dnotam/|478CF164B5FD1D3E43383F3E499124D9|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'

    # A request session
    session = requests.Session()

    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

    session.headers.update ({'host': urlparse(home_url).netloc})

    session.headers.update ({'Referer': home_url})


    try:
        response = session.get(home_url, verify=False, proxies=proxies)

        if response.status_code != 200:
            print "%s - Error Getting TechOps Home URL" %(threading.current_thread().getName())
            time.sleep(30)
            exit(1)
    except:
        print "%s - Error Getting TechOps Home URL" %(threading.current_thread().getName())
        time.sleep(30)
        exit(1)

    submitted_techops_notams = 0
    while submitted_techops_notams < notams_to_submit:

        session.headers.update(
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Content-Type': 'text/x-gwt-rpc; charset=utf-8',
             'X-GWT-Permutation': '04700B765F96A728C7C52F770DBF68B8',
             'X-GWT-Module-Base': 'https://155.178.63.75/dnotam2/dnotam/',
             'Referer': 'https://notamdemo.aim.nas.faa.gov/dnotamtest/'
             }
        )

        try:
            response = session.post(utility_url, data=utility_data, verify=False, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting TechOps Utility Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting TechOps Utility Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        session.cookies.update( { 'JSESSIONIDXSRFH':'178461532378352670' } )

        try:
            response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting TechOps XSRF Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting TechOps XSRF Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        xsrfToken = json.loads ( response.text.lstrip('//OK') )

        login_data = '7|2|9|https://155.178.63.75/dnotam2/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + \
                     '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|'\
                     + username + '|' + password +'|1|2|3|4|5|6|4|7|7|7|7|8|9|4|0|'

        try:
            response = session.post(login_url,verify=False,data=login_data, proxies=proxies)

            if response.status_code != 200 or 'Exception' in response.text:
                print "%s - Error Posting TechOps Login Data" %(threading.current_thread().getName())
                time.sleep(30)
                os._exit(1)
        except:
            print "%s - Error Posting TechOps Login Data" %(threading.current_thread().getName())
            time.sleep(30)
            os._exit(1)

        session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )

        start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=length,minutes=random.randint(1,20)))
        start_time = '%02d%02d' %(start_date.hour, start_date.minute)
        end_time = '%02d%02d' %(end_date.hour, end_date.minute)

        notam_data = {
            'PID_TYPE_2461' : 'LAA',
            'PID_STATUS_2462' : 'UNSERVICEABLE',
            'PID_EFASTYP_8772' :'',
            'PID_RCOTYP_8775' : 'RCO',
            'PID_CDTYP_8778' : 'CD',
            'PID_CTAFTYP_8781' : '',
            'PID_RCAGTYP_8784' : '',
            'PID_GNDTYP_8787' : 'GNDCTL',
            'PID_BASFREQ_8790' : '',
            'PID_BASFRQ_8931' : '',
            'PID_FREQ_2469#0' : '100.00',
            'IS_DYNAMIC_FORM' : 'true',
            'CONDITION_TEXT' : '',
            'START_DATE' : [start_date.strftime('%m/%d/%Y'), start_date.strftime('%m/%d/%Y')],
            'END_DATE' : [end_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')],
            'USER_ID' : ['24012','Niru Venreddy'],
            'TRANSACTION_ID' : 'undefined',
            'FEATURE_ID' : '6160',
            'SCENARIO_ID' : '504',
            'AIRPORT_ID' : ['15', 'AOCC'],
            'START_TIME' : start_time,
            'END_TIME' : end_time,
            'US_FAA' : '!ACY XX/XXX ACY COM LOCAL AP ADVISORY SERVICE 100.00 OUT OF SERVICE %s%s-%s%s' %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'ICAO' : 'XX/XXX NOTAMN \nQ) ZDC/QSAAS/IV/B/AE/000/999/3927N07434W005 \nA) KACY \nB) %s%s \nC) %s%s \n\nE) COM LOCAL AP ADVISORY SERVICE 100.00 OUT OF SERVICE'
                     %(start_date.strftime('%y%m%d'),start_time, end_date.strftime('%y%m%d'), end_time),
            'PLAIN' : '<table border="0"><tbody><tr><td><b>Issuing Airport:</b></td><td>(ACY) Atlantic City Intl</td></tr>'
                      '<tr><td><b>NOTAM Number:</b></td><td>XX/XXX</td></tr>'
                      '<tr><td colspan = "2"><b>Effective Time Frame</b></td></tr>'
                      '<tr><td><b>Beginning: </b></td><td> Thursday, April 12, 2018 0200(UTC) </td></tr>'
                      '<tr><td><b>Ending: </b></td><td>Thursday, April 12, 2018 0500(UTC) </td></tr>'
                      '<tr><td colspan = "2"><b>Affected Areas </b></td></tr><tr><td><b>Airport:</b></td><td>ACY</td></tr>'
                      '<tr><td><b>Air Traffic control service: </b></td><td>Local airport advisory </td></tr>'
                      '<tr><td><b>Status: </b></td><td> Out of Service </td></tr><tr><td><b>Radio frequency: </b></td><td>100.00</td></tr><tr><td><b></b></td></tr>'
                      '<tr></tr></tbody></table>',
            'ACTION' : 'Activate',
            'PPR_RADIO' : '',
            'C_TRANSACTION_ID' : '',
            'ARPT_DSG' : 'AOCC',
            'ACCOUNT_DESIGNATOR' : '',
            'ROLE' : 'FAA',
            'COMPLEX_SCHED' : '',
            'FORM_KEY' : '1523461745538',
            'ON_CLICK_NEW_BTN_TIME' : 'undefined',
            'END_DATE_OPTIONAL' : 'NO',
            'NOTES' : '',
            'NOTAM_R_NUMBER' : 'undefined',
            'USER_TYPE' : 'OCC',
            'RMLS_LOG_ID' : '123',
            'xsrfToken' : xsrfToken[2][1]
        }

        submission_time = datetime.datetime.utcnow()

        try:
            response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting TechOps NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting TechOps NOTAM" %(threading.current_thread().getName())
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
            submitted_techops_notams += 1

        submission_time = (datetime.datetime.utcnow() - submission_time).total_seconds()

        submitted_notams.append({'notamNumber':submission_response['notamNumber'],
                                 'transactionId':submission_response['transactionId'],
                                 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R'),
                                 'responsetime':submission_time})

        print "%s - TechOps NOTAM %d Submitted: NOTAM Number = %s Response Time = %d seconds" % ( threading.current_thread().getName(), submitted_techops_notams, submission_response['notamNumber'], submission_time)

        time.sleep(delay)

        if (submitted_techops_notams % cancel_rate) == 0:

            time.sleep(60)

            session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

            for notams in submitted_notams:
                log_message = 'SUBMIT - '
                for k,v in notams.items():
                    log_message += '%s=%s    ' %(k, v)
                logger.info(log_message)

            item = submitted_notams.pop(0)

            del submitted_notams[:]

            cancel_data = '7|0|77|https://155.178.63.75/dnotam2/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F' \
                          '|gov.faa.aim.dnotam.ui.client.AirportInformationService|cancelNotam|java.lang.String/2004016611' \
                          '|gov.faa.aim.dnotam.ui.dto.UserTO/1159427881|' + item['transactionId'] + '||[[Ljava.lang.String;/4182515373|[Ljava.lang.String;/2600011424' \
                          '|11|0|Classification-All|-1|12|Communications|22|COM|1|13|Lighted Aids|75|LIGHTED AID|2|14|Navaids|25|NAV|3|15|Radar' \
                          '|76|RADAR|4|16|Weather|77|WEATHER|5|43|Obstruction|OBST|18|AOCC-AOCC|20|POCC-POCC|http://155.178.63.75:9081/dnotam2/dnotam/index.html' \
                          '|9090090099|java.util.Date/3385151746|Niru|https://notams.aim.faa.gov/nmoccuserguide.pdf|10.182.199.52|QA Analyst' \
                          '|Venreddy|Success|niru.venreddy@techops.gov|Passwd1#|java.util.ArrayList/4159755760|gov.faa.aim.dnotam.ui.dto.UserPreference/1057420195' \
                          '|EXPIRY_NOTIFICATION_HRS|48|SHOWPAGINATION|YES|SHOWMAP|NO|ROWLIMIT|50|CANCEL_DAYS|gov.faa.aim.dnotam.ui.dto.UserRole/1873077557' \
                          '|OCC|AOCC|POCC|73GaU5txY8hpDOUEHQZQ00p|Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/67.0.3396.99 Chrome/67.0.3396.99 Safari/537.36' \
                          '|24012|72BF830FD055B93A35324F04396F97E5| Issued NOTAM is incorrect.|1|2|3|4|3|5|6|5|7|6|0|8|8|0|0|0|9|7|10|8|11|12|13|12|12|0|13|14' \
                          '|10|8|15|11|16|12|17|18|16|19|10|8|20|11|21|12|22|23|21|24|10|8|25|11|26|12|27|28|26|29|10|8|30|11|31|12|32|33|31|34|10|8|35|11' \
                          '|36|12|37|38|36|39|10|8|40|11|41|12|12|42|41|43|9|2|10|2|30|44|10|2|45|46|8|0|47|8|8|0|48|0|49|WTI$itu|23|8|0|50|51|21|52|53|54|0' \
                          '|30|0|55|56|0|9|6|0|0|8|57|0|0|90|58|5|59|60|61|59|62|63|59|64|65|59|66|67|59|68|24|8|0|0|32|0|58|2|69|70|65|0|70|0|0|0|71|15|71|0|0|0' \
                          '|0|0|0|0|69|70|65|0|70|0|0|0|72|20|72|0|0|0|0|0|0|0|55|73|0|0|0|8|0|8|8|0|WTI$itu|74|75|70|49|WTI$itu|0|76|2018|8|77|'

            cancel_time = datetime.datetime.utcnow()

            try:
                response = session.post(cancel_url,verify=False,data=cancel_data, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Error Canceling TechOps NOTAM" %(threading.current_thread().getName())
                    time.sleep(30)
                    continue
            except:
                print "%s - Error Canceling TechOps NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue

            cancel_time = (datetime.datetime.utcnow() - cancel_time).total_seconds()

            canceled_techops_notams += 1

            print "%s - TechOps NOTAM %d Canceled: NOTAM Number = %s Response Time = %d seconds" %(threading.current_thread().getName(), canceled_techops_notams,item['notamNumber'], cancel_time)

            log_message = 'CANCEL - notamNumber=%s    responsetime=%d seconds' %(item['notamNumber'], cancel_time)
            logger.info(log_message)
