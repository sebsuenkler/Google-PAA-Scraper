#function to create the user directory with addons to make parallell calls of firefox
import string
import random
import os
import shutil


def create_user_dir():

    def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    data_dir = 'user-data-dirs/'+id_generator()

    if not os.path.exists(data_dir):

        dest_dir = data_dir+'/extensions'

        os.makedirs(dest_dir)

        src_dir = 'user-data-dirs/addons'


        for root, dirs, files in os.walk(src_dir):  # replace the . with your starting directory
           for file in files:
              path_file = os.path.join(root,file)
              shutil.copy2(path_file, dest_dir) # change you destination dir


    return data_dir
