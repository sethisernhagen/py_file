from argparse import ArgumentParser
import os
import shutil
import scandir

# person = raw_input('Enter your name: ')
# print('Hello', person)

ENDINGS = (
    ".avi",
    ".AVI",
    ".mp4",
    ".MP4",
    "-GTi",
    " HD",
    ".mkv",
    ".MKV"
)

SCAN_PATH = "F:\\movies"
TEST_MODE = False
MIN_SIZE = 1000000

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--noprompt",
        action="store_true",
        help="Do not prompt before deleting folder",
    )
    parser.add_argument(
        "--path",
        dest="scan_path",
        help="Path to scan",
    )
    return parser.parse_args()

def delete_folder(path):
    if(TEST_MODE):
        print("TEST DELETED: " + path)
    else:

        shutil.rmtree(path, ignore_errors=True)
        print("DELETED: " + path)
    print("\n")
        

def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in scandir.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total


def __main__():
    args = parse_args()
    
    for entry in os.listdir(args.scan_path):
        folder_path = os.path.join(args.scan_path, entry)
        
        try:
            if(os.path.isdir(folder_path)):
                if (len(os.listdir(folder_path)) == 0 or get_tree_size(folder_path) < MIN_SIZE):
                    if(folder_path.endswith(ENDINGS) or args.noprompt):
                        delete_folder(folder_path)
                    else:
                        do_delete = raw_input(folder_path + "?:")
                        if(do_delete == "y"):                
                            delete_folder(folder_path)    
        except Exception as error:
            print("{}-{}".format(folder_path, error))
                       
__main__()       
