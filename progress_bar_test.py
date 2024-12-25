import time
from progress.bar import IncrementalBar

lenght = 589

mylist = [1] * lenght

bar = IncrementalBar('Graphs', max = lenght)

for item in mylist:
    bar.next()
    time.sleep(0.01)

bar.finish()