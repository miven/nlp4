import zipfile
path="/outputTMPlaji"
zipfile.ZipFile('济南市人民政府解读.zip').extractall(path)

import os
zip_list = os.listdir(path)
for zip_file in zip_list:


    try:
        zip_file1 = zip_file.encode('cp437').decode('gbk')

    except:
        zip_file1 = zip_file.encode('utf-8').decode('utf-8')
    os.rename(path+'/'+zip_file,path+'/'+zip_file1)
