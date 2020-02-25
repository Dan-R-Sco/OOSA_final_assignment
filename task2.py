
#######################################################
# import necessary packages

from osgeo import gdal             # package for handling geotiff data
from osgeo import osr              # package for handling projection information
from gdal import Warp
import numpy as np
import argparse
import os


from handleTiff import tiffHandle

##################################
# define a command line reader

def getCmdArgs():
    '''
    Read commandline arguments
    '''
    p = argparse.ArgumentParser(description=("Command line parser to provide filename and resolution"))
    p.add_argument("--input", dest ="inName", type=str, default="/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/ILVIS1B_AQ2015_1017_R1605_067952.h5", help=("Input file \nDefault = 10/17/2015"))
    p.add_argument("--output", dest ="outName", type=str, default="data.tif", help=("Input file \nDefault = data.tif"))
    p.add_argument("--res", dest = "res", type=int, default=100, help=("Resolution of data processing \nDefault=10m"))
    p.add_argument("--subset", dest = "subset", type=int, default=3)
    cmdargs = p.parse_args()
    return cmdargs


##########################################
# main
if __name__ == '__main__':
  # read the command line
  cmdargs=getCmdArgs()


  '''batch process 2015 data, with bounds'''

  subset =cmdargs.subset
  res = cmdargs.res

  path = '/geos/netdata/avtrain/data/3d/oosa/assignment/lvis/2015/'
  h5_files = [f for f in os.listdir(path) if f.endswith('.h5') and not f.endswith('067952.h5') and not f.endswith('071670.h5') and not f.endswith('043439.h5') and not f.endswith('069267.h5')] #produces list of h5 files in 2015 directory (not including oversea flight lines)
  for i in h5_files:
      inName= str(path) + str(i)
      #outName = str(i[26:-3]) + '.tif'
      #print(outName)
      #print(inName)
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

              outName = str(i[26:-3]) + str(j) + '.tif'

              lvis=tiffHandle(inName,minX=x0,minY=y0,maxX=x1,maxY=y1)

              if lvis.nodataflag == 0:
                  lvis.setElevations()
                  lvis.estimateGround()
                  lvis.reproject(4326,3031)
                  lvis.writeTiff(lvis.zG,res,outName)
