import time


print "\033[s"


for i in range(100):
    print str(i) + "\033[u"
    time.sleep(1)
