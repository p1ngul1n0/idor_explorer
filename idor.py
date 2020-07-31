import requests
import time
import warnings
from colorama import *
import ast
import regex

init(autoreset=True)
warnings.simplefilter("ignore")
class target:
	def __init__(self,url,method,payload_type,*args,**kwargs): #target initilization
		print ("_"*100)
		self.url = url
		self.method = method
		self.payload_type = payload_type
		self.headers = {}
		self.proxies = {}

		#Verify if optional arguments are set
		if (kwargs.get('cookies') != None):
			self.headers.update({"Cookie": kwargs.get('cookies')})

		if (kwargs.get('proxy') != None):
			self.proxies["http"] = "http://"+kwargs.get('proxy')
			self.proxies["https"] = "http://"+kwargs.get('proxy')

		if (kwargs.get('headers') != None):
			self.headers.update(ast.literal_eval(kwargs.get('headers')))

		if (kwargs.get('post_data') != None):	
			self.post_data = kwargs.get('post_data')
			if (len(regex.compile(r'\{(?:[^{}]|(?R))*\}').findall(self.post_data)) >= 1):
				self.headers['Content-Type'] =  'application/json'
		else:
			self.post_data = ""

		if (kwargs.get('delay') != None):
			self.time = int(kwargs.get('delay'))
		else:
			self.time = 0


	def present(count,request,method,payload): #Present request info function
		print ("| {} | {} | {} | {} | {} | {} |".format(count,payload,method.upper(),request.url,request.status_code,len(request.content)))

	def prepare(self): #Request and validate params to explore

		if (self.payload_type == 'num'): #If numeric payload type
			self.min_value = int(input("     {}>>{} {}Start value:{} ".format(Fore.BLUE,Style.RESET_ALL,Fore.WHITE,Style.RESET_ALL)))
			self.max_value = int(input("     {}>>{} {}End value:{} ".format(Fore.BLUE,Style.RESET_ALL,Fore.WHITE,Style.RESET_ALL)))
			if (self.min_value >= self.max_value):
				print ("|{}[ERROR]{} The start value is lower or equal the final value!".format(Fore.RED,Style.RESET_ALL))
				return False
			else:
				self.requests_number = (self.max_value+1) -(self.min_value)
				return True

		if (self.payload_type == 'list'): #If list payload type
			file = input("     {}>>{} {}File list:{} ".format(Fore.BLUE,Style.RESET_ALL,Fore.WHITE,Style.RESET_ALL))
			try:
				opened_file = open(file,'r')
				self.list = opened_file.readlines()
				self.requests_number = len(self.list)
				return True
			except:
				print ("|{}[ERROR]{} Couldn't access the file!".format(Fore.RED,Style.RESET_ALL))
				return False

	def explore(self): #Start loop of requests
		
		#Present arguments to explore
		print ("_"*100)
		print ("| {}PUBLIC IP IN USE{} {}".format(Fore.WHITE,Style.RESET_ALL,requests.get('https://api.ipify.org').text))
		print ("| {}METHOD{} {}".format(Fore.WHITE,Style.RESET_ALL,self.method.upper()))

		print ("| {}URL{}  {}".format(Fore.WHITE,Style.RESET_ALL,self.url))

		print ("| {}PAYLOAD{} {} | {} {} REQUESTS{}".format(Fore.WHITE,Style.RESET_ALL,
															self.payload_type.upper(),
															self.requests_number,
															Fore.WHITE,Style.RESET_ALL))

		print ("| {}TIME BETWEEN REQUESTS{} {} {}seconds".format(Fore.WHITE,Style.RESET_ALL,self.time,Fore.WHITE))
		if (len(self.proxies)==2):
			print ("| {}PROXY{} {}".format(Fore.WHITE,Style.RESET_ALL,self.proxies['http']))
		input("       Press ENTER to start...")
		print ("| ID | PAYLOAD | METHOD | URL | STATUS | SIZE |")

		count = 0
		if (self.payload_type == 'num'): #Loop for numeric increase
			payload_number = self.min_value
			
			for payload_number in range(self.min_value,self.max_value+1):
				url = self.url.replace("IDOR",str(payload_number))
				try:
					new_data = str(self.post_data)
					defined_data = new_data.replace("IDOR",str(payload_number))
				except:
					defined_data = ""
				request = requests.request(self.method,url,headers=self.headers,
										   proxies=self.proxies,verify=False,data=defined_data)
				count += 1
				target.present(count,request,self.method,payload_number)
				time.sleep(self.time)

		elif (self.payload_type == 'list'): #Loop for list file
			for element in self.list:
				new_element = element.rstrip('\n')
				url = self.url.replace("IDOR",new_element)
				new_data = str(self.post_data)
				defined_data = str(new_data.replace("IDOR",new_element))
				request = requests.request(self.method,url,headers=self.headers,
										   proxies=self.proxies,verify=False,data=defined_data)
				count +=1
				target.present(count,request,self.method,new_element)
				time.sleep(self.time)
