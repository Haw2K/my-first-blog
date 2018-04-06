from datetime import datetime
myFile = open('/home/deeplearning/djangogirls/blog/append.txt', 'a')
myFile.write('\nAccessed on ' + str(datetime.now()))