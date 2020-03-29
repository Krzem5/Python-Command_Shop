def command(seq,cmds):
	"""

-> LIST:thing1|thing2|thing3 etc.
-> INT:min range,max range
-> FLOAT:min range,max range
-> NUMBER:min range,max range
-> string
"""
	def number(seq):
		dot=False
		if seq.startswith("-"):seq=seq[1:]
		for char in seq:
			if not (char in list("0123456789") or (char=="." and not dot)):
				return -1
			if char==".":dot=True
		if dot:return 0
		return 1
	if seq.startswith("/"):seq=seq[1:]
	seq=seq.split(" ")
	if type(cmds)==dict:cmd=cmds[seq[0]]
	else:cmd=cmds
	seq=" ".join(seq[1:])
	if not seq.endswith(" "):seq+=" ";aes=True
	else:aes=False
	o=[]
	sqi=0
	while True:
		if sqi==len(cmd.split(";")):break
		sq=cmd.split(";")[sqi]
		sqi+=1
		if sq.startswith("LIST:"):
			s=-1
			for k in sq[5:].split("|"):
				if seq.startswith(k+" "):
					 seq=seq[len(k+" "):]
					 s=sq[5:].split("|").index(k)
					 break
			if s==-1:return Exception(f"\'{seq.split(' ')[0]}\' is not in list {sq[5:].split('|')}")
			o+=[(s,k)]
		elif sq.startswith("INT:"):
			s=seq.split(" ")[0]
			if s!="" and number(s)==1:
				s=int(s)
				if s<int(sq[4:].split(",")[0]) or s>int(sq[4:].split(",")[1]):
					return Exception(f"{s} is smaller than {sq[4:].split(',')[0]} or bigger than {sq[4:].split(',')[1]}")
				o+=[s]
				seq=seq[len(s+" "):]
			else:return Exception(f"\'{s}\' is not an intiger")
		elif sq.startswith("FLOAT:"):
			s=seq.split(" ")[0]
			if s!="" and number(s)==0:
				s=float(s)
				if s<float(sq[6:].split(",")[0]) or s>float(sq[6:].split(",")[1]):
					return Exception(f"{s} is smaller than {sq[6:].split(',')[0]} or bigger than {sq[6:].split(',')[1]}")
				o+=[s]
				seq=seq[len(s+" "):]
			else:return Exception(f"\'{s}\' is not a float")
		elif sq.startswith("NUMBER:"):
			s=seq.split(" ")[0]
			if s!="" and number(s)>-1:
				s=float(s)
				if s<float(sq[7:].split(",")[0]) or s>float(sq[7:].split(",")[1]):
					return Exception(f"{s} is smaller than {sq[7:].split(',')[0]} or bigger than {sq[7:].split(',')[1]}")
				o+=[s]
				seq=seq[len(s+" "):]
			else:return Exception(f"\'{s}\' is not a number")
		else:
			if not seq.startswith(sq+" "):
				return Exception(f"\'{seq.split(' ')[0]}\' is not the same string as \'{sq}\'")
			seq=seq[len(sq+" "):]
	if aes:seq=seq[:-1]
	if seq!="":return Exception(f"\'{seq}\' is not matching \'\'")
	return o
if __name__=="__main__":
	COMMANDS={"maks":"LIST:very_good|good|ok|bad|very_bad"}
	print(command("/maks very_good",COMMANDS))