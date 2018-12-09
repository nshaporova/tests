import json
import requests
import hashlib

class add_N_cameras:


    def __init__(self,overcast_uri,overcast_realmname,overcast_realmpasswd,overcast_setname,num_cameras,camera_attr,set_attr):
        self.api_url_base = overcast_uri
        self.login_name = overcast_realmname
        self.login_password = overcast_realmpasswd
        self.setName = overcast_setname
        self.numcameras = num_cameras
        self.keyLogin = ""
        self.tokenLogin = ""
        self.camera = camera_attr
        self.set = set_attr
        self.mysession = requests.Session()


    
    def get_LoginInfo(self):
        getLoginInfoUrl = self.api_url_base + "/api/call/getLoginInfo"
        response = self.mysession.get(getLoginInfoUrl)

        if response.status_code == 200:
            loginjson1 = json.loads(response.content.decode('utf-8'))
            print(json.loads(response.content.decode('utf-8')))

            self.keyLogin = loginjson1['loginInfo']['encryptionKey']
            print(self.keyLogin)
            print("-------")
           
            print(response.headers)
            print("----------")
            self.headers = response.headers
            self.cookies = response.cookies
            return "ok"
        else :
            return "get_loginInfo error" 

    def get_Login(self):
        print("Login method")
        tmpHash = hashlib.sha512(self.login_password.encode('utf-8')).hexdigest()

        tmpHash1 = self.keyLogin+tmpHash+self.keyLogin

        credentials = hashlib.sha512(tmpHash1.encode('utf-8')).hexdigest()
        authdate = { "credentials" : credentials, "name" : self.login_name }
        print(authdate)
        getLoginUrl = self.api_url_base + "/api/call/login"
        print(getLoginUrl)
        response1 = self.mysession.post(getLoginUrl,json=authdate)
        print(json.loads(response1.content.decode('utf-8')))
        if response1.status_code == 200:
            taketoken=response1.headers['Set-Cookie']
            self.tokenLogin = taketoken[(taketoken.index("=")+1):taketoken.index(";")]
            return "ok"
        else :
            return "get_Login error"  	


    def add_object(self,attr):
    #attr should be a prepared json
        headers = {'Content-type': 'application/json','Content-Encoding': 'utf-8','X-token': self.tokenLogin}
        addObjectUrl= self.api_url_base + "/api/call/addObject"
        response2 = self.mysession.post(addObjectUrl,json=attr, headers=headers)
        print(response2.content.decode('utf-8'))
        if response2.status_code == 200:
            obj_obj = json.loads(response2.content.decode('utf-8'))["obj"]
            return obj_obj
        else :
            return "add_object error"


    def get_object(self):
        objlist = self.api_url_base + "/api/call/getObjectList?isAll=true&type=set"
        response3 = self.mysession.get(objlist)
        if response3.status_code == 200:
            allobjects = json.loads(response3.content.decode('utf-8'))
            return allobjects
        else :
            return "get_camera error "

# search in result_json by name
    def find_object_by_name(self,my_json,name):
        result = 0
        for z in my_json['list']:
            if z['name'] == name:
                result = z['obj']
                return result

