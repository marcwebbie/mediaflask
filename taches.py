from celery import Celery

celery = Celery('taches', broker='redis://localhost:6379')

@celery.task
def add(x, y):
    return x + y
