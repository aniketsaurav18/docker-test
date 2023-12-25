import os
import docker
import hashlib
import multiprocessing
from multiprocessing import Process, set_start_method, get_start_method
from Compiler.util import get_command, get_extension, get_target_method
from config import LOCAL_DIR, CONTAINER_TIMEOUT

code = 'n = int(input("Enter the value of n: "))\nnumbers = [float(input()) for i in range(n)]\nprint([number**2 for number in numbers])'

input = "3\n1\n2\n3"
language = "python"


def compile(code, input, language):
    dockerClient = docker.from_env()
    manager = multiprocessing.Manager()
    # the dict that will be send to the separate python process for collecting the result
    return_dict = manager.dict()

    result, command_string = get_command(language)

    if not result:
        return_dict['result'] = command_string
        return return_dict
    LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
    dataFilePath = LOCAL_DIR+"/data/"
    # saving the code in a temp file
    container_name = str(hashlib.sha1(os.urandom(128)).hexdigest())[:10]
    file_name_code = container_name + str(get_extension(language))
    file_path_code = dataFilePath + file_name_code
    file_name_input = container_name + '.txt'
    file_path_input = dataFilePath + file_name_input
    try:
        file = open(file_path_code, 'w')
        file.write(str(code))
        file.close()
        file = open(file_path_input, 'w')
        file.write(input)
        file.close()
    except Exception as e:
        print("writing error")
        print(e)
        return_dict['result'] = f"Error while writing code on temp file + ${str(e)}"
        return return_dict

    # getting which compiler method will handle this request
    target_method = get_target_method(language)

    # setting the start method to 'spawn' for Windows
    # try:
    #     set_start_method('spawn')
    # except RuntimeError:
    #     print("error in spawn")
    #     pass  # 'spawn' method was already set

    # starting the docker container in separate process
    process = multiprocessing.Process(target=target_method,
                                      args=(dockerClient, file_name_code, file_name_input, container_name, dataFilePath, return_dict))
    process.start()

    # setting the timeout for the process
    process.join(CONTAINER_TIMEOUT)

    # if the process/container is still alive kill the process
    if process.is_alive():
        process.terminate()
        process.join()
        return_dict['result'] = 'Time limit Exceeded'

    # check if the container is still running. if yes, kill the container
    running_containers = dockerClient.containers.list(
        filters={'name': container_name}, all=True)
    if running_containers:
        running_containers[0].remove(force=True)

    # remove the temp file
    # os.remove(file_path_code)
    # os.remove(file_path_input)
    print(return_dict)
    return return_dict


#
if __name__ == '__main__':
    compile(code, input, language)
