import json
import requests
import hashlib 
import random

mysession = requests.Session()


api_url_base = 'https://test1.vsaas.videonext.net'
login_name = 'addtest@videonext.net'
login_password = '1q2w3e4r5t'
keyLogin = ""
tokenLogin = ""
SetName = "nataset1"



def get_LoginInfo():
    getLoginInfoUrl = api_url_base + "/api/call/getLoginInfo"
    response = mysession.get(getLoginInfoUrl)

    if response.status_code == 200:
        loginjson1 = json.loads(response.content.decode('utf-8'))
        global keyLogin 
        keyLogin = loginjson1['loginInfo']['encryptionKey']
        return "ok"
    else :
        return "get_loginInfo error" 

def get_Login():
    tmpHash = hashlib.sha512(login_password.encode('utf-8')).hexdigest()
    
    tmpHash1 = keyLogin+tmpHash+keyLogin
    credentials = hashlib.sha512(tmpHash1.encode('utf-8')).hexdigest()
   
    authdate = { "credentials" : credentials, "name" : login_name }
    
    getLoginUrl = api_url_base + "/api/call/login"
    response1 = mysession.post(getLoginUrl,json=authdate)
    if response1.status_code == 200:
        taketoken=response1.headers['Set-Cookie']
        global tokenLogin
        tokenLogin = taketoken[(taketoken.index("=")+1):taketoken.index(";")]
       
        return "ok"
    else :
        return "get_Login error"  	


def add_object(attr) :
    #attr should be a prepared json
    headers = {'Content-type': 'application/json','Content-Encoding': 'utf-8','X-token': tokenLogin}
    addObjectUrl= api_url_base + "/api/call/addObject"
    response2 = mysession.post(addObjectUrl,json=attr, headers=headers)
    print(response2.content.decode('utf-8'))
    if response2.status_code == 200:
        obj_obj = json.loads(response2.content.decode('utf-8'))["obj"]
        return obj_obj
    else :
        return "add_object error"


def get_object() :
    objlist = api_url_base + "/api/call/getObjectList?isAll=true&type=set"
    response3 = mysession.get(objlist)
    if response3.status_code == 200:
        allobjects = json.loads(response3.content.decode('utf-8'))
        return allobjects
    else :
        return "get_camera error "

# search in result_json by name
def find_object_by_name(my_json,name):
    result = 0
    for z in my_json['list']:
        if z['name'] == name:
            result = z['obj']
    return result

# search result_json by obj
def find_object_by_obj(my_json,obj):
    result = 0
    for z in my_json['list']:
        if z['obj'] == obj:
            result = 1
    return result     
					

def logout() :
    logouturl = api_url_base + "/api/call/logout"
    response4 = mysession.get(logouturl)
    if response4.status_code == 200:
        return "logout ok"
    else :
        return "logout error"    

####simple add camera scenario
# login
# add_camera
# verify_that_camera_exists
# logout 
def add_one_camera(attr):
    key1=get_LoginInfo()
    if key1 != "get_loginInfo error" :
        #print(keyLogin)
        print("step1: login info is OK")
        token1=get_Login()
        if token1 !="get_Login error" :
            print("step2: login is ok")
            camid=add_object(attr)
        
            if camid != "add_object error" :
                print("!!!camera added id: "+camid)
                allcameras = get_object()
                if find_object_by_obj(allcameras,camid) :
                    print("verified : camera is really added")
                else :
                    print("verified : camera was not added")

                if logout() == "logout ok":
                    print("step5: logout ok")


##the simple set //nataset// was added 
#setattr = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"set","attributes":{"NAME":"natset1"}}
##test for adding several cameras to some set

def add_many_cameras(whatset,howmany):
    key1=get_LoginInfo()
    if key1 != "get_loginInfo error" :
        print("step1: login info is OK")
        token1=get_Login()
        if token1 !="get_Login error" :
            print("step2: login is ok")

            #verify, is set was added already
            alldevices = get_object()
            print(alldevices)
            setid = find_object_by_name(alldevices,whatset)
            print(setid)
            if setid == 0 :
                setattr = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"set","attributes":{"NAME":whatset}}
                result = add_object(setattr)
                print(result)
                if result != "add_object error" :
                    setid = result
                else:
                    print("error while adding set")
            else :

            #prepare camattr
            #use prepared 
                camera = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"camera","attributes":{"AUDIO_FORMAT_LIST":"","AUDIO_LIST":"disable:DISABLE","CAMERAMODEL":"DEMO","CAMERA_LIST":"1","DEVIP":"0.0.0.10","FIRMWARE":"1.0","HTTP_PORT":"80","IMAGESIZE_LIST":"640x480","MEDIA_FORMAT_LIST":"h264","MODELID":"field","PASSWD":"pass","SOURCE":"/opt/demo/data/10-field.640x480","SOURCE_BASE":"/opt/demo/data/10-field","USRNAME":"root","DEVURL":"","RTP_UNICAST_PORT":"","METADATA_PORT":"","RTP_MULTICAST_PORT":"","MULTICAST_IP":"","NAME":"DEMO field232","LOCATION":"","PROTO":"FAKE","CAMERAFIRMWARE":"1.0","IMAGESIZE":"640x480","MEDIA_FORMAT":"h264","ENCODER_SETTING_OVERRIDE":"yes","STORAGE_POOL":"35105020-7dc9-11e8-bcf2-42010a8e0002","CAMERA":"1","ARCHSTATE":"OFF"},"setid":setid}

                for j in range(howmany):
                    camera["attributes"]["NAME"] = camera["attributes"]["NAME"]+str(random.random())
                    cameraid = add_object(camera)
                    print(str(j)+" "+cameraid)
            
            if logout() == "logout ok":
                print(" logout ok")   


add_many_cameras("Natalia",3)   