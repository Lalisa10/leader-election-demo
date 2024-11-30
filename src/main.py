# from fastapi import FastAPI, HTTPException
#
# from DistributedMutex import DistributedMutex
# from constant import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
# from MySqlHandler import TransactionRequest, MySQLHandler
#
#
# # Biến xác định vai trò của server (leader/follower)
# mysql_handler = MySQLHandler(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME)
#
#
# app = FastAPI()
#
# @app.post("/post_transaction",response_model=TransactionRequest)
# async def handle_transaction(transaction: TransactionRequest):
#         # Ghi dữ liệu vào MySQL
#     await mysql_handler.leader_task(transaction.account_number, transaction.password, transaction.amount)
#     return transaction
#
# @app.get("/get_transactions",response_model=list[TransactionRequest])
# async def get_transactions():
#     transactions = await mysql_handler.worker_task()
#     return transactions
#
# if __name__ == "__main__":
#     mutex = DistributedMutex(leader_task(), worker_task())
#     mutex.run()