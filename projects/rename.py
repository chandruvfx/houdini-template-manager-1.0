import os 
a = r"D:\houdini_bundles\flames\flames_big\v001\img"

b =1
for i in os.listdir(a):
    old = os.path.join(a, i)
    new = os.path.join(a, f"flames_big_{str(b).zfill(3)}.jpg")
    # print(old, new)
    os.rename(old, new)
    b= b+1

