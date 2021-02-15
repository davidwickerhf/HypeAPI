import click, json, datetime, os, csv, logging

from banking import Hype
from banking.utils import utils


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
def profile(username, password, birthday):
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
        info = hype.get_profile_info()
        click.echo('')
        for key in info:
            click.echo(f'{key}: {info[key]}')
    except Exception as error:
        click.echo(str(error))


@hype.command()
@click.option('--username', prompt=True, required=True, type=click.STRING, help='Your HYPE email')
@click.password_option('--password', help='Your HYPE password', confirmation_prompt=False)
@click.option('--birthday', required=False, type=click.STRING, default=None, help='Your birthday: yyyy-mm-dd')
@click.option('--limit', required=False, default=999999, type=click.INT, help='Amount of movements to retrieve')
@click.option('--csvfile', is_flag=True, required=False, default=False, help='Use this flag to output the transactions in a CSV file')
@click.option('--jsonfile', is_flag=True, required=False, default=False, help='Use this flag to output the transactions in a JSON file')
@click.option('--output', type=click.Path(exists=True, dir_okay=True), help="The path of the output folder", required=False, default=None)
def movements(username, password, birthday, limit, csvfile, jsonfile, output):
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
        # Get & Format movements
        movements = hype.get_movements(limit)
        parsed = utils.parse_movements(movements)

        # Output in console
        click.echo('')
        if not csvfile and not jsonfile:
            for index, movement in enumerate(parsed):
                for key in movement:
                    click.echo(f'{key}: {movement[key]}')
                click.echo()
            return
        
        if not output:
            while True:
                output = click.prompt('Input the path of the desired output folder')
                if os.path.isdir(output):
                    break

        # Get user code
        profile = hype.get_profile_info()
        user = str(profile.get('userCode'))

        # Format timestamp
        date = movements.get('end')
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        date = int(date.timestamp())

        # Output JSON file
        if jsonfile:
            filename = f'{output}/{date}_{user}.json' if output else f'{date}_{user}.json'
            with open(filename, 'w+') as file:
                json.dump(parsed, file)
                click.echo(f'Movements saved to JSON file {filename}')

        # Output CSV file
        if csvfile:
            filename = f'{output}/{date}_{user}.csv' if output else f'{date}_{user}.csv'
            columns = ['id', 'title', 'amount', 'income', 'date', 'subType', 'category', 'reference', 'name', 'surname']

            rows = list()
            for movement in parsed:
                data = list()
                data.append(movement.get('id'))
                data.append(movement.get('title'))
                data.append(movement.get('amount'))
                data.append(movement.get('income'))
                data.append(movement.get('date'))
                data.append(movement.get('subType'))
                data.append(movement.get('category'))
                data.append(movement.get('reference'))
                data.append(movement.get('name'))
                data.append(movement.get('surname'))
                rows.append(data)

            with open(filename, 'w+') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)
                click.echo(f'Movements saved to CSV file {filename}')


    except Exception as error:
        logging.warning('Error', exc_info=error)
        click.echo(str(error))


if __name__ == '__name__':
    hype(prog_name='hype')