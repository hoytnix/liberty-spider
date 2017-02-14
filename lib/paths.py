import os

cwd = os.path.abspath(os.path.dirname(__file__))
pd = os.path.abspath(os.path.join(cwd, os.pardir))
database_path = os.path.join(pd, 'database.db')
exit_path = os.path.join(pd, 'exit-flag.txt')