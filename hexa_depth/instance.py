from dataclasses import dataclass
import numpy as np
from typing import List, Dict
import cv2
from pathlib import Path

def _check_color(self, file_name: str):
    color_code = Path(file_name).basename.split('-')[-2]
    assert color_code in ['rgb', 'ir'], f"Color code is neither rgb nor ir. It is {color_code}."
    return color_code

@dataclass
class HexaDepth:
    """Class for keeping track of an depth eatimation."""
    distance: int # distance between two cameras
    cam_codes: str 
    rgb: List[np.ndarray] = None
    ir: List[np.ndarray] = None
    rgb_depth_map: np.ndarray = None
    ir_depth_map: np.ndarray = None
    base_depth: int = 180 # mm

    @staticmethod
    def from_file(filepaths: Dict[List[str, str]]) -> "HexaDepth":
        """
        Input
        { 'rgb': [rgb image 1, rgb image 2], 'ir': [ir image 1, ir image 2] }
        """
        assert len(filepaths) == 2, f"Not two files are in the list. Here are files {filepaths}"
        assert _check_color(filepaths[0]) != _check_color(filepaths[1]), f"Error! Two different color codes are found."
        for filepath in filepaths:
                 
        
        rgb = [
            cv2.cvtColor(cv2.imread(filepaths[0]), cv2.COLOR_BGR2RGB), 
            cv2.cvtColor(cv2.imread(filepaths[1]), cv2.COLOR_BGR2RGB)
            ]
        ir = [
            cv2.cvtColor(cv2.imread(filepaths[0]), cv2.COLOR_BGR2GRAY), 
            cv2.cvtColor(cv2.imread(filepaths[1]), cv2.COLOR_BGR2GRAY)
            ]
