from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def superuser(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp apps")


@task
def bot(c):
    c.run("python bot/main.py")


@task
def load(c):
    c.run(
        "python manage.py loaddata user.json categories.json category_translation.json product_translation.json products.json images.json"
    )


@task
def dump(c):
    c.run("python manage.py dumpdata apps.productimage > images.json")


@task
def lang(c):
    c.run("django-admin makemessages -l uz")
    c.run('django-admin makemessages -l ru')


@task
def compile(c):
    c.run("django-admin compilemessages")
