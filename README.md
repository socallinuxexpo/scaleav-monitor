# Setting up the Scale-AV Monitoring Computer

**n.b.** These instructions have been tested on Ubuntu.  Other linux variants may work but results are not tested or guarenteed. This code requires many specific packages to handle media and GUI interaction.

**n.b.** This application requires an Intel CPU (newer i5 and i7) that has a hardware decoder for H264 video. It is recommended that the configuration be set to one stream for development and testing.

## Installation
### Operating system configuration
- Install the latest Ubuntu release
- Select the full installation, not the minimal installation
- Select installing encumbered software to get the video tools
- When prompted, remove the installation media and reboot
- Let updates install, you may be prompted to reboot again
- Update the OS
```
sudo apt upgrade
```
- Install the required packages
```
sudo apt install vlc git gir1.2-gtk-3.0 gir1.2-gst-plugins-base-1.0 python3-gi gstreamer-1.0 python3-gst-1.0 libcanberra-gtk3-module gstreamer1.0-vaapi
```
- Install proprietary video drivers
  - From the launcer open 'Software & updates'
    - On the 'Additional Drivers' tab select 'Using NVIDIA driver...'
    - Select Apply Changes
    - Select Close

### Make sure the video drivers were recognized
```
sudo apt install vainfo
```
Verify that the nvidia driver is selected (not nouveau) and that VDPAU is being used
```
sudo vainfo
  libva info: Trying to open /usr/lib/x86_64-linux-gnu/dri/nvidia_drv_video.so
  Driver version: Splitted-Desktop Systems VDPAU backend for VA-API - 0.7.4
```

### Set up incoming ssh connection support
```
sudo apt install openssh-server
```

### Open the firewall for incoming ssh connections
```
sudo ufw allow ssh
```
```
Rules updated
Rules updated (v6)

```

## Install the ScaleAV software
### Clone the git repository
```
cd ~
mkdir code
cd code
git clone https://github.com/socallinuxexpo/scaleav-monitor.git
cd scaleav-monitor
```

### Set up monitoring a test stream on your local host
```
vi config/rooms
```
```
0	http://localhost:8080/mixed
```

## Test streaming
### Start the test stream to monitor
- Download an mp4 sample file, we use Mike's ~/20150111_150020.mp4
- Stream the test video from the command line
```
cvlc 20150111_150020.mp4 --loop --sout='#http{mux=ffmpeg{mux=flv},dst=:8080/mixed}'
```
- Or stream using the VLC GUI
```
vlc
```
  - Media -> Stream...
  - File tab<br>
    ![VLC Open Media](markup/VLC%20Open%20Media.png)
    - [ Add ]
      - Browse to the test video downloaded in the step above
      - [ Open ]
  - [ Stream ]
  - [ Next ]
    - Select format = http
    ![VLC Destination](markup/VLC%20Destination.png)
    - [ Add ]
      - Set path to /mixed, port to 8080
      ![VLC Destination 2](markup/VLC%20Destination%202.png)
  - [ Next ]
    - Deselect active transcoding
    - Select profile "Video - H.264 + MP3 (MP4)"
    ![VLC Output](markup/VLC%20Output.png)
  - [ Next ]
    - Deselect Stream all elementary streams
    ![VLC Output 2](markup/VLC%20Output%202.png)
    - Copy the generated stream output string for command line use
  - [ Stream ]

### Run the software to monitor the test signal
```
bin/mothership 
```

## Execution:
### Set up the rooms to monitor
```
vi config/rooms
```
```
0	http://room-101.scaleav.us:8080/mixed
1	http://room-103.scaleav.us:8080/mixed
2	http://room-107.scaleav.us:8080/mixed
3	http://room-104.scaleav.us:8080/mixed
4	http://room-106.scaleav.us:8080/mixed
5	http://room-211.scaleav.us:8080/mixed
6	http://room-212.scaleav.us:8080/mixed
7	http://ballroom-a.scaleav.us:8080/mixed
8	http://ballroom-b.scaleav.us:8080/mixed
9	http://ballroom-c.scaleav.us:8080/mixed
10	http://ballroom-de.scaleav.us:8080/mixed
11	http://ballroom-f.scaleav.us:8080/mixed
12	http://ballroom-g.scaleav.us:8080/mixed
13	http://ballroom-h.scaleav.us:8080/mixed
14	http://extra1.scaleav.us:8080/mixed
15	http://extra-2.scaleav.us:8080/mixed
16	http://extra-3.scaleav.us:8080/mixed
```

### Run the software to monitor the conference
```
bin/mothership 
```

## Contribution

To contribute to this project, please create a branch in your git repository, make the change, test it using the following basic test procedure (see Testing), and then push the branch to GitHub. Then create a pull request describing the work, any notes/caveates, testing performed, and submit it. We will review it together and pull it into the master branch when the work is completed.

In the scaleav-monitor repository checkout:
```
git checkout -b "<username>/<brief-description-of-work>
<do work>
git push -u origin <branch name>
...
i.e.
git checkout -b "mstarch/fixing-push-button"
<do work and test>
git push -u origin mstarch/fixing-push-button
```
## Configuration

`config/rooms` contains a list of stream urls (one per line).  To add or remove rooms, edit this file. Lines follow the following format:

```
<index> <room-video-url>
i.e.
0 http://example.com:8080/mixed
```
## Description

This repository holds the python, GStreamer, and GTK+ reworking of the ScaleAV video stream monitoring software. This solution has several advantages above the original solution:

- **Unified Window and Event code:**
  The same solution handels the tracking of window events, and the window display removing the need for external event tracking.
- **GStreamer:**
  GStreamer allows greater control over the incoming streams, and provides a lightweight alternative to VLC windows. This will yield better performance in the post XVideo-driver systems. GStreamer usage replaces several technologies including Jack Audio, and VLC with a single technology choice.
- **Python:** 
  A unified solution in python replaces a multi-language, multi-technology stack, which reduces the learning curve and minimizes the codebase. This allows for easier maintainability in a volunteer-staffed environment.

## Design
![Monitoring Design](https://docs.google.com/drawings/d/1FYnyoz1_jLDq2tF6BK0-b9wwbiFCWoeLrj8FOu2rJr8/pub?w=1273&h=867 "ScaleAV Monitor Design")
## Installation and Execution

These instructions assume a Debian/Ubuntu system with Python 3 installed.
**Note:** Only tested on Ubuntu
