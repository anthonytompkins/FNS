import requests
import json, urllib, time, re, gzip, datetime, random, string

proxies = { 'http': 'http://localhost:8585', 'https': 'http://localhost:8585'}
#proxies = None

# URLs
home_url = "https://notamdemo.aim.nas.faa.gov/en2plus/"
xsrf_url = "https://notamdemo.aim.nas.faa.gov/en2plus/en2/xsrf"
login_url = "https://notamdemo.aim.nas.faa.gov/en2plus/en2/airportInfoService"
form_url = "https://notamdemo.aim.nas.faa.gov/en2plus/en2/dnotamFormHandler"
utiltiy_url = "https://notamdemo.aim.nas.faa.gov/en2plus/en2/utilityService"

# login email
username = "en2.test@faa.gov"
# password
password = "Test123!"

submitted_notams = []

xsrf_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|E1EF26ED6384B9AF4934C71870F2E259|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

utility_data = '7|0|4|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|8C30C5E7368E7D64D2853D893E5C2495|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'
# A request session
session = requests.Session()

session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0'})

session.headers.update ({'host':'notamdemo.aim.nas.faa.gov'})

session.headers.update ({'Referer':'https://notamdemo.aim.nas.faa.gov/en2plus/'})


response = session.get(home_url, verify=False, proxies=proxies)
print response.status_code
print response.text

for i in range(1):

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

    response = session.post(utiltiy_url, data=utility_data, verify=False, proxies=proxies)
    print response.status_code
    print response.text

    session.cookies.update( { 'JSESSIONIDXSRF3N2':'330581523574837336' } )

    response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)
    print response.status_code
    xsrfToken = json.loads ( response.text.lstrip('//OK') )

    login_data = '7|2|9|https://notamdemo.aim.nas.faa.gov/en2plus/en2/|0196662329E3ED777244D915ABB428BD|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + \
                 '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|'\
                 + username + '|' + password + '|1|2|3|4|5|6|2|7|7|8|9|'


    response = session.post(login_url,verify=False,data=login_data, proxies=proxies)
    print response.status_code
    print response.text.lstrip('//OK')

    session.headers.update ( { 'Content-Type':'application/x-www-form-urlencoded' } )


    start_date = datetime.datetime.utcnow()
    end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=4))
    start_time = '%02d%02d' %(datetime.datetime.utcnow().hour, (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).minute)
    end_time = '%02d%02d' %((datetime.datetime.utcnow() + datetime.timedelta(hours=4)).hour, (datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,5))).minute)
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


    response = session.post(form_url,verify=False,data=notam_data, proxies=proxies)
    print response.status_code
    notam_response = response.text.encode('ascii','ignore')

    print notam_response

    notam_response = notam_response.lstrip("MessageTO").replace('[','').replace(']','')

    print notam_response

    items = [i.strip() for i in notam_response.split('~')]
    items = [i.split('=') for i in items]

    print items

    submission_response = {}

    for item in items:
        if item.__len__() == 2:
            submission_response[item[0]] = item[1]

    if submission_response['errorCode'] != '0':
        continue

    print 'notamNumber: ' + submission_response['notamNumber']
    print 'transactionId: ' + submission_response['transactionId']
    print 'timestamp: ' + datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R')


    submitted_notams.append({'notamNumber':submission_response['notamNumber'], 'transactionId':submission_response['transactionId'], 'timestamp':datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R')})

    print submitted_notams

    time.sleep(20)


session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

for item in submitted_notams:

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


    time.sleep(10)

    response = session.post(login_url,verify=False,data=cancel_data, proxies=proxies)

    print response.status_code

    cancel_response = json.loads ( response.text.lstrip('//OK') )

    print cancel_response
