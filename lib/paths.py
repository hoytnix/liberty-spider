import os

cwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.abspath(os.path.join(cwd, os.pardir))
app = os.path.join(project, 'lycosidae')

database_path = os.path.join(project, 'database.db')
exit_path = os.path.join(project, 'exit-flag.txt')
env_path = os.path.join(project, 'env.txt')
log_path = os.path.join(project, 'lycos.log')