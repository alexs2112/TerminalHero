class BumpLocation:
    def __init__(self, diff, milliseconds):
        self.current = (0,0)
        self.end = diff
        self.total_time = milliseconds
        self.time_elapsed = 0

    def get_pos_delta(self):
        return self.current

    def update(self, time):
        self.time_elapsed += time
        percentage = time / self.total_time
        self.current = (self.current[0] + self.end[0] * percentage, self.current[1] + self.end[1] * percentage)

    def finished(self):
        return self.time_elapsed >= self.total_time
