from swen344_db_utils import *

def rebuild_tables():
    exec_sql_file("src/chat.sql")
    exec_sql_file("src/chat_data.sql")

