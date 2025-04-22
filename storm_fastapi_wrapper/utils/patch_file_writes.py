import builtins

original_open = open
memory_file_log = {}  # Stores in-memory written content

class InMemoryFileWriter:
    def __init__(self, path, mode, *args, **kwargs):
        self.path = path
        self.mode = mode
        self.content = ''
        self.closed = False

    def write(self, data):
        if self.closed:
            raise ValueError("Write to closed file.")
        self.content += data

    def writelines(self, lines):
        for line in lines:
            self.write(line)

    def close(self):
        memory_file_log[self.path] = self.content
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

def open_override(path, mode='r', *args, **kwargs):
    if 'w' in mode or 'a' in mode:
        print(f"[Redirected] Writing to '{path}' is blocked. Capturing in memory.")
        return InMemoryFileWriter(path, mode)
    return original_open(path, mode, *args, **kwargs)

# Activate the override
builtins.open = open_override

def get_memory_file_log():
    return memory_file_log
