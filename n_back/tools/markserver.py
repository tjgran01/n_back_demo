import socket

class MarkServer(object):
    """A MarkServer object is a socket connection that opens port 5560.
    The MarkServer object, once initalized, listens for a connection on that
    port, and then waits for the the data_transfer method to be called.

    Args:
        None
    Returns:
        None
    """

    def __init__(self):
        self.host = ""
        self.port = 5560
        self.server = self.start_server()

        while True:
            self.conn = self.setup_connection()
            if self.conn:
                break
        print("We have a connection!")


    def setup_connection(self):
        """Sets up a connection with client device.

        Args:
            self
        Returns:
            conn: A connection object."""

        self.server.listen(1) # Allows one connection at a time.
        conn, address = self.server.accept()
        print(f"Conected to: {address[0]}: {str(address[1])}")
        return conn


    def start_server(self):
        """Creates the socket on the server side and binds the socket to the
        port number typed into this script (5560).

        Args:
            self
        Returns:
            server: A socket object.
        Raises:
            socket.error: If the socket is already opened, the program halts."""

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created.")
        try:
            server.bind((self.host, self.port))
        except socket.error as e:
            if e == "[Errno 48] Address already in use":
                print("Already in use! Close and try again.")
                server.close()
        print("Socket bind complete.")
        return server


    def data_transfer(self, data):
        """Sends string data from the server (self) to the client device.

        Args:
            self
            data: The information to be transfered.
        Returns:
            None
        Rasies:
            TypeError: If the data that is trying to be be transfered cannot
            be converted into a string."""

        try:
            data = str(data)
        except TypeError as e:
            print("Data provided cannot be converted to a string.")
            return None
        self.conn.sendall(str.encode(data))
        if data == "KILL":
            time.sleep(2)
            self.close_connection()
        #print("Data has been sent to the client.")


    def close_connection(self):
        """Closes the connection between the server and the client device.

        Args:
            self
        Returns:
            None"""
        print("KILL Command issued! Closing program.")
        self.conn.close()
