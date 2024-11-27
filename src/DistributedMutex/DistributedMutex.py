from BlobLeaseManager import BlobLeaseManager
import asyncio
from BlobSetting import BlobSetting
from constant import CONNECTION_STRING, CONTAINER_NAME, BLOB_NAME
from multiprocessing import Process, Pipe

class DistributedMutex:
    def __init__(self, leader_task : callable, worker_task: callable):
        self.leader_task = leader_task
        self.worker_task = worker_task
        self.lease_manager = BlobLeaseManager(BlobSetting(CONNECTION_STRING, CONTAINER_NAME, BLOB_NAME))

    async def run_task(self, pipe):
        while True:
            lease_status = pipe.recv()
            if lease_status is True:
                await self.leader_task()
            else:
                await self.worker_task()

    def run(self):
        parent_conn, child_conn = Pipe()

        lease_manager_process = Process(target=self.run_asyncio_lease_manager, args=(parent_conn,))
        task_process = Process(target=self.run_asyncio_task, args=(child_conn,))

        lease_manager_process.start()
        task_process.start()

        lease_manager_process.join()
        task_process.join()

    def run_asyncio_task(self, pipe):
        asyncio.run(self.run_task(pipe))
    
    def run_asyncio_lease_manager(self, pipe):
        asyncio.run(self.lease_manager.run(pipe))

