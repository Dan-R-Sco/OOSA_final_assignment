![alt text](https://coursera-university-assets.s3.amazonaws.com/a9/e4018cf6f3036dcc6762b8058a92f1/square.png "Logo Title Text 1")

# OOSA Final Assignment Repository
### S2002365

This repository contains the python files generated during for the OOSA Final Project Assignment, completed 28/02/2020. The scripts can be used to process raw LVIS data, find the ground elevation and output a gap-filled DEM. 

The original scripts from the OOSA-code-public repository can be found at https://github.com/edinburgh-university-OOSA/OOSA-code-public/tree/master/week4/lvis.  

 In this example, files from Operation IceBridge (airborne data that bridged the gap between ICESat and ICESat-2) are used over Pine Island Glacier, Antarctica. LVIS data can be downloaded from this  [website](https://lvis.gsfc.nasa.gov/Data/Data_Download.html). 
 
The scripts developed during the assignment are described here:

## lvisClass .py 
---

This script was originally written by Steve and imported from [assignment_2020](https://github.com/edinburgh-university-OOSA/assignment_2020) into my repository. 

It creates a class (**lvisData**) to hold LVIS data
with methods to read. Please refer to the [original README](https://github.com/edinburgh-university-OOSA/assignment_2020/blob/master/README.md) for more detail. 

### *Methods include*: 
 - **readLVIS()** - reads LVIS data from input file 
 - **setElevations()** - decodes LVIS's RAM efficient elevation format and produces an array of elevations per waveform bin
 - **getOneWave()** - returns a single waveform as an array 
 - **dumpCoords()** - returns all coords as two arrays 
 - **dumpBounds()** - returns bounds (minX, minY, maxX, maxY)
 
 #### *Usage Example*

```python
#import
from lvisClass import lvisData
#initialise class
lvis = lvisData(inName)
#set the elevation arrays  
lvis.setElevations()
```
*This example code reads in the entire dataset into RAM, and then sets the elevation arrays so the data is now ready to be processed. In order to  subset the data into a smaller amount, it is possible to set some bounds. Please refer  to the usage example given in the [original README](https://github.com/edinburgh-university-OOSA/assignment_2020/blob/master/README.md) to do this.*


## processLVIS .py 
---
In this script a class (**lvisGround**) is created that inherits from the **lvisData** class (in *lvisClass.py* script) and adds the following additional methods to process LVIS data (HDF5 file): 
  - **estimateGround()** - calls on the appropriate other methods in the class to process waveforms and estimate ground. Populates *self.zG*. 
  - **setThreshold()** - sets a noise threshold 
  - **CofG()** - finds center of gravity for all waveforms in the file to generate a new array that populates *self.zG*. This represents the estimated ground elevation. 
  - **findStats()** - finds standard deviation and mean of noise. Populates *self.meanNoise* and *self.stdevNoise*. 
  - **denoise()** - denoises waveform data, populating *self.denoised*. 

#### *Usage Example*

```python
#import
from processLVIS import lvisGround
#initialise class
lvis = lvisData(inName)
#set the elevation arrays  
lvis.setElevations()
lvis.estimateGround()
```
*This example code reads in the entire dataset into RAM, sets the elevation arrays and runs a series of methods to estimate the ground elevation from each waveform. It is recommended to subset the data by using bounds (see above) in order to minimise issues with processing time.*




## task1 .py 
---
This script can be used to process a single LVIS flightline (HDF5 file) into a DEM of any resolution required by the user. 

A series of inputs can be defined at the commandline by the user, or left as default. These options include: 
- Input filename 
- Output filename (default *data.tif*)
- Resolution (m)
- Use of bounds (Yes/No, default *No*)
- Subset value (default *0*)

#### *Usage Example*

```python
python3 task1.py --input filename1.h5 --output file1.tif --res 10 --bounds Yes --subset 2 
```
*This example code takes the file **filename1.h5** , finds the data's bounds (user input), and in this case reads the bottom left quarter  in  into RAM. It then runs the methods to set the elevation arrays, find the ground elevations, reproject and finally write the output tiff (**file1.tif**) to memory.*
