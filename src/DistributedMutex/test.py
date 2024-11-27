from DistributedMutex import DistributedMutex
import asyncio
import datetime

async def leader_task():
   print("I'm the leader!")
   await asyncio.sleep(10)

async def worker_task():
   print("I'm a worker!")
   await asyncio.sleep(10)

def main():
    mutex = DistributedMutex(leader_task, worker_task)
    mutex.run()
    
main()

