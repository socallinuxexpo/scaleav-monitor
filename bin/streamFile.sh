#!/bin/bash

vlc 20150111_150020.mp4 --sout '#http{mux=ffmpeg{mux=flv},dst=:8080/}'

