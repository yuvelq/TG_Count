from datetime import datetime
from json import load as jload
from os.path import getmtime, getsize
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
__version__    = '1.6.0 Beta'


try: 
    from config import *
except:
    print('config.py file is missing.')
    quit()


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
                global id_dict
                id_dict = {}
            elif r.status_code == 404:
                print(f"We couldn't find {file} in the especified URL.")
                quit()
            else:
                print(f'{r.status_code}\nWe found an unexpected error.')
                quit()

        except Exception as err:
            print(f"{err}\nWe can't continue.")
            quit()


# Resolve DMR ID
def resolve_cs(dmr_id):
    if not isinstance(dmr_id,int):
        return dmr_id
    else:
        if dmr_id in id_dict:
            return id_dict[dmr_id]
        else:
            return 'N0CALL'


# General variables
today = None
id_dict = {}
size_ref = None

while True:

    if DOWNLOAD_FILES:
        files = ((USER_URL,REFRESH_USER), (TG_NAME_URL,REFRESH_TG_NAME), (SUBSCRIBER_URL,REFRESH_LOCAL))
        for url,update in files:
          file_update(url,update)
    else:
        file_update(TG_NAME_URL,REFRESH_TG_NAME)

    
    date_utc = datetime.strftime(datetime.utcnow(), '%Y-%m-%d')
    date_sys = datetime.strftime(datetime.now(), '%Y-%m-%d')

    if not today:
        tg_count = {}
        if SERVER_IN_DOCKER:
            today = date_utc
        else:
            today = date_sys        
    else:
        if SERVER_IN_DOCKER:
            if today != date_utc:
                today = None
                continue
        else:
            if today != date_sys:
                today = None
                continue

    # Reset pointer by delta size
    file_size = getsize(Path(PATH_TO_LOG,LOG_NAME))
    if not size_ref:
        size_ref = file_size
        last_line = None
    else:
        if not file_size or size_ref > file_size:
            size_ref = file_size
            last_line = None
        else:
            size_ref = file_size

    try:
        with Path(PATH_TO_LOG,LOG_NAME).open() as log:
            if last_line:
                    log.seek(last_line)

            for line in log:
                if LOG_NAME == 'lastheard.log':
                    line_split = line.rstrip().split()
                    if line_split[0] != today: continue
                    qso_time = float(line_split[2].split(',')[1])
                    if qso_time < 6 : continue
                    call_id = int(''.join(line_split[3:]).split(',')[8])
                    if call_id in VANISH: continue
                    tg_number = int(line_split[3].split(',')[6][2:])

                else:
                    if '*CALL END*' not in line: continue
                    line_split = line.rstrip().split()
                    if line_split[1] != today: continue
                    if line_split[11][1:-1] in VANISH: continue
                    try:
                        if line_split[-3] == 'Packet':
                            tg_number = int(line_split[-12][1:-2])
                            qso_time = float(line_split[-1][:-2])
                        else:
                            tg_number = int(line_split[-5][1:-2])
                            qso_time = float(line_split[-1])
                    except Exception as err:
                        print(f'Unrecognized log format, skipping this line:\n {err}')
                        continue
                    if qso_time < 6 : continue

                    call_id = line_split[10]
                    if call_id.isdigit():
                        call_id = int(line_split[10])

                if tg_number not in tg_count :
                    tg_count[tg_number] = {'count':1, 'qso_count':qso_time, 'call_sign':{}}
                else:
                    tg_count[tg_number]['count'] += 1
                    tg_count[tg_number]['qso_count'] += qso_time

                if call_id not in tg_count[tg_number]['call_sign']:
                    tg_count[tg_number]['call_sign'][call_id] = qso_time
                else:
                    tg_count[tg_number]['call_sign'][call_id] += qso_time

            last_line = log.tell()
        del log

    except FileNotFoundError as err:
        print(f'{err}\nPlease check the name and the path to the log file and try again.\nBye')
        quit()


    if DOWNLOAD_FILES:
        if not id_dict:
            # Make a dictionary of the IDs
            with open(USER_URL.split('/')[-1], encoding='utf-8') as csv:
                data_usercsv = reader(csv)
                for row in data_usercsv:
                    if len(row)  < 7 or not row[0].isdigit(): continue
                    if row[0] not in id_dict:
                        id_dict[int(row[0])] = row[1]
                del data_usercsv

            # Make a dictionary with the user IDs
            with open(SUBSCRIBER_URL.split('/')[-1],encoding='utf-8') as local_json:
                data_localjson = jload(local_json)
                for user in data_localjson['results']:
                    id_ = user['id']
                    if id_ not in id_dict:
                        id_dict[id_] = user['callsign']
                del data_localjson


    # Sort the callsing for every TG
    for tg_name in tg_count:
        temp_ = []
        for key,value in tg_count[tg_name]['call_sign'].items():
            temp_.append((value,resolve_cs(key)))

        sorted(temp_,reverse=True)
        tg_count[tg_name]['call_sort'] = []
        for value,key in temp_[:4]:
            tg_count[tg_name]['call_sort'].append(key)


    # Sort the dictionary for the top TG
    count_lst =sorted([(value['qso_count'],key) for key,value in tg_count.items()],reverse=True)

    #Make a list of the 20 first TG
    final_tg =[key  for value,key in count_lst[:20]]


    # Resolve TG name
    with open(TG_NAME_URL.split('/')[-1], encoding='utf-8') as tg_json:
        data_tgjson = jload(tg_json)
        for tg_id in data_tgjson["results"]:
            if tg_id['tgid'] in final_tg and 'tg_name' not in tg_count[tg_id['tgid']] :
                tg_count[tg_id['tgid']]['tg_name'] = tg_id['callsign']
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
        print(f'{err}\nPlease check the name and the path to the template file and try again.')
        quit()


    with Path(PATH_TO_WRITE,WRITE_FILE).open('+w',encoding='utf-8') as new :
        for line in template_lines[:header_end] :
            new.write(line)

        for tg_id in final_tg:
            qso_count = tg_count[tg_id]['count']
            qso_time = min_sec(round(tg_count[tg_id]['qso_count']/60, 2))
            user = " - ".join(tg_count[tg_id]['call_sort'])

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


    if DOWNLOAD_FILES:
        final_tup = (count_lst, final_tg)
    else:
        final_tup = (count_lst, final_tg)

    for ite in final_tup:
        del ite
    del final_tup

    print(f"Done!, now we'll wait {TIME_TO_WRITE} minute(s)")
    sleep(TIME_TO_WRITE*60)
