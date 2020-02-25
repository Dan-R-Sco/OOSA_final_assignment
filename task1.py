
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
    p.add_argument("--res", dest = "res", type=int, default=10, help=("Resolution of data processing \nDefault=10m"))
    cmdargs = p.parse_args()
    return cmdargs


##########################################
# main
if __name__ == '__main__':
  # read the command line
  cmdargs=getCmdArgs()

  #sets filename as the input from the command line parser
  #inName=cmdargs.inName
  res = cmdargs.res
  #outName = cmdargs.outName

  # if using bounds
    # initialise class, find bounds
  #b=tiffHandle(inName,onlyBounds=True)

  # set some bounds
  #x0=b.bounds[0]
  #y0=b.bounds[1]
  #x1=(b.bounds[2]-b.bounds[0])/150+b.bounds[0]
  #y1=(b.bounds[3]-b.bounds[1])/150+b.bounds[1]

  #initialise class
  lvis = tiffHandle(inName) #using no bounds
  #lvis=tiffHandle(inName,minX=x0,minY=y0,maxX=x1,maxY=y1) #if using bands, read in bands

  # set elevation
  lvis.setElevations()
  # find the ground
  lvis.estimateGround()
  #reproject lat and long coords
  lvis.reproject(4326,3031)
  #write tiff for bounds
  lvis.writeTiff(lvis.zG,res,outName)
