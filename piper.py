# This file is part of Piper.
#
#    Piper is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Piper is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Piper.  If not, see <http://www.gnu.org/licenses/>.
#
# Piper Copyright (C) 2013  Christopher Cassano

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import qrcode
from Adafruit_Thermal import *



def print_keypair(pubkey, privkey):

#open the printer itself
    printer = Adafruit_Thermal("/dev/tty.usbserial-A9MXHFZB", 19200, timeout=5)
    #printer = Adafruit_Thermal("/dev/tty.usbmodem26221", 19200, timeout=5)


    finalImgName = "blankz.bmp"
    finalImgFolder = "./Images/"
    finalImg = Image.open(finalImgFolder + finalImgName)



    #---begin the public key qr code generation and drawing section---

    #we begin the QR code creation process
    #feel free to change the error correct level as you see fit
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )

    qr.add_data(pubkey)
    qr.make(fit=True)

    pubkeyImg = qr.make_image()

    #resize the qr code to match our design
    pubkeyImg = pubkeyImg.resize((175, 175), Image.NEAREST)

    font = ImageFont.truetype("UbuntuMono-R.ttf", 25)
    draw = ImageDraw.Draw(finalImg)

    # 110,38
    #startPos = (70, 38)
    startPos=(110,38)
    charDist = 15
    lineHeight = 23
    lastCharPos = 0

    keyLength = len(pubkey)

    while (keyLength % 17 != 0):
        pubkey += " "
        keyLength = len(pubkey)


    #draw 2 lines of 17 characters each.  keyLength always == 34 so keylength/17 == 2
    for x in range(0, keyLength / 17):
        lastCharPos = 0
        #print a line
        for y in range(0, 17):
            theChar = pubkey[(x * 17) + y]
            charSize = draw.textsize(theChar, font=font)

            #if y is 0 then this is the first run of this loop, and we should use startPos[0] for the x coordinate instead of the lastCharPos
            if y == 0:
                draw.text((startPos[0], startPos[1] + (lineHeight * x)), theChar, font=font, fill=(0, 0, 0))
                lastCharPos = startPos[0] + charSize[0] + (charDist - charSize[0])
            else:
                draw.text((lastCharPos, startPos[1] + (lineHeight * x)), theChar, font=font, fill=(0, 0, 0))
                lastCharPos = lastCharPos + charSize[0] + (charDist - charSize[0])


    #draw the QR code on the final image
    #150, text at 110, so offset txt/qrcode 40
    finalImg.paste(pubkeyImg, (150, 106))

    #---end the public key qr code generation and drawing section---





    #---begin the private key qr code generation and drawing section---

    #we begin the QR code creation process
    #feel free to change the error correct level as you see fit
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(privkey)
    qr.make(fit=True)

    privkeyImg = qr.make_image()

    #resize the qr code to match our design
    privkeyImg = privkeyImg.resize((220, 220), Image.NEAREST)

    #draw the QR code on the final image
    # 110 - 125 = offset of 15
    finalImg.paste(privkeyImg, (125, 560))

    startPos = (110, 807)
    charDist = 15
    lineHeight = 23
    lastCharPos = 0

    keyLength = len(privkey)

    while (keyLength % 17 != 0):
        privkey += " "
        keyLength = len(privkey)


    #draw 2 lines of 17 characters each.  keyLength always == 34 so keylength/17 == 2
    for x in range(0, keyLength / 17):
        lastCharPos = 0
        #print a line
        for y in range(0, 17):
            theChar = privkey[(x * 17) + y]
            charSize = draw.textsize(theChar, font=font)
            #print charSize
            if y == 0:
                draw.text((startPos[0], startPos[1] + (lineHeight * x)), theChar, font=font, fill=(0, 0, 0))
                lastCharPos = startPos[0] + charSize[0] + (charDist - charSize[0])
            else:
                draw.text((lastCharPos, startPos[1] + (lineHeight * x)), theChar, font=font, fill=(0, 0, 0))
                lastCharPos = lastCharPos + charSize[0] + (charDist - charSize[0])


    # Print the whole image
    printer.printImage(finalImg, True)

    printer.sleep()      # Tell printer to sleep
    printer.wake()       # Call wake() before printing again, even if reset
    printer.setDefault() # Restore printer to defaults



def genAndPrintKeys():

    #this actually generates the keys.  see the file genkeys.py or genkeys_forget.py
    import genkeys as btckeys

    btckeys.genKeys()

    if btckeys.keysAreValid == False:
        printer.write("Error: The generated keys (public/private) are not the correct length.  Please try again.")

    print_keypair(btckeys.pubkey, btckeys.privkey)



    #time.sleep(2)
    #printer.feed(3)


