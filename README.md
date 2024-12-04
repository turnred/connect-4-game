##### Table of Contents
[Introduction](#connect-4-game)

[Statement of Work](#project-title)

# Connect-4 Game

This is a simple Connect-4 game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script.  Usage: server.py -p [PORT]
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.  Usage: client.py -h [HOST] -p [PORT]
3. **Play the game:** Once two players are connected, players enter their usernames and take turns placing chips.  First to four in a row wins!

**Protocol**
The server and client communicate with JSON messages, akin to the ones used in CS 314 and 414.  Messages follow a request/response structure, with the client receiving the server's responses.  Clients listen for additional game information beyond requests, such as the state or current board status.

**Known Issues**
1. The client and server enter infinite loops upon connecting.
2. All communication is done over plaintext.  There is no encryption.
3. There is no JSON schema validation, so a malicious actor could send malformed packets to the server.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]

# Statement of Work

* Simple Connect-4

# Game Rules
1. **The first player to connect makes the first move.**
2. **Players can only drop tokens on their turn, in a column that isn't full.
3. **Once there are 4 colors in a row in any direction, the game ends.

## Team

* Ethan Turner

## Project Objective:

* Develop a synchronous connect-4 game using Python and sockets.

## Scope:

* This project and team is limited to developing a simple Python game with networking support.

### Inclusions:

* Python
* Sockets 
* User Interface (Maybe)

### Exclusions:

* AI generated code

## Deliverables:

*client.py, a client script that interfaces with the game
*server.py, a server script that hosts the game

## Timeline:

### Key Milestones:

* Sprint 1: Working TCP sockets
* Sprint 2: Message Protocol 
* Sprint 3: Synchronous multiplayer functionality
* Sprint 4: Gameplay, state, UI
* Sprint 5: Error handling and test cases

### Task Breakdown:

* Implement TCP sockets and connectivity support
* Implement a message protocol that transfers data cleanly between both clients and the server
* Using the implemented TCP sockets and message protocol, begin the skeleton of client server relationship
* Create the game itself and allow clients to post actions to the server
* Catch unexpected actions, exceptions, disconnects, or other cases and end the client gracefully

## Technical Requirements:

### Hardware:

* A wifi card
* A PC that runs the wifi card

### Software:

* Python 3.x
* A working operating system

## Assumptions:

* Users are expected to be able to understand how to run a python script, or double click a file with python installed

## Roles and Responsibilities:

* Project Manager, Team Lead, Scrum Manager, AGILE Overseer, Sponsor, Client, Technologies and Expansion Lead, Research and Development Senior Administrator, and Human Resources Associate - Ethan Turner

## Communication Plan:

* The ""team"" will have daily, concurrent meetings on all topics of development.

## Additional Notes:

* I have probably written more lines on this SOW than python code I have written.

