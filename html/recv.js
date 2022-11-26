recv_state = "EXPECT_LEN"

// an Uint8Array can be backed by an ArrayBuffer and using it's internal storage
recv_buffer = new Uint8Array(0)
len_metadata = 0
metadata = null
payload = null
event_list = []

ws = new WebSocket("ws://shunting.mynetgear.com:1346");
// change binary type from "blob" to "arraybuffer"
// Refer to https://developer.mozilla.org/en-US/docs/Web/API/WebSocket/binaryType
// for more details
ws.binaryType = "arraybuffer"
ws.addEventListener("message", function(event) {
  var event_data = null
  var text_payload = null

  if (event_list !== null) {
    event_list.push(event)
  }
  console.log("Got message: " + event.data);
  event_data = event.data
  if (typeof(event.data) === "string") {
    event_data = new TextEncoder().encode(event_data)
  } else if (event.data instanceof ArrayBuffer) {
    event_data = new Uint8Array(event_data)
  } else {
    throw new Error("Unexpected event data " + event.data);
  }
  recv_buffer = Uint8Array_concat(recv_buffer, event_data)
  console.log("recv_buffer contains " + recv_buffer.byteLength + " bytes")

  if (recv_state == "EXPECT_LEN") {
    if (recv_buffer.byteLength >= 8) {
      // get len_metadata
      len_metadata = Uint8Array_to_uint64(recv_buffer.slice(0, 8))
      console.log("Got metadata length " + len_metadata)
      recv_buffer = recv_buffer.slice(8)
      recv_state = "EXPECT_META";
    }
  }
  if (recv_state == "EXPECT_META") {
    if (recv_buffer.byteLength >= len_metadata) {
      metadata = JSON.parse(new TextDecoder().decode(recv_buffer.slice(0, len_metadata)))
      console.log("Got metadata " + metadata)
      recv_buffer = recv_buffer.slice(len_metadata)
      recv_state = "EXPECT_PAYLOAD"
    }
  }
  if (recv_state == "EXPECT_PAYLOAD") {
    if (recv_buffer.byteLength >= metadata.file_size) {
      payload = recv_buffer.slice(0, metadata.file_size)
      recv_buffer = recv_buffer.slice(metadata.file_size)
      recv_state = "EXPECT_LEN"
      console.log("Got " + payload.byteLength + " bytes payload")
      // TODO: compare the md5sum. md5.min.js works for string but seems to not
      // work for Uint8Array

      render(payload)
    }
  }
});
