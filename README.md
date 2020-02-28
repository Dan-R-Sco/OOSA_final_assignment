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
 - **readLVIS()** - reads LVIS data from input file. **self.nodataflag added by me** 
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



## handleTiff .py 
---

This script contains a class containing methods that can be used to write and read geotiff files. It inherits from the **lvisGround()** class in the **processLVIS. py** script. Methods include: 
- **writeTiff(self, data, res, filename, epsg=3031)** - This takes an array RAM (data), a resolution (user specified - in m), an output filename and epsg projection to write a geotiff to disk. 
- **readTiff(self, filename, epsg=3031)** - This method can read a geotiff into RAM  

#### *Usage Example*

```python
#import
from processLVIS import lvisGround
#initialise class
lvis = tiffHandle(inName)
#set the elevation arrays  
lvis.setElevations()
lvis.estimateGround()
lvis.reproject(4326,3031)
lvis.writeTiff(self.zG, res, outName)
```
*This example code initialises a tiffHandle() class object, reads in the entire dataset (inName) into RAM, sets the elevation arrays and runs a series of methods to estimate the ground elevation from each waveform. It then reprojects the array from WGS 84 (4326) to Antarctic Polar Stereographic (3031) before writing a geotiff to disk (self.zG sets the ground elevations to be the input data, resolution and outName are specified by the user). Usually run through the task1 .py and task2 .py scripts which both feature a command line parser for these user inputs.*



## handleTiffPlus .py 
---

This script contains a class containing methods that can be used to write and read geotiff files. It does not inherit from lvisGround(), but it builds upon the methods in handleTiff() (described above). The difference is that this class is more suitable for processing geotiff inputs, reading them into RAM and then outputting new geotiffs. Methods include: 
- **readTiff(self, filename, epsg=3031)** - This method can read a geotiff into RAM. Used in this project to read in the individual flight line geotiffs to use for the merge function.  
- **writeTiff(self, data, res, filename, epsg=3031)** - This writes a new geotiff layer to disk from a raster that has been read into RAM by the readTiff function and other manipulation carried out. In this project this function is used in the gap fill method of task 2, when the **handleTiffPlus()** class is inherited by **gapFillTiff()**.


#### *Usage Example*

See the usage example below, for the gapFillTiff() class  used in task2. This calls on the methods of **handleTiffPlus()** when inherited. 


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



## task2 .py 
---
This script can be used to combine and gap fill the elevation data from the LVIS Icebridge flights. There are three main parts to the script: batch processing, merging rasters and gap fill function. 

Firstly, a series of inputs can be defined at the commandline by the user, or left as default. These options include: 
- Directory path (for files for batch processing)
- Year of dataset 
- Resolution (for creating rasters in batch processing)
- Subset value (for batch processing) 
- Input filename (for merging)
- Directory path (for files for tiff merging 
- Window size (for size of focal window in gap fill)

##### Functions and Methods
- **mergeTiffs()** - function to merge a series of tiffs into a single geotiff raster layer. Used in this project to merge DEMs of flightlines from the same year. 
- **gapFillTiff(tiffHandlePlus)** - class that adds a gap fill function to the tiffHandlePlus class. The **gapFill()** method includes a series of nested loops that use a moving focal window to identify and fill in no data pixels in the raster by assigning it a mean value of surrounding pixels (window size defined by the user). A window size of 30 pixels is recommended for the 2015 LVIS data in order to bridge (interpolate) the gaps between the flight lines.

##### if __name__ == '__main__':
- **Stage 1: Batch Processing** - a series of functions and methods called to batch process the data 
- **Stage 2: Merge** - merges the subsetted 2015 tiffs into one mosaicked raster. Can be adjusted slightly to complete for the 2009 files. 
- **Stage 3: Gap Fill**  - calls classes and methdos to fill the gaps of the resultant mosaicked raster. 

This has not been tested with all methods running one after another at once. I would recommend commenting out the sections of code in the execution section (bottom of script) to enable one stage (batch process vs merge vs gap fill) to be completed one at a time. This is an area of future  development of the code. 

#### *Usage Example (for geotiff merge - comment out stage 1 and 3)*

```python
python3 task2.py --input merged_file.tif --tiff_dir filepath_name 
```

