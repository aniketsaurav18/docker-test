import docker
import os
from config import DOCKER_IMAGE, AUTO_REMOVE, MEMORY_LIMIT, FILE_OPEN_MODE
CONTAINER_DIR = '/data/' # the container directory where code execution take place

def pythonRunner(dockerClient, file_name_code, file_name_input, container_name, dataFilePath, return_dict):
    print(file_name_code)
    print(file_name_input)
    pythonRunCommand = "python3 " + "script.py" + " < " + "input.txt"
    containerDir = CONTAINER_DIR
    if not os.path.exists(dataFilePath + file_name_code):
            raise Exception('File not found : ' + str(dataFilePath + file_name_code))
    try: 
        result = dockerClient.containers.run(DOCKER_IMAGE, pythonRunCommand,
                                       remove=AUTO_REMOVE, mem_limit=MEMORY_LIMIT,
                                       name=container_name,
                                       volumes={dataFilePath: {
                                                'bind': containerDir,
                                                'mode': FILE_OPEN_MODE}
                                                })
    except Exception as e:
         print("printing exception in docker python exec")
         return_dict["result"] = str(e)
         
    return_dict['result'] = result

