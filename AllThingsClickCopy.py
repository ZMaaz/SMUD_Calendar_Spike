'''
.Description
Master Click Functions

.Version
-Steven On - Original Release - 20200425
'''
import os.path
import xml

import requests
import json
import xml.etree.ElementTree as ET

def helloWorld(message):
    print(message)

def prodSXPCheck(prod):
    # api-endpoint
    URL_Objects = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/IntegrationServices/sxpint.aspx"
    PRODURL_Objects = "https://fse-na-int01.cloud.clicksoftware.com/so/IntegrationServices/sxpint.aspx"
    if prod == 'True':
        return PRODURL_Objects
    else:
        return URL_Objects

def prodObjectCheck(prod):
    # api-endpoint
    URL_Objects = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/objects/"
    PRODURL_Objects = "https://fse-na-int01.cloud.clicksoftware.com/so/api/objects/"
    if prod == 'True':
        return PRODURL_Objects
    else:
        return URL_Objects

def prodMultiCheck(prod):
    # api-endpoint
    URL_Multi = "https://fse-na-sb-int01.cloud.clicksoftware.com/so/api/Services/Integration/ServiceOptimization/ExecuteMultipleOperations"
    PRODURL_Multi = "https://fse-na-int01.cloud.clicksoftware.com/so/api/Services/Integration/ServiceOptimization/ExecuteMultipleOperations"
    if prod == 'True':
        return PRODURL_Multi
    else:
        return URL_Multi

def deleteClickObject(objName, key, prod, username, password):
    url = prod + objName + '/' + str(key)
    print(url)
    try:
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.delete(url=url, headers=headers,auth=(username,password))
        print(r)
    except Exception as e:
        print(e)

def environmentUsr(environment):
    devUsr = "admin@smudsb"
    qaUsr = "admin@smudd2"
    testUsr = "admin@smudd3"
    prodUsr = "admin@smudp"
    if environment == "PROD":
        return prodUsr
    elif environment == "QA":
        return qaUsr
    elif environment == 'DEV':
        return devUsr
    else:
        return testUsr

def environmentPwd(environment):
    devPwd = "WellPhoClickSB-1"
    qaPwd = "WellPhoClickD2-1"
    testPwd = "WTPhoClickD3-1"
    prodPwd = "WellPhoClickP-1"
    if environment == "PROD":
        return prodPwd
    elif environment == "QA":
        return qaPwd
    elif environment == "DEV":
        return devPwd
    else:
        return testPwd


############# Functions ######################
# batch function
def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


############# Click Calls ######################

#Get Click object per CallID
def GetClickObject(obj, PARAMS, url, username, password):
    #print('Get Click Objects')
    #print(obj,PARAMS,url,username,password)
    print(url + obj + '?' + PARAMS)
    print(url)
    ObjList = []
    #Get REST Call
    try:
        from requests.auth import HTTPBasicAuth
        r = requests.get(url=url + obj + '?'+ PARAMS,auth=(username, password)) #Steven
        #r = requests.get(url,auth=(username, password)) #Mahrukh
        #print(r)

        print(r.status_code)
        if (r.status_code == 200 or r.status_code == 500):
            #convert string response to Python JSON
            data = r.json()
            #print(data)
            #print('object Size: ' + str(len(data)))
            #loop through objects and create an object List
            for item in data:
                ObjList.append(item)
            '''
            #Get object properties
            for item in data[0]:
                print(item)
            '''
            return ObjList
    except Exception as e:
        print(e)

#retrieve Key
def GetClickObjKey(objName, prop, value, username, password, url):
    try:
        from requests.auth import HTTPBasicAuth
        r = requests.get(url=url + objName + "?$filter=" + prop + " eq '" + value + "'", auth=(username, password))
        # print(r.status_code)
        if r.status_code == 200 or r.status_code == 500:
            data = r.json()
            # print('object Size: ' + str(len(data)))
            return data[0]["Key"]
    except Exception as e:
        print(e)

