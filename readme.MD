## Computer vision tool to estimate a depth map from a pair of images

Currently beta version.

### Format of yaml
```
near:
  camera:
    - G8T1-K001-2173-0EWX
    - G8T1-K001-2173-0EX9
  distance: 72 # Baseline in mm
  depth: 180 # Z-Distance between the camera and a pot base.
medium:
  camera:
    - G8T1-K001-2173-0EW4
    - G8T1-K001-2173-0CVH
  distance: 175
  depth: 180
far:
  camera:
    - G8T1-K001-2173-0EX3
    - G8T1-K001-2173-0F0M
  distance: 216
  depth: 180
```