from datetime import datetime
from json import load as jload
from os.path import getmtime
from pathlib import Path
from time import sleep, time
import sys, signal
from csv import reader
from requests import get

__author__     = 'Christian Quiroz - OA4DOA'
__copyright__  = 'Copyright (c) Christian Quiroz, OA4DOA 2021'
__credits__    = 'Norman Williams, M6NBP'
__maintainer__ = 'Christian OA4DOA'
__email__      = 'christianyuvel@dmr-peru.pe'
__license__    = 'GNU GPLv3'
__version__    = '1.2'


################################## Config Here #######################################
# Path and and name of the log file
PATH_TO_LOG = "./"
LOG_NAME    = "freedmr.log"

# Files and the time to update in "DAYS".
USER_URL     = "https://www.radioid.net/static/user.csv"
REFRESH_USER = 7

TG_NAME_URL     = "http://downloads.freedmr.uk/downloads/talkgroup_ids.json"
REFRESH_TG_NAME = 7

SUBSCRIBER_URL = "http://downloads.freedmr.uk/downloads/local_subscriber_ids.json"
REFRESH_LOCAL  = 15

# Path and file name of the template that we'll use to write PHP file.
PATH_TO_TEMPLATE = "./templates"
TEMPLATE_NAME    = "tgcount.php"

# Path and file name to where we'll write the PHP and the time in "MINUTES" to update the file. 
PATH_TO_WRITE = "./"
WRITE_FILE    = "count.php"
TIME_TO_WRITE = 3

# The IDs in this list won't be take into account for TG count.
VANISH = ('1234567',)

################################## End of Config #######################################


# Close gently
def signal_handler(signal, frame):
    print('\nBye')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Show time in a friendly format
def min_sec(f):
    minu = int(f)
    seco = int(f % 1 * 60)
    if seco < 10:
        second = f'{seco}'.zfill(2)
    else:
        second = seco
    return f'{minu}:{second}'

# Download or update the source files
def file_update(url,update):
    file = url.split('/')[-1]
    try:
        file_date = getmtime(file)
        delta = round((time() - file_date)/3600,1)
        if delta >= update*24:
            raise FileNotFoundError('Time to Download again')

    except FileNotFoundError:
        print(f'Downloading {file}...')
        try:
            r = get(url)
            if r.status_code == 200:
                with open(file, 'wb') as f:
                    f.write(r.content)
                print(f'{file} downloaded correctly.')
            elif r.status_code == 404:
                print(f"We couldn't find {file_name} in the especified URL.\nBye.")
                quit()  
            else:
                print(f'{r.status_code}\nWe found an unexpected error.\nBye.')
                quit()

        except Exception as err:
            print(f"{err}\nWe can't continue.\nBye.")
            quit()


