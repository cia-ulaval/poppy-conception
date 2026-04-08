FROM ros:rolling-perception

# Installation des outils de build et CycloneDDS
RUN apt-get update -q && \
    apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends \
            build-essential \
            python3-colcon-common-extensions \
            ros-rolling-rmw-cyclonedds-cpp \
            ros-rolling-rosbridge-server \
            python3-rosdep \
            python3-pip \
            udev \
            git \
    && rm -rf /var/lib/apt/lists/*

RUN  pip3 install --no-cache-dir dynamixel-sdk --break-system-packages

WORKDIR /ros2_ws


    

# Sourcing automatique pour chaque nouveau terminal
RUN echo "source /opt/ros/rolling/setup.bash" >> ~/.bashrc
RUN echo "if [ -f /ros2_ws/install/setup.bash ]; then source /ros2_ws/install/setup.bash; fi" >> ~/.bashrc

CMD ["bash"]
