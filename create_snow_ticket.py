
# CodeFest 2020

#MIT License

#Copyright (c) 2020 Phil Selker

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.



import requests
import json
import config

from config import SNOW_URL, SNOW_TABLE, SNOW_ADMIN, SNOW_PASS

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # Disable insecure https warnings

def create_incident(description, shortdescription, priority):

    # This function will create a new incident and add showtech.txt file

    url = SNOW_URL + '/table/' + SNOW_TABLE
    payload = {'description': description,
               'short_description': shortdescription,
               'priority': priority
               }
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response = requests.post(url, auth=(SNOW_ADMIN, SNOW_PASS), data=json.dumps(payload), headers=headers)
    
    print('\nServiceNow REST API call response: ' + str(response.status_code))
    
    incident_json = response.json()
    sys_id = incident_json['result']['sys_id']
    
    print('\nIncident sys_id: ' + str(sys_id))
    
    ## use the sys_id of the record to POST the showtech.txt file to the new ticket
    
    url = SNOW_URL + '/attachment/file?table_name=' + SNOW_TABLE + '&table_sys_id=' + sys_id + '&file_name=showtech.txt' 
    
    # read the file contents into filecontents
    filecontents = open('/bootflash/tech.txt', 'r').read()
   
    headers = {'Content-Type': 'test/plain', 'Accept': 'application/json'}
    response = requests.post(url, auth=(SNOW_ADMIN, SNOW_PASS), data=filecontents, headers=headers)
    
    print('\nServiceNow REST API call response: ' + str(response.status_code))
   
    # Decode the JSON response 
    rdata = response.json()
    print(rdata)
    
    return 


# main application


comments = ('The CSR 1000 created this incident using APIs \n\n RECOMMENDED ACTION:  Call Cisco TAC and open a case.\n\n Call 800-553-2447 or click: https://cisco.com/go/support \n Provide relevant details and add the showtech.txt file at the top of this ticket to the TAC case')
incident = create_incident(comments, 'CSR 1000 Device HRN57 Notification -  Critical problem with an interface', 1)

print('Created ServiceNow Incident')

print('\nEnd Application Run')
