with open('sven_en_hyp.txt', 'r') as hyp, open('sven_en_ref.txt', 'r') as ref, open('i_hyp.txt', 'w') as out1, open('i_ref.txt', 'w') as out2:
    hyp=hyp.readlines()
    ref=ref.readlines()
    number=0
    for i,j in zip(hyp,ref):
        i=i.rstrip('\n') +' '+ '('+str(number)+')' +'\n'
        out1.write(i)
        j=j.rstrip('\n') +' '+ '('+str(number)+')' +'\n'
        out2.write(j)
        number+=1

