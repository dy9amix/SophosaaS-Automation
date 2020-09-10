import time
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from enum import Enum
from apiCalls.prox_create_vm import createVM
from apiCalls.prox_token_generate import generateToken
from apiCalls.sophos_interface import configureInterface
from apiCalls.prox_delete_vm import deleteVM
from apiCalls.listSubscribers import listSubscribers
from apiCalls.start_vm import startVM, stopVM
from apiCalls.configure_vlan import configure_vlan

app = FastAPI()

################CORS###############################
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
###################################################

#############Authentication Script#################
SECRET_KEY = "625712595e6a626d28899169059330437e354daada28067281922d90120fb0bb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "testadmin": {
        "username": "testadmin",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$ffTjmxj6fiSTYaWIuzkH8.Wj6hl.Xj.1aqXvb4dBn6qq53Z9sLusO",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


###########End of Script##########################

class Input(BaseModel):
    name: str
    lanIP: str
    lanSubnet: str
    wanIP: str
    wanSubnet: str
    wanGateway: str
    vlan_ID: int

class deleteInput(BaseModel):
    subscriberName: str


@app.post("/createsubscriber")
def newclient(input: Input, token: str = Depends(oauth2_scheme)):
    vmiD = input.vlan_ID + 100
    authData = generateToken()
    token = authData['data']['CSRFPreventionToken']
    ticket = authData['data']['ticket']
    createVM(csrfToken=token, authCookie=ticket, client_name=input.name, vmId=vmiD)
    time.sleep(140)
    configure_vlan(vmID=vmiD, vlan=input.vlan_ID)
    time.sleep(60)
    startVM(csrfToken=token, authCookie=ticket, vmId=vmiD)
    time.sleep(120)
    print('LAN:',input.lanIP,'LAN')
    Interface_result = configureInterface(lanIP=input.lanIP,lanSubnet=input.lanSubnet,
                                            wanIP=input.wanIP,wanSubnet=input.wanSubnet,wanGateway=input.wanGateway)
    print(Interface_result)
    return {"message" : f"Deployment complete. Please open https://{input.lanIP}:4444 to register this subscriber"}


@app.post("/decommission")
def decommission(inputVal:deleteInput, token: str = Depends(oauth2_scheme)):
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
        stopVM(csrfToken=token, authCookie=ticket, vmId=val)
        time.sleep(60)
        deleteVM(token=token, ticket=ticket, vmID=val)
    return {"message":"Subscriber successfully deleted"}