while True:
    # General variables
    tg_count = {}
    count_lst = []
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')

    files = ((USER_URL,REFRESH_USER),(TG_NAME_URL,REFRESH_TG_NAME),(SUBSCRIBER_URL,REFRESH_LOCAL))
    for url,update in files:
        file_update(url,update)

    try:
        with Path(PATH_TO_LOG,LOG_NAME).open() as log:
            for line in log:
                if '*CALL END*' not in line: continue
                line_split = line.split()
                if line_split[1] != today: continue
                if line_split[10] in VANISH: continue
                tg_number = line_split[16]
                qso_time = float(line_split[-1])
                call_id = line_split[10]
                if qso_time < 6 : continue

                if tg_number not in tg_count :
                    tg_count[tg_number] = {'count':1, 'qso_count':qso_time, 'call_sign':{}}
                else:
                    tg_count[tg_number]['count'] += 1
                    tg_count[tg_number]['qso_count'] += qso_time

                if len(call_id) == 7 or 6:
                    if call_id not in tg_count[tg_number]['call_sign']:
                        tg_count[tg_number]['call_sign'][call_id] = 1
                    else:
                        tg_count[tg_number]['call_sign'][call_id] += 1

    except FileNotFoundError as err:
        print(f'{err}\nPlease check the name and the path to the log file and try again.\nBye')
        quit()


    # Make a list  of the DMR ID found.
    id_lst = []
    for tg in tg_count:
        for dmr_id in tg_count[tg]['call_sign']:
            if dmr_id not in id_lst:
                id_lst.append(dmr_id)

    # Make a dictionary of the found IDs
    id_dict = {}
    with open(USER_URL.split('/')[-1], encoding='utf-8') as csv:
        data_usercsv = reader(csv)
        for row in data_usercsv:
            if len(row) < 7: continue
            if row[0] in id_lst:
                id_dict[row[0]] = row[1]
                ## print(id_dict)
        del data_usercsv

    # Make a dictionary with the user IDs
    with open(SUBSCRIBER_URL.split('/')[-1],encoding='utf-8') as local_json:
        data_localjson = jload(local_json)
        for user in data_localjson['results']:
            id_ = str(user['id'])
            if id_ in id_lst:
                id_dict[id_] = user['callsign']
        del data_localjson

    # Translate the DMR ID to callsing in the main dictionary.
    for tg_num in tg_count:
        for id_num,value in list(tg_count[tg_num]["call_sign"].items()):
            try:
                int(id_num)/1
                if id_num in id_dict:
                    tg_count[tg_num]['call_sign'][id_dict[id_num]] = value
                    del tg_count[tg_num]['call_sign'][id_num]
                else:
                    tg_count[tg_num]['call_sign']['N0CALL'] = value
                    del tg_count[tg_num]['call_sign'][id_num]

            except ValueError:
                continue

    # Sort the callsing for every TG
    for ser_name in tg_count:
        temp_ = []
        for key,value in tg_count[ser_name]['call_sign'].items():
            temp_.append((value,key))
        temp_.sort(reverse=True)
        tg_count[ser_name]['call_sort'] = []
        for value,key in temp_:
            tg_count[ser_name]['call_sort'].append(key)
        del tg_count[ser_name]['call_sign']

    #Sort the dictionary for the top TG
    for key, value in tg_count.items():
        count_lst.append((value['qso_count'],key))
        count_lst.sort(reverse=True)

    #Make a list of the 20 first TG
    final_tg = []
    for value,key in count_lst[:20] :
        final_tg.append(key)

    with open(TG_NAME_URL.split('/')[-1], encoding='utf-8') as tg_json:
        data_tgjson = jload(tg_json)
        for tg_id in data_tgjson["results"]:
            if str(tg_id['id']) in final_tg :
                tg_count[str(tg_id['id'])]['tg_name'] = tg_id['callsign']
        del data_tgjson

    try:
        with Path(PATH_TO_TEMPLATE,TEMPLATE_NAME).open() as template:
            template_lines = template.readlines()
            # Where is the end of the table header
            count = 0
            header_end = 0
            for line in template_lines:
                count += 1
                if header_end == 0:
                    if '</tr>' in line:
                        header_end = count
                if '</table>' in line:
                    table_end = count - 1
                    break

    except FileNotFoundError as err:
        print(f'{err}\nPlease check the name and the path to the template file and try again.\nBye')
        quit()

    with Path(PATH_TO_WRITE,WRITE_FILE).open('+w') as new :
        for line in template_lines[:header_end] :
            new.write(line)

        for tg_id in final_tg :
            qso_count = tg_count[tg_id]['count']
            qso_time = min_sec(round(tg_count[tg_id]['qso_count']/60, 2))
            user = " - ".join(tg_count[tg_id]['call_sort'][:4])

            new.write('    <tr>\n')
            new.write(f'        <td>&nbsp;<b>{tg_id}</b>&nbsp;</td>\n')
            if 'tg_name' in tg_count[tg_id]:
                tg_name = tg_count[tg_id]['tg_name']
                new.write(f'        <td>&nbsp;<b>{tg_name}</b>&nbsp;</td>\n')
            else:
                new.write('        <td>&nbsp;<b></b>&nbsp;</td>\n')
            new.write(f'        <td>&nbsp;<b>{qso_count}</b>&nbsp;</td>\n')
            new.write(f'        <td>&nbsp;<b>{qso_time}</b>&nbsp;</td>\n')
            new.write(f'        <td>&nbsp;<b>{user}</b>&nbsp;</td>\n')
            new.write('    </tr>\n')

        for line in template_lines[table_end:]:
            new.write(line)
        
        del template_lines
        
    final_tup = (tg_count, count_lst, VANISH, id_lst, id_dict, final_tg)
    for ite in final_tup:
        del ite
    del final_tup

    print(f"Done!, now we'll wait {TIME_TO_WRITE} minute(s)")
    sleep(TIME_TO_WRITE*60)
