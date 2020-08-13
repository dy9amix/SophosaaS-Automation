import time
from fastapi import FastAPI
from typing import List
from pydantic import BaseModel
from apiCalls.prox_create_vm import createVM
from apiCalls.prox_token_generate import generateToken
from apiCalls.sophos_interface import configureInterface
from apiCalls.prox_delete_vm import deleteVM
from apiCalls.listSubscribers import listSubscribers
from apiCalls.start_vm import startVM
app = FastAPI()

class Input(BaseModel):
    name: str
    Id : int
    lanIP: str
    lanSubnet: str
    wanIP: str
    wanSubnet: str
    wanGateway: str

class deleteInput(BaseModel):
    subscriberName: str

@app.post("/createsubscriber")
def newclient(input: Input):
    authData = generateToken()
    token = authData['data']['CSRFPreventionToken']
    ticket = authData['data']['ticket']
    createVM(csrfToken=token, authCookie=ticket, client_name=input.name, vmId=input.Id)
    time.sleep(240)
    startVM(csrfToken=token, authCookie=ticket, vmId=input.Id)
    Interface_result = configureInterface(lanIP=input.lanIP,lanSubnet=input.lanSubnet,wanIP=input.wanIP,wanSubnet=input.wanSubnet,wanGateway=input.wanGateway)
    print(Interface_result)
    return {"message" : f"Deployment complete. Please open https://{input.lanIP}:4444 to complete this deployment"}

@app.post("/decommission")
def decommission(inputVal:deleteInput):
    val = None
    authData = generateToken()
    token = authData['data']['CSRFPreventionToken']
    ticket = authData['data']['ticket']
    subscribersList = listSubscribers(csrf_token=token, auth_ticket=ticket)
    for n in subscribersList['data']:
        if n['name']==inputVal.subscriberName:
            val = int(n['vmid'])
    if val == None:
        raise Exception("Subscriber not Found check the name and try again")
    else:
        deleteVM(token=token, ticket=ticket, vmID=val)
    return {"message":"Subscriber successfully deleted"}