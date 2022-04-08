import os

def touch_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
        #print("Directory \"%s\" is created." % dir)
        'blah blah blah'
    else:
        #print("Directory \"%s\" has already existed. Do nothing to it." % dir)
        'blah blah blah'
