def LengthFixer(String):
    
    spacerThing = ""
    if len(String)>49:
            return ('|'+String[:45]+'... '+'|')
    for i in range(1, int(50-len(String))):
        spacerThing +=" "
        if len(String+spacerThing)==49:
            return '|'+String+spacerThing+'|'
class Setup():
    def __init__(self):
        import os
        if os.sys.platform == 'win32':
            if os.sys.maxsize == 9223372036854775807:
                # Maximum positive integer on 64-bit systems
                FFMPEG_BIN="./ffmpeg/bin/win64/ffmpeg.exe" # Windows 64 bit
            elif os.sys.maxsize == 2147483647:
                # Maximum positive integer on 32-bit systems
                FFMPEG_BIN="./ffmpeg/bin/win32/ffmpeg.exe" # Windows 32 bit
            else:
                FFMPEG_BIN="./ffmpeg/bin/win32/ffmpeg.exe"
                # That's the same path as Windows 32 bit,
                # but I wanted it for code cleanliness
        elif 'linux' in os.sys.platform:
            if os.sys.maxsize == 9223372036854775807:
                # Maximum positive integer on 64-bit systems
                FFMPEG_BIN="./ffmpeg/bin/linux64/ffmpeg" # Linux 64 bit
            elif os.sys.maxsize == 2147483647:
                # Maximum positive integer on 32-bit systems
                FFMPEG_BIN="./ffmpeg/bin/linux32/ffmpeg" # Linux 32 bit
            else:
                FFMPEG_BIN="./ffmpeg/bin/linux32/ffmpeg"
                # That's the same path as Linux 32 bit,
                # but I wanted it for code cleanliness
        else:
            print(Helpers.LengthFixer("Your operating system isn't currently supported."))
            raise NotImplementedError
        self.FFMPEG_BIN = FFMPEG_BIN
    def FFMPEG(self):
        return self.FFMPEG_BIN
def GetFrame(Time, FFMPEG_BIN):
    # Video Imports
    import numpy
    import subprocess as sp

    pipe = sp.Popen([ FFMPEG_BIN,"-ss", Time,
                   "-i", "./Frozen/Frozen.mp4",
                   "-f", "image2pipe",
                   "-pix_fmt", "rgb24",
                   "-vcodec", "rawvideo", "-"],
                   stdin = sp.PIPE, stdout = sp.PIPE)
    raw_image = pipe.stdout.read(1920*856*3)
    image =  numpy.fromstring(raw_image, dtype='uint8').reshape((856,1920,3))
    pipe.stdout.close()
    return image

def ConvertToPNG(RAW_Data, PATH='./Image.png'):
    # Image Imports
    import PIL
    from PIL import Image

    numarr = RAW_Data.astype('uint8')
    img = Image.fromarray(numarr);

    img.save(PATH)
def UploadToImgur(PATH, clientId, clientSecret=None, imageTitle="Frozen Screen Grab", imageDescription=''):
    import pyimgur
    im = pyimgur.Imgur(clientId, clientSecret)
    up = im.upload_image(PATH, title=imageTitle, description=imageDescription)
    return up.link
    
