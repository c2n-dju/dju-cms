def my_callback(sender, **kwargs):
    print("Request finished!")
    print(kwargs)

from django_cas_ng.signals import cas_user_authenticated

cas_user_authenticated.connect(my_callback)
