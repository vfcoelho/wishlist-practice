class Lambda(object):

    def __call__(self, f):

        def run (event,context):

            return f(event=event,context=context)

        return run