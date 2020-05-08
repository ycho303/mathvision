from glob import glob
import os

for i in range(40):
    i += 1
    folder = 's'+ str(i)
    print(folder)
    [os.rename(f, "{}{}".format(folder+'_', f.replace("./att_faces/{}/".format(folder), ''))) for f in glob("./att_faces/{}/*.pgm".format(folder))]