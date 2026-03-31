"""TCP quiz server for a small CSE 310 networking project."""

import json
import random
import socket


HOST = "127.0.0.1"
PORT = 5001
DATA_FILE = "data.json"


def load_questions():
    """Load quiz questions from the local JSON file for each request."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file).get("questions", [])
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def find_question(question_id, questions):
    """Return one question that matches the given ID or None if not found."""
    for question in questions:
        if question.get("id") == question_id:
            return question
    return None


def build_question_response(question):
    """Create a response dictionary that sends question text to the client."""
    return {
        "status": "ok",
        "type": "question",
        "question_id": question.get("id"),
        "question": question.get("question"),
        "choices": question.get("choices", []),
    }


def normalize_answer_input(user_answer, choices):
    """Convert a letter answer like A, B, or C into the matching choice text."""
    cleaned_answer = str(user_answer).strip()
    letter_map = {"a": 0, "b": 1, "c": 2}
    answer_index = letter_map.get(cleaned_answer.lower())

    if answer_index is not None and answer_index < len(choices):
        return str(choices[answer_index]).strip().lower()

    return cleaned_answer.lower()


def handle_get_question():
    """Read the JSON file and return one random question to the client."""
    questions = load_questions()
    if not questions:
        return {"status": "error", "message": "No quiz data was found."}

    question = random.choice(questions)
    return build_question_response(question)


def handle_get_hint(request_data):
    """Read the JSON file and return the hint for the requested question."""
    questions = load_questions()
    question_id = request_data.get("question_id")
    question = find_question(question_id, questions)

    if question is None:
        return {"status": "error", "message": "Question ID was not found."}

    return {
        "status": "ok",
        "type": "hint",
        "question_id": question_id,
        "hint": question.get("hint", "No hint is available."),
    }


def handle_check_answer(request_data):
    """Read the JSON file and compare the client's answer with the correct one."""
    questions = load_questions()
    question_id = request_data.get("question_id")
    question = find_question(question_id, questions)

    if question is None:
        return {"status": "error", "message": "Question ID was not found."}

    user_answer = normalize_answer_input(
        request_data.get("answer", ""),
        question.get("choices", []),
    )
    correct_answer = str(question.get("answer", "")).strip().lower()
    is_correct = user_answer == correct_answer

    return {
        "status": "ok",
        "type": "answer_result",
        "question_id": question_id,
        "correct": is_correct,
        "correct_answer": question.get("answer"),
        "message": "Correct!" if is_correct else "That answer is not correct.",
    }
def process_request(request_data):
    """Choose which request handler to run based on the action from the client."""
    action = request_data.get("action")

    if action == "get_question":
        return handle_get_question()
    if action == "get_hint":
        return handle_get_hint(request_data)
    if action == "check_answer":
        return handle_check_answer(request_data)

    return {"status": "error", "message": "Unknown request type."}


def receive_json(client_socket):
    """Receive one JSON request from the connected client socket."""
    raw_data = client_socket.recv(4096).decode("utf-8")
    if not raw_data:
        return None

    try:
        return json.loads(raw_data)
    except json.JSONDecodeError:
        return {"action": "invalid"}


def send_json(client_socket, response_data):
    """Send one JSON response back to the connected client socket."""
    message = json.dumps(response_data)
    client_socket.sendall(message.encode("utf-8"))


def start_server():
    """Start the TCP server, accept clients, and send back quiz responses."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            print(f"Connected to client: {address}")

            try:
                request_data = receive_json(client_socket)
                if request_data is None:
                    send_json(client_socket, {"status": "error", "message": "Empty request."})
                elif request_data.get("action") == "invalid":
                    send_json(client_socket, {"status": "error", "message": "Bad JSON format."})
                else:
                    response_data = process_request(request_data)
                    send_json(client_socket, response_data)
            except OSError:
                send_json(client_socket, {"status": "error", "message": "Server error occurred."})
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server_socket.close()


def main():
    """Run the quiz server when this file is started directly."""
    start_server()


if __name__ == "__main__":
    main()
