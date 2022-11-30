import yaml
import glob
import os
from pathlib import Path
from typing import List
import re

def checkCode(file: str, codes: List[str]):
    if file in codes:
        return True
    else:
        return False

def extractCode(file_name: str):
    """Extract camera code from file name. """
    camRegex = re.compile(r'\w\w\w\w-\w\w\w\w-\w\w\w\w-\w\w\w\w')  # Match the Code Pattern.
    return camRegex.search(file_name)[0]

def main(LOCAL_PATH, DEPTH, setup):
    #TODO: split list based on key, segment based on time. A nested list has two images. (if only one, then ignore it.)
    #TODO: work with RGB and IR. (See what's better)
    imgs = glob.glob(os.path.join(LOCAL_PATH, '*.jpg'))

    filtered_imgs = [[]]*len(setup)

    for i, (key, val) in enumerate(setup.items()):
        #TODO check if image file is within camera code
        
        if checkCode()
        filtered_imgs[i].append()
        
    imgs.sort(key = lambda x: Path(x).basename.split('-')[-1])
    print('h')
    pass

if __name__ == "__main__":
    
    LOCAL_PATH = "/media/huijo/SSD_Storage/S3_Download/ecf"
    DEPTH = 180 # mm

    with open('credential/hexa.yaml', 'r') as stream:
        setup = yaml.safe_load(stream)

    main(LOCAL_PATH, DEPTH, setup)