function Uint8Array_concat(ar1, ar2) {
  res = new Uint8Array(ar1.byteLength + ar2.byteLength)
  res.set(ar1)
  res.set(ar2, ar1.byteLength)
  return res
}

function Uint8Array_to_uint64(ar) {
  // the number is in network byte order
  if (ar.byteLength !== 8) {
    throw new Error("Require a Uint8Array with 8 bytes, but got " + ar)
  }
  res = 0
  for (var i = 0; i < 8; ++i) {
    res = res * 256 + ar[i];
  }
  return res
}
