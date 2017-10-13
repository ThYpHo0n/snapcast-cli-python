import json
import telnetlib

import click


def doRequest(server, port, request, requestId):
    telnet = telnetlib.Telnet(server, port)
    request = request + "\r\n"
    telnet.write(request.encode('ascii'))
    while (True):
        response = telnet.read_until("\r\n".encode('ascii'), 2)
        jResponse = json.loads(response)
        if 'id' in jResponse:
            if jResponse['id'] == requestId:
                telnet.close()
                return jResponse
    return


@click.group()
def cli():
    pass


@click.command()
@click.option('--server', default='127.0.0.1', help='Snapserver ip address')
@click.option('--port', default='1705', help='Snapserver port')
def list(server, port):
    """List all clients."""
    click.echo('list Server %s:%s' % (server, port))
    response = doRequest(server, port, json.dumps({'jsonrpc': '2.0', 'method': 'Server.GetStatus', 'id': 1}), 1)
    click.echo('response %s' % response)


@click.command()
@click.argument('client')
@click.option('--server', default='127.0.0.1', help='Snapserver ip address')
@click.option('--port', default='1705', help='Snapserver port')
def mute(client, server, port):
    """Mute a client"""
    click.echo('mute Server %s:%s' % (server, port))
    request = json.dumps({'jsonrpc': '2.0', 'method': 'Client.SetMute', 'params': {'client': client, 'mute': True}, 'id': 1})
    response = doRequest(server, port, request, 1)
    click.echo('response %s' % response)


cli.add_command(list)
cli.add_command(mute)

if __name__ == '__main__':
    cli()
