from dataclasses import dataclass
import numpy as np
from typing import List, Dict
import cv2
from pathlib import Path


@dataclass
class HexaStereo:
    """Class for keeping track of stereo images."""
    distance: int # distance between two cameras in mm
    cam_codes: str # unique camera code
    base_depth: int # manually measured depth to the pot in mm
    rgb: List[np.ndarray] = None # rgb channel
    ir: List[np.ndarray] = None # gray channel

    def _check_color(self, file_name: Path):
        color_code = file_name.stem.split('-')[-2]
        assert color_code in ['rgb', 'ir'], f"Color code is neither rgb nor ir. It is {color_code}."
        return color_code

    def registerRGB(self, filepaths: List[Path]) -> "HexaDepth":
        """
        Input: [rgb image 1, rgb image 2]
        """
        assert len(filepaths) == 2, f"Not two files are in the list. Here are files {filepaths}"
        assert self._check_color(filepaths[0]) == self._check_color(filepaths[1]), f"Error! Two different color codes are found."            
        
        self.rgb = [
                cv2.cvtColor(cv2.imread(filepaths[0].__str__()), cv2.COLOR_BGR2RGB), 
                cv2.cvtColor(cv2.imread(filepaths[1].__str__()), cv2.COLOR_BGR2RGB)
                ]
        return self

    def registerIR(self, filepaths: List[str]) -> "HexaDepth":
        """
        Input: [ir image 1, ir image 2]
        """
        assert len(filepaths) == 2, f"Not two files are in the list. Here are files {filepaths}"
        assert self._check_color(filepaths[0]) == self._check_color(filepaths[1]), f"Error! Two different color codes are found."            
        
        self.ir = [
            cv2.cvtColor(cv2.imread(filepaths[0].__str__()), cv2.COLOR_BGR2GRAY), 
            cv2.cvtColor(cv2.imread(filepaths[1].__str__()), cv2.COLOR_BGR2GRAY)
            ]
        
        return self
        

@dataclass
class HexaDepth(HexaStereo):
    """Class for keeping track of an depth eatimation."""
    rgb_depth_map: np.ndarray = None
    ir_depth_map: np.ndarray = None
    #TODO: build depth estimation process.
    pass

