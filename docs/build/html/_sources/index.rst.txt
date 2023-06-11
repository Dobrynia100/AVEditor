.. AVEditor documentation master file, created by
   sphinx-quickstart on Wed Jun  7 19:34:37 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AVEditor's documentation!
====================================
This is the documentation for the AVEditor application, which allows you to download and convert videos from YouTube.

Usage
-----
1. Insert the link to a video from YouTube in the 'Link' input field.
2. Specify the save path for the downloaded file in the 'Save path' input field.
3. Click the 'Video' button to download the video.
4. Click the 'Audio' button to download only the audio from the video.
5. Click the 'Convert to mp3' button to convert an mp4 file to mp3 format.
5. Click the 'Convert to webm' button to convert an mp4 file to webm format.

Note:For converting file to mp3 you need to insert path with a file name in the 'Save path' input field.
Inserted path should be without root directory "\AVEditor\example.mp4" not "C:\AVEditor\example.mp4".
Gif Maker Usage
-----
1.Press the 'Make a Gif' button to open GIF Maker window.
2.Insert the path to a mp4 video in the 'Path to mp4 file' input field.
3.Optionally, check the 'Add text' checkbox to add your text in to GIF.
4.Choose loop method if needed.
5.Click the 'Make a Gif' button to generate gif.

Settings
--------
The application provides the following settings that can be customized:

1. Appearance Mode: Allows you to choose the appearance mode of the application interface. Options include 'Light', 'Dark', and 'System' (follows the system theme).
2. Language: Allows you to choose the language of the user interface. Options include 'English' and 'Russian'.

Saving Settings
---------------
To save the current settings, click the 'Save Settings' button.

Note: Make sure you have a stable internet connection while using the application to download videos from YouTube.

Dependencies
------------
The AVEditor application requires the following dependencies:

- pytube: A library for downloading YouTube videos.
- moviepy: A library for video editing and conversion.
- customtkinter: A custom tkinter library for enhanced GUI elements.



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
