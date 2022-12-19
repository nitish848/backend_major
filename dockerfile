# FROM ubuntu:20.04
# RUN apt-get update && \
#     apt-get -y install sudo
# WORKDIR /usr
# COPY ./ ./
# RUN sudo apt-get update
# RUN sudo apt-get install python3.9 -y
# RUN sudo apt-get install python3-pip -y
# RUN sudo pip3 install --upgrade pip 
# RUN pip install -r requirements.txt
# RUN sudo apt-get install curl -y
# RUN curl https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh --output anaconda.sh
# RUN sha256sum anaconda.sh
# RUN bash anaconda.sh -yes
# RUN conda create -n newenvt1 anaconda python=3.9
# RUN  conda activate newenvt1
# CMD ["uvicorn","main:app", "--reload"]
# EXPOSE 8000

FROM ubuntu:latest
WORKDIR /usr
COPY ./ ./
# RUN apt update && apt install  openssh-server sudo -y
# # Create a user “sshuser” and group “sshgroup”
# RUN groupadd sshgroup && useradd -ms /bin/bash -g sshgroup sshuser
# # Create sshuser directory in home
# RUN mkdir -p /home/sshuser/.ssh
# # Copy the ssh public key in the authorized_keys file. The idkey.pub below is a public key file you get from ssh-keygen. They are under ~/.ssh directory by default.
# COPY idkey.pub /home/sshuser/.ssh/authorized_keys
# # change ownership of the key file. 
# RUN chown sshuser:sshgroup /home/sshuser/.ssh/authorized_keys && chmod 600 /home/sshuser/.ssh/authorized_keys
# # Start SSH service
# RUN service ssh start
# # Expose docker port 22
# EXPOSE 22
CMD ["uvicorn","main:app","--host","0.0.0.0" "--reload"]
EXPOSE 8000