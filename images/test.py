import numpy as np

x = np.array([np.zeros((3, 3)) for x in range(9)])
y = np.copy(x)
temp_blocks = np.zeros((3, 3))
#print(temp_blocks)
indices = np.where(temp_blocks == 0)
for block in x:
    block[0, 2] = 1
    block[1,1] = 1
    block[1,2] = 1
    #print(block.trace())
for block in x:
    for id in range(0,3):
        continue
        #print(block[:, id][block[:,id] == 1].sum())

a = x[1]
print(a.all(a==0))
# b=np.diag(a[::-1])
# print(b[b==1].sum())
