import idor
import pyfiglet
import argparse

print (pyfiglet.figlet_format("I D O R", font = "speed" )) #Presentation
print ("[VERSION] 0.2")
print ("[AUTHOR] Lucas Antoniaci")

#Add arguments for argparse
parser = argparse.ArgumentParser(description='Exploit an IDOR')
parser.add_argument("-u",required=True,help="The URL to exploit, place IDOR in place of desired payload('-u https://example/user/IDOR/info") 
parser.add_argument("-m",required=True,help="Request HTTP method (get/post/put)")
parser.add_argument("-t",required=True,help="Payload type (-t num/list)")
parser.add_argument("-c",help="Request cookies(-c 'co1=1,co2=2')")
parser.add_argument("-p",help="Proxy (-p 127.0.0.1:8080)")
parser.add_argument("-he",help="Headers (-he \"{\'Custom header\': \'teste\'}\")")
parser.add_argument("-d",help="POST data (-d ' {name: \"John\", age: 31, city: \"New York\"}')")
parser.add_argument("-td",help="Time between requests in seconds, default is zero (-td 10)")
args = parser.parse_args()

#Create target object
target = idor.target(args.u,args.m,args.t,
					cookies=args.c,proxy=args.p,
					headers=args.he,post_data=args.d,delay=args.td)

#Prepare and execute exploration
if (target.prepare()):
	target.explore()