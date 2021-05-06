from django.dispatch import Signal

#instance means any object with details, which will be sent
#instead of pre_save or post_save signal, we made object_viewed signal
user_logged_signal = Signal(providing_args=['instance','request'])
