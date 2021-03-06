#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM continuumio/miniconda3

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# This Dockerfile adds a non-root user with sudo access. Use the "remoteUser"
# property in devcontainer.json to use it. On Linux, the container user's GID/UIDs
# will be updated to match your local UID/GID (when using the dockerFile property).
# See https://aka.ms/vscode-remote/containers/non-root-user for details.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Copy environment.yml (if found) to a temp locaition so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/

#Add China mirrors for apt and pip to speedup the downloads
#USER root
#RUN sed -i '1i\#Add China apt mirrors for speedup the apt downloads' /etc/apt/sources.list \
#	&& sed -i '1a\deb http://mirrors.aliyun.com/debian/ buster main non-free contrib' /etc/apt/sources.list \
#	&& sed -i '1a\deb http://mirrors.aliyun.com/debian-security buster/updates main' /etc/apt/sources.list \
#	&& sed -i '1a\deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib' /etc/apt/sources.list \
#	&& sed -i '1a\deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib' /etc/apt/sources.list \
#    && mkdir ~/.pip \
#	&& echo '[global]' > ~/.pip/pip.conf \
#	&& echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >>~/.pip/pip.conf \
#	&& echo '[install]'>> ~/.pip/pip.conf \
#	&& echo 'trusted-host = https://pypi.tuna.tsinghua.edu.cn' >> ~/.pip/pip.conf    
#USER docker

# Configure apt and install packages
RUN echo 'deb http://mirrors.aliyun.com/debian/ buster main non-free contrib' > /etc/apt/sources.list \
	&& echo 'deb http://mirrors.aliyun.com/debian-security buster/updates main' >> /etc/apt/sources.list \
	&& echo 'deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib' >> /etc/apt/sources.list \
	&& echo 'deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib' >> /etc/apt/sources.list \
    && mkdir ~/.pip \
	&& echo '[global]' > ~/.pip/pip.conf \
	&& echo 'index-url = https://pypi.tuna.tsinghua.edu.cn/simple' >>~/.pip/pip.conf \
	&& echo '[install]'>> ~/.pip/pip.conf \
	&& echo 'trusted-host = https://pypi.tuna.tsinghua.edu.cn' >> ~/.pip/pip.conf \	
	&& apt-get update \
    && apt-get -y install --no-install-recommends apt-utils dialog 2>&1 \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    && apt-get -y install git openssh-client less iproute2 procps iproute2 lsb-release \
    #
    # Install unzip
    && apt-get -y install unzip unrar\
    #
    # Install pylint
    && /opt/conda/bin/pip install pylint lxml\
    #
    # Update Python environment based on environment.yml (if present)
    && if [ -f "/tmp/conda-tmp/environment.yml" ]; then /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp \
    #
    # Install extra pip packages
    && if [ -f "pippackages.txt" ]; then /opt/conda/bin/pip install -r pippackages.txt; fi \
    #    
    # Create a non-root user to use if preferred - see https://aka.ms/vscode-remote/containers/non-root-user.
    && groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    # [Optional] Add sudo support for the non-root user
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    #
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*


	
# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog
