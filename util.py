class LRStruct:
    __slots__ = "left", "right"
    def __init__(self, left, right):
        self.left = left
        self.right = right
class DebugLogger:
    __slots__ = "_interval", "_tick", "_printed_tags"
    def __init__(self, interval):
        self._interval = interval
        self._tick = 0
        self._printed_tags = {}
    def tick(self):
        self._tick += 1
    def lazy_print(self, func):
        if (self._tick % self._interval) == 0:
            print(func())
    def print(self, msg):
        self.lazy_print(lambda: msg)
    def lazy_print_once(self, tag, func):
        if not (tag in self._printed_tags):
            self._printed_tags[tag] = True
            print(func())
    def print_once(self, tag, msg):
        self.lazy_print_once(tag, lambda: msg)
    def reset_print_tag(self, tag):
        if tag in self._printed_tags:
            del self._printed_tags[tag]
