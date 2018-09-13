def Xor(start,key,length):
	print("[*] XOR start: {}".format(hex(start)))
	for ptr in range(start, start+length, 8): 
	    PatchQword(ptr, Qword(ptr) ^ key);
	Message("[*] XOR done :)\n")
