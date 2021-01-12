"""
valid attributes:

opt -->('opt',('XXX','YYY','ZZZ),'not valid selection')
str -->('str','XXX','not valid string')
val -->('val','FROM','TO','not valid number')

"""
def make_cmd(callname,args):
    cmd='%s '%(callname)
    for i in range(len(args)):
        if args[i][0]=='opt':
            cmd+='['
            for n in range(len(args[i][1])):
                if n==len(args[i][1])-1:
                    cmd+='%s'%(args[i][1][n])
                else:
                    cmd+='%s/'%(args[i][1][n])
            cmd+='] '
        elif args[i][0]=='val':
            cmd+='value '
        elif args[i][0]=='str':
            cmd+='%s '%(args[i][1])
    cmds={'structure':cmd[0:len(cmd)],'attributes':args}
    return cmds
def test_for_cmd(seq,cmds,callname):
    if not seq.startswith(callname):
        raise Exception("cmd %s is not reconiced"%(callname))
    seq=seq[len(callname)+1:]
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
                        index=n
            if cnt==3:
                raise Exception(cmds['attributes'][i][3])
            seq=seq[len(cmds['attributes'][i][1][index])+1:]
        elif cmds['attributes'][i][0]=='str':
            if not seq.startswith(cmds['attributes'][i][1]):
                raise Exception(cmds['attributes'][i][3])
            else:
                seq=seq[len(cmds['attributes'][i][1])+1:]
        elif cmds['attributes'][i][0]=='val':
            num=seq
            num.split()
            num_from_seq=num[0]
            del num
            if not int(cmds['attributes'][i][2])>int(num_from_seq)>int(cmds['attributes'][i][1]):
                raise Exception(cmds['attributes'][i][4])
            else:
                seq=seq[len(str(num_from_seq))+1:]
    return True
if __name__=='__main__':
    file=open(input('>>>'),'r')
    callname,attributes=None,None
    for line in file:
        if callname==None:
            callname=line[0:len(line)-1]
        else:
            attributes=line
    make_cmd(callname,attributes)
    print('\n\n\n')
    print(test_for_cmd(input('>>>0.0.1 command maker 2017 make_cmds.pyw>>>'),make_cmd(callname,attributes),callname))
