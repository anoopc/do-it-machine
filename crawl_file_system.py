
import os
import shutil

image_cache = {}
image_types = ['png', 'jpeg', 'jpg', 'gif', 'mov']
total_size = 0

def get_extension(file):
    return os.path.splitext(file)[1][1:].lower()

def crawl(directory):
    global total_size
    for path, sub_dirs, files in os.walk(directory):
        for file in files:
            if get_extension(file) in image_types:
                # is an image file
                # if 'copy' in file:
                #     file_new_name = file[:file.find('copy')].strip() + os.path.splitext(file)[1]
                #     print '{} renamed name {}'.format(file, file_new_name)
                #     os.rename(os.path.join(path, file), os.path.join(path, file_new_name))
                #     file = file_new_name
                full_path = os.path.join(path, file)
                file_stat = os.stat(full_path)
                total_size += file_stat.st_size
                if file in image_cache:
                    print 'duplicate for {}, {}'.format(image_cache[file], full_path)
                    # print 'should remove file:{}'.format(full_path)
                    # os.remove(full_path)
                else:
                    image_cache[file] = full_path

def magic():
    destination_dir = '/Users/anoopchaurasiya/Desktop/Desktop1/iPhotoBackup'
    dir = '/Users/anoopchaurasiya/Pictures/iPhoto Library.photolibrary/Masters'
    counter = 0
    unique_counter = 0
    for path, sub_dirs, files in os.walk(dir):
        for file in files:
            if get_extension(file) in image_types:
                counter += 1
                full_path = os.path.join(path, file)
                if not file_already_exists(path, file):
                    unique_counter += 1
                    print 'will copy {}, {}'.format(file, full_path)
                    shutil.copyfile(full_path, os.path.join(destination_dir, file))
    print 'total Files:{}, unique count:{}'.format(counter, unique_counter)

def file_already_exists(path, file):
    if file in image_cache:
        full_path = os.path.join(path, file)
        if os.stat(full_path).st_size == os.stat(image_cache[file]).st_size:
            return 1
        else:
            print 'found false duplicate for file:{}, {}, {}'.\
                format(file, image_cache[file], full_path)
    return 0

def solve():
    # root_dirs = ['/Users/anoopchaurasiya/Pictures/iPhoto Library.photolibrary/Masters']
    root_dirs = ['/Users/anoopchaurasiya/Desktop/Desktop1']
    for root_dir in root_dirs:
        print 'crawling {}'.format(root_dir)
        crawl(root_dir)
        print 'current image count: {}'.format(len(image_cache))
    print 'total size: {} GB'.format((total_size / 1024.0 / 1024.0 / 1024.0))

def main():
    solve()
    magic()

if __name__ == '__main__':
    main()
