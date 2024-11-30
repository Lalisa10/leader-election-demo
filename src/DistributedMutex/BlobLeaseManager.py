from azure.storage.blob.aio import BlobServiceClient # type: ignore
from azure.storage.blob.aio._lease_async import BlobLeaseClient # type: ignore
from BlobSetting import BlobSetting
import asyncio
from constant import LEASE_DURATION, ACQUIRE_DURATION, RENEW_DURATION
from multiprocessing import Pipe
import multiprocessing 

class BlobLeaseManager:
    def __init__(self, blob_setting : BlobSetting):
        self.blob_client = blob_setting.get_blob_client()
        self.lease = None

    def get_lease(self):
        return self.lease

    def has_lease(self):
        return self.lease is not None
    
    async def acquire_lease(self):
        try:
            self.lease = await self.blob_client.acquire_lease(lease_duration=LEASE_DURATION)
            print("Successfully acquired lease!")
        except:
            print("Failed to acquire lease!")
            self.lease = None
        return self.lease
        
    async def renew_lease(self):
        try:
            await self.lease.renew()
            print("Successfully renewed lease!")
        except:
            self.lease = None
            print("Failed to renew lease!")
        return self.lease
    
    async def release_lease(self):
        if self.lease is None:
            return
        await self.lease.release()

    async def acquire_lease_periodically(self, pipe):
        while not self.has_lease():
            await asyncio.gather(self.acquire_lease(), asyncio.sleep(ACQUIRE_DURATION))
            pipe.send(self.lease is not None)
    
    async def renew_lease_periodically(self, pipe):
        while self.has_lease():
            try:
                await asyncio.gather(self.renew_lease(), asyncio.sleep(RENEW_DURATION))
                pipe.send(self.lease is not None)
            except:
                print("Lease expired! Attempting to acquire lease...")
                self.lease = None
                await self.acquire_lease_periodically(pipe)


    async def run(self, pipe):
        while True:
            await self.acquire_lease_periodically(pipe)
            await self.renew_lease_periodically(pipe)
