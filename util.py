class LRStruct:
    __slots__ = "left", "right"
    def __init__(self, left, right):
        self.left = left
        self.right = right
class DebugPrinter:
    __slots__ = "_interval", "_tick"
    def __init__(self, interval):
        self._interval = interval
        self._tick = 0
    def tick(self):
        self._tick += 1
    def lazy_print(self, func):
        if self._tick % self._interval == 0:
            print(func())
    def print(self, msg):
        self.lazy_print(lambda: msg)
