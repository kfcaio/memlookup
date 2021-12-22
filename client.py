from urllib.parse import urljoin

import click
import requests


def get(node: str, key: str):
    url = urljoin(node, key)
    response = requests.get(url)

    print(response.text)


def set(node: str, key: str, value: str = None):
    if value is None:
        raise Exception("Method set needs <key> and <value>")

    response = requests.post(node, json={"key": key, "value": value})

    if response.ok:
        print(response.json())

@click.command()
@click.option(
    '--method',
    type=click.Choice(['get', 'set']),
    multiple=False,
)
@click.option(
    '--node',
    type=str,
    required=True
)
@click.option(
    '--key',
    type=str,
    required=True
)
@click.option(
    '--value',
    type=str,
    required=False
)
def cli(node, method, key, value):
    """Client to retrieve data from server

    Communicate with the server to access data. For example, it should be
    possible to run the server program on a machine as follows:

    $ ./server


    On the same machine (or a second machine), it should be possible to store
    items of data and retrieve them using this program. The interface should
    look roughly as follows:

    - Stores a value against a specific key in the server located at "node".

    $ ./client <node> set <key> <value>

    - Retrieves a value for a specific key and prints it, if found.

    $ ./client <node> get <key> <value>

    Below is an example of what should be expected to work. In this example,
    the server is being used to store the names of capital cities for a country.

    $ ./client 127.0.0.1 set norway oslo

    $ ./client 127.0.0.1 set denmark copenhagen

    $ ./client 127.0.0.1 get norway

    > oslo

    $ ./client 127.0.0.1 get sweden

    > error: not found

    """
    if method == "get":
        get(node, key)

    elif method == "set":
        set(node, key, value)


if __name__ == "__main__":
    cli()
