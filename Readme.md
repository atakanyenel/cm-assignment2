# Connected Mobility Assignment 2

This is the code for assignment 2. To set the system up, use `sh setup.sh`. It will download a file from <https://norvig.com/big.txt> This file is 6 MB , so no need to commit it. It The script will also copy the downloaded file to required folders.

## Structure
- setup.sh : This file downloads the big.txt file that we are using for data transfer. When you clone the project for the first time ,run this with `sh setup.sh`. Running it multiple times won't do anything if *big.txt* is already present.

- code/client.py : This is the code that runs in mininet sta1. **This code won't work outside mininet environment.** It works likes this: Every 3 seconds, check which interfaces I'm connected. If I'm connected to 1 interface, run the the code with slow server IP by calling this python file with a different argument. If connected to two interfaces, kill the slow server process and run the fast server process by calling this python file with different argument. If there are no interfaces, kill all processes just to make sure.  

- code/server.py : This code runs in mininet host h1. This code works outside mininet environment. It creates a server that listens on port *5555*. You can connect to it using `telnet localhost 5555`, when connected , the server first expects a number, which states which from which byte of the file it should start sending. 

- sim/fast_server.py : This file is to simulate the fast connection between the client and the server. This is not for mininet. It listens on port *1111*, has a delay of 0.1 second between sending chunks.

- sim/slow_server.py : This file simulates the slow connection between client and server. Listens on *5555*. It has a delay of 0.2 second between sending chunks.

- sim/local_client.py : This simulates the client on mininet. It gets a random number every 3 seconds between 1-3. If number is 1, It connects to slow server, if 2, to fast server, if 3 , no connection. It highly uses shell commands, so designed for Unix. **The random command on line 62 is MAC OS specific , to run it in Linux change it to `shuf -i 1-3 -n 1`.**
## Running the simulation
There is a simulation, which I used to debug without mininet. To run the simulation , go to *sim* folder, open 3 different terminals to see the effects and run `python fast_server.py`, `python slow_server.py`, `python local_client.py main` on 3 different terminals. **Make sure that you are inside *sim* folder because Python reads the file to its relative path.**

## Running in Mininet
The mininet files are inside *code* directory.
Using the Mininet machine, run `sudo python base_scenario.py` inside **main project** folder. *base_scenario.py* automatically runs `code/server.py` in the host h1 from the port 5555. Now open a new terminal for *sta1* using `xterm sta1` in the mininet console. In the *sta1* terminal run `python code/client.py main`. After the process there will be a new file called *received.txt*, don't forget to delete it before you run the experiment again. Also don't forget `sudo mn -c`.

## Things to Consider
- You can check if the files are same using `md5 big.txt received.txt` on OSX and `md5sum big.txt received.txt` on Linux. The hashes should be same. 
- Even after the file transfer is complete, client still sends requests to server. So If you add something to *big.txt* while the program is running, the client will get it. This is on purpose, to be able to add streams in the future.
- **The system works most of the time. Sometimes the processes get mixed when changing interface and the client does not spawn new processes. To fix it ,just `ctrl-c` the client and start it again.**
- The implementations of `md5` and `md5sum` is different between OSX and Linux, no need to worry if you read a different hash for the same file.