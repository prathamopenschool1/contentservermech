import os
import json
import logging



infoLogger = logging.getLogger("info_logger")
errorLogger = logging.getLogger("error_logger")

class NodeDeleter(object):

    channel_name = ""
    store_files = ""
    store_img = ""
    files_data = ""
    zip_files = ""
    video_files = ""
    audio_files = ""
    m4v_files = ""
    mp4_files = ""
    mp3_files = ""
    wav_files = ""
    pdf_files = ""
    wrong_extension = ""
    localUrl = ""

    current_dir = os.getcwd()
    new_current_dir = os.path.join(current_dir, 'storage')

    headers = {
        'cache-control': "no-cache",
        'content-type': "application/json",
        "Accept": "application/json"
    }


    def child_node_dir(self, appName, filename_obj):
        print('static path >>>>>>>>. .', self.new_current_dir, self.current_dir)
        print("self >>>> ", appName, filename_obj)

        self.channel_name = os.path.join(self.new_current_dir, appName)
        print("sefl storre >>>>>>>>>>> ", self.channel_name)

        self.store_files = os.path.join(self.channel_name, 'content')
        self.store_img = os.path.join(self.channel_name, 'images')

        for files_ in filename_obj:
            print(files_, type(files_))
            if files_.endswith('.png') or files_.endswith('.jpg') or files_.endswith('.jpeg') or files_.endswith('.mpeg'):
                fname = os.path.join(self.store_img, files_)
                print("new fname >>>> ", fname)
                file_exists = os.path.exists(fname)
                print(">>>>>>> f exists ", file_exists)
            else:
                continue




