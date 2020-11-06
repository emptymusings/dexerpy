from pydexcom import Dexcom
import json
import sys
import getopt
import mariadb
from datetime import datetime

def main(argv):
    dexcom_user_name = ''
    dexcom_password = ''
    db_server = ''
    db_port = 3306
    db_user_name = ''
    db_password = ''
    database = ''
    most_recent = True

    try:
        opts, args = getopt.getopt(argv, "",['dex-user=', 'dex-pw=', 'server=', 'port=', 'db-user=', 'db-pw=', 'db=', 'max'])
    except getopt.GetoptError:
        print(f'Error parsing arguments.  Usage: dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --server <mariaDb server> --port <mariaDb port> --db-user <database username> --db-pw <database password> --db <database name> [--max]')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(f'Usage: dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --server <mariaDb server> --port <mariaDb port> --db-user <database username> --db-pw <database password> --db <database name> [--max]')
            sys.exit()
        elif opt == '--dex-user':
            dexcom_user_name = arg
        elif opt == '--dex-pw':
            dexcom_password = arg
        elif opt == '--server':
            db_server = arg
        elif opt == '--port':
            db_port = arg        
        elif opt == '--db-user':
            db_user_name = arg
        elif opt == '--db-pw':
            db_password = arg
        elif opt == '--db':
            database = arg
        elif opt == '--max':
            most_recent = False
        else:
            print(f'Invalid Argument.')
            print(f'Usage: dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --server <mariaDb server> --port <mariaDb port> --db-user <database username> --db-pw <database password> --db <database name> [--max]')
            sys.exit()

    bgs = get_readings(dexcom_user_name, dexcom_password, most_recent)
    print(f'Got {len(bgs)} readings -> storing results')
    
    store_readings(db_user_name, db_password, db_server, db_port, database, bgs)

def get_readings(dexcom_user_name, dexcom_password, latest_reading = True):
    dexcom = Dexcom(dexcom_user_name, dexcom_password)
    bgs = []

    if (latest_reading):
        print('Getting latest reading from Dexcom')
        bgs.append(dexcom.get_current_glucose_reading())
    else:
        print('Getting max readings from Dexcom')
        bgs = dexcom.get_glucose_readings()

    return bgs

def store_readings(db_user_name, db_password, host, port, database, bgs):
    try:    
        connection = mariadb.connect(
            user=db_user_name,
            password=db_password,
            host=host,
            port=port,
            database=database        
        )
    

        cursor = connection.cursor()

        sql_command = f'INSERT INTO {database}.values (mg_dl, mmol_l, trend_val, trend_desc, reading_time) VALUES(?, ?, ?, ?, ?)'
        records = []

        for bg in bgs:
            records.append((bg.mg_dl, bg.mmol_l, bg.trend, bg.trend_description, datetime.strftime(bg.time, "%Y-%m-%d %H:%M:%S")))
        
        print(f'Sending {len(bgs)} readings to database')      
        cursor.executemany(sql_command, records)
        connection.commit()
        print(f'Readings saved successfully')

    except mariadb.Error as e:
            print(f"Error storing data to the database: {e}")
            sys.exit(1)

    finally:    
        connection.close()


if __name__ == '__main__':
    main(sys.argv[1:])