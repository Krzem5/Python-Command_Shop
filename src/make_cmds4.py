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
        elif args[i][0]=='valF':
            cmd+='float '
        elif args[i][0]=='str':
            cmd+='%s '%(args[i][1])
    cmds={'structure':cmd[0:len(cmd)],'attributes':args}
    return cmds
def test_for_cmd(seq,cmds,callname):
    output=[]
    if not seq.startswith(callname):
        return None
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
                return None
            seq=seq[len(cmds['attributes'][i][1][index])+1:]
            output.append((cmds['attributes'][i][0],cmds['attributes'][i][1][index]))
        elif cmds['attributes'][i][0]=='str':
            if not seq.startswith(cmds['attributes'][i][1]):
                return None
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
                return None
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
                return None
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
                return None
            else:
                seq=seq[len(str(num_from_seq))+1:]
                output.append((cmds['attributes'][i][0],num_from_seq))
    return output
def function(cmd,attribute):
    function_file=attribute[len(attribute)-1][1]
    file=open('open_cmd.py','w')
    file_func=open(function_file,'r')
    for line in file_func:
        line=str(line)
        for num in range(len(cmd)):
            try:
                if cmd[num][0]=='str' or cmd[num][0]=='valS' or cmd[num][0]=='opt':
                    line=line.replace('###%s###'%(int(num+1)),('\''+cmd[num][1]+'\''))
                elif cmd[num][0]=='valN' or cmd[num][0]=='valF':
                    line=line.replace('###%s###'%(int(num+1)),(cmd[num][1]))
            except:
                pass
        file.write(line)
    file.close()
    file_func.close()
    import open_cmd
    
        
if __name__=='__main__':
    attributes_list=[('/receipe',('str','search','invalid option argument'),('opt',('category','name','expireDay'),'invalid option argument'),('valS','invalid string argument'),('function','recepie_search.txt')),\
                     ('/receipe',('str','make','invalid option argument'),('valS','invalid string argument'),('str','price','invalid string attribute'),('valF','0','1000000','invald float attribute'),\
                      ('str','category','invalid string argument'),('valS','invalid string argument'),('str','expireDay','invalid string argument'),('valS','invalid string argument'),('function','receipe_make.txt'))]
    for item in attributes_list:
        cmds=make_cmd(item[0],item)
        print(cmds['structure'])
        del cmds
    while True:
        cmd=input('>>>0.1.1 command maker 2017 make_cmds4.pyw>>>')
        end=False
        counter=0
        for x in range(len(attributes_list)):
            if not end:
                attributes=attributes_list[x]
                stat=test_for_cmd(cmd,make_cmd(attributes[0],attributes),attributes[0])
                if stat==None:
                    counter+=1
                else:
                    end=True
                    function(stat,attributes_list[x])
        if counter==len(attributes_list):
            print('Exception: invalid command')
