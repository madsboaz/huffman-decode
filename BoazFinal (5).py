#Madelyn Boaz
# Define Vertex class which represents a node in the Huffman Tree
class Vertex:
    def __init__(self,key):
        self.id = key  
        self.connectedTo = {}  
        self.letter = None  
        self.leftChild = None  
        self.rightChild = None  
        self.parent = None  
        self.payload = 0
        
    def addLeftChild(self, nbr):
        self.connectedTo[nbr] = 0  
        self.leftChild= nbr
        nbr.parent = self  
    
    def addRightChild(self, nbr):
        self.connectedTo[nbr] = 1  
        self.rightChild = nbr
        nbr.parent = self  
        
    def getConnections(self):
        return self.connectedTo.keys()  

    def getId(self):
        return self.id  

    def getWeight(self, nbr):
        return self.connectedTo[nbr]  
    
    def __str__(self):
        return str(self.id) + ' connectedTo: ' \
               + str([x.id for x in self.connectedTo])

# Function to create the Huffman Tree
def makeHuffman(freqDict):
    letterNode = {}  
    vCount = 0  
    v = []  

    # Create initial vertices for each character in the frequency dictionary
    for letter in freqDict:
        vertex = Vertex(vCount)
        vertex.letter = letter
        vertex.payload = freqDict[letter]
        letterNode[letter] = vertex
        v.append(vertex)
        vCount += 1

    
    while len(v) > 1:
        v.sort(key=lambda x: x.payload)  # Sort vertices payload
        v1 = v.pop(0)  #Remove first two and form new vertex
        v2 = v.pop(0)  
    
        new = Vertex(vCount + 1)
        new.addLeftChild(v1)  
        new.addRightChild(v2)  
        new.payload = v1.payload + v2.payload  
        v.append(new)  
        vCount += 1

    return v[0], letterNode  # Return the root of the Huffman Tree and the letterNode dictionary

# Function to decode a binary string using the Huffman Tree
def decode(string, root):
    vertex = root
    decodedMessage = ""
    
    for bit in string:
        if int(bit) == 0:
            vertex = vertex.leftChild  # Move to the left child if the bit is 0
        else:
            vertex = vertex.rightChild  # Move to the right child if the bit is 1
        
        if vertex.letter != None:  # If a leaf node is reached (vertex contains a letter)
            decodedMessage += vertex.letter  # Append the letter to the decoded message
            vertex = root  # Return to the root for the next sequence of bits

    return decodedMessage

# Function to encode a single letter using the Huffman Tree
def encode(letter, letterNode):
    string = ''
    vertex = letterNode[letter]
    
    while vertex.parent != None:  # Traverse from the letter node to the root
        string = str(vertex.parent.getWeight(vertex)) + string  
        vertex = vertex.parent  # Move to the parent vertex
        
    return string

# Function to encode a full message using the Huffman Tree
def encodeMessage(message, letterNode):
    return ''.join(encode(letter, letterNode) for letter in message)  # Encode each letter and concatenate the results

# Function to decode an encoded message
def decodeCode(encodedMessage, root):
    return decode(encodedMessage, root)  # Decode the encoded message using the Huffman Tree


# The string provided to form the frequency table
text = 'in a general sense cryptography is concerned with encrypting and decrypting information that you do not want other people to see'

# Create frequency table from the text
freq = {}  # Changed from using defaultdict to a simple dictionary
for char in text:
    if char in freq:
        freq[char] += 1
    else:
        freq[char] = 1

# Create the Huffman Tree and letterNode dictionary
root, letterNode = makeHuffman(freq)

# Demonstrate encoding a message
message = 'this is the way it is'
encodedMessage = encodeMessage(message, letterNode)
print(f"Encoded message: {encodedMessage}")

# Demonstrate decoding a message
encodedString = '1011000001110100001010000111111011111011110100001110001110100111011111001100110101111100110011101011101'
decodedMessage = decodeCode(encodedString, root)
print(f"Decoded message: {decodedMessage}")

# Huffman hash tables for reference
def huffmanHash(letterNode):
    letterTable = {}
    codeTable = {}
    for v in letterNode:
        letterTable[v] = encode(v, letterNode)
        codeTable[letterTable[v]] = v
    return letterTable, codeTable
