# Overview

This project is a small Python networking program that uses a TCP client and server on `localhost`. I built a quiz application where the client sends a request to the server, the server reads quiz information from a local JSON file, and then the server sends a response back to the client. The client displays the response in the terminal so the communication is easy to see and understand.

The program supports three main requests:

- `get_question`
- `get_hint`
- `check_answer`

To use the program, I start the server first so it can listen for connections. After that, I start the client in a second terminal window. The client shows a simple menu that lets me get a question, ask for a hint, check an answer, or quit the program.

To start the server:

```bash
python3 server.py
```

To start the client:

```bash
python3 client.py
```

My purpose for writing this software was to get more practice with Python networking, sending data between two programs, reading from a local file, and building a simple client/server application that I could understand, test, and clearly explain.

[Software Demo Video](https://youtu.be/3gp3dXmratA)

# Network Communication

This program uses a client/server architecture. The server waits for incoming connections, and the client connects to the server when the user chooses a menu option.

The program uses TCP sockets through Python's built-in `socket` module. In my code, the server listens on port `5001` using the address `127.0.0.1`, which is the local machine.

The client and server exchange data in JSON format. Each client request is a small JSON object with an `action` field and, when needed, extra data. For example:

```json
{ "action": "get_question" }
```

```json
{ "action": "get_hint", "question_id": 2 }
```

```json
{ "action": "check_answer", "question_id": 2, "answer": "127.0.0.1" }
```

The server reads the request, processes it, and sends a JSON response back. A response includes a status plus the data the client needs to display, such as a question, a hint, or an answer result.
One TCP connection is used per request: the client connects, sends one JSON message, receives one JSON response, and the connection closes.

# Development Environment

I built this project on my computer using Visual Studio Code and the terminal. I used Git and GitHub to track the project files.

The program is written in Python 3. I used only Python's standard library so the project stays simple and easy to run. The main libraries used were:

- `socket` for TCP networking
- `json` for reading the local quiz file and formatting messages between the client and server
- `random` for choosing a quiz question on the server side

# Useful Websites

- [Python socket documentation](https://docs.python.org/3/library/socket.html)
- [Python json documentation](https://docs.python.org/3/library/json.html)
- [Real Python: Python Sockets](https://realpython.com/python-sockets/)
- [IBM: What is TCP?](https://www.ibm.com/think/topics/tcp)

# Future Work

- Add more quiz questions and organize them by topic.
- Let the user choose a specific question instead of always getting a random one.
- Keep track of the user's score during a session.
- Improve the error messages so the client gives clearer feedback when something goes wrong.
