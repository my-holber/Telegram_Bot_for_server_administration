#!/usr/bin/python3

from pexpect import pxssh


from pexpect import pxssh

class Connection:
    def __init__(self):
        self.s = pxssh.pxssh()  # Create pxssh object for each instance

    def connect(self, ip, username, password, port, comande):
        try:
            # Use the pxssh object stored in self.s
            if not self.s.login(ip, username, password, port=port):
                return "SSH session failed on login."
            else:
                self.s.sendline(comande)  # Run the command
                self.s.prompt()  # Wait for the command to complete
                result = self.s.before.decode()  # Capture the output
                self.s.logout()  # Close the SSH connection
                return result  # Return the result of the command
        except pxssh.ExceptionPxssh as e:
            return f"pxssh failed on login: {e}"

