import requests
import os
import datetime
from time import sleep

hs_id = "121A323A232xaCQY3t9NxpqxD4pFH121Gg11LZP1CTaMZRZS"
#replace the hs_id value with your hotspots ID

api_url = "https://api.helium.io/v1/hotspots/"
roles_ext = "/roles"
cursors_ext = "?cursor="
blocks_data_url = "https://api.helium.io/v1/blocks"
roles_data_url = f"https://api.helium.io/v1/hotspots/{hs_id}/roles"
numele_hotspotului = "your_hs_name"


while True:
    blocks_data = requests.get(blocks_data_url).json()['data'][0]['height']
    roles_data = requests.get(roles_data_url).json()
    cursor_id = roles_data['cursor']
    activity_url = f"{roles_data_url}{cursors_ext}{cursor_id}"
    last_activity_height = requests.get(activity_url).json()['data'][0]['height']
    blocks_since_last_activity = (int(blocks_data)-(int(last_activity_height)))
    print(f"Ultima activitate a lui {numele_hotspotului} este acum {blocks_since_last_activity} blocks")
    sleep(1800)
    if blocks_since_last_activity > 150:
       file = open(""+numele_hotspotului+"_reboot_log.txt","a")
       file.write(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
       file.write(" || Hotspotul nu a avut activitate de mai mult de 100 block-uri, asa ca i-am dat restart\n")
       file.close()
       os.system("curl -X POST -H 'Authorization: Basic d7121216c2872323598' http://10.6.0.2:2112/reboot") #this is sensecap api
       print(f" {numele_hotspotului} nu activitate de mai mult de 100 de blocuri, voi restarta minerul. Ultima activitate a fost acum {blocks_since_last_activity}")
       sleep(200)