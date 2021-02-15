import click, json
from banking import Hype


@click.group()
def hype():
    """A command line util to access the Hype API."""
    pass


@hype.command()
@click.option('--username', prompt=True, required=True, type=click.STRING, help='Your HYPE email')
@click.password_option('--password', help='Your HYPE password', confirmation_prompt=False)
@click.option('--birthday', required=False, type=click.STRING, default=None, help='Your birthday: yyyy-mm-dd')
def balance(username, password, birthday):
    hype = Hype()
    try:
        hype.login(username, password, birthday)
    except Exception as error:
        click.echo(str(error))

    code = click.prompt('OTP Code')
    try:
        hype.otp2fa(code)
    except Exception as error:
        click.echo(str(error))

    try:
        balance:dict = hype.get_balance()
        click.echo('')
        for key in balance:
            click.echo(f'{key}: \u20ac{balance[key]}')
    except Exception as error:
        click.echo(str(error))

@hype.command()
@click.option('--username', prompt=True, required=True, type=click.STRING, help='Your HYPE email')
@click.password_option('--password', help='Your HYPE password', confirmation_prompt=False)
@click.option('--birthday', required=False, type=click.STRING, default=None, help='Your birthday: yyyy-mm-dd')
@click.option('--limit', required=False, default=999999, type=click.INT, help='Amount of movements to retrieve')
def movements(username, password, birthday, limit):
    hype = Hype()
    try:
        hype.login(username, password, birthday)
    except Exception as error:
        click.echo(str(error))

    code = click.prompt('OTP code')
    try:
        hype.otp2fa(code)
    except Exception as error:
        click.echo(str(error))

    try:
        movements = hype.get_movements(limit)
        with open('movements.json', 'w+') as file:
            json.dump(movements, file)
    except Exception as error:
        click.echo(str(error))


if __name__ == '__name__':
    hype(prog_name='hype')