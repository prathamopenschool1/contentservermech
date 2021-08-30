import os
import logging
import platform
from zipfile import BadZipFile, ZipFile



infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")


def extraction(file_with_path, AppName):

    system_os = platform.system()

    path = os.getcwd()
    if system_os == "Windows":
        new_path = os.path.join(path, r'storage'+'\\'+str(AppName)+'\\'+r'content\zips')
        # print("new path is", new_path)
    else:
        new_path = os.path.join(path, 'storage/'+str(AppName)+'/content/zips')
    index = ''
    try:
        with ZipFile(file_with_path, 'r') as zip1:
            zip1.extractall(new_path)
            index_files = zip1.namelist()

            for s in index_files:
                if 'index.html' in s:
                    index = s
                    return index
                else:
                    continue
            else:
                infoLogger.info("only for Android: " + str(AppName) + ' in ' + str(new_path))
                return "-2"
    except BadZipFile as bd:
        errorLogger.error(str(bd) + " for : " + str(AppName) + ' in ' + str(new_path))
        return '-1'

# extraction(r"C:\contentservermech\contentserver\pos\static\storage\content\extractions\Pictionary_L1_HI.zip")
