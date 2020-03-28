"""
valid attributes:

opt_cmd -->('opt_cmd',{'XXX':{#cmd#,'YYY':#cmd#,'ZZZ':#cmd#},'not valid selection')
opt -->('opt',('XXX','YYY','ZZZ),'not valid selection')
str -->('str','XXX','not valid string')
valN -->('valN','FROM','TO','not valid number')
valS -->('valS','not valid string')
valF -->('valF','FROM','TO','not valid float')
function -->('function','FUNC-NAME.txt')

"""

def make_cmd(callname,args,skip=False):
	if not skip:cmd='%s '%(callname)
	else:cmd='['
	for i in range(len(args)):
		if args[i][0]=='opt':
			cmd+='['
			for n in range(len(args[i][1])):
				if n==len(args[i][1])-1:
					cmd+='%s'%(args[i][1][n])
				else:
					cmd+='%s;'%(args[i][1][n])
			cmd+=']'
		elif args[i][0]=='opt_cmd':
			cmd+='['
			for n in args[i][1]:
				cmd+='%s:%s;'%(n,make_cmd('',args[i][1][n][0],skip=True)['structure'])
			cmd+=']'
		elif args[i][0]=='valN':
			cmd+='value '
		elif args[i][0]=='valS':
			cmd+='string '
		elif args[i][0]=='valF':
			cmd+='float '
		elif args[i][0]=='str':
			cmd+='%s '%(args[i][1])
	if skip:cmd+=']'
	cmds={'structure':cmd[0:len(cmd)],'attributes':args}
	return cmds

def test_for_cmd(seq,cmds,callname,skip=False):
	output=[]
	if not skip and not seq.startswith(callname):return False,None
	if not skip:seq=seq[len(callname)+1:]
	for i in range(len(cmds['attributes'])):
		if cmds['attributes'][i][0]=='opt':
			exit_loop=False
			index=None
			cnt=0
			for n in range(len(cmds['attributes'][i][1])):
				if not exit_loop:
					if not seq.startswith(cmds['attributes'][i][1][n]):
						cnt+=1
					else:
						exit_loop=True
						index=n-1
			if cnt==len(cmds['attributes'][i][1]):
				return False,cmds['attributes'][i][2]
			seq=seq[len(cmds['attributes'][i][1][index])+1:]
			output.append((cmds['attributes'][i][0],cmds['attributes'][i][1][index]))
		elif cmds['attributes'][i][0]=='opt_cmd':
			exit_loop=False
			index=None
			cnt=0
			for n in cmds['attributes'][i][1]:
				if not exit_loop:
					if not seq.startswith(n):
						cnt+=1
					else:
						exit_loop=True
						index=len(n)-1
						n_=n
			if cnt==len(cmds['attributes'][i][1]):
				return False,cmds['attributes'][i][2]
			seq=seq[index+1:]
			output.append((cmds['attributes'][i][0],cmds['attributes'][i][1][n_]))
			exit_=False
			for itm in cmds['attributes'][i][1][n_]:
				if not exit_:
					optput_=test_for_cmd(seq,make_cmd('',itm,skip=True) ,'',skip=True)
					if output!=None:exit_=True
			if not exit_:return False,cmds['attributes'][i][2]  
			return True,output
		elif cmds['attributes'][i][0]=='str':
			if not seq.startswith((str(cmds['attributes'][i][1])+' ')):
				return False,cmds['attributes'][i][2]
			else:
				seq=seq[len(cmds['attributes'][i][1])+1:]
			output.append((cmds['attributes'][i][0],cmds['attributes'][i][1]))
		elif cmds['attributes'][i][0]=='valN':
			num=seq
			exit_loop=False
			num_from_seq=''
			for n in range(len(num)):
				if not exit_loop:
					if num[n]==' ':
						exit_loop=True
					else:
						num_from_seq+=num[n]
			del num
			if not int(cmds['attributes'][i][2])>int(num_from_seq)>int(cmds['attributes'][i][1]):
				return False,cmds['attributes'][i][3]
			else:
				seq=seq[len(str(num_from_seq))+1:]
				output.append((cmds['attributes'][i][0],num_from_seq))
		elif cmds['attributes'][i][0]=='valS':
			num=seq
			exit_loop=False
			string_from_seq=''
			for n in range(len(num)):
				if not exit_loop:
					if num[n]==' ':
						exit_loop=True
					else:
						string_from_seq+=num[n]
			del num
			if not str(string_from_seq):
				return False,cmds['attributes'][i][1]
			else:
				seq=seq[len(string_from_seq)+1:]
				output.append((cmds['attributes'][i][0],string_from_seq))
		elif cmds['attributes'][i][0]=='valF':
			num=seq
			exit_loop=False
			num_from_seq=''
			for n in range(len(num)):
				if not exit_loop:
					if num[n]==' ':
						exit_loop=True
					else:
						num_from_seq+=num[n]
			del num
			if not float(cmds['attributes'][i][2])>float(num_from_seq)>float(cmds['attributes'][i][1]):
				return False,cmds['attributes'][i]
			else:
				seq=seq[len(str(num_from_seq))+1:]
				output.append((cmds['attributes'][i][0],num_from_seq))
	return True,output

def function(cmd,attribute):
	function_file=attribute[len(attribute)-1][1]
	file=open('open_cmd.py','w')
	file_func=open(function_file,'r')
	file.write('done=False\n')
	for line in file_func:
		line=str(line)
		for num in range(len(cmd)):
			try:
				if cmd[num][0]=='str' or cmd[num][0]=='valS' or cmd[num][0]=='opt' or cmd[num][0]=='opt_cmd':
					line=line.replace('###%s###'%(int(num+1)),('\''+cmd[num][1]+'\''))
				elif cmd[num][0]=='valN' or cmd[num][0]=='valF':
					line=line.replace('###%s###'%(int(num+1)),(cmd[num][1]))
			except:
				pass
		file.write(line)
	file.write('done=True')
	file.close()
	file_func.close()
	import open_cmd
	while True:
		if open_cmd.done:
			break
	f=open('open_cmd.py','w')
	f.write('')
	f.close()
def Command(commands,input_):
	end=False
	counter=0
	for x in range(len(commands)):
		if not end:
			attributes=commands[x]
			stat,output=test_for_cmd(input_,make_cmd(attributes[0],attributes),attributes[0])
			if not stat:
				print(output)
			else:
				end=True
				if commands[x][int((len(commands[x])-1))][0]=='function':function(output,commands[x])
			return None
	if input_.startswith('/add'):
		input_=input_[5:]
		return input_
	if counter==len(commands):
		raise Exception('Inavlid command input')
	  
if __name__=='__main__':
	valid_commands=[('//shop',('opt_cmd',{'sell':[(('opt',('potatos','pumkins','melons','carrots'),'invalid item'),('valF',0.10,10000.0,'invalid price'),('valN',1,100,'invalid itm number'))],'buy':[(('opt',('potatos','pumkins','melons','carrots'),'invalid item'),('valN',0,100,'invalid itm number'))]},'invalid selection'),('function','shop.py'))]
	# print(make_cmd(valid_commands[0][0],valid_commands[0])['structure'],'\n')
	while True:
		cmd=input('>>> v2.3 command maker 2017 make_cmds6.pyw >>>')
		print(Command(valid_commands,cmd))
		# if inp!=None:valid_command.append(inp)
