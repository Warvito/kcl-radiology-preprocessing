FROM hdneuro/spm-clinical:20220421

# LD_LIBARY_PATH must be empty to allow Linux and Python updates and installations
ENV LD_LIBRARY_PATH ""

# Install essentials
RUN chmod 1777 /tmp \
 && apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install \
    libxt6 libxmu6 libxpm4 python3 python3-pip python3-venv ipython3

ARG USER_ID
ARG GROUP_ID
ARG USER
RUN addgroup --gid $GROUP_ID $USER
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID $USER

# Set up environment variable for MATLAB Runtime. This should be done after installing Linux and Python components.
ENV MCR_VERSION v910
ENV LD_LIBRARY_PATH /opt/mcr/${MCR_VERSION}/runtime/glnxa64:/opt/mcr/${MCR_VERSION}/bin/glnxa64:/opt/mcr/${MCR_VERSION}/sys/os/glnxa64:/opt/mcr/${MCR_VERSION}/sys/opengl/lib/glnxa64:/opt/mcr/${MCR_VERSION}/extern/bin/glnxa64


RUN mkdir -p /workspace/src
COPY src /workspace/src
COPY requirements.txt /workspace/requirements.txt
RUN pip3 install -r /workspace/requirements.txt

ENTRYPOINT ["python3", "/workspace/src/preprocess_image.py"]