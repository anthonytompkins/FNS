import requests, os, threading, logging
import json, time, datetime, random, string
from urlparse import urlparse

def en2_generator(_home_url,_username,_password,_notams,_length,_delay,_cancel_rate, _log_file_path):

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
    xsrf_url = home_url + "en2/xsrf"
    login_url = home_url + "en2/airportInfoService"
    form_url = home_url + "en2/dnotamFormHandler"
    utility_url = home_url + "en2/utilityService"
    cancel_url = home_url + "en2/airportInfoService"

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

    submitted_en2_notams = 0
    canceled_en2_notams = 0

    xsrf_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|E1EF26ED6384B9AF4934C71870F2E259|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

    utility_data = '7|0|4|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|8C30C5E7368E7D64D2853D893E5C2495|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'
    # A request session
    session = requests.Session()

    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

    session.headers.update ({'host': urlparse(home_url).netloc})

    session.headers.update ({'Referer': home_url})

    try:
        response = session.get(home_url, verify=False, proxies=proxies)

        if response.status_code != 200:
            print "%s - Error Getting EN2 Home Url" %(threading.current_thread().getName())
            time.sleep(30)
            exit(1)
    except:
        print "%s - Error Getting EN2 Home Url" %(threading.current_thread().getName())
        time.sleep(30)
        exit(1)

    submitted_en2_notams = 0
    while submitted_en2_notams < notams_to_submit:

        session.headers.update(
            {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate',
             'Content-Type': 'text/x-gwt-rpc; charset=utf-8',
             'X-GWT-Permutation': '578B73B06A8B1665F602BBCC942329F1',
             'X-GWT-Module-Base': 'https://notamdemo.aim.nas.faa.gov/en2plus/en2/',
             'Referer': 'https://notamdemo.aim.nas.faa.gov/en2plus/'
             }
        )

        try:
            response = session.post(utility_url, data=utility_data, verify=False, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting EN2 Utility Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting EN2 Utility Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue


        session.cookies.update( { 'JSESSIONIDXSRF3N2':'330581523574837336' } )

        try:
            response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting EN2 XSRF Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting XSRF EN2 Data" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        xsrfToken = json.loads ( response.text.lstrip('//OK') )

        login_data = '7|2|9|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|0196662329E3ED777244D915ABB428BD|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + \
                     '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|'\
                     + username + '|' + password + '|1|2|3|4|5|6|2|7|7|8|9|'


        try:
            response = session.post(login_url,verify=False,data=login_data, proxies=proxies)

            if response.status_code != 200 or 'Exception' in response.text:
                print "%s - Error Posting EN2 Login Data" %(threading.current_thread().getName())
                time.sleep(30)
                os._exit(1)
        except:
            print "%s - Error Posting EN2 Login Data" %(threading.current_thread().getName())
            time.sleep(30)
            os._exit(1)

        session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )

        start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=length,minutes=random.randint(1,20)))
        start_time = '%02d%02d' %(start_date.hour, start_date.minute)
        end_time = '%02d%02d' %(end_date.hour, end_date.minute)

        free_form_text = 'AIRSPACE %s' %((random.choice(string.letters)).capitalize())

        notam_data = {
            'arptObstacle' : 'on',
            'START_DATE' : [start_date.strftime('%m/%d/%Y'), start_date.strftime('%m/%d/%Y')],
            'END_DATE' : [end_date.strftime('%m/%d/%Y'), end_date.strftime('%m/%d/%Y')],
            'NOTES' : '',
            'FREE_FORM_TEXT' : free_form_text,
            'USER_ID' : '8003',
            'TRANSACTION_ID' : '',
            'FEATURE_ID' : '0',
            'SCENARIO_ID' : '101',
            'AIRPORT_ID' : ['345078',''],
            'i_groupid' : '1',
            'START_TIME' : start_time,
            'END_TIME' : end_time,
            'US_FAA' : '!ISP XX/XXX ZNY %s %s%s-%s%s' %(free_form_text, start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'ICAO' : '!ISP XX/XXX ZNY %s %s%s-%s%s' %(free_form_text, start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'PLAIN' : '',
            'ACTION' : 'Activate',
            'PPR_RADIO' : '',
            'C_TRANSACTION_ID' :'',
            'ARPT_DSG' : 'ZNY',
            'ACCOUNT_DESIGNATOR' : 'ISP',
            'SESSION_ID' : session.cookies['JSESSIONID'],
            'COMPLEX_SCHED' : '',
            'FORM_KEY' : '1523574968436',
            'ON_CLICK_NEW_BTN_TIME' : 'undefined',
            'SAVE_FAVORITE' : '',
            'FORM_TYPE' : 'ENII'
        }

        submission_time = datetime.datetime.utcnow()

        try:
            response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)

            if response.status_code != 200:
                print "%s - Error Posting EN2 NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting EN2 NOTAM" %(threading.current_thread().getName())
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
            submitted_en2_notams += 1

        submission_time = (datetime.datetime.utcnow() - submission_time).total_seconds()

        submitted_notams.append({'notamNumber':submission_response['notamNumber'],
                                 'transactionId':submission_response['transactionId'],
                                 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R'),
                                 'responsetime':submission_time})


        print "%s - EN2 NOTAM %d Submitted: NOTAM Number = %s Response Time = %d seconds" % (threading.current_thread().getName(), submitted_en2_notams, submission_response['notamNumber'], submission_time)

        time.sleep(delay)

        if (submitted_en2_notams % cancel_rate) == 0:

            time.sleep(60)

            session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

            for notams in submitted_notams:
                log_message = 'SUBMIT - '
                for k,v in notams.items():
                    log_message += '%s=%s    ' %(k, v)
                logger.info(log_message)

            item = submitted_notams.pop(0)

            del submitted_notams[:]

            cancel_data = '7|2|64|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|0196662329E3ED777244D915ABB428BD|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' \
                      'A9C9AB7C56FD2B82EF20831A6FE8ABA1|gov.faa.aim.dnotam.ui.client.AirportInformationService|cancelNotam|java.lang.String/2004016611|' \
                      'gov.faa.aim.dnotam.ui.dto.UserTO/1465918794|' + item['transactionId'] + '||[[Ljava.lang.String;/4182515373|[Ljava.lang.String;/2600011424|' \
                      '1|0|FPA|2|ABQ|4|COU|7|FTW|12|PNM|3|CSA-Central Area|ESA-Eastern Area|WSA-Western Area|http://notamdemo.aim.nas.faa.gov/en2plus/en2/index.html|' \
                      '5555555555|java.util.Date/3385151746|1523641648182|Anthony|172.26.22.194|Tompkins|Success|en2.test@faa.gov|Test123!|java.util.ArrayList/4159755760|' \
                      'gov.faa.aim.dnotam.ui.dto.UserPreference/1057420195|EXPIRY_NOTIFICATION_HRS|48|SHOWPAGINATION|YES|SHOWMAP|NO|ROWLIMIT|50|CANCEL_DAYS|' \
                      'gov.faa.aim.dnotam.ui.dto.En2UserRole/119278024|CSA|Central Area|SP|ESA|Eastern Area|WSA|Western Area|' \
                      'http://notamdemo.aim.nas.faa.gov/fns/file2?filename=en2sampleuserguide_Narmada.pdf|00ef75a1cfee275ee649b1f8784f|http://notamdemo.aim.nas.faa.gov/fnshelp/en2spluserguide.pdf|' \
                      'http://notamdemo.aim.nas.faa.gov/fnshelp/en2subuserguide.pdf|Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0|8003|' \
                      'FSS| Published|1|2|3|4|5|6|3|7|8|7|9|8|0|10|10|0|0|0|0|11|5|12|7|13|14|15|14|14|15|15|12|7|16|13|17|14|14|17|17|12|7|18|13|19|14|14|19|19|12|7|20|13|21|14|14|21|21|' \
                      '12|7|22|13|23|14|14|23|23|11|3|12|2|24|25|12|2|13|26|12|2|16|27|10|28|10|0|10|0|29|30|WLADvey|31|13|10|1|32|17|33|10|34|35|36|30|3|10|37|0|0|38|5|39|40|41|39|42|43|39|44' \
                      '|45|39|46|47|39|48|16|10|0|2|0|0|38|3|49|50|24|51|0|0|52|49|53|13|54|0|0|52|49|55|16|56|0|0|52|57|29|58|1|59|10|0|10|10|0|60|0|0|WLADvey|61|62|63|30|WLADvey|0|2018|10|64|'

            cancel_time = datetime.datetime.utcnow()

            try:
                response = session.post(cancel_url,verify=False,data=cancel_data, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Error Canceling NOTAM: %s" %(threading.current_thread().getName(), response.text)
                    time.sleep(30)
                    continue
            except:
                print "%s - Error Canceling NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue

            cancel_time = (datetime.datetime.utcnow() - cancel_time).total_seconds()

            canceled_en2_notams += 1

            print "%s - EN2 NOTAM %d Canceled: NOTAM Number = %s Response Time = %d seconds" %(threading.current_thread().getName(), canceled_en2_notams,item['notamNumber'], cancel_time)

            log_message = 'CANCEL - notamNumber=%s    responsetime=%d seconds' %(item['notamNumber'], cancel_time)
            logger.info(log_message)