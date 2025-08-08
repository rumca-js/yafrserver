
class Status(object):
    obj = None

    def __init__(self):
        self.reading_entries = False
        self.reading_sources = False


    def get_object():
        if not Status.obj:
            c = Status()
            Status.obj = c

        return Status.obj

