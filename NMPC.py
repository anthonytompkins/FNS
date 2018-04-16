import requests
import json, urllib, time, re, gzip, datetime, random

proxies = { 'http': 'http://localhost:8585', 'https': 'http://localhost:8585'}
#proxies = None

# URLs
home_url = "https://notamdemo.aim.nas.faa.gov/nmpc/"
xsrf_url = "https://notamdemo.aim.nas.faa.gov/nmpc/action/user/login"
login_url = "https://notamdemo.aim.nas.faa.gov/nmpc/action/user/login"
form_url = "https://notamdemo.aim.nas.faa.gov/nmpc/action/notam/publish"
utiltiy_url = "https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/utilityService"

# login email
username = "nmpc.test@faa.gov"
# password
password = "Test123!"

submitted_notams = []

xsrf_data = "7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|CCA65B31464BDB27545C23C142FEEEF8|com.google.gwt.user.client.rpc.XsrfTokenService|getNewXsrfToken|1|2|3|4|0|"

utility_data = '7|0|4|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|478CF164B5FD1D3E43383F3E499124D9|gov.faa.aim.dnotam.ui.client.UtilityService|getLogFileLocations|1|2|3|4|0|'
# A request session
session = requests.Session()

session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:39.0) Gecko/20100101 Firefox/39.0',
                        'host':'notamdemo.aim.nas.faa.gov',
                        'Referer':'https://notamdemo.aim.nas.faa.gov/nmpc/'})


response = session.get(home_url, verify=False, proxies=proxies)
print response.status_code
print response.text

for i in range(1):

    session.headers.update(
        {'Accept': 'text/plain, application/json, */*',
         'Accept-Language': 'en-US,en;q=0.5',
         'Accept-Encoding': 'gzip, deflate, br',
         'Content-Type': 'application/json;charset=utf-8',
         #'X-GWT-Permutation': '91DAC5113A41AD9FACB523FF735B4CB6',
         #'X-GWT-Module-Base': 'https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/',
         'Referer': 'https://notamdemo.aim.nas.faa.gov/nmpc/'
         }
    )

    #response = session.post(utiltiy_url, data=utility_data, verify=False, proxies=proxies)
    #print response.status_code
    #print response.text

    #session.cookies.update( { 'JSESSIONIDXSRFH':'317101520124880832' } )

    #response = session.post(xsrf_url,verify=False,data=xsrf_data, proxies=proxies)
    #print response.status_code
    #xsrfToken = json.loads ( response.text.lstrip('//OK') )

    #login_data = '7|2|9|https://notamdemo.aim.nas.faa.gov/dnotamtest/dnotam/|1D09985EB283A7F23DE6CEA240EECD6F|com.google.gwt.user.client.rpc.XsrfToken/4254043109|' + xsrfToken[2][1] + '|gov.faa.aim.dnotam.ui.client.AirportInformationService|performLogin|java.lang.String/2004016611|load.test@airports.com|Password123!|1|2|3|4|5|6|4|7|7|7|7|8|9|4|0|'
    login_data = {'email' : username, 'password' : password }

    response = session.post(login_url,verify=False,json=login_data, proxies=proxies)
    print response.status_code
    login_response = json.loads ( response.text )

    print login_response

    session.headers.update ( { 'Referer': 'https://notamdemo.aim.nas.faa.gov/nmpc/pages/scenario_IAP_TEMP.html' } )

    start_date = datetime.datetime.utcnow()
    end_date = (datetime.datetime.utcnow() + datetime.timedelta(hours=4))
    start_time = '%02d%02d' %(datetime.datetime.utcnow().hour, (datetime.datetime.utcnow() + datetime.timedelta(minutes=1)).minute)
    end_time = '%02d%02d' %((datetime.datetime.utcnow() + datetime.timedelta(hours=4)).hour, (datetime.datetime.utcnow() + datetime.timedelta(minutes=random.randint(1,5))).minute)

    notam_data = {
        'procedures':[{'name':'BRIDGE VISUAL RWY 29','printableVersionNumber':'1','status':'ACTIVE','startdate':'09/18/2014','featureid':'8288553','selected':'true'},
                      {'name':'STADIUM VISUAL RWY 29','printableVersionNumber':'3','status':'ACTIVE','startdate':'06/25/2015','featureid':'8651938','selected':'false'}],
        'airportId':'EWR',
        'projectId':'697',
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


    response = session.post(form_url,verify=False,json=notam_data, proxies=proxies)
    print response.status_code
    submission_response = json.loads(response.text)

    submission_response = {'notamNumber':submission_response['notamNumber'].encode('ascii','ignore'), 'code':submission_response['code'], 'timestamp': datetime.datetime.utcnow().strftime('%A, %B %e, %Y %R')}

    print submission_response

    if submission_response['code'] != 0:
        continue

    print 'notamNumber: ' + submission_response['notamNumber']
    print 'timestamp: ' + submission_response['timestamp']

    submitted_notams.append(submission_response)

    print submitted_notams

    time.sleep(20)

session.headers.update ( { 'Content-Type':'text/x-gwt-rpc; charset=utf-8' } )

for item in submitted_notams:

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


    time.sleep(10)

    response = session.post(login_url,verify=False,data=cancel_data, proxies=proxies)

    print response.status_code

    cancel_response = json.loads ( response.text.lstrip('//OK') )

    print cancel_response