#Get Click Object count
def GetClickObjectCount(URL, PARAMS, obj,username, password):
    try:
        from requests.auth import HTTPBasicAuth
        r = requests.get(url = URL + obj + "?$top=1&$count=true" + PARAMS, auth=(username,password))
        print(URL + obj + "?$top=1&$count=true" + PARAMS)
        #print(r.status_code)
        if(r.status_code == 200 or r.status_code == 500):
            data = r.json()
            return data["Count"]
    except Exception as e:
        print(e)

#Get objects in batches
def GetClickObjectsBatch(obj,PARAMS, url, username, password):
    ObjList = []
    print('Get Click Object In Batch')
    BatchSize = 9999
    ObjCount = GetClickObjectCount(url, PARAMS,obj, username, password)
    print(url, PARAMS, obj, username, password)
    print(ObjCount)
    if ObjCount > BatchSize:
        print('Time to Batch!')
        # Chunk total asset count by 1000 and retrieve batches
        while (True):
            print('Batching ' + str(ObjCount) + ' items')
            i = 0
            for x in batch(range(0, ObjCount), BatchSize):
                rangeStr = str(x)
                ndx = rangeStr.split(',')[0].split('(')[1]
                runCount = rangeStr.split(',')[1].split(')')[0]
                try:
                    from requests.auth import HTTPBasicAuth
                    r = requests.get(url=url + obj + "?$top=" + str(BatchSize) + "&$skip=" + ndx + PARAMS, auth=(username, password))
                    # print(r.status_code)
                    if (r.status_code == 200 or r.status_code == 500):
                        data = r.json()
                        # print(data)
                        # print('object Size: ' + str(len(data)))
                        for item in data:
                            ObjList.append(item)
                except Exception as e:
                    print(e)
                print('... ' + runCount + ' items count')
            break
        return ObjList
    else:
        try:
            from requests.auth import HTTPBasicAuth
            r = requests.get(url=url + obj + "?$top=9999&$skip=0" + PARAMS,
                             auth=(username, password))
            # print(r.status_code)Yes
            if (r.status_code == 200 or r.status_code == 500):
                data = r.json()
                # print(data)
                # print('object Size: ' + str(len(data)))
                for item in data:
                    ObjList.append(item)
                return ObjList
        except Exception as e:
            print(e)

# update obj's in batches
def UpdateClickObjectsBatch(dataBatch, URL, username, password):
    print('Update Click Objects')
    ObjCount = len(dataBatch)
    if ObjCount > 99:
        print('Time to Batch!')
        # Chunk total asset count by 1000 and retrieve batches
        while (True):
            print('Batching ' + str(ObjCount) + ' items')
            i = 0
            for x in batch(range(0, ObjCount), 99):
                # Click's Api for Batching 100 at a time
                ExecuteMultipleOperations = {"OneTransaction": False, "ContinueOnError": True, "Operations": []}
                Operations = []
                for ndx in x:
                    Operation = {"Action": "CreateOrUpdate", "Object": dataBatch[ndx]}
                    Operations.append(Operation)
                ExecuteMultipleOperations["Operations"] = Operations

                try:
                    # Attempt a POST call to Click
                    from requests.auth import HTTPBasicAuth
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    print(json.dumps(ExecuteMultipleOperations))
                    # print(URL)
                    r = requests.post(URL, data=json.dumps(ExecuteMultipleOperations), headers=headers,
                                      auth=(username, password))
                    print(r.status_code)
                    if (r.status_code == 200 or r.status_code == 500):
                        res = r.text
                        print(res)
                    else:
                        res = r.text
                        print(res)
                except Exception as e:
                    print(e)
            break
    else:
        # Click's Api for Batching 100 at a time
        ExecuteMultipleOperations = {"OneTransaction": False, "ContinueOnError": True, "Operations": []}
        Operations = []
        for data in dataBatch:
            Operation = {"Action": "CreateOrUpdate", "Object": data}
            Operations.append(Operation)
        ExecuteMultipleOperations["Operations"] = Operations

        try:
            # Attempt a POST call to Click
            from requests.auth import HTTPBasicAuth
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            print(json.dumps(ExecuteMultipleOperations))
            # print(URL)
            r = requests.post(URL, data=json.dumps(ExecuteMultipleOperations), headers=headers,
                              auth=(username, password))
            print(r.status_code)
            if (r.status_code == 200 or r.status_code == 500):
                res = r.text
                print(res)
            else:
                res = r.text
                print(res)
        except Exception as e:
            print(e)

