import socket


class ATM():
    def __init__(self):
        self.client()

    def client(self):
        HOST = '127.0.0.1'
        PORT = 6666

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (HOST, PORT)
        sock.connect(server_address)

        try:

            msg = input("Enter account number:\n")
            msg += "\r\n"
            sock.send(bytes(msg, "utf-8"))
            data = sock.recv(4096)
            if data:

                txt = data.decode('utf-8').strip()
                print(txt)
                if txt == 'Account number correct'.strip():

                    sock.send(bytes("ACK account number correct\r\n", "utf-8"))
                    data = sock.recv(4096)

                    while data:

                        txt = data.decode('utf-8').strip()
                        print(txt)

                        out = input('Enter 1 for Deposit, 2 for Withdraw and 3 for Done: ')
                        if out == '1':
                            tmp = input("Enter the sum you wish to deposit: ")
                            sock.send(bytes('Deposit %s\r\n' % tmp, "utf-8"))
                        elif out == '2':
                            tmp = input("Enter the sum you wish to withdraw: ")
                            sock.send(bytes('Withdraw %s\r\n' % tmp, "utf-8"))
                        else:
                            print('Communication Ended successfully')
                            sock.send(bytes("DONE\r\n", "utf-8"))
                        data = sock.recv(4096)

        except Exception as e:
            print(e)
            sock.close()
        finally:
            sock.close()


if __name__ == '__main__':
    atm = ATM()
