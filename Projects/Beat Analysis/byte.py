import numpy as np

class NegativeIntegerWhenUnsigned(Exception):
    def __init__(self, message):
        self.message = message

class InvalidNumberOfIndexes(Exception):
    def __init__(self, message):
        self.message = "number of indexes of barr must always be divisible by 8"
        self.message += '\n'
        self.message += message

# class representing a bytearray in a touple
# contains methods to manipulate the binary data
class Byte:
    barr = ()
    byteOrder = 'little'
    signed = True
    bitLen = 0

    # constructor
    # barrLen is in bytes, must not be <= 0
    # if barrLen is 0, byteArray must be given in order to count it from its length
    # if byteArray is given, but barrLen isn't 0, don't overwrite barrLen
    # if byteArray is not given (None), ignore input dec and map bytearray (in int) to it instead
    def __init__(self, dec = 0, barrLen = 0, byteArray = None, byteorder='little', signed=True):
        self.byteOrder = byteorder
        self.signed = signed
        if byteArray != None:
            dec = int.from_bytes(byteArray, byteorder, signed=signed)
            if barrLen == 0:
                    barrLen = byteArray.__len__()
        self.bitLen = barrLen*8
        
        neg = False
        if dec < 0:
            if not signed:
                raise NegativeIntegerWhenUnsigned("")
            neg = True # set flag to indicate that dec is actually negative
        
        barrLen *= 8 # convert to bits from bytes
        dec = self.cropDec(dec, barrLen, signed)
        
        barr = [0 for i in range(barrLen)]
        dec = abs(dec) # make dec positive
        for i in range(barrLen):
            barr[-i-1] = dec%2
            dec //= 2
    
        if neg:
            barr = self.complementBarr(barr)
        if byteorder=='little':
            barr = self.changeByteOrderOfBarr(barr)

        self.barr = tuple (barr)

    # switch between little and big endian
    def changeByteOrderOfBarr (self, barr):
        length = barr.__len__()
        if length % 8 != 0:
            raise InvalidNumberOfIndexes("")
        length //= 8
        newBarr = [] 
        for byte in range(length-1, -1, -1):
            for bit in range(8):
                newBarr.append(barr[byte*8+bit])
        return newBarr

    # return the complement of barr
    # negates whole barr and adds 1
    def complementBarr(self, barr):
        length = barr.__len__() 
        newBarr = []
        # bitwise NOT
        for i in range(length):
            bit = 1 if barr[i] == 0 else 0
            newBarr.append(bit)
        # add 1
        for i in range(length):
            if newBarr[-1-i] == 0:
                newBarr[-1-i] = 1
                break
            newBarr[-1-i] = 0
        return newBarr

    # use barrToInt method to convert atribute barr of the class to int
    # with respect to byteOrder and signed attributes
    #
    # returns self.barr converted to int
    def toInt(self):
        return self.barrToInt(self.barr, self.byteOrder, self.signed)

    # converts a given barr to int
    # barr should have a length divisible by 8, otherwise you're risking InvalidNumberOfIndexes exception
    # assumes complement code for negative numbers
    def barrToInt(self, barr, byteOrder='little', signed=True):
        if byteOrder == 'little':
            barr = self.changeByteOrderOfBarr(barr)
        neg = False
        if signed and barr[0] == 1:
            neg = True
            barr = self.complementBarr(barr)
        length = barr.__len__()
        ans = 0
        k = 1
        for i in range(length):
            ans += barr[-1-i]*k
            k *= 2
        return ans if not neg else -ans
        
    # converts barr attribute of the class into bytearray
    # might raise InvalidNumberOfIndexes exception if length of barr is not divisible by 8 
    def toBytearray(self):
        length = self.barr.__len__()
        if length % 8 != 0:
            raise InvalidNumberOfIndexes("")
        length //= 8
        arrOfInt = []
        for byte in range(length):
            arrOfInt.append(self.barrToInt(self.barr[byte*8:byte*8+8], signed=False))
        return bytearray(arrOfInt)

    # multiplies self.barr by a coeficient (k)
    #
    # return new self.barr
    def multiplyBy(self, k):
        val = self.toInt()
        val *= k
        val = int (val)
        val = self.cropDec(val, self.bitLen, self.signed)
        newBarr = Byte(dec = val, barrLen = self.bitLen//8, byteorder = self.byteOrder, signed = self.signed)
        self.barr = newBarr.barr
        return self.barr

    # crops integer so it fits its barr of given bitLen
    # if bigger than maximum storable value is set to maximum storable value
    # if smaller than minimum storable value is set to minimum storable value
    #
    # return cropped integer
    def cropDec(self, dec, bitLen, signed = True):
        maxValue = (2**(bitLen-1)-1) if signed else (2**(bitLen)-1)
        minValue = -maxValue-1 if signed else 0
        if dec > maxValue:
            dec = maxValue
        if dec < minValue:
            dec = minValue
        return dec


# multiply a barr 'all_bytes' with a sample of given 'bitlen' by a float 'f'
def multiply(all_bytes, f, bitlen, signed=True): 
    # Works for 8, 16, 32 and 64 bit integers:
    dtype = "%sint%d" % ("" if signed else "u",   bitlen)
    max_value = 2 ** (bitlen- (1 if signed else 0)) - 1
    min_value = -max_value-1

    input_data = np.frombuffer(all_bytes, dtype=dtype)
    processed = np.clip(input_data * f, min_value, max_value)
    return bytes(processed.astype(dtype))
