import os, random, sys
n=0
random.seed()
print(str(sys.path[0]) + '\DispPics')
for root, dirs, files in os.walk(str(sys.path[0])+ '\DispPics'):
  for name in files:
    n += 1
    if random.uniform(0, n) < 1:
        rfile=os.path.join(root, name)
print(rfile)