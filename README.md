# NSDSYST-Project
 
A distributed system for multiplayer games  
*Date Accomplished: February 22, 2022*

## Use
A distributed system for Tic-Tac-Toe and Hangman

## Pre-requisites
1. Python / Python3
  * Programming language used.
  * To download in **Linux**: `sudo apt-get install python3`
  * To download in **Windows**: [Python for Windows](https://www.python.org/downloads/windows/)
2. Curl
  * Command that allows the transfer (upload / download) of data using command line interface.
  * To download in **Linux**: `sudo apt-get install curl`
  * To download in **Windows**: [Curl for Windows](https://curl.se/windows/)

## Download
Download the project through the following commands:
* Linux:
``` sudo curl -L -O https://github.com/bernicebetito/NSDSYST-Project/archive/master.zip ```
* Windows:
``` curl -L -O https://github.com/bernicebetito/NSDSYST-Project/archive/master.zip ```

Once downloaded, the project can be used through the following commands:
* For the main server:
  * Linux: `sudo python3 main_server.py`
  * Windows: `python main_server.py`
* For the game server:
  * Linux: `sudo python3 game_server.py`
  * Windows: `python game_server.py`
* For the player:
  * Linux: `sudo python3 player.py`
  * Windows: `python player.py`

Note:  
_Seven machines would be needed, one for the main server, one server for each game, and two players for each game._

## Guide
Both games could be played simultaneously. Run the main server first then each of the game server. The port number of each game is pre-specified. The user will be asked to choose which game to run based on the port number upon running the game server program.