import click
from banking import TimPay


@click.group()
def timpay():
    """A command line util to access the TimPay API."""
    pass


@timpay.command()
def balance():
    # TODO
    pass

@timpay.command()
def transactions():
    # TODO
    pass


if __name__ == '__name__':
    timpay(prog_name='timpay')