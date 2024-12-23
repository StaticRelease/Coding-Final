import socket
import sys

# Constants
HOST = "localhost"
PORT = 5000
BUFFSIZE = 1024
FORMAT = "utf-8"
ADDRESS = (HOST, PORT)

# Initialize the client socket
client = socket.socket()
client.connect(ADDRESS)


# Function to receive file content from the server
def receive_file_content():
    """Receive file content from the server."""
    return client.recv(BUFFSIZE).decode(FORMAT)


# Function to send an option to the server
def choose_option(option):
    """Send the chosen option to the server."""
    client.send(str(option).encode(FORMAT))


# Function to ask the user if they want to retry
def retry():
    """Ask the user if they want to retry the game."""
    retry_input = input("Do you want to retry? (yes/no): ")
    if retry_input.lower() != 'yes':
        print("Exiting the game.")
        sys.exit()


# Function to handle the initial interaction and options
def start_game():
    """Start the game interaction with the server."""
    print(client.recv(1024).decode())  # Receive welcome message from server
    print(client.recv(1024).decode())  # Receive saga choice prompt

    while True:  # Outer loop for saga choice and file reception
        try:
            data_file = int(input("Enter 1: "))  # User enters 1 for choosing a saga
            choose_option(data_file)  # Send choice to the server

            the_file = receive_file_content()  # Receive file content from server

            if data_file == 1:
                print(the_file)  # Display the file content if saga 1 is selected

            while True:  # Inner loop for further options after saga choice
                next_choice = int(input("Choose your next option: "))
                choose_option(next_choice)  # Send next choice to the server

                if next_choice == 1:
                    print("The story continues as it goes. Yajirobi cuts the tail of the Great Ape Vegeta, "
                          "Gohan and Krillin fend off Vegeta enough, hurting him, and Goku tells them to let him go. The end.")
                    retry()  # Ask the user if they want to retry

                elif next_choice == 2:
                    choice = receive_file_content()  # Receive the file content for option 2
                    print(choice)

                elif next_choice in [3, 4]:
                    choice = receive_file_content()  # Receive the file content for options 3 and 4
                    print(choice)
                    print("End of the game.")
                    retry()  # Ask the user if they want to retry

                else:
                    print("Invalid choice. Please try again.")
                    retry()  # Ask if the user wants to retry

        except ValueError:
            print("Invalid input. Please enter a number.")
            retry()  # Ask if the user wants to retry


# Close the client connection gracefully
def close_connection():
    """Close the client connection."""
    print("Closing the connection.")
    client.close()


if __name__ == "__main__":
    try:
        start_game()  # Start the game
    finally:
        close_connection()  # Ensure the connection is closed when the game ends or user exits
