# dexerpy
Tracks glucose readings from the Dexcom G6 over time by storing them in a MariaDB database, utilizing the pydexcom package.

## Requirements
- Python
- A MariaDB server (this package *may* need to be installed on the local client, as well, when using a remote server)
- installation for packages in the `requirements.txt

## Usage
Run `dexreadings.py` using the python command line (note, all arguments are required):
```sh
python3 dexreadings.py --dex-user <dexcom user name> --dex-pw <dexcom password> --server <url or IP address of the MariaDb server> --port <port of the MariaDb server, 3306 by default> --db-user <MariaDb username> --db-pw <MariaDb password> --db <MariaDb database>
```
