import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS


"""
This short scripts will organize the pics in current directory into year/month directories based on creation date
The creatin date is pulled from EXIF data
"""
 
def get_filenames_from_dir(path):
    image_files_list = list()
    for fn in os.listdir(path):
        if os.path.isfile(os.path.join(path, fn)) and fn.rpartition('.')[2].lower() == 'jpg':
            image_files_list.append(fn)
    print ("I've found {} pictures".format(len(image_files_list)))
    return image_files_list
    

def get_exif(fn):
    ret = dict()
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret
    

def build_exif_create_date_dict(path):
    fn_create_date = dict()    
    fn_list = get_filenames_from_dir(path)
    for fn in fn_list:
        img_data = get_exif('{}/{}'.format(path, fn))
        fn_create_date.update({fn: img_data.get('DateTimeOriginal')})
    return fn_create_date


def get_year_month_from_date(exif_c_date):
    exif_y_m = exif_c_date.split(':', 2)[:2]
    return exif_y_m


def organize_pics(fn_create_date, path):
    moved_image_number = 0
    for key, value in fn_create_date.iteritems():
        if not value:
            print('{} has no origin date'.format(key))
            pass
        else:
            y_and_m = get_year_month_from_date(value)
            year = y_and_m[0]
            month = y_and_m[1]
            new_path = os.path.join(path, year, month)
            if os.path.exists(new_path) and os.path.isdir(new_path):
                try:
                    shutil.move(os.path.join(path, key), os.path.join(new_path, key))
                except OSError as why:
                    print why
            else:
                try:
                    print('Creating new directory: {}'.format(new_path))
                    os.makedirs(new_path)
                    shutil.move(os.path.join(path, key), os.path.join(new_path, key))
                except OSError as why:
                    print why
            moved_image_number += 1
    print 'Moved {} images to folders'.format(moved_image_number)

if __name__ == '__main__':
    current_dir = os.getcwd()
    fn_create_date = build_exif_create_date_dict(current_dir)
    organize_pics(fn_create_date, current_dir)
