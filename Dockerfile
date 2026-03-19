FROM ros:rolling-perception

# Installation des outils de build et CycloneDDS
RUN apt-get update -q && \
    apt-get upgrade -yq && \
    apt-get install -yq --no-install-recommends \
    build-essential \
    python3-colcon-common-extensions \
    ros-rolling-rmw-cyclonedds-cpp \
    python3-rosdep \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /ros2_ws

# Sourcing automatique pour chaque nouveau terminal
RUN echo "source /opt/ros/rolling/setup.bash" >> ~/.bashrc
RUN echo "if [ -f /ros2_ws/install/setup.bash ]; then source /ros2_ws/install/setup.bash; fi" >> ~/.bashrc

CMD ["bash"]
