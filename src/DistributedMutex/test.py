from DistributedMutex import DistributedMutex
from constant import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from MySqlHandler import MySQLHandler

def main():
    mysql_handler = MySQLHandler(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    mutex = DistributedMutex(mysql_handler.leader_task, mysql_handler.worker_task)
    mutex.run()
main()

