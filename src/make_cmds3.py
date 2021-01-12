"""
valid attributes:

opt -->('opt',('XXX','YYY','ZZZ),'not valid selection')
str -->('str','XXX','not valid string')
valN -->('valI','FROM','TO','not valid number')
valS -->('valS','not valid string')
valF -->('valF','FROM','TO','not valid float')

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
        elif args[i][0]=='valN':
            cmd+='value '
        elif args[i][0]=='valS':
            cmd+='string '
        elif args[i][0]=='str':
            cmd+='%s '%(args[i][1])
    cmds={'structure':cmd[0:len(cmd)],'attributes':args}
    return cmds
def test_for_cmd(seq,cmds,callname):
    output=[]
    if not seq.startswith(callname):
        raise Exception("cmd %s is not reconiced"%(seq.split()[0]))
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
            if cnt==len(cmds['attributes'][i][1]):
                raise Exception(cmds['attributes'][i][2])
            seq=seq[len(cmds['attributes'][i][1][index])+1:]
            output.append((cmds['attributes'][i][0],cmds['attributes'][i][1][index]))
        elif cmds['attributes'][i][0]=='str':
            if not seq.startswith(cmds['attributes'][i][1]):
                raise Exception(cmds['attributes'][i][2])
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
                raise Exception(cmds['attributes'][i][3])
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
                raise Exception(cmds['attributes'][i][1])
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
                raise Exception(cmds['attributes'][i][3])
            else:
                seq=seq[len(str(num_from_seq))+1:]
                output.append((cmds['attributes'][i][0],num_from_seq))
    return output
if __name__=='__main__':
    attributes=('/recepie',('opt',('search','make'),'invalid selection argument'),('valS','invalid string argument'),('str','coast','invalid string argument'),('valF','0','11','invalid number argument'))
    print(test_for_cmd(input('>>>0.1.1 command maker 2017 make_cmds3.pyw>>>'),make_cmd(attributes[0],attributes),attributes[0]))
