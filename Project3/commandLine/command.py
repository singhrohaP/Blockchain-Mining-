import multiprocessing
import socket
import json

from Blockchain.peer import Peer


class Command(object):

    def start_peer(self, host, port):
        peer = multiprocessing.Process(target=self._start_peer, args=(host, port))
        peer.start()
        print(f'Peer running at {host}:{port}')

    def _start_peer(self, host, port):
        peer = Peer(host, port)
        peer.start()

    def connect_peer(self, host, port, target_host, target_port):
        print('Connecting......')
        message = {'type': 'CONNECT', 'host': target_host, 'port': target_port}
        result = self.unicast(host, port, message)
        if result == 'OK':
            print(f'Peer {host}:{port} connected to {target_host}:{target_port}')
        else:
            print('Connection failed')
        return result

    def mineData(self, host, port, data):
        print('Mining.....')
        message = {'type': 'MINE', 'data': data}
        result = self.unicast(host, port, message)
        if result == 'OK':
            print('A new block was mined')
        else:
            print('Mining failed')
        return result

    def showChain(self, host, port):
        message = {'type': 'SHOW'}
        result = self.unicast(host, port, message)
        if result:
            chain = json.loads(result)
            for block in chain:
                index = block['index']
                prev_hash = block['previous_hash']
                timestamp = block['timestamp']
                data = block['data']
                nonce = block['nonce']
                hash = block['hash']
                print('\n')
                print(f'# Block {index}')
                print('+-----------+----------------------------------------------------------------+')
                print(f'| prev_hash |{prev_hash: >{64}}|')
                print('|-----------|----------------------------------------------------------------|')
                print(f'| timestamp |{timestamp: >{64}}|')
                print('|-----------|----------------------------------------------------------------|')
                print(f'|    data   |{data[:64]: >{64}}|')
                print('|-----------|----------------------------------------------------------------|')
                print(f'|   nonce   |{nonce: >{64}}|')
                print('|-----------|----------------------------------------------------------------|')
                print(f'|    hash   |{hash: >{64}}|')
                print('+-----------+----------------------------------------------------------------+')
        else:
            print('Empty blockchain!')
        return result

    def unicast(self, host, port, message):
        pool = multiprocessing.Pool(1)
        result = pool.apply_async(
            self.sendMessage, args=(host, port, message))
        pool.close()
        pool.join()
        return result.get()

    def sendMessage(self, host, port, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(json.dumps(message).encode('utf-8'))
            response = s.recv(655350)
            return response.decode('utf-8')
