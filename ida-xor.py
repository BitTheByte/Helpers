#From :https://github.com/tq2ctf/writeups/tree/master/2018_06_23_GoogleCTF/keygenme

def XorData(start,key,length):
	print(f"[*] XOR start: {hex(start)}")
	for ptr in range(start, start+length, 8): 
	    PatchQword(ptr, Qword(ptr) ^ key);
	Message("[*] XOR done :)\n")
