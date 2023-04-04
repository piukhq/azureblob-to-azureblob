import click

from app.main import AzureBlobCopier


@click.group()
def cli():
    pass


@cli.command(name="upload")
def upload():
    run = AzureBlobCopier()
    return run


@cli.command(name="diff")
def diff():
    run = AzureBlobCopier()
    return run.diff_containers()
