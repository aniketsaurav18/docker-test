from Compiler.Execution.pythonRunner import pythonRunner

commands = {
    'python': "python",
    'java': "java",
    'cpp': 'g++',
}


extensions = {
    'python': '.py',
    'java': '.java',
    'cpp': 'cpp'
}


def get_command(language):
    if language not in commands:
        return False, 'Invalid language.'

    return True, commands[language]


def get_extension(language):
    return extensions[language]


def get_target_method(language):
    if language == 'python':
        return pythonRunner

    else:
        return "false"

    # elif language == 'java':
    #     return java_runner

    # elif language == 'cpp':
    #     return cpp_runner
