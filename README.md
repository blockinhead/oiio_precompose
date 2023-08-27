# OpenImageIO precompose script  
  
## Overview
This is a script to precompose multiple exr sequences to a single result exr sequence. The sequences may be of different length, so you can use a still background image.  
This script relies on 
- OpenImageIO which can be built by [these](https://github.com/OpenImageIO/oiio/blob/master/INSTALL.md) instructions. Some windows binaries can be found [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#openimageio).
- clique, which can be installed with pip  
  
The script is intended to be used in post-render automations

## Usage
```shell
python oiio_precompose.py --src /some/path/bg.*.exr --src /some/path/mg.*.exr --src /some/path/fg.*.exr --start 1 --end 91 --target /some/path/res
```  
this will create a new sequence ```/some/path/res.0001.exr .. res.0091.exr```  
