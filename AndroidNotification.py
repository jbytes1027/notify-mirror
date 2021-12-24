class AndroidNotification:
    def __init__(self, header, body, application, package, id_num):
        self.application = application
        self.body = body
        self.package = package
        self.header = header
        self.id = id_num
