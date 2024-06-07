import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []

questions = [

    "What is the Italian word for PIE? \n a.Mozarella\n b.Pasty\n c.Patty \n d.Pizza"

    "Water boils at 212 Units at which scale? \n a.Farenheit\n c.Celsius\n Rankine\n d.Kelvin"

    "Which sea creature has 3 hearts? \n a.Dolphin\n b.Octopus\n c.Walrun\n d.Seal"

    "How many wonders are there in the world? \n a.7\n b.8\n c.10\n d.4"

    "How many states are there in the India? \n a.24\n b.29\n c.30\n d.31"

]

answers = [

    ["d", "a", "b", "a", "b"]

]

def get_random_question_answer(client_socket, questions, answers) :
    if len(questions) != len(answers) :
        raise ValueError("Questions and answers lists must have the same length")
    
    random_index = random.randint(0, len(questions) -1)
    question = questions[random_index]
    answer = answers[random_index](questions.encode('utf-8'))

    return random_index, question, answer

def validate_message(message, answer):

  return message.lower().strip() == answer.lower().strip()

def clientthread(client_socket, question, answer, clients, clients_score) :
    random_index, question, answer = get_random_question_answer(client_socket, questions, answers)
    client_score = clients_score.get(client_socket, 0)

    while True :
        try : 
            data = client_socket.recv(1024).decode()
            if not data : 
                break

            if not validate_message(data, answer):
                print("CLient sent invalid message")
                break

            if validate_message(data, answer) :
                client_score += 1
                clients_scores[client_socket] = client_score
                response = "Correct ! Your score is now {client_score}".encode('utf-8')
                client_socket.sendall(response)

                reemove_question(questions, answers, random_index)
                random_index, question, answer = get_random_question_answer(client_socket, questions, answers)

            else:
                response = "Wrong answer. Try again!".encode()
                client_socket.sendall(response)

        except ConnectionResetError:
     
            print("Client connection closed")
            clients.remove(client_socket)
            clients_scores.pop(client_socket, None)  
            break

        except :
            print("CLient connection closed")
            break

    client_socket.close()

def broadcast(message, connection) :
    for clients in list_of_clients :
        if clients != connection :
            try:
                clients.send(message.encode('utf-8'))

            except :
                remove(clients)

def remove (connection) :
    if connection in list_of_clients :
        list_of_clients.remove(connection)

def clientthread(conn, addr) :
    conn.send("Welcome to the Quiz" .encode('utf-8'))
    conn.send("You will recieve a question. The answer to the question should be from a b c or d\n".encode('utf-8'))
    conn.send("Good Luck\n\n".encode('utf-8'))
    while True :
        try:
            message = conn.recv(2048).decode('utf-8')
            if message :
                print("<" + addr[0] + ">" + message)
                message_to_send = "<" + addr[0] + ">" + message
                boradcast(message_to_send, conn)
            else :
                remove(conn)
        except :
            continue

while True :
    conn, addr = server.accept()
    list_of_clients.append(conn)
    print (addr[0] + "connected")
    new_thread = Thread(target = clientthread, args = (conn, addr))
    new_thread.start()