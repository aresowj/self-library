
def get_django_model_classes(module):
    # getmembers() will return a tuple like (('class_name', class_ref), ()...)
    return [ret[1] for ret in inspect.getmembers(module, inspect.isclass) if issubclass(ret[1], models.Model)]
