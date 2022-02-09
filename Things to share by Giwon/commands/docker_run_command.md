# docker run commmand, change the NAME part
docker run --gpus all -it \
    --privileged \
    -v /dev/video0:/dev/video0 \
    -v /dev/snd:/dev/snd \
    --shm-size=8gb \
    --net=host \
    --env=unix$DISPLAY \
    -e="QT_X11_NO_MITSHM=1" \
    -v="/tmp/.X11-unix:/tmp/.X11-unix" \
    --name=NAME \
    detectron2:v0


# after opening detectron container
pip install -e .