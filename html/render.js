function render_text(text) {
  var div = null
  console.log("Render text")

  div = document.createElement("div")
  div.innerHTML = "<pre>" + text + "</pre>"
  div.style.border = "solid 1px green"
  document.body.prepend(div)
}
