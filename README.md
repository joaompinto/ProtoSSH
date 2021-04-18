# ProtoSSH

This a proof-of-concept implementation of an SSH Client using Python (Windows Only).

# How to test

## Start test ssh server
Using Docker start a sample sshd container:

```sh
docker run -d -p 2222:22 --name test_sshd rastasheep/ubuntu-sshd
```

## Install the requirements
```sh
pip install -r requirements.txt
```
## Run the client
```sh
python -m protossh
```

# Approach
After establishing the connection, the main app creates two threads:
- NetworkReadThread - which reads server data and sends it to stdout
- KeyboardReadThread - which reads keyboard inputs and sends it to the ssh server

The main thread blocks waiting for an item to be placed in the "TerminateQueue()", which happens when the network connection is terminated.