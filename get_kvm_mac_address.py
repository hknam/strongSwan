import subprocess
import shlex
import sys

def get_client_list():
    command = "virsh list --all"
    args = shlex.split(command)
    try:
        with subprocess.Popen(args, stdout=subprocess.PIPE) as proc:
            output = str(proc.stdout.read())
    except Exception as e:
        print(e)
        sys.exit(1)

    output_list = output.split('\\n')
    client_list = output_list[2:len(output_list)-2]

    for line in client_list:
        #starts :' -     '
        client = line[7:]
        strip_index = client.find(' ')
        name = client[:strip_index]
        print(name)


def main():
    get_client_list()

if __name__ == "__main__":
    get_client_list()
