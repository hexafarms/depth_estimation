from dataclasses import dataclass
import numpy as np
from typing import List, Dict
import cv2
from pathlib import Path
from matplotlib import pyplot as plt

def _computeDisparity(stereo: object, img1_rect: np.ndarray, img2_rect: np.ndarray) -> np.ndarray:
    return stereo.compute(img1_rect, img2_rect).astype(np.float32)/16

def _check_color(file_name: Path):
    color_code = file_name.stem.split('-')[-2]
    assert color_code in ['rgb', 'ir'], f"Color code is neither rgb nor ir. It is {color_code}."
    return color_code

@dataclass
class HexaStereo:
    """Class for keeping track of stereo images."""
    distance: int # distance between two cameras in mm
    cam_codes: str # unique camera code
    base_depth: int # manually measured depth to the pot in mm
    rgb: List[np.ndarray] = None # rgb channel
    ir: List[np.ndarray] = None # gray channel


    def registerRGB(self, filepaths: List[Path]) -> "HexaStereo":
        """
        Input: [rgb image 1, rgb image 2]
        """
        assert len(filepaths) == 2, f"Not two files are in the list. Here are files {filepaths}"
        assert self._check_color(filepaths[0]) == _check_color(filepaths[1]), f"Error! Two different color codes are found."            
        
        self.rgb = [
                cv2.cvtColor(cv2.imread(filepaths[0].__str__()), cv2.COLOR_BGR2RGB), 
                cv2.cvtColor(cv2.imread(filepaths[1].__str__()), cv2.COLOR_BGR2RGB)
                ]
        return self

    def registerIR(self, filepaths: List[str]) -> "HexaStereo":
        """
        Input: [ir image 1, ir image 2]
        """
        assert len(filepaths) == 2, f"Not two files are in the list. Here are files {filepaths}"
        assert self._check_color(filepaths[0]) == _check_color(filepaths[1]), f"Error! Two different color codes are found."            
        
        self.ir = [
            cv2.cvtColor(cv2.imread(filepaths[0].__str__()), cv2.COLOR_BGR2GRAY), 
            cv2.cvtColor(cv2.imread(filepaths[1].__str__()), cv2.COLOR_BGR2GRAY)
            ]
        
        return self
        

@dataclass
class HexaPallelDepth(HexaStereo):
    """
    Class for keeping track of an depth eatimation.
    Assuming that two parallel(pre-rectified) images provided. 
    """
    rgb_disparity_map: np.ndarray = None
    ir_disparity_map: np.ndarray = None
    
    def computeDisparity(self, show: bool= True, minDisparity: int=10, numDisparities: int=35, blockSize: int= 11):
        stereo = cv2.StereoSGBM_create(minDisparity=minDisparity, numDisparities=numDisparities, blockSize=blockSize)

        self.rgb_disparity_map = _computeDisparity(stereo, self.rgb[0], self.rgb[1])
        self.ir_disparity_map = _computeDisparity(stereo, self.ir[0], self.ir[1])

        if show:
            fig, ax = plt.subplots(figsize=(16,8), nrows=2, ncols=2)
            ax[0,0].set_title('Left image')
            ax[0,0].imshow(self.rgb[0])
            ax[0,1].set_title('Right image')
            ax[0,1].imshow(self.rgb[1])

            ax[1,0].set_title('Disparity map (RGB)')
            im3 = ax[1,0].imshow(self.rgb_disparity_map)
            fig.colorbar(im3, ax=ax[1,0], fraction=0.03, pad=0.04)

            ax[1,1].set_title('Disparity map (IR)')
            im4 = ax[1,1].imshow(self.ir_disparity_map)
            fig.colorbar(im4, ax=ax[1,1], fraction=0.03, pad=0.04)
            plt.show()

@dataclass
class HexaNonPallelDepth(HexaStereo):
    """
    Class for keeping track of an depth eatimation.
    Assuming that two non-parallel images provided.
    Additional rig geometry information and rectification is needed compared to HexaPallelDepth. 
    """
    pass