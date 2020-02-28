
'''
Script to batch process LVIS flight line data into tiffs and merge them into a single, gap-filled DEM
'''
#######################################################
# import necessary packages
from osgeo import gdal             # package for handling geotiff data
from osgeo import osr              # package for handling projection information
from gdal import Warp
import numpy as np
import argparse
import os
import time
import rasterio
from rasterio.merge import merge

#import other classes
from handleTiff import tiffHandle

##################################
# define a command line reader

def getCmdArgs():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Command line parser to provide filename and resolution"))
    p.add_argument("--input", dest ="inFilename", type=str, default="/home/s2002365/oosa/project/code/merged_2015.tif", help=("Input file \nDefault = 2015 Mosaicked Raster"))
    p.add_argument("--path", dest ="path", type=str, default="/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/", help=("Path to directory with files for batch processing"))
    p.add_argument("--year", dest ="year", type=str, default='_15.tif', help=("Enter ending to the filename to help identify (e.g. year of batch procesing) \nDefault='_15.tif'"))
    p.add_argument("--res", dest = "res", type=int, default=100, help=("Resolution of data processing \nDefault=100m"))
    p.add_argument("--subset", dest = "subset", type=int, default=3)
    p.add_argument("--tiff_dir", dest ="tiff_dir", type=str, default="/home/s2002365/oosa/project/code", help=("Path to directory with processed tiff files for merging"))
    p.add_argument("--window", dest = "window", type=int, default=30, help=("Number of pixels used to look in each direction in the focal window \nDefault=30"))
    cmdargs = p.parse_args()
    return cmdargs


##########################################

def mergeTiffs():

    '''Merges subsetted 2015 tiffs into a single raster'''

    tiff_dir = cmdargs.tiff_dir
    out_file = '/home/s2002365/oosa/project/code/merged_2015.tif'
    rasters_2015 = [f for f in os.listdir(tiff_dir) if f.endswith('.tif')and not f.endswith('_09.tif')]
    unmerged_2015 = []
    for raster in rasters_2015:
        src = rasterio.open(raster)
        unmerged_2015.append(src)

    # Merge function returns merged single raster and transform info
    merge_2015, out_trans = merge(unmerged_2015)

    #copy the metadata
    out_meta = src.meta.copy()

    #update metadata
    out_meta.update({"driver": "Gtiff",
                     "height": merge_2015.shape[1],
                     "width": merge_2015.shape[2],
                     "transform": out_trans,
                     "crs": "+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
                     }
                    )
    #write raster to disk
    with rasterio.open(out_file, "w", **out_meta) as dest:
        dest.write(merge_2015)
        print("Image written to ", out_file)

##########################################

class gapFillTiff(tiffHandlePlus):

    '''class to add gap fill function to tiffHandle class'''

    ##########################################

    def gapFill(self, data, window):

        '''fills gaps in DEM'''

        self.array = np.copy(data)
        for i in range(window,(self.nY-window)): #accounts for impact of array edge
            for j in range(window, (self.nX-window)):
                if self.array[i][j] == -999.0:
                    box = self.array[i-window: i+window, j-window: j+window] #creates temp variable for window array
                    tempFocalSum = 0
                    cellsVisited = 0
                    focalMean =0

                    #iterate through window to find pixels with data
                    for row in box:
                        for x in row:
                            if x >-100:
                                tempFocalSum += x
                                cellsVisited += 1

                    #calculate focal mean
                    if cellsVisited > 0:
                        focalMean = tempFocalSum/cellsVisited

                    #fill in gaps in array with focal mean
                    if focalMean > 0:
                        self.array[i][j] = focalMean

##########################################

# main
if __name__ == '__main__':

  # read the command line
  cmdargs=getCmdArgs()

  '''STAGE 1: batch process h5 data, with bounds to subset'''

  subset =cmdargs.subset
  res = cmdargs.res
  path = cmdargs.path
  year = cmdargs.year

  #produce list of h5 files in directory (not including oversea flight lines)
  h5_files = [f for f in os.listdir(path) if f.endswith('.h5')]
  for i in h5_files:
      inName= str(path) + str(i)
      b=tiffHandle(inName,onlyBounds=True)

      #define subset size
      subset_width = (b.bounds[2]-b.bounds[0])/subset
      subset_height = (b.bounds[3]-b.bounds[1])/subset

      #loop through to set set bounds
      for j in range(subset):
          for k in range(subset):
              x0=b.bounds[0] + (j*subset_width)
              y0=b.bounds[1] + (k*subset_height)
              x1=b.bounds[0] + ((j+1)*subset_width)
              y1=b.bounds[0] + ((k+1)*subset_height)

              #sets output filename for each DEM
              outName = str(i[26:-3]) + str(j) + year

              #initialise class
              lvis=tiffHandle(inName,minX=x0,minY=y0,maxX=x1,maxY=y1)

              #only writes tiffs for files containing data
              if lvis.nodataflag == 0:
                  lvis.setElevations()
                  lvis.estimateGround()
                  lvis.reproject(4326,3031)
                  lvis.writeTiff(lvis.zG,res,outName)

  '''STAGE 2: merge the subsetted 2015 tiffs into one mosaicked raster'''
  mergeTiffs()

  '''STAGE 3: fill the gaps of the mosaicked raster'''
  filename = cmdargs.inFilename
  window = cmdargs.window
  start_time = time.time()
  b=gapFillTiff()
  b.readTiff(filename)
  b.gapFill(b.data, window)
  b.writeTiff(b.array, 100, "gapFill_2015.tif")
  print("My program took "+ str(time.time() - start_time) + " seconds to run")
