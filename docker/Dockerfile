FROM ubuntu
MAINTAINER M Starch "lestarch@googlemail.com"

#Install dependencies
RUN apt-get update
RUN apt-get install -y git gir1.2-gtk-3.0 gir1.2-gst-plugins-base-1.0 python3-gi gstreamer-1.0 python3-gst-1.0 libcanberra-gtk3-module

#Install software github.com
RUN mkdir -p /usr/local/
RUN git clone https://github.com/LeStarch/gstreamer-pencil-tests.git /usr/local/gstreamer

#Mount X11 volume
VOLUME /tmp/.X11-unix:/tmp/.X11-unix:re
#Run the monitor scripts
CMD PYTHONPATH=/usr/local/gstreamer python3 -m app.main
