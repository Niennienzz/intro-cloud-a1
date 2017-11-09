import rx
from rx import Observable, Observer


class ManagerObserver(Observer):
    def on_next(self, value):
        print(value)

    def on_error(self, e):
        print("Got error: %s" % e)

    def on_completed(self):
        print("Sequence completed")
