#making of unique slug
import random
import string

from django.utils.text import slugify

def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_order_id_generator(instance):
    """
    This is for a Django project to create random and unique order id.
    """
    order_new_id = random_string_generator()

    #checks the new order id in database if its unique or not
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    #if its already there, if not return the order id
    if qs_exists:
        #again runs the same function to create new one
        return unique_order_id_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug = slug,
                    randstr = random_string_generator(size=4)
                    )
        return unique_slug_generator(instance,new_slug=new_slug)
    return slug
