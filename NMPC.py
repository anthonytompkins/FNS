import requests, os, threading, logging
import json, time, datetime, random
from urlparse import urlparse

def nmpc_generator(_home_url,_username,_password,_project_id, _notams,_length,_delay,_cancel_rate,_log_file_path):

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

    project_id = _project_id

    # URLs
    if _home_url[-1] != '/':
        _home_url += '/'

    home_url = _home_url
    login_url = home_url + "action/user/login"
    form_url = home_url + "action/notam/publish"
    project_url = home_url + "action/notam/listByProject?projectId=" + project_id
    cancel_url = home_url + "action/notam/cancelNotams"

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

    submitted_nmpc_notams = 0
    canceled_nmpc_notams = 0

    # A request session
    session = requests.Session()

    session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0',
                            'host': urlparse(home_url).netloc,
                            'Referer': home_url})

    try:
        response = session.get(home_url, verify=False, proxies=proxies)

        if response.status_code != 200:
            print "%s - Error Getting NMPC Home URL" %(threading.current_thread().getName())
            time.sleep(30)
            exit(1)
    except:
        print "%s - Error Getting NMPC Home URL" %(threading.current_thread().getName())
        time.sleep(30)
        exit(1)

    while submitted_nmpc_notams < notams_to_submit:

        session.headers.update(
            {'Accept': 'text/plain, application/json, */*',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate, br',
             'Content-Type': 'application/json;charset=utf-8',
             'Referer': 'https://notamdemo.aim.nas.faa.gov/nmpc/'
             }
        )


        login_data = {'email' : username, 'password' : password }

        try:
            response = session.post(login_url,verify=False,json=login_data, proxies=proxies)

            if response.status_code != 200 or 'Exception' in response.text:
                print "%s - Error Posting NMPC Login Data" %(threading.current_thread().getName())
                time.sleep(30)
                os._exit(1)
        except:
            print "%s - Error Posting NMPC Login Data" %(threading.current_thread().getName())
            time.sleep(30)
            os._exit(1)

        session.headers.update ( { 'Referer': 'https://notamdemo.aim.nas.faa.gov/nmpc/pages/scenario_IAP_TEMP.html' } )

        start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
        end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=length,minutes=random.randint(1,20)))
        start_time = '%02d%02d' %(start_date.hour, start_date.minute)
        end_time = '%02d%02d' %(end_date.hour, end_date.minute)

        notam_data = {
            'procedures':[{'name':'BRIDGE VISUAL RWY 29','printableVersionNumber':'1','status':'ACTIVE','startdate':'09/18/2014','featureid':'8288553','selected':'true'},
                          {'name':'STADIUM VISUAL RWY 29','printableVersionNumber':'3','status':'ACTIVE','startdate':'06/25/2015','featureid':'8651938','selected':'false'}],
            'airportId':'EWR',
            'projectId': project_id,
            'scenario':'IAP_TEMP',
            'keyword':'VFP',
            'minimums':'Minimums',
            'minimumsException':'',
            'minimumsExceptionText':'',
            'procChangeNote':'',
            'procEquipment':'',
            'procChangeNoteException':'',
            'procChangeNoteExceptionText':'',
            'startAsap':'Y',
            'permanent':'N',
            'estimated':'Y',
            'selectedProcedures':{'name':'BRIDGE VISUAL RWY 29','printableVersionNumber':'1','status':'ACTIVE','startdate':'09/18/2014','featureid':'8288553','selected':'true'},
            'procedureChangeTypes':[{'name':'Procedure NA','selected':'false'},
                                    {'name':'Alternate Minimums NA','selected':'false'},
                                    {'name':'Straight-in Minimums NA','selected':'false'},
                                    {'name':'Circling Minimums NA','selected':'false'},
                                    {'name':'Additional Equipment Required','selected':'false'}],
            'procedureChangeType':'{}',
            'tempObstacles':[],
            'missedApproaches':[],
            'notes':[],
            'rwyNotes':[],
            'fixMinimums':[],
            'additionalNotes':[],
            'otherNotes':[],
            'locId':'4601',
            'scenarioId':'807',
            'startDate': start_date.strftime('%y%m%d%H%M'),
            'endDate': end_date.strftime('%y%m%d%H%M'),
            'domesticFormat':'!FDC X/XXXX EWR VFP NEWARK LIBERTY INTL, Newark, NJ.\nBRIDGE VISUAL RWY 29, AMDT 1...\nMINIMUMS.\n%s%s-%s%sEST'
                             %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'icaoFormat':'Q) ZNY/QPKXX/V/NBO/A/000/999/4041N07410W025\nA) KEWR\nB) %s%s\nC) %s%sEST\nE) VFP NEWARK LIBERTY INTL, Newark, NJ.\nBRIDGE VISUAL RWY 29, AMDT 1...\nMINIMUMS.\n'
                         %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'plainTextFormat':'Affected Facility: EWR,NEWARK LIBERTY INTL, Newark, NJ.\nNOTAM Number:  X/XXXX\n Effective Time Frame\nValid From: %s%s\nValid To: %s%sEST\nProcedure Affected: Visual Flight Procedure\nBRIDGE VISUAL RWY 29, AMDT 1...\nMINIMUMS.\n'
                              %(start_date.strftime('%y%m%d'), start_time, end_date.strftime('%y%m%d'), end_time),
            'featureId':'8288553',
            'obstacles':'',
            'contacts':[],
            'teamId':'10',
            'distList':''
        }

        submission_time = datetime.datetime.utcnow()

        try:
            response = session.post(form_url,verify=False,json=notam_data, proxies=proxies)

            #print '%s - %s' %(threading.current_thread().getName(), response.text)

            if response.status_code != 200:
                print "%s - Error Posting NMPC NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue
        except:
            print "%s - Error Posting NMPC NOTAM" %(threading.current_thread().getName())
            time.sleep(30)
            continue

        submission_response = json.loads(response.text)

        if submission_response['code'] != 0:
            print response.text
            continue
        else:
            submitted_nmpc_notams += 1

        submission_time = (datetime.datetime.utcnow() - submission_time).total_seconds()

        submission_response = {'notamNumber': submission_response['notamNumber'].encode('ascii', 'ignore'),
                               'code': submission_response['code'],
                               'timestamp': datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R'),
                               'responsetime': submission_time
                               }

        session.headers.update(
            {'Referer': 'https://notamdemo.aim.nas.faa.gov/nmpc/pages/notamList.html?projectId=' + project_id + '&uid=15jc4wevw'})

        notam_num_found = False

        while notam_num_found == False:

            try:
                response = session.get(project_url, verify=False, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Error Getting NMPC Project Data" %(threading.current_thread().getName())
                    time.sleep(30)
                    continue
            except:
                print "%s - Error Getting NMPC Project Data" %(threading.current_thread().getName())
                time.sleep(30)
                continue

            project_response = json.loads(response.text)

            for project in project_response:
                if project.get('notamnumber') != None and submission_response['notamNumber'] == project['notamnumber'].encode('ascii','ignore'):
                    submission_response['transactionId'] = project['transactionid']
                    notam_num_found = True
                    submitted_notams.append(submission_response)
                    break

        print "%s - NMPC NOTAM %d Submitted: NOTAM Number = %s Response Time = %d seconds" % (threading.current_thread().getName(), submitted_nmpc_notams, submission_response['notamNumber'], submission_time)

        time.sleep(delay)

        if (submitted_nmpc_notams % cancel_rate) == 0:

            time.sleep(60)

            for notams in submitted_notams:
                log_message = 'SUBMIT - '
                for k,v in notams.items():
                    log_message += '%s=%s    ' %(k, v)
                logger.info(log_message)

            item = submitted_notams.pop(0)

            del submitted_notams[:]

            cancel_data = {'transactionIds':[item['transactionId']],'reason':'Facility Return to Service'}

            cancel_time = datetime.datetime.utcnow()

            try:
                response = session.post(cancel_url,verify=False,json=cancel_data, proxies=proxies)

                if response.status_code != 200:
                    print "%s - Error Canceling NMPC NOTAM" %(threading.current_thread().getName())
                    time.sleep(30)
                    continue
            except:
                print "%s - Error Canceling NMPC NOTAM" %(threading.current_thread().getName())
                time.sleep(30)
                continue

            cancel_time = (datetime.datetime.utcnow() - cancel_time).total_seconds()

            canceled_nmpc_notams += 1

            print "%s - NMPC NOTAM %d Canceled: NOTAM Number = %s Response Time = %d seconds" % (threading.current_thread().getName(), canceled_nmpc_notams, item['notamNumber'], cancel_time)

            log_message = 'CANCEL - notamNumber=%s    responsetime=%d seconds' % (item['notamNumber'], cancel_time)
            logger.info(log_message)


