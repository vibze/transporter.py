def transporter_job(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return inner