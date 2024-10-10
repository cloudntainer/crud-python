import psutil

memory = psutil.virtual_memory()
if memory.percent > 75:
    print(f"Warning: Memory usage is at {memory.percent}%")
else:
    print(f"Memory usage is within the threshold ({memory.percent}%)")
