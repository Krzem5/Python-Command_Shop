done=False
action=###1###
1_,2_,3_=###2###,###3###,###4###
d_=open('shop_d.txt','r')
d=d.read()
if action=='sell':d+='%s%s%s',%(1_,2_,3_)
elif action=='buy':for line in d_:if line.startswith(1_):d.replace(line,'')
d_.close()
file=open('shop_d.txt','w')
file.write(d)
file.close()

done=True