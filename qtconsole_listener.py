#!/usr/bin/python3

"""
An application that features a Jupyter-QtConsole and listens for commands to
execute on a TCP port.

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
from qtpy import QtWidgets
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtNetwork
from qtconsole.rich_jupyter_widget import RichJupyterWidget
from qtconsole.manager import QtKernelManager
import argparse




class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, port, kernel_name):
        super().__init__()

        self.server = QtNetwork.QTcpServer(self)
        if not self.server.listen(QtNetwork.QHostAddress.LocalHost, port):
            raise Exception("Unable set up a local TCP server at port %d"%port)
        self.server.newConnection.connect(self.new_connection)

        kernel_manager = QtKernelManager(kernel_name=kernel_name)
        kernel_manager.start_kernel()

        kernel_client = kernel_manager.client()
        kernel_client.start_channels()

        self.jupyter_widget = RichJupyterWidget()
        self.jupyter_widget.kernel_manager = kernel_manager
        self.jupyter_widget.kernel_client = kernel_client

        #self.jupyter_widget.set_default_style("linux")
        #self.jupyter_widget.syntax_style = "monokai"
        self.jupyter_widget._set_font(QtGui.QFont("Ubuntu Mono", 12))

        self.setCentralWidget(self.jupyter_widget)
        print("Kernel %s listening at port %d."%(kernel_name, port))


    def shutdown_kernel(self):
        self.jupyter_widget.kernel_client.stop_channels()
        self.jupyter_widget.kernel_manager.shutdown_kernel()
        self.server.close()


    def new_connection(self):
        socket = self.server.nextPendingConnection()
        socket.setReadBufferSize(SOCKET_BUF_SIZE)
        socket.waitForReadyRead(-1)

        # expected number of bytes
        text_size = int(socket.readLine().data().decode("utf-8"))
        assert text_size > 0

        print("Reading %d bytes."%text_size)
        text = QtCore.QByteArray()
        first = True
        while text.size() != text_size:
            # first batch with no wait, data is pending (I think)
            if not first and not socket.waitForReadyRead(-1):
                print("Error receiving %d bytes of data. Ignoring this batch."%text_size)
                socket.disconnectFromHost()
                socket.close()
                return
            buf = socket.readAll()
            text.append(QtCore.QByteArray.fromRawData(buf))
            print(text.size())
            first = False

        print("%d bytes received."%text_size)
        #socket.write(QtCore.QByteArray.fromRawData("OK".encode("utf-8")))
        #socket.waitForBytesWritten(-1)
        socket.disconnectFromHost()
        socket.close()
        socket = None

        assert text_size == text.size()
        text = text.data().decode("utf-8")
        self.execute(text)


    def execute(self, code):
        cursor = self.jupyter_widget._get_end_cursor()
        cursor.beginEditBlock()
        try:
            for line in code.splitlines():
                cursor.insertText(line+"\n")
                self.jupyter_widget._insert_continuation_prompt(cursor, False)
        finally:
            cursor.endEditBlock()
        self.jupyter_widget.do_execute(source=code, complete=True, indent=False)







if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='An application that features a Jupyter-QtConsole\
        and listens for commands to execute on a TCP port.',
        epilog='Copyright (C) 2020 Marek Gagolewski (https://www.gagolewski.com)',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("kernel", default="python3", type=str, nargs='?',
        help="The id of an installed kernel, e.g., 'python3' (the default),\
            'bash' or 'ir'.")
    parser.add_argument("--port", default=6666, type=int,
            help="TCP port the localhost shall listen at.")
    args = parser.parse_args()


    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(args.port, args.kernel)
    window.show()
    app.aboutToQuit.connect(window.shutdown_kernel)
    app.exec_()
