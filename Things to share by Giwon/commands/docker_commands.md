# basic docker run command for detectron2 : creating container
docker run --gpus all -it \
  --shm-size=8gb --env=unix$DISPLAY --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
  --name=Giwon detectron2:v0

# basic docker run command for detectron2 : creating container _second try
docker run --gpus all -it \
    --privileged \
    -v /dev/video0:/dev/video0 \
    -v /dev/snd:/dev/snd \
    --shm-size=8gb \
    --net=host \
    --env=unix$DISPLAY \
    -e="QT_X11_NO_MITSHM=1" \
    -v="/tmp/.X11-unix:/tmp/.X11-unix" \
    --name=Giwon_d3 \
    detectron2:v0



# rename containers
docker rename [old] [new]
