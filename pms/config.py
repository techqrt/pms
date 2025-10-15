from decouple import config
 
class Configurations:
    db_name = config('DB_NAME')
    db_user = config('DB_USER')
    db_password = config('DB_PASSWORD')
    db_host = config('DB_HOST')
    db_port = config('DB_PORT')
    debug = False if config('DEBUG') == 'False' else True