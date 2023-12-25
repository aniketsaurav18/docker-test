LOCAL_DIR = 'E:/Personal Projects/Online code compiler'
CONTAINER_TIMEOUT = 10 # how much time a process will run before terminating (in seconds)
DOCKER_IMAGE = "python-exec" # name of the docker image
AUTO_REMOVE = True # remove the container after code execution
MEMORY_LIMIT = '8000k'  # the memory limit for the each docker container
FILE_OPEN_MODE = 'ro' #read only : use rw for read write (container permission)