#!/usr/bin/env python
# -*- coding: utf-8 -*-



from bs4 import BeautifulSoup as bs
from clint.textui import colored,progress
from url_normalize import url_normalize
import itertools,sys,requests,urllib.request,os
from pathlib import Path
from termcolor import colored

__author__ = "Burak Ünal"
__web__ = "https://burakunal.me"

dizin = Path().absolute()
print(chr(27) + "[2J")
header ="""
  _    _         _   __       _   _         _                         _  _
 | |  | |       | | / _|     | | | |       (_)                       (_)| |
 | |  | |  ___  | || |_      | | | | _ __   _ __   __ ___  _ __  ___  _ | |_  _   _ 
 | |/\| | / _ \ | ||  _|     | | | || '_ \ | |\ \ / // _ \| '__|/ __|| || __|| | | |
 \  /\  /| (_) || || |    _  | |_| || | | || | \ V /|  __/| |   \__ \| || |_ | |_| |
  \/  \/  \___/ |_||_|   (_)  \___/ |_| |_||_|  \_/  \___||_|   |___/|_| \__| \__, |
          ______                        _                    _                 __/ |
          |  _  \                      | |                  | |               |___/
          | | | | ___ __      __ _ __  | |  ___    __ _   __| |  ___  _ __ 
          | | | |/ _ \\ \ /\ / /| '_ \ | | / _ \  / _` | / _` | / _ \| '__|
   __     | |/ /| (_) |\ V  V / | | | || || (_) || (_| || (_| ||  __/| |     __
   \ \    |___/  \___/  \_/\_/  |_| |_||_| \___/  \__,_| \__,_| \___||_|    / /
    \ \____________________________________________________________________/ /
     \______________________________________________________________________/
              D4rkbrain            __     __ https://github.com/burakunaltr
                                   \ \   / /
                                    \ \_/ /
                                     \   /
                                      \_/     
"""
print(colored(header,"green"))

href = "https://wolf.university/"
exit = False
def yazdir(url):
    global exit
    global href
    say=0
    link=[]
    client = requests.session()
    soup = bs(client.get(url).text,'html.parser')
    print(colored("Which one?","red"))
    for a,b in zip(soup.findAll('td',{'class':'n'}),soup.findAll('td',{'class':'s'})):
        if b.text == '- \xa0':
            link.append([str(say),a.text,"DIRECTORY "])
        else:
            link.append([str(say),a.text,"FILE ("+b.text+")"])
        say += 1

    for item in enumerate(link):
        print(colored(("[ "+str(int(item[1][0])+1)+" ]").ljust(6),"green"),colored(" » ","white")+colored("| "+(item[1][2]).ljust(14)+"|","blue"),colored(item[1][1].rstrip('/'),"white"))
    print(colored("Press q to exit !","red"))
    sor = input("Select one : ")
    os.system('cls' if os.name == 'nt' else 'clear')
    if sor =="q":
        print(colored(header,"blue")+colored("\n                            Come back when you need ..","green"))
        exit=True
    elif (int(sor) > len(link)) or (int(sor) == 0):
        print(colored("You have entered more than the list length.","yellow"))
        return 0
    elif sor.isdigit():
        sor=int(sor)-1
        git = link[sor][1]
        if "FILE" in link[sor][2]:
            indir = href + git
            with open(str(dizin)+"/"+git,'wb') as f:
                cek = client.get(indir, stream=True)
                print(colored("Downloading : "+git,"yellow"))
                total_length = int(cek.headers.get('content-length'))
                for chunk in progress.bar(cek.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
                print(colored("[\tCOMPLETED !\t]","green"))
                
                return 0
        else:
            href = url_normalize(href+git)

while exit == False:
    try:
        yazdir(href)
    except ValueError:
        print(colored("İnvalid value.","red"))
    