import socket


class Bank:
    def __init__(self, file):
        print('Server booting')
        self.server(file)

    def server(self, file):

        gaveaccountnum = False
        HOST = '127.0.0.1'
        PORT = 6666
        with open(file, 'r') as f:
            lines = [line for line in f]
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # solution for: "socket.error: [Errno 98] Address already in use"
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind((HOST, PORT))
        server_socket.listen(10)

        n = len(lines)
        flag = False
        while True:
            if not flag:
                sock, client_address = server_socket.accept()
                flag = True
            try:
                data = sock.recv(4096)
                if data:
                    txt = data.decode('utf-8')
                    print(txt)
                    if not gaveaccountnum:
                        txt = txt.split(' ')
                        i = 0
                        while i < n and not lines[i].split(', ')[0] == txt[0].strip():
                            i += 1
                        if i < n:
                            sock.send(bytes('Account number correct\r\n', "utf-8"))
                            gaveaccountnum = True
                            continue
                        else:
                            sock.send(bytes('Account number incorrect\r\n', "utf-8"))
                            sock.close()
                            flag = False
                    else:
                        if txt.strip() == 'ACK account number correct'.strip():
                            sock.send(bytes('enter your choise:\r\n', "utf-8"))

                        elif txt.startswith("Withdraw"):
                            flag = self.withdraw(file, lines, i, txt.split(' ')[1])
                            if flag:
                                sock.send(bytes('The money was withdrawn\r\n', "utf-8"))
                            else:
                                sock.send(bytes('Not enoth money\r\n', "utf-8"))

                        elif txt.startswith("Deposit"):
                            self.deposit(file, lines, i, txt.split(' ')[1])
                            sock.send(bytes("The money was deposited\r\n", "utf-8"))

                        elif txt.strip() == 'DONE'.strip():
                            gaveaccountnum = flag = False
                            sock.close()

                        else:
                            print("Bad msg end communication")
                            gaveaccountnum = flag = False
                            sock.close()

            except Exception as e:
                print(e.with_traceback())
                sock.close()
                gaveaccountnum = flag = False
                continue
        server_socket.close()

    def deposit(self, file, lines, i, amount):
        lines[i] = lines[i].replace(lines[i].split(', ')[1], self.addStrs(lines[i].split(', ')[1], amount))
        print(lines[i])
        f = open(file, 'w')
        f.writelines(lines)
        f.close()

    def withdraw(self, file, lines, i, amount):
        if int(lines[i].split(', ')[1]) < int(amount):
            return False
        lines[i] = lines[i].replace(lines[i].split(', ')[1], self.subStrs(lines[i].split(', ')[1], amount))
        print(lines[i].split(', ')[1])
        f = open(file, 'w')
        f.writelines(lines)
        f.close()
        return True

    def addStrs(self, a, b):
        return str(int(a) + int(b)) + '\n'

    def subStrs(self, a, b):
        return str(int(a) - int(b)) + '\n'


if __name__ == '__main__':
    fname = 'accounts.txt'
    bank = Bank(fname)
