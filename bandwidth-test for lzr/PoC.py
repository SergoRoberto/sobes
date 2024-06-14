import socket
import struct


# Структура пакета Start Test Request протокола Bandwith-test
def create_start_test_request():
    protocol = 1 # TCP
    direction = 1 # наприавление - передача
    random_data = 1 # не использовать 
    tcp_count = 0 # 
    tx_size = 1500 # размер передачи
    client_buffer_size = 0 # неизвестно
    remote_tx_speed = 0 # unlim
    local_tx_speed = 0 # unlim

    ret = struct.pack('!4Bhhll', 
                        protocol,
                        direction,
                        random_data,
                        tcp_count,
                        tx_size,
                        client_buffer_size,
                        remote_tx_speed,
                        local_tx_speed)
    return ret

def send_bandwidth_test_request(ip, port=2000):
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        print(f"Connected to bandwidth-test server at {ip}:{port}")


        if s.recv(1024) != b'\x01\x00\x00\x00':
            return ConnectionError
        
        request = create_start_test_request()
        s.sendall(request)
        
        
        response = s.recv(1024)[:4]
        if response == b'\x01\x00\x00\x00':
            return False, ''
        elif response == b'\x02\x00\x00\x00':
            return True, '<6.43'
        elif response == b'\x03\x00\x00\x00':
            return True, '>=6.43'
        else:
            return ConnectionError
        
if __name__ == "__main__":
    ip = '192.168.0.12'
    
    auth, version = send_bandwidth_test_request(ip)
    if auth == ConnectionError:
        print('ConnectionError')
    else:
        print(f"Authentication: {auth}\nVersion RouterOS: {version}")