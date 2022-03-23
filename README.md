# HEASARC and NEOSSat Data Viewer

nasa-spaceapps-2020

By George Berdovskiy and Shuzheng (Tom) Zhang

<p align="center">
  <img src="https://raw.githubusercontent.com/Shuzhengz/nasa-spaceapps-2020/main/static/readme/main.png" alt="Main Example Photo" width="750"/>
</p>

## Set up instructions:

1. Install pip, see how to do it at https://pip.pypa.io/en/stable/installation/
2. Install flask using `pip install flask`
3. Install packages using pip, you can see the full list in `requirements.txt`
    1. You can install them manually, or navigate to this directory in terminal/command prompt and type in:
        1. `pip install -r requirements.txt`
4. Navigate to directory `nasa-spaceapps-2020` in terminal/command prompt
5. Run the webapp using `python viewer.py`
    1. If you see line `Running on http://127.0.0.1:5000/` in the terminal, this indicates that the app is working
    2. If not, check for missing packages and dependencies
6. Now go to your browser (We have only tested Firefox), and type in `http://127.0.0.1:5000/` in the address bar
7. The webapp should now be up and running

## Features:

### Sky Sphere

A sphere that you can drag around and select an object to see and download its information

### HEASARC Search

Searching the HEASARC database to find your object

<p align="center">
  <img src="https://raw.githubusercontent.com/Shuzhengz/nasa-spaceapps-2020/main/static/readme/search.png" alt="Search Photo" width="550"/>
</p>

### List of Retrieved Objects

Lists the objects and lets the user download FITS image

<p align="center">
  <img src="https://raw.githubusercontent.com/Shuzhengz/nasa-spaceapps-2020/main/static/readme/list.png" alt="List" width="550"/>
</p>
