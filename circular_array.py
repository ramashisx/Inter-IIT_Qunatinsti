class circular_array:
    def __init__(self, size):
        self.size = size
        self.array = [None] * size
        self.index = 0
        self.count = 0
    def insert(self, value):
        self.array[self.index] = value
        self.index = (self.index + 1) % self.size
        self.count = min(self.count + 1, self.size)
    def get(self, index):
        return self.array[(self.index + index) % self.size]
    def get_min(self):
        if(self.count == 0):
            return None
        idx = self.index
        num = self.array[idx-1]

        for i in range(1,self.count):
            idx = (idx - 1) % self.size
            num = min(num, self.array[idx])
        return num
    def get_max(self):
        if(self.count == 0):
            return None
        idx = self.index
        num = self.array[idx-1]

        for i in range(1,self.count):
            idx = (idx - 1) % self.size
            num = max(num, self.array[idx])
        return num

    def __len__(self):
        return self.count
    def __getitem__(self, index):
        return self.get(index)
    def __setitem__(self, index, value):
        self.array[(self.index + index) % self.size] = value
    def __repr__(self):
        return repr(self.array[:self.count])
    def __str__(self):
        return str(self.array[:self.count])
    def __iter__(self):
        for i in range(self.count):
            yield self[i]
    def __reversed__(self):
        for i in range(self.count):
            yield self[-i-1]
    def __contains__(self, value):
        for i in range(self.count):
            if self[i] == value:
                return True
        return False
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(self.count):
            if self[i] != other[i]:
                return False
        return True
    def __ne__(self, other):
        return not self == other
    def __lt__(self, other):
        for i in range(min(self.count, other.count)):
            if self[i] < other[i]:
                return True
            if self[i] > other[i]:
                return False
        return self.count < other.count
    def __le__(self, other):
        for i in range(min(self.count, other.count)):
            if self[i] < other[i]:
                return True
            if self[i] > other[i]:
                return False
        return self.count <= other.count
    def __gt__(self, other):
        for i in range(min(self.count, other.count)):
            if self[i] > other[i]:
                return True
            if self[i] < other[i]:
                return False
        return self.count > other.count
    