from optparse import OptionParser
import socket
import json

def send(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 1345))
        s.sendall(path.encode())

def main():
    usage = "usage: sgcat path"
    parser = OptionParser(usage=usage)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error(f"Require a single positional argument")
    print(f"options {options}")
    print(f"args {args}")
    send(args[0])
    print("bye")

if __name__ == "__main__":
    main()
