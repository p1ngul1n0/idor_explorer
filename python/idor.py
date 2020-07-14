import requests
import time
import warnings
#Lib to explore IDOR in APIs
warnings.simplefilter("ignore")
class target: #TARGET CLASS
	def __init__(self, url,): #target initilization

		print ("_"*100)
		methods = ["GET","POST","PUT"]
		self.method = methods[int(input("   > Select a method\n     >> 1-GET\n     >> 2-POST\n     >> 3-PUT\n     >> Insert ID:"))-1]
		self.url = url #set object parameters
		self.cookies = {}
		self.headers = {}
		self.proxies = {}
		self.post_data = {}

		if (input("   > Use cookies ? (y) ") == "y"): #ask for cookies
			while(True): #cookies addition loop
				cookie_name = input("     >> Enter new cookie name: ")
				cookie_value = input("     >> Enter new cookie value: ")
				self.cookies[cookie_name] = cookie_value
				if(input("     >> Add more cookies ? (y) ") != "y"):
					break

		if (input("   > Use custom headers ? (y) ") == "y"): #ask for headers
			while(True): #headers addition loop
				header_name = input("     >> Enter new cookie name: ")
				header_value = input("     >> Enter new cookie value: ")
				self.headers[header_name] = header_value
				if(input("     >> Add more headers ? (y) ") != "y"):
					break
		if (input("   > Use proxy ? (y) ") == "y"): #ask for proxy
			proxy_host = input("     >> Enter proxy host: ")
			proxy_port = input("     >> Enter proxy port: ")
			self.proxies["http"] = "http://"+proxy_host+":"+proxy_port
			self.proxies["https"] = "http://"+proxy_host+":"+proxy_port

		if (self.method == "POST" or self.method == "PUT"): #If request method post or put ask for body data
			print (self.method)
			self.post_data = input("   > Enter body data with IDOR on payload place: ")
			encoding = int(input("     >> Select a encoding\n     >> 1-JSON\n     >> Insert ID:")) #ask for encoding
			if (encoding == 1): #Add according Content Type
				self.headers['Content-Type'] =  'application/json'

		self.payload_type = int(input("   > Payload type\n     >> 1-Numeric\n     >> 2-List\n     >> Insert ID:"))
		if (self.payload_type == 1):
			self.min_value = int(input("     >> Start value: "))
			self.max_value = int(input("     >> End value: "))
		
		elif (self.payload_type == 2):
			file = input("     >> File list: ")
			opened_file = open(file,'r')
			self.list = opened_file.readlines()
		self.time = int(input("   > Delay between requests(seconds): "))

	def present(count,request,method,payload):

		print ("ID:{} METHOD:{} PAYLOAD: {} URL:[{}] CODE:{} SIZE:{}".format(count,method,payload,request.url,request.status_code,len(request.content)))
		if (len(request.request.body) > 2):
			print ("    BODY     {}".format(request.request.body))
		if (request.content != None):
			print ("    RESPONSE     {}".format(request.content))

	def explore(self): #Start loop of requests

		if (self.payload_type == 1): #Loop for numeric increase
			payload_number = self.min_value
			count = 0
			for payload_number in range(self.min_value,self.max_value+1):
				url = self.url.replace("IDOR",str(payload_number))
				new_data = str(self.post_data)
				defined_data = new_data.replace("IDOR",str(payload_number))
				request = requests.request(self.method,url,headers=self.headers,cookies=self.cookies,
							               proxies=self.proxies,verify=False,data=defined_data)
				count += 1
				target.present(count,request,self.method,payload_number)
				time.sleep(self.time)

		elif (self.payload_type == 2): #Loop for list file
			for element in self.list:
				new_element = element.rstrip('\n')
				url = self.url.replace("IDOR",new_element)
				new_data = str(self.post_data)
				defined_data = str(new_data.replace("IDOR",new_element))
				request = requests.request(self.method,url,headers=self.headers,cookies=self.cookies,
							               proxies=self.proxies,verify=False,data=defined_data)
				target.present(count,request,self.method,new_element)
				time.sleep(self.time)