from server import Server
from conf import config


def main():

    Server(config['server']).start()


if __name__ == '__main__':
    main()
