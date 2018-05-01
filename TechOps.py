import requests
import json, urllib, time, re, gzip, datetime, random, urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = { 'http': 'http://localhost:8585', 'https': 'http://localhost:8585'}
proxies = None

# URLs
home_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/#1"
xsrf_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/xsrf"
login_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/airportInfoService"
form_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/dnotamFormHandler"
utility_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/utilityService"
cancel_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/airportInfoService"

# login email
username = "nmtech.test@faa.gov"
# password
password = "Test123!"

submitted_notams = []
canceled_notams = []

submitted_techops_notams = 0
canceled_techops_notams = 0

xsrf_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|CCA65B31464BDB27545C23C142FEEEF8|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

utility_data = '7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|478CF164B5FD1D3E43383F3E499124D9|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'

# A request session
session = requests.Session()

session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

session.headers.update ({'host':'notamdemo.aim.nas.faa.gov'})

session.headers.update ({'Referer':'https://notamdemo.aim.nas.faa.gov/dnotamtest/'})


try:
    response = session.get(home_url, verify=False, proxies=proxies)

    if response.status_code != 200:
        print "Error Getting TechOps Home URL"
        time.sleep(30)
        exit(1)
except:
    print "Error Getting TechOps Home URL"
    time.sleep(30)
    exit(1)

for i in range(10):

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
            print "Error Posting TechOps Utility Data"
            time.sleep(30)
            continue
    except:
        print "Error Posting TechOps Utility Data"
        time.sleep(30)
        continue

    session.cookies.update( { 'JSESSIONIDXSRFH':'317101520124880832' } )

    try:
        response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)

        if response.status_code != 200:
            print "Error Posting TechOps XSRF Data"
            time.sleep(30)
            continue
    except:
        print "Error Posting TechOps XSRF Data"
        time.sleep(30)
        continue

    xsrfToken = json.loads ( response.text.lstrip('//OK') )

    login_data = '7|2|9|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + \
                 '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|'\
                 + username + '|' + password +'|1|2|3|4|5|6|4|7|7|7|7|8|9|4|0|'

    try:
        response = session.post(login_url,verify=False,data=login_data, proxies=proxies)

        if response.status_code != 200:
            print "Error Posting TechOps Login Data"
            time.sleep(30)
            continue
    except:
        print "Error Posting TechOps Login Data"
        time.sleep(30)
        continue

    session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )

    start_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,20))
    end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=4,minutes=random.randint(1,20)))
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
        'USER_ID' : ['8004','Anthony Tompkins'],
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

    try:
        response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)

        if response.status_code != 200:
            print "Error Posting TechOps NOTAM"
            time.sleep(30)
            continue
    except:
        print "Error Posting TechOps NOTAM"
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
        print response.text
        continue
    else:
        submitted_techops_notams += 1

    submitted_notams.append({'notamNumber':submission_response['notamNumber'], 'transactionId':submission_response['transactionId'], 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R')})

    print "TechOps Submitted NOTAMS: %d" %(submitted_techops_notams)

    time.sleep(2)

    if (submitted_techops_notams % 10) == 0:

        time.sleep(60)

        session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

        item = submitted_notams.pop(0)

        cancel_data = '7|2|83|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|' \
                  'com.google.gwt.user.client.rpc.XsrfToken/4254043109|6662D02745FB83DF3C87D3EB478A29C1|gov.faa.aim.dnotam.ui.client.AirportInformationService|' \
                  'cancelNotam|java.lang.String/2004016611|gov.faa.aim.dnotam.ui.dto.UserTO/1159427881|'+ item['transactionId'] +'||[[Ljava.lang.String;/4182515373|[Ljava.lang.String;' \
                  '/2600011424|11|0|Classification-All|-1|12|Communications|22|COM|1|13|Lighted Aids|75|LIGHTED AID|2|14|Navaids|25|NAV|3|15|Radar|76|RADAR|4|16|Weather' \
                  '|77|WEATHER|5|43|Obstruction|OBST|18|AOCC-Atlantic OCC|10|MOCC-Mid States OCC|20|POCC-Pacific OCC|http://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/index.html' \
                  '|5555555555|java.util.Date/3385151746|Anthony|http://notamdemo.aim.nas.faa.gov/fnshelp/nmoccuserguide.pdf|172.26.22.194|FAA|Tompkins|Success' \
                  '|nmtech.test@faa.gov|Test123!|java.util.ArrayList/4159755760|gov.faa.aim.dnotam.ui.dto.UserPreference/1057420195|EXPIRY_NOTIFICATION_HRS|48|SHOWPAGINATION|YES|SHOWMAP' \
                  '|NO|ROWLIMIT|50|CANCEL_DAYS|gov.faa.aim.dnotam.ui.dto.UserRole/1873077557|OCC|AOCC|Atlantic OCC|MOCC|Mid States OCC|POCC|Pacific OCC|5612f2315bb61cf410caf1636ea5' \
                  '|Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0|8004|1|2|3|4|5|6|3|7|8|7|9|8|0|10|10|0|0|0|11|7|12|8|13|14|15|14|14|0|15|16|12|8|17|13|18' \
                  '|14|19|20|18|21|12|8|22|13|23|14|24|25|23|26|12|8|27|13|28|14|29|30|28|31|12|8|32|13|33|14|34|35|33|36|12|8|37|13|38|14|39|40|38|41|12|8|42|13|43|14|14|44|43|45|11|3|12|2|32' \
                  '|46|12|2|47|48|12|2|49|50|10|0|51|10|10|0|52|0|53|WK1YS_P|11|10|0|54|55|15|56|57|58|0|32|0|59|60|0|44|3|0|0|10|61|0|0|90|62|5|63|64|65|63|66|67|63|68|69|63|70|71|63|72|26|10' \
                  '|0|0|32|0|62|3|73|74|65|0|74|0|0|0|75|15|76|0|0|0|0|0|0|0|73|74|65|0|74|0|0|0|77|10|78|0|0|0|0|0|0|0|73|74|65|0|74|0|0|0|79|20|80|0|0|0|0|0|0|0|28|81|0|0|0|10|0|10|10|0|' \
                  'WK1YS_P|82|83|74|53|WK1YS_P|0|4|2018|10|10|'

        try:
            response = session.post(cancel_url,verify=False,data=cancel_data, proxies=proxies)

            if response.status_code != 200:
                print "Error Canceling TechOps NOTAM"
                time.sleep(30)
                continue
        except:
            print "Error Canceling TechOps NOTAM"
            time.sleep(30)
            continue

        canceled_notams.append(item)

        canceled_techops_notams += 1

        print "TechOps Canceled NOTAMS: %d" %(canceled_techops_notams)
