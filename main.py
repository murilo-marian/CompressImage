def readImage(filepath):
    with open(filepath, "r") as image:
        image.readline().strip()
        
        line = image.readline().strip()
        
        width, height = map(int, line.split())
        bits = int(image.readline().strip())
        
        conteudo = image.read()
        numeros = conteudo.split()
        pixels = []
        row = []
        rgb = []
        for num in numeros:
            rgb.append(int(num))
            
            if len(rgb) == 3:
                row.append(rgb)
                rgb = []
            
            if len(row) == width: 
                pixels.append(row)
                row = []
        
    return pixels, bits, width, height

def readCompressedImage(filepath):
    with open(filepath, "r") as image:
        type = image.readline().strip()
        
        line = image.readline().strip()
        
        width, height = map(int, line.split())
        bits = int(image.readline().strip())
        
        conteudo = image.read()
        numeros = conteudo.split()
        decompressedSeparated = []
        mult = 1
        for num in numeros:
            if int(num) < 0:
                mult = -int(num)
                continue
            else:
                for i in range(mult):
                    decompressedSeparated.append(num)
        pixels = [[0 for _ in range(3)] for _ in range(width * height)]
        counter = 0
        rgbCounter = 0
        value = 0
        for value in decompressedSeparated:
            if counter == width * height:
                counter = 0
                rgbCounter += 1
            pixels[counter][rgbCounter] = value
            counter += 1
    return pixels, type, bits, width, height



def compress(pixels):
    prevValue = pixels[0][0][0]
    instance = 1
    compressed = []
    value = 0
    first = True
    for i in range(len(pixels[0][0])):
        for j in range(len(pixels)):
            for k in range(len(pixels[0])):
                if first:
                    first = False
                    continue
                
                value = pixels[j][k][i]
                
                if value == prevValue:
                    instance += 1
                    continue
                
                compressed.append(-instance)
                compressed.append(prevValue)
                prevValue = value
                instance = 1
    
    if instance != 1:
        compressed.append(-instance)
    compressed.append(value)
        
    return compressed

def decompress(compressedImage, newImageName):
    compressed, type, bits, width, height = readCompressedImage(compressedImage)
    with open(newImageName, "w") as decompressedImage:
        decompressedImage.write(type + "\n")
        decompressedImage.write(str(width) + " " + str(height) + "\n")
        decompressedImage.write(str(bits) + "\n")
        for i in compressed:
            decompressedImage.write((" ".join(map(str, i))))
            decompressedImage.write(" ")
        print("saved")

def saveIMG(filename, type, bits, pixels, width, height):
    with open(filename, "w") as newImage:
        newImage.write(type + "\n")
        newImage.write(str(width) + " " + str(height) + "\n")
        newImage.write(str(bits) + "\n")
        
        for row in pixels:
            newImage.write(str(row) + " ")
        print("saved")


img, bits, width, height = readImage("EntradaRGB.ppm")
compressed = compress(img)
saveIMG("teste.rle", "P3", bits, compressed, width, height)
decompress("teste.rle", "decompressed.ppm")