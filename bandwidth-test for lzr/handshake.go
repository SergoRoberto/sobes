package bandwidthtest

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"os"

	"github.com/stanford-esrg/lzr"
)

// Handshake implements the lzr.Handshake interface
type HandshakeMod struct {
}

type startTestRequest struct {
	protocol           uint8
	direction          uint8
	random_data        uint8
	tcp_count          uint8
	tx_size            uint16
	client_buffer_size uint16
	remote_tx_speed    uint32
	local_tx_speed     uint32
}

func createStartTestRequest() *startTestRequest {
	request := &startTestRequest{
		protocol:           1,    // TCP
		direction:          1,    // наприавление - передача
		random_data:        1,    // не использовать
		tcp_count:          0,    //
		tx_size:            1500, // размер передачи
		client_buffer_size: 0,    // неизвестно
		remote_tx_speed:    0,    // unlim
		local_tx_speed:     0,    // unlim
	}
	return request
}

func (h *HandshakeMod) GetData(dst string) []byte {

	request := createStartTestRequest()

	var buffer bytes.Buffer
	if err := binary.Write(&buffer, binary.BigEndian, request); err != nil {
		fmt.Printf("Failed to encode request: %v\n", err)
		os.Exit(1)
	}
	return buffer.Bytes()
}

func (h *HandshakeMod) Verify(data string) string {
	if bytes.Equal([]byte(data), []byte("\x01\x00\x00\x00")) {
		return "bandwidthtest, Authentication: false"
	}
	if bytes.Equal([]byte(data), []byte("\x02\x00\x00\x00")) {
		return "bandwidthtest, Authentication: true, Version RouterOS: <6.43"
	}
	if bytes.Equal([]byte(data), []byte("\x03\x00\x00\x00")) {
		return "bandwidthtest, Authentication: true, Version RouterOS: >=6.43"
	}
	return ""
}

func RegisterHandshake() {
	var h HandshakeMod
	lzr.AddHandshake("bandwidthtest", &h)
}
