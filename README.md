# Frame for Raspberry pi 🖼️

Hello ! This is the reposit of my Frame 

## Require to do 
The latest version of the OS for your Raspberry Pi.

For this project i use Waveshare 7in3 7colors screen (you can find in amazon)
Then I followed the steps of their [documentations](https://www.waveshare.com/wiki/7.3inch_e-Paper_HAT_(F)_Manual#Python). You have to do the setup.py to have share python lib 

Finally, you need to install Comitup, but using this [tutorial](https://github.com/davesteele/comitup/wiki/Installing-Comitup)

## OnWeb setup

To fully use The Frame, open all the files and change the capitalized information. Then, you need to host it on a web server (either locally or on a remote server).
(PHP require)

## OnFrame setup
To properly configure the frame, you need to go to the deviantart.py, plex.py, and fixed.py files to enter the required information (I've tried to provide comments wherever possible).

You also need a channel on NTFY.sh.

Finally, before launching everything, run these commands in the SSH of the Raspberry:

```ssh
pip install Pillow
pip install requests
pip install plexapi
```

To test run :
```ssh
python3 main.py
```

## Disclaimer
I'm a beginner in all areas of this project, so the files may not be perfectly written, and the website design may not be amazing. But the goal of sharing this project is to make it cooler and better over time!

I did my best to comment on all the lines that I found important. And I must say, as a good Frenchman, my English is not the best you'll ever read...

✨Amusez-vous bien✨
