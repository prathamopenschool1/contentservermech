import os
import string
import secrets
import requests
import logging
from pathlib import Path
from zipfile import ZipFile
from subprocess import PIPE, Popen



class CommonHelpers:

    homeDir = str(Path.home())
    tmpDir = os.path.join(homeDir, 'tmp')

    # This retrieves a Python logging instance (or creates it)
    infoLogger = logging.getLogger("info_logger")
    errorLogger = logging.getLogger("error_logger")

    @classmethod
    def create_tmp_dir(cls):
        if not os.path.exists(cls.tmpDir):
            os.makedirs(cls.tmpDir)
    
    @classmethod
    def get_secret_string(cls, length):
        secret_string = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))
        return secret_string

    # TO extract knowledge portal zip
    @classmethod
    def get_the_zip(cls):
        #upgrade_dns()

        check_path = '/var/www/'

        if os.path.exists(check_path):
            try:
                zip_file_url = "http://rpi.prathamskills.org/apps/index.zip"
                path_to_put = "/var/www/html/index.zip"

                os.system('sudo chmod 777 -R /var/www/')

                if os.path.exists(path_to_put):
                    os.system('sudo rm -rf /var/www/html/index.zip')

                file_to_get = requests.get(zip_file_url)

                with open(path_to_put, "wb") as new_file:
                    for chunk in file_to_get.iter_content(chunk_size=1024):
                        new_file.write(chunk)

            except Exception as d:
                print(d)
                cls.errorLogger.error("Error Exception 1 while extarcting knowledge portal zip :--- " + str(d))

            try:
                file_name = "/var/www/html/index.zip"
                with ZipFile(file_name, 'r') as zip:
                    zip.extractall('/var/www/html/')
                cls.infoLogger.info("Extracting knowledge portal Done >>")
            except Exception as e:
                print(e)
                cls.errorLogger.error("Error Exception 2 while extarcting knowledge portal zip :--- " + str(e))

            print("Done >>")
