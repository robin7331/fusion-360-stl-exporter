![](https://github.com/robin7331/fusion-360-stl-exporter/blob/278a46c86478415c53f652c1e81449717dc26e73/media/banner.png)

# What it does

With complex designs you end up having many bodies you'd like to export and 3D print.
This script adds a one-click script for an automated STL export of specific bodies in your design.   
It also makes sure your timeline is at the very end before exporting so you don't miss anything.


# What is being exported
As with most designs, you might have stock parts like screws or nuts you don't want to export.   
**This script takes your project's name in camel_case and looks for bodies that have that name prepended to their own name.**

![](https://github.com/robin7331/fusion-360-stl-exporter/blob/ffbec123f7e391dc65842881dff77d9ff8a1cc5c/media/export.png)

Only those two bodies will be exported.

# How To Install

- Clone or download this repo to some folder on your machine
- Boot up Fusion 360 and and open the scripts dialog
![](https://github.com/robin7331/fusion-360-stl-exporter/blob/91b60065c28ce351a411eba46dbad3384e7c4443/media/install.png)
- Click the little plus icon and add the folder you cloned / downloaded
- You should now see the `export-stl` script
![](https://github.com/robin7331/fusion-360-stl-exporter/blob/73e54d9de395e4e86e50bc1008362e4f67a68373/media/export-stl.png)

# How To Use
When ready for exporting simply open the 'Add-Ins' dialog and double click on your script.
Depending on the size of your design this may take a few minutes.
   
When done a little dialog appears.   
The files are stored in the script directory.   
![](https://github.com/robin7331/fusion-360-stl-exporter/blob/093660dd761eab5a210f6c45f3af5e0658199036/media/files.png)


