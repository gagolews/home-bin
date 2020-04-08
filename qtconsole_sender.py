#!/usr/bin/python3

"""
Send to a TCP port the commands execute on a Jupyter-QtConsole.

Copyright (C) 2020 Marek Gagolewski (https://www.gagolewski.com)
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


SOCKET_BUF_SIZE = 2048

import sys
import os, os.path, tempfile
import qtpy
from qtpy import QtCore
from qtpy import QtNetwork
import argparse



def write_socket(text, port):
    socket = QtNetwork.QTcpSocket()
    socket.connectToHost(QtNetwork.QHostAddress.LocalHost, port)
    if not socket.isValid() or not socket.waitForConnected(-1):
        raise Exception("Unable connect to a local TCP server at port %d"%port)


    text_bytes = text.encode("utf-8")
    text_size = len(text_bytes)

    # send the number of bytes to read:
    socket.write(QtCore.QByteArray.fromRawData(
        ("%d\n"%text_size).encode("utf-8")))
    if not socket.waitForBytesWritten(-1):
        raise Exception("Error sending buffer size to socket.")

    # send data buffer

    cur = 0
    while cur < text_size:
        cur_next = min(cur+SOCKET_BUF_SIZE, text_size)
        cur_n = socket.writeData(text_bytes[cur:])
        if cur_n < 0 or not socket.waitForBytesWritten(-1):
            raise Exception("Error sending buffer to socket.")
        cur += cur_n

    print("Wrote %d bytes."%text_size)

    socket.waitForDisconnected(-1)
    socket.close()
    socket = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Send to a TCP port the commands execute\
        on a Jupyter-QtConsole',
        epilog='Copyright (C) 2020 Marek Gagolewski (https://www.gagolewski.com)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("cmd", type=str, help="Command to execute.")
    parser.add_argument("--port", default=6666, type=int,
            help="TCP port to connect at the localhost.")
    args = parser.parse_args()

    text = args.cmd
    #text = repr(str(list(range(1))))
    write_socket(text, args.port)
