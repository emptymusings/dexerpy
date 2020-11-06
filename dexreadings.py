from pydexcom import Dexcom
import json
import sys
import getopt

def main(argv):
    dexcom_user_name = ''
    dexcom_password = ''
    db_user_name = ''
    db_password = ''
    most_recent = True

    try:
        opts, args = getopt.getopt(argv, "",['dex-user=', 'dex-pw=', 'db-user=', 'db-pw', 'max'])
    except getopt.GetoptError:
        print(f'dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --db-user <database username> --db-pw <database password> --max')
        sys.exit(2)
    
    for opt, arg in opts:
        if opt == '-h':
            print(f'dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --db-user <database username> --db-pw <database password> [--max]')
            sys.exit()
        elif opt == '--dex-user':
            dexcom_user_name = arg
        elif opt == '--dex-pw':
            dexcom_password = arg
        elif opt == '--db-user':
            db_user_name = arg
        elif opt == '--db-pw':
            db_password = arg
        elif opt == '--max':
            most_recent = False
        else:
            print(f'Invalid Argument.')
            print(f'dexreadings.py --dex-user <dexcom username> --dex-pw <dexcom password> --db-user <database username> --db-pw <database password>')
            sys.exit()

    bgs = get_readings(dexcom_user_name, dexcom_password, most_recent)

    print(f'Got {len(bgs)} readings -> parsing')

    for bg in bgs:
        print(bg.__dict__)

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

if __name__ == '__main__':
    main(sys.argv[1:])