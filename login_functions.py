import json
import requests
import hashlib 
import random

mysession = requests.Session()


api_url_base = 'https://test1.vsaas.videonext.net'
login_name = 'addtest@videonext.net'
login_password = '1q2w3e4r5t'

camera = {"nodeid":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":"camera","attributes":{"AUDIO_FORMAT_LIST":"","AUDIO_LIST":"disable:DISABLE","CAMERAMODEL":"DEMO","CAMERA_LIST":"1","DEVIP":"0.0.0.10","FIRMWARE":"1.0","HTTP_PORT":"80","IMAGESIZE_LIST":"640x480","MEDIA_FORMAT_LIST":"h264","MODELID":"field","PASSWD":"pass","SOURCE":"/opt/demo/data/10-field.640x480","SOURCE_BASE":"/opt/demo/data/10-field","USRNAME":"root","DEVURL":"","RTP_UNICAST_PORT":"","METADATA_PORT":"","RTP_MULTICAST_PORT":"","MULTICAST_IP":"","NAME":"DEMO field232","LOCATION":"","PROTO":"FAKE","CAMERAFIRMWARE":"1.0","IMAGESIZE":"640x480","MEDIA_FORMAT":"h264","ENCODER_SETTING_OVERRIDE":"yes","STORAGE_POOL":"35105020-7dc9-11e8-bcf2-42010a8e0002","CAMERA":"1"},"setid":"2fb619b6-7dc9-11e8-bcf2-42010a8e0002"}
camera["attributes"]["NAME"] = camera["attributes"]["NAME"]+str(random.random())

getLoginInfoUrl = api_url_base + "/api/call/getLoginInfo"
response = mysession.get(getLoginInfoUrl)
cookies= response.cookies
#print('----------')
#print(cookies)
#print('----------')

if response.status_code == 200:
#	print("first step of login\n")
	loginjson1 = json.loads(response.content.decode('utf-8'))
	key=loginjson1['loginInfo']['encryptionKey']
#	print(key)
	tmpHash = hashlib.sha512(login_password.encode('utf-8')).hexdigest()
#	print(key+tmpHash+key) 
	tmpHash1 = key+tmpHash+key
	credentials = hashlib.sha512(tmpHash1.encode('utf-8')).hexdigest()
#	print(credentials)
	authdate = { "credentials" : credentials, "name" : login_name }
        
#	headers = {'Content-type': 'application/json',
#           'Content-Encoding': 'utf-8'}
	getLoginUrl = api_url_base + "/api/call/login"

	response1 = mysession.post(getLoginUrl,json=authdate)
#	print(json.loads(response1.content.decode('utf-8'))) 
#	print(response1.status_code)
	if response1.status_code == 200:
		print(" verified : login is successfull")
		taketoken=response1.headers['Set-Cookie']
		
		token=taketoken[(taketoken.index("=")+1):taketoken.index(";")]
	#	print(token)	

		cookies1=response1.cookies
		headers = {'Content-type': 'application/json','Content-Encoding': 'utf-8','X-token': token,'X-requested-with': 'XMLHttpRequest'}

		addObjectUrl= api_url_base + "/api/call/addObject"

		response2 = requests.post(addObjectUrl,json=camera,cookies=cookies1, headers=headers)
	#	print(response2.content.decode('utf-8'))


		if response2.status_code == 200:
	#		print(json.loads(response2.content.decode('utf-8')))
			print(" verified : addobject ok")
			camobj = json.loads(response2.content.decode('utf-8'))["obj"]
			
		#	datapost = { "parentObj":"0690c63f-b7b1-47da-8af4-ea49483ec154","type":("camera"),"withAttributes":"true"}
			objlist = api_url_base + "/api/call/getObjectList?parentObj=0690c63f-b7b1-47da-8af4-ea49483ec154"
			listObjects = api_url_base + "/api/call/getObjectList?parentObj="+"'0690c63f-b7b1-47da-8af4-ea49483ec154'"

		#	print(listObjects)
			response3 = requests.get(objlist,cookies=cookies1,headers=headers)
			if response3.status_code == 200:
				allcameras = json.loads(response3.content.decode('utf-8'))
				addingresult = 0
				for x in allcameras['list']:
					if x['obj'] == camobj:
						addingresult = 1
				if addingresult == 1:
					print(" verified : camera was really added !!!")
				logouturl = api_url_base + "/api/call/logout"
				response4 = requests.get(logouturl,cookies=cookies1,headers=headers)
				if response4.status_code == 200:
					print(" verified : logout ok")	
			else: 
				print("error while getting list of cameras")	
		else:
			print("error while adding camera")		
	else:	
		print("login,password were incorrect")

else:
        print("some problem with server")
