# Scale-AV Monitoring Computer

**Note:** this system requires intel chips (newer i5 and i7) that have a built in decoder for H264 video to run at full scale. It is recommended that the configuration be set to one stream when running off this hardware and for development.

## Checkout and Installation (Ubuntu Only)

Ubuntu is recommended as an Operating System, other linux variants may work but are not guarenteed. This code requires many specific packages to handle media and GUI interaction.

Install and clone on Ubuntu using the following instructions:
```
sudo apt-get install -y git gir1.2-gtk-3.0 gir1.2-gst-plugins-base-1.0 python3-gi gstreamer-1.0 python3-gst-1.0 libcanberra-gtk3-module gstreamer1.0-vaapi
git clone https://github.com/LeStarch/scaleav-monitor.git
```

## Execution:

To run the software:
```
cd scaleav-monitor/bin
./mothership
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

## Testing

TBD


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

## Known Bugs
- Windows are designed to regenerate when killed, forcing an external process termination
- If a window is killed too quickly after regneration, property-not-found errors may arise due to incomplete initialization

## Docker Support

Docker is being considered as one of the Scale-AV global deployment strategies. Thus it would be convenient to use Docker to deploy the monitoring application.

**Working Features:**
- Build from Dockerfile
- X11 support
- Video

**Known Bugs:**
- DBus support
- Audio

**Recommendation:** A simple dependency install script may be advisable to a full Docker build for this application.
