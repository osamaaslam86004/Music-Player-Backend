import concurrent.futures

# create a thread pool with the default number of worker threads
pool = concurrent.futures.ThreadPoolExecutor()

# report the number of worker threads chosen by default
# Note: `_max_workers` is a protected variable and may change in the future
print(pool._max_workers)