"""TCP quiz client for a small CSE 310 networking project."""

import json
import socket


HOST = "127.0.0.1"
PORT = 5001


def send_request(request_data):
    """Open a TCP connection, send one JSON request, and return the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            client_socket.sendall(json.dumps(request_data).encode("utf-8"))
            raw_response = client_socket.recv(4096).decode("utf-8")
            return json.loads(raw_response)
    except ConnectionRefusedError:
        return {"status": "error", "message": "Server is not running."}
    except json.JSONDecodeError:
        return {"status": "error", "message": "Response was not valid JSON."}
    except OSError:
        return {"status": "error", "message": "Network error occurred."}


def print_question(response_data):
    """Display the question and answer choices in a clear beginner-friendly way."""
    print("\nQuestion:")
    print(response_data.get("question", "No question text found."))

    choices = response_data.get("choices", [])
    if choices:
        print("Choices:")
        labels = ["A", "B", "C"]
        for index, choice in enumerate(choices):
            if index < len(labels):
                print(f"{labels[index]}. {choice}")
            else:
                print(f"- {choice}")


def get_question():
    """Ask the server for one question and return its question ID if successful."""
    response_data = send_request({"action": "get_question"})
    if response_data.get("status") == "ok":
        print_question(response_data)
        return response_data.get("question_id")

    print(f"\nError: {response_data.get('message')}")
    return None


def get_hint(question_id):
    """Ask the server for a hint for the current question ID."""
    if question_id is None:
        print("\nGet a question first before asking for a hint.")
        return

    response_data = send_request({"action": "get_hint", "question_id": question_id})
    if response_data.get("status") == "ok":
        print(f"\nHint: {response_data.get('hint')}")
    else:
        print(f"\nError: {response_data.get('message')}")


def check_answer(question_id):
    """Send the user's answer to the server and print the result."""
    if question_id is None:
        print("\nGet a question first before checking an answer.")
        return

    user_answer = input("\nEnter your answer: ").strip()
    response_data = send_request(
        {"action": "check_answer", "question_id": question_id, "answer": user_answer}
    )

    if response_data.get("status") == "ok":
        print(response_data.get("message"))
        print(f"Correct answer: {response_data.get('correct_answer')}")
    else:
        print(f"\nError: {response_data.get('message')}")


def show_menu():
    """Print the client menu so the user can choose a request type."""
    print("\nQuiz Client Menu")
    print("1. Get question")
    print("2. Get hint")
    print("3. Enter an answer")
    print("4. Quit")


def main():
    """Run the client menu loop and keep track of the current question ID."""
    current_question_id = None

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            current_question_id = get_question()
        elif choice == "2":
            get_hint(current_question_id)
        elif choice == "3":
            check_answer(current_question_id)
        elif choice == "4":
            print("Client closed.")
            break
        else:
            print("Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
