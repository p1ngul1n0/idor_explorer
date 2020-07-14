import idor
import pyfiglet

print (pyfiglet.figlet_format("IDOR", font = "speed" )) #Presentation
print ("|-v0.1")
print ("|-Author: Lucas Antoniaci")
#Request URL from user and create target object
target = idor.target(input(" > Insert URL with 'IDOR' in payload place: "))
target.explore()