class AndroidNotification:
    def __init__(self, title, body, application, package, id):
        self.application = application
        self.body = body
        self.package = package
        self.title = title
        self.id = id
