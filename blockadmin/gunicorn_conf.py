import multiprocessing

def post_fork(server, worker):
   from psycogreen.gevent import patch_psycopg
   patch_psycopg()

workers = min(multiprocessing.cpu_count() - 1, 4)
worker_class = 'gevent'
worker_connections = 10240

max_requests = 3000
max_requests_jitter = 100
