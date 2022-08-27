#This is where all the magic really happens.
#If you're going to use some of my code be nice and make your app open source! (And by the way give me some credit *coughs*)
#If you can let me know too, I'd be excited to hear someone uses something I made!

import subprocess
from bs4 import BeautifulSoup
import requests
import json
import re
try:
    with open('./data/data.json','r') as f:
        data=json.load(f)
    data=data
    try:
        with open('./data/download.json','r') as f:
            download=json.load(f)
        download=download
    except:
        print('SCMD List Manager & SCMD Workshop Downloader made by Berdy Alexei\nERROR 3: SCMD List Manager should only be opened when called by SCMD Workshop Downloader\n<<Open SCMD Workshop Downloader instead>>')
        close=input('\n\n### Press Enter to close this window ###\n\n')
        exit()
    appcondition='https://steamcommunity.com/app/'
    itemcondition='https://steamcommunity.com/sharedfiles/filedetails/?id='
    collectioncondition='https://steamcommunity.com/workshop/browse/?section=collections&appid='
    scriptadd=''
    repeat=data["repeat"]
    if not download:
        print('SCMD List Manager & SCMD Workshop Downloader made by Berdy Alexei\nERROR 3: SCMD List Manager should only be opened when called by SCMD Workshop Downloader\n<<Open SCMD Workshop Downloader instead>>')
        close=input('\n\n### Press Enter to close this window ###\n\n')
        exit()
    else:
        if data["mode"]==1 or data["mode"]==3 or data["mode"]==5:
            gIDi=[]
            items=[]
            collections=[]
            successcount=0
            errorcount=0
            print('Analysing links... (Multiple-mode)')
            for coln in range(len(download['list'])):
                print(f'Classifying links: {coln+1} of {len(download["list"])}')
                collectiondetector=0
                try:
                    for link in BeautifulSoup(requests.get(download['list'][coln]).text, 'html.parser').find_all('a'):
                        if collectioncondition in str(link.get('href')):
                            collectiondetector+=1
                    if collectiondetector<1:
                        items.append(download['list'][coln])
                        successcount+=1
                    else:
                        collections.append(download['list'][coln])
                        successcount+=1
                except:
                    errorcount+=1
            for coln in range(len(items)):
                print(f'Analyzing items links: {coln+1} of {len(items)}')
                try:
                    for link in BeautifulSoup(requests.get(items[coln]).text, 'html.parser').find_all('a'):
                        if appcondition in str(link.get('href')):
                            duo=(str(link.get('href')))
                    gIDi+=re.findall('\d+',str(duo))
                    wIDi=re.findall('\d+',str(items))
                except:
                    errorcount+=1
                    successcount-=1
            try:
                for wIDc in range(len(items)):
                    scriptadd+=f' +workshop_download_item {gIDi[wIDc]} {wIDi[wIDc]} validate'
                    if data["bscim"]==True:
                        for i in range(repeat):
                            scriptadd+=f' +workshop_download_item {gIDi[0]} {wIDi[wIDc]} validate'
                        print(f'BSIM Treatment given to item #{wIDc+1} repeated {repeat} time/s.')
            except:
                pass
            downloadlist=[]
            for coln in range(len(collections)):
                print(f'Analyzing collections links: {coln+1} of {len(collections)}')
                for link in BeautifulSoup(requests.get(collections[coln]).text, 'html.parser').find_all('a'):
                    if itemcondition in str(link.get('href')):
                        downloadlist.append(str(link.get('href')))
                downloadlist.remove(f'{collections[coln]}')
                downloadlist=re.findall('\d+',str(downloadlist))
                for dupe in downloadlist:
                    if downloadlist.count(dupe)>1:
                        downloadlist.remove(dupe)
                for link in BeautifulSoup(requests.get(download['list'][0]).text, 'html.parser').find_all('a'):
                    if appcondition in str(link.get('href')):
                        applink=str(link.get('href'))
                wIDi=downloadlist
                gIDi=re.findall('\d+',str(applink))
                for wIDc in range(len(wIDi)):
                    scriptadd+=f' +workshop_download_item {gIDi[0]} {wIDi[wIDc]} validate'
                    if data["bscim"]==True:
                        for i in range(repeat):
                            scriptadd+=f' +workshop_download_item {gIDi[0]} {wIDi[wIDc]} validate'
                if data["bscim"]==True:       
                    print(f'BSIM Treatment given to {len(wIDi)} items {repeat} time/s.')
                print(f'Registered {len(wIDi)} items.')
            if (errorcount>0 and successcount==0) or successcount==0:
                print(f'ERROR 2: All introduced links are wrong')
                print('<< Having a bad Internet conection can also make this error to happen. Try again later. >>')
                with open('./data/download.json','w') as f:
                    json.dump('',f)
            else:
                script=download["script"]+scriptadd
                datetime=download["datetime"]
                with open('./data/download.json','w') as f:
                    json.dump('',f)
                if data["mode"]==3 or data["mode"]==5:
                    writer=open(f'./generated scripts/script {datetime[0]}.bat','w')
                    writer.write(script)
                    writer.close()
                    print(f'Script generated as: script {datetime[0]}.bat')
                if  data["mode"]==1 or data["mode"]==5:
                    try:
                        print('Download started\n')
                        subprocess.call('{}'.format(script))
                    except FileNotFoundError:
                        if data["mode"]==3 or data["mode"]==5:
                            print("\nERROR 0: Too many elements tried to be downloaded. Close this Window and try again introducing less.\nATTENTION: The created script probably won't work either because of that.\n")
                        else:
                            print('\nERROR 0: Too many elements tried to be downloaded. Close this Window and try again introducing less.\n')
        else:
            print('Analysing links... (Single-mode)')
            try:
                for link in BeautifulSoup(requests.get(download["list"][0]).text, 'html.parser').find_all('a'):
                    if appcondition in str(link.get('href')):
                        applink=str(link.get('href'))
                gIDi=re.findall('\d+',str(applink))
                wIDi=re.findall('\d+',str(download["list"]))
                for wIDc in range(len(wIDi)):
                    print(f'Analyzing items links: {wIDc+1} of {len(wIDi)}')
                    scriptadd+=f' +workshop_download_item {gIDi[0]} {wIDi[wIDc]} validate'
                    if data["bscim"]==True:
                        for i in range(repeat):
                            scriptadd+=f' +workshop_download_item {gIDi[0]} {wIDi[wIDc]} validate'
                        print(f'BSIM Treatment given to item #{wIDc+1} repeated {repeat} time/s')
                script=download["script"]+scriptadd
                if data["mode"]==2 or data["mode"]==4:
                    datetime=download["datetime"]
                    writer=open(f'./generated scripts/script {datetime[0]}.bat','w')
                    writer.write(script)
                    writer.close()
                    print(f'Script generated as: script {datetime[0]}.bat')
                if data["mode"]==0 or data["mode"]==4:
                    try:
                        with open('./data/download.json','w') as f:
                            json.dump('',f)
                        print('Download started\n')
                        subprocess.call('{}'.format(script))
                    except FileNotFoundError:
                        if data["mode"]==2 or data["mode"]==4:
                            print("\nERROR 0: Too many elements tried to be downloaded. Close this Window and try again introducing less.\nATTENTION: The created script probably won't work either because of that.\n")
                        else:
                            print('\nERROR 0: Too many elements tried to be downloaded. Close this Window and try again introducing less.\n')
            except:
                print('ERROR 1: The first link entered is incorrect')
                print('<< Having a bad Internet conection can also make this error to happen. Try again later. >>')
        with open('./data/download.json','w') as f:
            json.dump('',f)
except:
    print('ERROR 4: Required files could not be accessed')
    print('<< In SCMD Workshop Downloader press the configuration button and access the ERRORS & SOLUTIONS tab to know the details and how to solve the problem. >>')
try:
    close=input('\n\n### Press Enter to close this window ###\n\n')
except:
    pass