# search result_json by obj
    def find_object_by_obj(self,my_json,obj):
        result = 0
        for z in my_json['list']:
            if z['obj'] == obj:
                result = 1
            return result     
					

    def logout(self):
        logouturl = self.api_url_base + "/api/call/logout"
        response4 = self.mysession.get(logouturl)
        if response4.status_code == 200:
            return "logout ok"
        else :
            return "logout error"    

    def add_many_cameras(self):
        key1=self.get_LoginInfo()
        if key1 != "get_loginInfo error" :
            print("step1: login info is OK")
            token1=self.get_Login()
            if token1 !="get_Login error" :
                print("step2: login is ok")

            #verify, is set was added already
                alldevices = self.get_object()
                print(alldevices)
                setid = self.find_object_by_name(alldevices,self.setName)
                print(setid)
                if setid == 0 :
                #setattr = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"set","attributes":{"NAME":whatset}}
                    result = self.add_object(self.set)
                    print(result)
                    if result != "add_object error" :
                        setid = result
                    else:
                        print("error while adding set")
                else :

            #prepare camattr
            #use prepared 
                #camera = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"camera","attributes":{"AUDIO_FORMAT_LIST":"","AUDIO_LIST":"disable:DISABLE","CAMERAMODEL":"DEMO","CAMERA_LIST":"1","DEVIP":"0.0.0.10","FIRMWARE":"1.0","HTTP_PORT":"80","IMAGESIZE_LIST":"640x480","MEDIA_FORMAT_LIST":"h264","MODELID":"field","PASSWD":"pass","SOURCE":"/opt/demo/data/10-field.640x480","SOURCE_BASE":"/opt/demo/data/10-field","USRNAME":"root","DEVURL":"","RTP_UNICAST_PORT":"","METADATA_PORT":"","RTP_MULTICAST_PORT":"","MULTICAST_IP":"","NAME":"DEMO field232","LOCATION":"","PROTO":"FAKE","CAMERAFIRMWARE":"1.0","IMAGESIZE":"640x480","MEDIA_FORMAT":"h264","ENCODER_SETTING_OVERRIDE":"yes","STORAGE_POOL":"35105020-7dc9-11e8-bcf2-42010a8e0002","CAMERA":"1","ARCHSTATE":"OFF"},"setid":setid}
                #camera = {"nodeid":"0ac2020c-f19e-11e8-9777-62bfc35edbba","type":"camera","attributes":{"AUDIO_FORMAT_LIST":"","AUDIO_LIST":"disable:DISABLE","CAMERAMODEL":"DEMO","CAMERA_LIST":"1","DEVIP":"0.0.0.23","FIRMWARE":"1.0","HTTP_PORT":"80","IMAGESIZE_LIST":"1280x720","MEDIA_FORMAT_LIST":"h264","MODELID":"upstairs","PASSWD":"pass","SOURCE":"/opt/demo/data/23-upstairs.1280x720","SOURCE_BASE":"/opt/demo/data/23-upstairs","USRNAME":"root","DEVURL":"","RTP_UNICAST_PORT":"","METADATA_PORT":"","RTP_MULTICAST_PORT":"","MULTICAST_IP":"","NAME":"DEMO upstairs1","PROTO":"FAKE","CAMERAFIRMWARE":"1.0","IMAGESIZE":"1280x720","MEDIA_FORMAT":"h264","ENCODER_SETTING_OVERRIDE":"yes","STORAGE_POOL":"33ed81a6-e442-11e8-b91b-42010a8e0002","CAMERA":"1","AV_DELIVERY_HR":"LIVE_NR|LIVE_LR","FRAMERATE":"25"},"setid":"f4eebdf0-ed6d-11e8-86fc-42010a8e0002"}

                    for j in range(self.numcameras):
                        #camera["attributes"]["NAME"] = camera["attributes"]["NAME"]+str(random.random())
                        self.camera["attributes"]["NAME"] = str(j)
                        cameraid = self.add_object(self.camera)
                        print(str(j)+" "+cameraid)
            
                    if self.logout() == "logout ok":
                        print(" logout ok")



api_url_base = 'https://demo1.vsaas.videonext.net'
login_name = 'realm2'
login_password = '1q2w3e4r5t'
camera_attr = {"nodeid":"fe3858c7-f163-463f-b0bf-e8f3c218175c","type":"camera","attributes":{"AUDIO_FORMAT_LIST":"","AUDIO_LIST":"disable:DISABLE","CAMERAMODEL":"DEMO","CAMERA_LIST":"1","DEVIP":"0.0.0.10","FIRMWARE":"1.0","HTTP_PORT":"80","IMAGESIZE_LIST":"640x480","MEDIA_FORMAT_LIST":"h264","MODELID":"field","PASSWD":"pass","SOURCE":"/opt/demo/data/10-field.640x480","SOURCE_BASE":"/opt/demo/data/10-field","USRNAME":"root","DEVURL":"","RTP_UNICAST_PORT":"","METADATA_PORT":"","RTP_MULTICAST_PORT":"","MULTICAST_IP":"","NAME":"D","PROTO":"FAKE","CAMERAFIRMWARE":"1.0","IMAGESIZE":"640x480","MEDIA_FORMAT":"h264","ENCODER_SETTING_OVERRIDE":"yes","STORAGE_POOL":"b6c572b2-eca5-11e8-bafb-42010a8e0002","CAMERA":"1"},"setid":"b3bc04e6-eca5-11e8-bafb-42010a8e0002"}
SetName = "nataset1"
set_attr = {"nodeid":"fe3858c7-f163-463f-b0bf-e8f3c218175c","type":"set","attributes":{"NAME":"natset1"}}

#def __init__(self,overcast_uri,overcast_realmname,overcast_realmpasswd,overcast_setname,num_cameras,camera_attr,set_attr)
action = add_N_cameras(api_url_base,login_name,login_password,SetName,1,camera_attr,set_attr)
action.add_many_cameras()