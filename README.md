# ProtoSSH


ProtoSSH  is a pure python implementation of an SSH client using the [Paramiko] library.
The goal is not to get a full re-implementation of the openssh client, but instead provide some features which would be harder to get into opeenssh.

[Paramiko]: https://www.paramiko.org/
# Features

Features currently available:
- Password based authentication directly from the CLI (for dev purposes)
- Windows Single Sign On (Kerberos) authentication


# How to test

## Start test ssh server
Using Docker start a sample sshd container:

```sh
docker run -d -p 3333:22 --name test_sshd rastasheep/ubuntu-sshd
```

## Install the requirements
```sh
pip install -r requirements.txt
```
## Run the client
```sh
# User root, localhost, port 3333, password: root
python -m protossh -p3333 root:root@localhost
```

# Approach
After establishing the connection, the main app creates two threads:
- NetworkReadThread - which reads server data and sends it to stdout
- KeyboardReadThread - which reads keyboard inputs and sends it to the ssh server

The main thread blocks waiting for an item to be available from the "TerminateQueue()", which happens when the network connection is terminated.
