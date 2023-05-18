from celery import shared_task


@shared_task
def user_prin():
    print('---------work------------')