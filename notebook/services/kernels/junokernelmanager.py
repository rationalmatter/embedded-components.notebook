#
# Copyright (C) 2021, Rational Matter Ltd. All rights Reserved
#
# This software and/or source code may be used, copied and/or disseminated only with the written
# permission of Rational Matter Ltd, or in accordance with the terms and conditions stipulated in the
# agreement/contract under which the software and/or source code has been supplied by Rational Matter Ltd or
# its affiliates. Unauthorized use, copying, or dissemination of this file, via any medium, is strictly
# prohibited, and will constitute an infringement of copyright.
#

from jupyter_client.ioloop.manager import IOLoopKernelManager
from jupyter_client.asynchronous import AsyncKernelClient
from ipykernel.inprocess.channels import InProcessHBChannel
from traitlets import Type
import asyncio
import junoapp

class JunoDummyHBChannel(InProcessHBChannel):
    def __init__(self, *args):
        super(JunoDummyHBChannel, self).__init__()

class JunoKernelClient(AsyncKernelClient):
    hb_channel_class = Type(JunoDummyHBChannel)

class JunoKernelManager(IOLoopKernelManager):
    client_factory: Type = Type(JunoKernelClient)

    async def _launch_kernel(self, kernel_cmd, **kw):
        print('[JunoKernelManager] Ignoring request to launch kernel; launching natively instead')
        junoapp.launch_kernel(self.connection_file)
        # Wait till the native kernel manager finishes preparing a sub-interpreter for the kernel and initialising new kernel app instance.
        # This behaviour should be similar to standard Jupyter, which also doesn't start connecting to a new kernel right away, waiting
        # for it to finish initialising in its separate-process interpreter (or so it seems).
        # We could potentially replace this mechanism with a proper await-able: https://stackoverflow.com/questions/51029111/python-how-to-implement-a-c-function-as-awaitable-coroutine
        junoapp.log('[JunoKernelManager] Waiting for kernel app instance to finish initialising...')
        while junoapp.is_starting_kernel(self.connection_file):
            await asyncio.sleep(0.25)
        junoapp.log('[JunoKernelManager] We now have an initialised kernel app instance; leaving _launch_kernel now...')
        return None

    def is_alive(self):
        """Is the kernel process still running?"""
        if self.connection_file:
            return junoapp.is_kernel_active(self.connection_file)
        return False

    def restart_kernel(self, kernel_id):
        print('[JunoKernelManager] Ignoring attempt to restart kernel; launching natively instead')
        start_kernel()

    def shutdown_kernel(self, kernel_id='', now=True, restart=False):
        print('[JunoKernelManager] Ignoring attempt to shutdown kernel; shutting down current kernel natively instead')
        junoapp.shutdown_kernel(self.connection_file)
        return None

    def request_shutdown(self, restart=False):
        print('[JunoKernelManager] Ignoring request to shutdown kernel; shutting down current kernel natively instead')
        junoapp.shutdown_kernel(self.connection_file)

    def interrupt_kernel(self):
        print('[JunoKernelManager] Ignoring request to interrupt kernel; interrupting current kernel natively instead')
        junoapp.interrupt_kernel(self.connection_file)
