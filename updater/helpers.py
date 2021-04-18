def saveToFile(fileName, strToSave):
	with open(fileName, 'w', encoding='utf-8') as fileS:
		fileS.write(strToSave)


def encode_if_necessary(b):
	if type(b) is bytes:
		return b.decode('utf8')
	return b

def chunker(seq, size):
	return (seq[pos:pos + size] for pos in range(0, len(seq), size))