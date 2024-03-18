# Use the official TensorFlow image as a parent image
FROM tensorflow/tensorflow:latest

# Set the working directory
WORKDIR /mediapipe

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc-8 g++-8 \
        ca-certificates \
        curl \
        ffmpeg \
        git \
        wget \
        unzip \
        nodejs \
        npm \
        python3-dev \
        python3-opencv \
        python3-pip \
        libopencv-core-dev \
        libopencv-highgui-dev \
        libopencv-imgproc-dev \
        libopencv-video-dev \
        libopencv-calib3d-dev \
        libopencv-features2d-dev \
        software-properties-common && \
    add-apt-repository -y ppa:openjdk-r/ppa && \
    apt-get update && apt-get install -y openjdk-8-jdk && \
    apt-get install -y mesa-common-dev libegl1-mesa-dev libgles2-mesa-dev && \
    apt-get install -y mesa-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Clang 16
RUN wget https://apt.llvm.org/llvm.sh && \
    chmod +x llvm.sh && \
    ./llvm.sh 16 && \
    ln -sf /usr/bin/clang-16 /usr/bin/clang && \
    ln -sf /usr/bin/clang++-16 /usr/bin/clang++ && \
    ln -sf /usr/bin/clang-format-16 /usr/bin/clang-format

# Update alternatives for gcc and g++
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-8 100 --slave /usr/bin/g++ g++ /usr/bin/g++-8

# Install Python dependencies
RUN pip3 install --upgrade setuptools && \
    pip3 install wheel && \
    pip3 install future && \
    pip3 install absl-py numpy opencv-contrib-python protobuf==3.20.1 && \
    pip3 install six==1.14.0 && \
    pip3 install tensorflow && \
    pip3 install tf_slim && \
    pip3 install mediapipe

# Symlink python3 to python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install Bazel for building MediaPipe (Optional if you're not building from source)
ARG BAZEL_VERSION=6.1.1
RUN mkdir /bazel && \
    wget --no-check-certificate -O /bazel/installer.sh "https://github.com/bazelbuild/bazel/releases/download/${BAZEL_VERSION}/bazel-${BAZEL_VERSION}-installer-linux-x86_64.sh" && \
    wget --no-check-certificate -O /bazel/LICENSE.txt "https://raw.githubusercontent.com/bazelbuild/bazel/master/LICENSE" && \
    chmod +x /bazel/installer.sh && \
    /bazel/installer.sh && \
    rm -f /bazel/installer.sh

# Copy your Python script into the Docker image
COPY Thumbsup.py .

# Command to run the Python script
CMD ["python3", "hand_tracking.py"]
