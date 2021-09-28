import eel

eel.init('web')


@eel.expose                         # Expose this function to Javascript
def say_hello_py():
    print('Hello World')


eel.start('index.html', size=(1024, 300))
