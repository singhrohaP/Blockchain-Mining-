import json
import socket
import socketserver
import multiprocessing

from Blockchain.chain import Chain


class _PeerRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        messageStr = self.request.recv(655350).strip().decode('utf-8')
        messageObject = json.loads(messageStr)
        messageType = messageObject['type']
        response = 'OK'
        peer = self.server.peer
        if messageType == 'MINE':
            peer.mine(messageObject['data'])
        elif messageType == 'CONNECT':
            host = messageObject['host']
            port = messageObject['port']
            peer.peerConnect(host, port)
        elif messageType == 'PEERS':
            response = json.dumps(peer.peers)
        elif messageType == 'SHOW':
            response = json.dumps(peer.chain.to_dict())
        elif messageType == 'CHAIN':
            chain = messageObject['chain']
            peer.chainReplace(chain)
        self.request.sendall(response.encode('utf-8'))


class Peer(object):

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self._peers = set()
        self._chain = Chain()

    def start(self):
        server = socketserver.ThreadingTCPServer(
            (self.host, self.port), _PeerRequestHandler)
        server.peer = self
        try:
            server.serve_forever()
        except KeyboardInterrupt as _:
            server.server_close()

    def peerConnect(self, host, port):
        if (host, port) in self._peers:
            return
        self._peers.add((host, port))
        peers = self.requestPeers(host, port)
        self.addPeer(json.loads(peers))
        self.requestConnection()
        self.broadcastChain()

    def mine(self, data):
        self._chain.mine(data)
        self.broadcastChain()

    def chainReplace(self, chain):
        self._chain.replaceChain(chain)

    @property
    def chain(self):
        return self._chain

    @property
    def peers(self):
        return [{'host': host, 'port': port} for (host, port) in self._peers]

    def addPeer(self, peers):
        for peer in peers:
            host = peer['host']
            port = peer['port']
            if host == self.host and port == self.port:
                continue
            if (host, port) in self._peers:
                continue
            self._peers.add((host, port))

    # Communication

    def requestConnection(self):
        message = {'type': 'CONNECT', 'host': self.host, 'port': self.port}
        return self.messageBroadcast(message)

    def requestPeers(self, host, port):
        message = {'type': 'PEERS', 'host': self.host, 'port': self.port}
        return self.uniCast(host, port, message)

    def broadcastChain(self):
        message = {'type': 'CHAIN', 'chain': self._chain.to_dict()}
        return self.messageBroadcast(message)

    # Base communication

    def uniCast(self, host, port, message):
        pool = multiprocessing.Pool(1)
        result = pool.apply_async(
            self.sendMessage, args=(host, port, message))
        pool.close()
        pool.join()
        return result.get()

    def messageBroadcast(self, message):
        results = []
        pool = multiprocessing.Pool(5)
        for (host, port) in self._peers:
            results.append(pool.apply_async(
                self.sendMessage, args=(host, port, message)))
        pool.close()
        pool.join()
        return [result.get() for result in results]

    def sendMessage(self, host, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(message).encode('utf-8'))
            response = s.recv(655350, 0)
            return response.decode('utf-8')