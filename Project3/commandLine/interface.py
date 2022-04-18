import cmd
import os

from commandLine.command import Command


class Interface(cmd.Cmd):

    def __init__(self):
        super().__init__()
        self.prompt = '(blockchain) '
        self._default_host = '127.0.0.1'
        self._command = Command()

    '''
    * open
    funtion to open peer listening port 
    '''
    def do_open(self, port):
        self._command.start_peer(self._default_host, int(port))

    '''
    * mine
    funtion to mine a new block in a port
    '''
    def do_mine(self, arg):

        port = arg.split(' ')[0]
        data = arg.split(' ')[1]
        self._command.mineData(self._default_host, int(port), data)

    '''
    * connect
    function to connect two ports
    '''
    def do_connect(self, arg):

        port = arg.split(' ')[0]
        target_port = arg.split(' ')[1]
        self._command.connect_peer(
            self._default_host, int(port), self._default_host, int(target_port))

    '''
    * show
    function to print blocks of ports
    '''
    def do_show(self, port):
        
        self._command.showChain(self._default_host, int(port))

    def do_exit(self, _):
        exit()

    '''
    *  help
    function to print commands a user can use 
    '''
    def do_help(self, _):
        print('\n')
        print('Following commands can be used:\n')
        print('help \t\t\t\t to seek help with the commands that can be used\n')
        print('open <port> \t\t\t Open peer listening port Eg: open 3301\n')
        print(
            'connect <port> <target_port> \t '
            'Connecting one peer to another Eg: connect 3301 3302\n')
        print('mine <port> <data> \t\t Mining a new block Eg: mine 3301 networks\n')
        print('show <port> \t\t\t Printing blockchain history of a peer Eg: show 3301\n')
        print('exit \t\t\t\t Exit application\n')
