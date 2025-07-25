import os

# Download the static image from the local web folder
def fixed_download():
    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       'OnWeb', 'img.png')
    dst = 'img.png'

    if not os.path.exists(src):
        print('img.png not found in OnWeb directory')
        return False

    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        fdst.write(fsrc.read())
    print("FIXED DOWNLOADED")
    return True
