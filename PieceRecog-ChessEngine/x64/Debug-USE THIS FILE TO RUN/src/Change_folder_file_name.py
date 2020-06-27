import os
import re


path = 'D:\\WORKSTUFFS\\Tasks\\BR223_R9.3\\CTC_440\\premium_c_star3\\FUSA\\Remote_Piloted'
module = 'SM_Park'

if __name__ == "__main__":
    for (root,dirs,files) in os.walk(path, topdown=True):
        for i in range(len(files)):
            print(i)
            try:
                # print(re.findall(r'(.*)\.mf4',files[i])[0]+"_SM_Park.mf4")
                # print("_SM_Park".join(re.findall(r'(.*)\.mf4',files[i])[0]))
                if files[i] == (re.findall(r'.*\.mf4',files[i])[0]):
                    # print (root)
                    # print (files[i])
                    os.rename((os.path.join(root, files[i])),(os.path.join(root, re.findall(r'(.*)\.mf4',files[i])[0]+"_{}.mf4".format(module))))
                    print ('--------------------------------')
            except:
                print("nothing")