# update obj's in batches
def DeleteClickObjectsBatch(dataBatch, URL, username, password):
    print('Update Click Objects')
    ObjCount = len(dataBatch)
    if ObjCount > 99:
        print('Time to Batch!')
        # Chunk total asset count by 1000 and retrieve batches
        while (True):
            print('Batching ' + str(ObjCount) + ' items')
            i = 0
            for x in batch(range(0, ObjCount), 99):
                # Click's Api for Batching 100 at a time
                ExecuteMultipleOperations = {"OneTransaction": False, "ContinueOnError": True, "Operations": []}
                Operations = []
                for ndx in x:
                    Operation = {"Action": "Delete", "Object": dataBatch[ndx]}
                    Operations.append(Operation)
                ExecuteMultipleOperations["Operations"] = Operations

                try:
                    # Attempt a POST call to Click
                    from requests.auth import HTTPBasicAuth
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    print(json.dumps(ExecuteMultipleOperations))
                    # print(URL)
                    r = requests.post(URL, data=json.dumps(ExecuteMultipleOperations), headers=headers,
                                      auth=(username, password))
                    print(r.status_code)
                    if (r.status_code == 200 or r.status_code == 500):
                        res = r.text
                        print(res)
                    else:
                        res = r.text
                        print(res)
                except Exception as e:
                    print(e)
            break
    else:
        # Click's Api for Batching 100 at a time
        ExecuteMultipleOperations = {"OneTransaction": False, "ContinueOnError": True, "Operations": []}
        Operations = []
        for data in dataBatch:
            Operation = {"Action": "Delete", "Object": data}
            Operations.append(Operation)
        ExecuteMultipleOperations["Operations"] = Operations

        try:
            # Attempt a POST call to Click
            from requests.auth import HTTPBasicAuth
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            print(json.dumps(ExecuteMultipleOperations))
            # print(URL)
            r = requests.post(URL, data=json.dumps(ExecuteMultipleOperations), headers=headers,
                              auth=(username, password))
            print(r.status_code)
            if (r.status_code == 200 or r.status_code == 500):
                res = r.text
                print(res)
            else:
                res = r.text
                print(res)
        except Exception as e:
            print(e)

def UpdateClickObject(data, URL, username, password):
    print('Update Click Object')
    try:
        # Attempt a POST call to Click
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        print(json.dumps(data))
        print(URL)
        #r = requests.post(URL + 'Task', data=json.dumps(data), headers=headers, auth=(username, password)) #Steven
        r = requests.post(URL, data=json.dumps(data), headers=headers, auth=(username, password)) #Mahrukh
        print(r.status_code)
        if (r.status_code == 200 or r.status_code == 500):
            res = r.text
            print(res)
        else:
            res = r.text
            print(res)
    except Exception as e:
        print(e)

