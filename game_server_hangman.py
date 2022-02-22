import socket, json, re, time
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to convert a json object into a python object
def to_python(jsonObj):
    data = json.loads(jsonObj)
    return data

# Function to convert a python object into a json object
def to_json(pythonObj):
    data = json.dumps(pythonObj)
    return data

# JSON commands
register = '{"command": "register", "game": "hangman"}'
players_ready = '{"command": "ready", "game": "hangman", "player_one": "", "player_two": ""}'
success = '{"command": "retcode", "code": "SUCCESS"}'
error = '{"command": "retcode","code": "ERROR"}'

class GameServer (object):

    def __init__(self, lobby_host, lobby_port, server_host, server_port):
        global sock
        sock.bind((lobby_host, lobby_port))
        print("Lobby online")

        self.server_host = server_host
        self.server_port = server_port

    def connect_to_server(self):
        global sock

        # Ready register request
        self.registerRequest = to_python(register)
        self.registerRequest = to_json(self.registerRequest)

        # Send register request
        sock.sendto(bytes(self.registerRequest, "utf-8"), (self.server_host, self.server_port))

        # Process return code
        self.data = sock.recvfrom(1024)
        self.return_code = to_python(self.data[0])

        if self.return_code["code"] == "SUCCESS":
            print("Established communication with the main server")
            global registered
            registered = 1

        elif self.return_code["code"] == "ERROR":
            print("Error, main server refused communication")

        else:
            print("Unexpected error happened")

    def accept_players(self):
        global sock
        players = 0
        self.player_one_name = ""
        self.player_one_addr = ()
        self.player_two_name = ""
        self.player_two_addr = ()

        while players != 2:

            # Wait for players
            print("Waiting for players...")
            self.data = sock.recvfrom(1024)
            self.player_request = to_python(self.data[0])

            if self.player_request["command"] == "join":
                if players == 0 and self.player_request["game"] == "hangman":
                    self.player_one_name = self.player_request["username"]
                    self.player_one_addr = self.data[1]
                    print(f"Player {self.player_one_name} has connected")
                    players+=1

                    # Notify player
                    self.success = to_python(success)
                    self.success = to_json(self.success)
                    sock.sendto(bytes(self.success, "utf-8"), self.player_one_addr)

                elif players == 1 and self.player_request["game"] == "hangman":
                    self.player_two_name = self.player_request["username"]
                    self.player_two_addr = self.data[1]
                    print(f"Player {self.player_two_name} has connected")
                    players+=1

                    # Notify player
                    self.success = to_python(success)
                    self.success = to_json(self.success)
                    sock.sendto(bytes(self.success, "utf-8"), self.player_two_addr)

                else:
                    # Notify player
                    self.error = to_python(error)
                    self.error = to_json(self.error)
                    sock.sendto(bytes(self.error, "utf-8"), self.data[1])

        print("All players complete, notifying main server")

        # Ready notification
        self.ready = to_python(players_ready)
        self.ready["player_one"] = self.player_one_name
        self.ready["player_two"] = self.player_two_name
        self.ready = to_json(self.ready)

        sock.sendto(bytes(self.ready, "utf-8"), (self.server_host, self.server_port))

        # Process return code
        self.data = sock.recvfrom(1024)
        self.return_code = to_python(self.data[0])

        if self.return_code["code"] == "SUCCESS":
            print("Notified the main server, awaiting game state")
            global playing
            playing = 1

        elif self.return_code["code"] == "ERROR":
            print("Error, main server refused communication")

        else:
            print("Unexpected error happened")

    def forward_and_receive(self):
        global playing
        global sock
        while playing == 1:

            # Receive game state
            self.data = sock.recvfrom(1024)
            self.game_state = to_python(self.data[0])
            print("Received game state")

            # Check if game is over
            if self.game_state["continue"] == "true":

                # Forward to players
                print(self.game_state)
                self.game_state = to_json(self.game_state)
                sock.sendto(bytes(self.game_state, "utf-8"), self.player_one_addr)
                sock.sendto(bytes(self.game_state, "utf-8"), self.player_two_addr)
                print("Forwarded game states")

                # Receive action from player and forward to main server
                self.data = sock.recvfrom(1024)
                self.action = to_python(self.data[0])
                self.action = to_json(self.action)
                sock.sendto(bytes(self.action, 'utf-8'), (self.server_host, self.server_port))
                print("Received and forwarded player action")

            elif self.game_state["continue"] == "false":

                # Forward to players
                self.game_state = to_json(self.game_state)
                sock.sendto(bytes(self.game_state, "utf-8"), self.player_one_addr)
                sock.sendto(bytes(self.game_state, "utf-8"), self.player_two_addr)

                # End game
                playing = 0
                print("Game ended")


if __name__ == "__main__":
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    while True:
        # Set variables for self address and destination port
        lobby_host = input("Enter IP address of lobby: ")
        lobby_port = int(input("Port of lobby (5555 for tic-tac-toe, 4444 for hangman): "))

        result = bool(re.match(regex, lobby_host))
        if (result):
            break

        else:
            print("Invalid IP Address, please try again.\n")

    while True:
        # Set variables for server address and destination port
        server_host = input("Enter IP address of main server: ")
        server_port = int(input("Port of main server (12345 for tic-tac-toe, 54321 for hangman): "))

        result = bool(re.match(regex, server_host))
        if (result):
            break

        else:
            print("Invalid IP Address, please try again.\n")

    # Initialize game server
    game = GameServer(lobby_host, lobby_port, server_host, server_port)

    # Connect to main server
    registered = 0
    playing = 0

    while registered == 0:
        game.connect_to_server()

    while playing == 0:
        game.accept_players()

    time.sleep(2)

    while playing == 1:
        game.forward_and_receive()
