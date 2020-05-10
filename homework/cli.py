import click
from homework.patient import *

@click.group()
def cli():
    pass


@cli.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--birth_date', '-a')
@click.option('--phone', '-a')
@click.option('--document_type', '-a')
@click.option('--document_id', '-a')
def create(first_name, last_name, birth_date, phone, document_type, document_id):
    test = Patient(first_name, last_name, birth_date, phone, document_type, document_id)
    test.save()
    click.echo("Создан новый пациент")


@cli.command()
@click.argument('value' , default = 10 )
def show(value):
    collection = PatientCollection()
    if value == 10:
        for patient in collection.limit(value):
            click.echo(patient)
    else:
        for patient in collection.limit(value):
            click.echo(patient)

@cli.command()
def count():
    count = 0
    var = pymysql.connect(host='localhost', port=3306, user='root', passwd='passwd',
                          db='forpat')
    conn = var.cursor(pymysql.cursors.DictCursor)
    conn.execute("SELECT * FROM patiens")
    rows = conn.fetchall()
    for row in rows:
        count = count + 1
    conn.close()
    var.close()
    click.echo(count)

if __name__ == '__main__':
    cli()