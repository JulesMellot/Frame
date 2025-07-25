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

The dashboard is now served locally with Flask so no external notification service is required.

### Quick installation script
Instead of installing everything manually you can simply run the provided script:

```bash
sudo ./install.sh
```

It installs the required Python packages, copies the `frame.service` file and
starts the dashboard automatically.

If you prefer to do it manually the old instructions are still below for
reference.

Run these commands in the SSH of the Raspberry:

```bash
pip install Pillow
pip install requests
pip install plexapi
pip install flask
```

To start the local dashboard manually run :
```bash
python3 dashboard.py
```
### For automation
`install.sh` already installs the service file for you. If you want to
manage it manually, copy `OnFrame/frame.service` to
`/etc/systemd/system/` and run:

```bash
sudo systemctl daemon-reload
sudo systemctl enable frame.service
sudo systemctl start frame.service
```

For the automatic update at 9 AM.
``` ssh
crontab -e
```
and add 
```
0 9 * * * python3 /home/pi/Frame/send.py
```
## Disclaimer
I'm a beginner in all areas of this project, so the files may not be perfectly written, and the website design may not be amazing. But the goal of sharing this project is to make it cooler and better over time!

I did my best to comment on all the lines that I found important. And I must say, as a good Frenchman, my English is not the best you'll ever read...

✨Amusez-vous bien✨
