import os
import shutil
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
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    # TO extract knowledge portal zip
    @classmethod
    def get_the_zip(cls):
        #upgrade_dns()

        check_path = '/var/www/'

        if os.path.exists(check_path):
            try:
                zip_file_url = "http://rpi.prathamskills.org/apps/index.zip"
                # path_to_put = "/var/www/html/"
                path_to_put = os.path.join(check_path, 'html')

                # os.system('sudo chmod 777 -R /var/www/')
                os.system(f'sudo chmod 777 -R {check_path}')

                index_file = os.path.join(path_to_put, 'index.zip')

                if os.path.exists(index_file):
                    os.system(f'sudo rm -rf {index_file}')

                file_to_get = requests.get(zip_file_url)

                with open(index_file, "wb") as new_file:
                    for chunk in file_to_get.iter_content(chunk_size=1024):
                        new_file.write(chunk)

                cls.infoLogger.info("file downloaded successfully>>>")

            except Exception as d:
                cls.errorLogger.error(f"Error Exception 1 while extracting knowledge portal zip :--- {str(d)}")

            try:
                # file_name = "/var/www/html/index.zip"
                with ZipFile(index_file, 'r') as zip:
                    zip.extractall(path_to_put)
                
                src_dirs = os.path.join(path_to_put, 'index')
                dest_dirs = path_to_put

                cls._copy_all(src_dirs, dest_dirs)
                cls.infoLogger.info("Extracting knowledge portal Done >>")
            except Exception as e:
                cls.errorLogger.error(f"Error Exception 2 while extarcting knowledge portal zip :--- {str(e)}")

    @classmethod
    def _copy_all(cls, src_dirs, dest_dirs):

        try:
            for file_name in os.listdir(src_dirs):
                source = os.path.join(src_dirs, file_name)
                destination = os.path.join(dest_dirs, file_name)

                if os.path.isfile(source):
                    shutil.copy(source, destination)
                elif os.path.isdir(source):
                    shutil.copytree(source, destination)

            cls.infoLogger.info("Copied successfully")

        except Exception as e:
            cls.errorLogger.error(f"Error Exception 2 while copying files  :--- {str(e)}")