# update ESB, recovery for Click
def GetESBClickAPIEndPoints(environment, integration_message_type):
    # get the URL
    if environment == 'PROD':
        prodESBendpoints = {}
        prodESBURL = "https://smud.gateway.webmethodscloud.com/gateway/"
        prodESBAPIKey = "apiKey=a03ec85d-0a6f-4f00-9dfd-fa3a5bba35ee"
        prodESBendpoints.update({"NotificationClassCharUpdate": str(prodESBURL + "clicksoftware/1.0/deviceLocation?" + prodESBAPIKey)})
        prodESBendpoints.update({"NotificationCreate": str(prodESBURL + "clicksoftware/1.0/notification?" + prodESBAPIKey)})
        prodESBendpoints.update({"NotificationCreateFromOrder": str(prodESBURL + "clicksoftware/1.0/notification?" + prodESBAPIKey)})
        prodESBendpoints.update({"TaskStorage": str(prodESBURL + "clicksoftware/1.0/storeTask?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentCancelled": str(prodESBURL + "erp/1.0/workorder/operation/cancelled?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentCommentCreate": str(prodESBURL + "erp/1.0/workorder/operation/comments?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentCompleted": str(prodESBURL + "erp/1.0/workorder/operation/completed?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentDispatched": str(prodESBURL + "erp/1.0/workorder/operation/dispatched?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentIncomplete": str(prodESBURL + "erp/1.0/workorder/operation/incomplete?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentOn-Site": str(prodESBURL + "erp/1.0/workorder/operation/onsite?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentScheduled": str(prodESBURL + "erp/1.0/workorder/operation/scheduled?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentTravel": str(prodESBURL + "erp/1.0/workorder/operation/travel?" + prodESBAPIKey)})
        prodESBendpoints.update({"AssignmentUnscheduled": str(prodESBURL + "erp/1.0/workorder/operation/unscheduled?" + prodESBAPIKey)})
        return prodESBendpoints[integration_message_type]
    elif environment == 'QA':
        qaESBendpoints = {}
        qaESBURL = "https://smuddev.gateway.webmethodscloud.com/gateway/"
        qaESBAPIKey = "APIKey=c6fc72cc-526a-4439-a6e2-e35aad8155bb"
        qaESBendpoints.update({"NotificationClassCharUpdate": str(qaESBURL + "clicksoftware_test/1.0/deviceLocation?" + qaESBAPIKey)})
        qaESBendpoints.update({"NotificationCreate": str(qaESBURL + "clicksoftware_test/1.0/notification?" + qaESBAPIKey)})
        qaESBendpoints.update({"NotificationCreateFromOrder": str(qaESBURL + "clicksoftware_test/1.0/notification?" + qaESBAPIKey)})
        qaESBendpoints.update({"TaskStorage": str(qaESBURL + "clicksoftware_test/1.0/storeTask?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentCancelled": str(qaESBURL + "erp_test/1.0/workorder/operation/cancelled?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentCommentCreate": str(qaESBURL + "erp_test/1.0/workorder/operation/comments?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentCompleted": str(qaESBURL + "erp_test/1.0/workorder/operation/completed?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentDispatched": str(qaESBURL + "erp_test/1.0/workorder/operation/dispatched?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentIncomplete": str(qaESBURL + "erp_test/1.0/workorder/operation/incomplete?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentOn-Site": str(qaESBURL + "erp_test/1.0/workorder/operation/onsite?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentScheduled": str(qaESBURL + "erp_test/1.0/workorder/operation/scheduled?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentTravel": str(qaESBURL + "erp_test/1.0/workorder/operation/travel?" + qaESBAPIKey)})
        qaESBendpoints.update({"AssignmentUnscheduled": str(qaESBURL + "erp_test/1.0/workorder/operation/unscheduled?" + qaESBAPIKey)})
        return qaESBendpoints[integration_message_type]
    elif environment == 'DEV':
        devESBendpoints = {}
        devESBURL = "https://smuddev.gateway.webmethodscloud.com/gateway/"
        devESBAPIKey = "APIKey=c6fc72cc-526a-4439-a6e2-e35aad8155bb"
        devESBendpoints.update({"NotificationClassCharUpdate": str(devESBURL + "clicksoftware/1.0/deviceLocation?" + devESBAPIKey)})
        devESBendpoints.update({"NotificationCreate": str(devESBURL + "clicksoftware/1.0/notification?" + devESBAPIKey)})
        devESBendpoints.update({"NotificationCreateFromOrder": str(devESBURL + "clicksoftware/1.0/notification?" + devESBAPIKey)})
        devESBendpoints.update({"TaskStorage": str(devESBURL + "clicksoftware/1.0/storeTask?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentCancelled": str(devESBURL + "erp/1.0/workorder/operation/cancelled?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentCommentCreate": str(devESBURL + "erp/1.0/workorder/operation/comments?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentCompleted": str(devESBURL + "erp/1.0/workorder/operation/completed?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentDispatched": str(devESBURL + "erp/1.0/workorder/operation/dispatched?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentIncomplete": str(devESBURL + "erp/1.0/workorder/operation/incomplete?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentOn-Site": str(devESBURL + "erp/1.0/workorder/operation/onsite?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentScheduled": str(devESBURL + "erp/1.0/workorder/operation/scheduled?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentTravel": str(devESBURL + "erp/1.0/workorder/operation/travel?" + devESBAPIKey)})
        devESBendpoints.update({"AssignmentUnscheduled": str(devESBURL + "erp/1.0/workorder/operation/unscheduled?" + devESBAPIKey)})
        return devESBendpoints[integration_message_type]

def UpdateClickToESB(environment, messagetype, data, username, password):
    print('Updating ESB with Click Data')
    try:
        # Attempt a POST call to Click
        from requests.auth import HTTPBasicAuth
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # print(json.dumps(data))
        print(GetESBClickAPIEndPoints(environment, messagetype))
        r = requests.post(GetESBClickAPIEndPoints(environment, messagetype), data=json.dumps(data), headers=headers)
        print(r.status_code)
        if (r.status_code == 200 or r.status_code == 500):
            res = r.text
            print(res)
            print(r.status_code)
        else:
            res = r.text
            print(res)
            print(r.status_code)
    except Exception as e:
        print(e)

#Send SXP Request
def GetSXPGeocodeAddress(url, username, password, street, city="", postcode=""):
    rtnMessage = ''
    try:
        headers = {"content-type": "application/xml;charset=utf-8"}
        body = '<SXPGeocodeAddress Revision="7.5.0">'
        body += '<Location>'
        body += '<Street>'+ street +'</Street>'
        body += '<City>'+ city +'</City>'
        body += '<State>CA</State>'
        body += '<PostCode>'+postcode+'</PostCode>'
        body += '<Country>US</Country>'
        body += '</Location>'
        body += '</SXPGeocodeAddress>'

        response = requests.post(url, data=body, headers=headers, auth=(username, password))
        root = ET.fromstring(response.content)
        for result in root:
            for item in result:
                if item.tag == 'NumOfMatchesFound':
                    if int(item.text) < 1:
                        rtnMessage = 'No Lat/Lon'
                        return rtnMessage
                if item.tag == 'Locations':
                    for locations in item:
                        for location in locations:
                            if location.tag == 'Street':
                                if location.text is not None:
                                    rtnMessage = location.text
                                else:
                                    rtnMessage = street
                            if location.tag == 'Latitude':
                                rtnMessage = rtnMessage + ',' + location.text
                            if location.tag == 'Longitude':
                                rtnMessage = rtnMessage + ',' + location.text
    except Exception as e:
        rtnMessage = 'Error: ' + str(e)
    return rtnMessage

def SplitLogFiles(SourceFile, OutputFileName, NumberOfLines=8000):
    # split the path
    RootPath = os.path.split(SourceFile)
    with open (SourceFile, 'rb') as fin:
        foutName = RootPath[0] + '/' + OutputFileName + '.txt'
        fout = open(foutName, "wb")
        for i,line in enumerate(fin):
            fout.write(line)
            if (i+1)%NumberOfLines == 0:
                fout.close()
                foutName = RootPath[0] + '/' + OutputFileName + "%d.txt"%(i/NumberOfLines+1)
                fout = open(foutName, "wb")
        fout.close()
    print('Split file competed!')
