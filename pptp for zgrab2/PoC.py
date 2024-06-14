import socket
import struct

magic_cookie = 0x1A2B3C4D

# Структура сообщения PPTP: Start-Control-Connection-Request
def create_start_control_connection_request():
    # Поля заполняются примерными данными; отрегулируйте по мере необходимости
    length = 156
    msg_type = 1
    magic_cookie = 0x1A2B3C4D
    control_message_type = 1
    reserved0 = 0
    protocol_version = 0x0100  # 1.0 256
    reserved1 = 0
    framing_capabilities = 0x1  # Asynchronous
    bearer_capabilities = 0x1  # Analog
    max_channel = 0  # Not used
    firmware_revision = 0x1
    hostname = b'PPTP_Client' + bytes((64 - len('PPTP_Client')))
    vendor = b'Python_Client' + bytes((64 - len('Python_Client')))
    ret = struct.pack('!HHIHHHHLLHH64s64s',
                          length,
                          msg_type,
                          magic_cookie,
                          control_message_type,
                          reserved0,
                          protocol_version,
                          reserved1,
                          framing_capabilities,
                          bearer_capabilities,
                          max_channel,
                          firmware_revision,
                          hostname,
                          vendor)
    return ret

def connect_to_pptp_server(ip, port=1723):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.connect((ip, port))
        print(f"Connected to PPTP server at {ip}:{port}")

        request = create_start_control_connection_request()
        sock.sendall(request)
        reply = struct.unpack('!HHLHHHBBLLHH64s64s', sock.recv(156))
        if reply[2] == magic_cookie:
            return reply
        return False
        

if __name__ == "__main__":
    #target_server_ip = "144.217.253.149"
    #target_server_ip = "213.219.205.156" 
    targets = ["213.219.205.156",
                "144.217.253.149",
                "54.36.174.134",]
    for target in targets:
        reply = connect_to_pptp_server(target)

        if not reply:
            print("соединение не удалось")
        else:
            print({'length' : reply[0],
                'msg_type' : reply[1],
                'magic_cookie' : reply[2],
                'control_message_type' : reply[3],
                'reserved0' : reply[4],
                'protocol_version' : reply[5],  # 1.0
                'result_code' : reply[6],
                'error_code' : reply[7],
                'framing_capabilities' : reply[8] , 
                'bearer_capabilities' : reply[9],  # Analog
                'max_channel' : reply[10],  # Not used
                'firmware_revision' : reply[11],
                'hostname' :  bytes(reply[12]).replace(b'\x00', b'').decode(),
                'vendor' : bytes(reply[13]).replace(b'\x00', b'').decode(),})