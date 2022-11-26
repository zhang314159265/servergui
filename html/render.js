function render(payload) {
  console.log("Render " + payload.byteLength + " bytes payload")

  if (payload.byteLength >= 4 && new TextDecoder().decode(payload.slice(1, 4)) === "PNG") {
    render_image(payload)
  } else {
    console.log("Assuming a text payload")
    text_payload = new TextDecoder().decode(payload)
    render_text(text_payload)
  }
}

function render_image(payload) {
  console.log("Render an image payload")
  var img = document.createElement("img")
  img.src = "data:image/png;base64," + btoa(Uint8Array_to_string(payload))
  document.body.prepend(img)
}

function render_text(text) {
  var div = null
  console.log("Render text")

  div = document.createElement("div")
  div.innerHTML = "<pre>" + text + "</pre>"
  div.style.border = "solid 1px green"
  document.body.prepend(div)
}
