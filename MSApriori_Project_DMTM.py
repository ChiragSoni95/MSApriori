import re
import itertools
allsets=[]
MISsorteditems=[]
MISsorted={}
countofitem=[]
countofcandidates={}
supportitem={}
L=[]
M=[]
Fk1=[]
finalsetF=[]
MIS={}
MIS1={}
T=[]
T1=[]
cbt=[]
cannot_be_together=[]
cannot_be_together1=[]
must_have=[]
must_have1=[]

count=dict()
count1=dict()

with open( 'parameterfile.txt' ) as param:
    content = param.readlines()
    # print content
    length = len( content ) - 3  # leaving sdc,cannot_be_together and _must_have constraints;save MIS key value pairs
    i = 0
    for i in range( length ):
        v = lambda x: x.strip()  # declaring a function to strip i.e removing leading and trailing spaces
        # here first map function runs oveer the iterator where the first item of the set is splited over the delimeter "="


        # splits individual element that stores first part in array at pos[0] of indivitems using list.
        # subsequently,then it maps the function where it is stripped to delete the white space at the start and end of first element
        indivitems = list( map( v, content[i].split( " = " ) ) )
        #print indivitems

        # Now, we need to obtain the MIS numeric value from the indivitems[0] and so on
        # we will be using search function
        # it will search for pattern MIS>>escaping brackets>>matching one or more word/number>>escaping brackets

        # lookup = re.search(r'MIS\(?(\w+)\)?', indivitems[0])

        lookup = re.search( r'\((.*?)\)', indivitems[0] )  # r denotes it will be given a regular expression

        # now group method will match the last pattern of the lookup value
        keyofMIS = lookup.group( 1 )
        # print keyofMIS

        # this means that the MIS value stored in index[1] of indivitems array is mapped to corresponding key i.e item
        MIS1[keyofMIS] = indivitems[1]
        MIS=MIS1
        #print MIS
        # print MIS
        #print type( MIS ) is dict
    temp = list( map( v, content[i + 1].split( " = " ) ) )  # start from index i+1,i is the last MIS key value pair
    sdc = float( temp[1] )
    # print sdc

    temp = list( map( v, content[i + 2].split( ": " ) ) )
    #print("temp after cannot be together" ,temp)
    for item in range(temp[1:][0].count('{')):
        if item == 0:
            l1=temp[1:][0]
        #print "l1=",l1
        m1 = l1.index( "{" )
        m2 = l1.index( "}" )
        #print "m1", m1
        #print "m2", m2
        line1=l1[m1+1 : m2]
        line2 = line1.split( ", " )
        l1 = l1[m2+1:]
        cbt.append(line2)

    #cannot_be_together1 = list( map( lambda x: map(str, list( x )), [ eval( temp[1] ) ] ) )[0]
    cannot_be_together=cbt
    #print (cannot_be_together)

    temp = list( map( v, content[i + 3].split( ": " ) ) )
    must_have1 = temp[1].split( " or " )
    must_have=must_have1
    # print must_have


with open( "inputdata.txt" ) as temp1:
    for line in temp1:
        l = list(
            line )  # this will represent the input line of transactions containing items as a single item sepereated by "," as a seperate entity
        m1 = l.index( "{" )
        m2 = l.index( "}" )
        line = line[m1 + 1:m2]
        line2 = line.split( ", " )  # each item in one sequence is stored in a list
        T1.append( line2 )
        T=T1
    #print T

#T=[{'20','30','80','70','50','90'},{'20','10','80','70'},{'10', '20', '80'},{'20', '30', '80'},{'20', '80'},{'20', '30', '80', '70', '50', '90', '100', '120', '140'}]

#MIS={'10':0.43,'20':0.30,'30':0.30,'40':0.40,'50':0.40,'60':0.30,'70':0.20,'80':0.20,'90':0.20,'100':0.10,'120':0.20,'140':0.15}

#sdc=0.1

#cannot_be_together= [{'20', '40'}]

#must_have= ['50','80','70','10','20','30','100']

def init_func():
    uniquesets=[]
    n=len(T)
    for transaction in T:
        for item in transaction:
            allsets.append(item)
            if item not in uniquesets:
                uniquesets.append(item)
    for item in uniquesets:
        countofitem = allsets.count(item)
        support= round(float(countofitem)/n,2)
        supportitem[item]=support
    #print(supportitem)
    #print "uniquesets=", uniquesets
    #print "allsets=",allsets
    #print type( supportitem )
    #print type( MISsorted )
    f = ''
    for value in M:

        #print "supportcount=", supportitem
        #print "MISsorted=", MISsorted
        if supportitem[value]>= MISsorted[value]:
            #print(MISsorted[value])
            #print "hi"
            L.append(value)
            f = value
            break
#here check whether the value is there in transaction ,because value might be having MIS Value but not in transaction
    for value in M:
        if (value in uniquesets and supportitem[value]>= MISsorted[f] and value!=f):
            L.append(value)
    #print "M=",M
    return L


def findsubsets(biglist,m):
    return set( itertools.combinations( biglist, m ) )

def MScandidate_gen(f,phi):
    tempCk=[]
    Ck=[]
    #joining step
    #lenf=len(f)
    #print "fhi=",f
    for i in range(len(f)):
        #print "hi"
        for j in range(i+1,len(f)):
            #print "hi1"
            first=f[i]
            second=f[j]
            #print first,second
            lenf1 = len( first ) - 1
            lenf2 = len( second ) - 1
            #print "first=",first
            #print "second=",second

            #print "-1=",second[-1]
            if first[:lenf1] == second[:lenf2] and MISsorted[first[-1]] <= MISsorted[second[-1]] and abs( supportitem[first[-1]] - supportitem[second[-1]] )<=phi:
                #print "hello"
                temp= first+ [second[-1]]
                tempCk.append(temp)
                #print "hELLO",tempCk
    for k in tempCk:
        #print k
        lenk = len( k ) - 1
        subset = findsubsets( k, lenk )
        #print subset
        for j in subset:
            j1=list(j)
            #print j1
            #print j1
            #print tempCk
            if k[0] in j or MISsorted[k[0]]==MISsorted[k[1]]:
                #print "hi"
                if j1 not in f:
                    tempCk.remove(k)

    #print "CSCGHDSCDSJCJCH",tempCk
    #print Ck
    return tempCk


def level_2_candidate_generation(L,phi):
    listC2 = []
    #print "l=",L
    for l in L:
            #print "nopoftrnsaction=",len(T)
            #print "support=",supportitem[l]
            #print "MIS=",MISsorted[l]
            #print "Hi"
            #print "support of 43:",supportitem['43']
            #print "support of 5:",supportitem['5']
            #print "mis OF 43:",MISsorted['8']
            if (supportitem[l] >= MISsorted[l]):
                #print supportitem[l]
                #print L.index(l)+1
                #temp1=[]
                p=L.index(l)
                temp1=L[p+1:len(L)]
                #print temp1

                for second_item in temp1:
                    #print "second item:", second_item
                    #print L[second_item]
                    #print "hi"
                    #print "suuport of second=",supportitem[second_item]
                    #print supportitem['120']
                    if (supportitem[second_item] >= MISsorted[l]) and (abs( supportitem[second_item] - supportitem[l] ) <= phi):
                        temp=[l,second_item]
                        #print temp
                        listC2.append(temp)
    #print "Candidate2",listC2
    return listC2


def contain(c,t):
    #print "passed c",c
    c1=set(c)
    if c1.issubset(t):
       return True
    else:
       return False

def apply_all_constraints(finalsetF,cannot_be_together,must_have):
    #print "finalsetFbeforeconstraints=",finalsetF
    fset=[]
    #print cannot_be_together
    #print type(cannot_be_together)
    for item in finalsetF:

        status=False
        for item2 in cannot_be_together:
            #print set( item2 ).issubset( set( item ) ), item2, 'yolo' , (item)
            if set(item2).issubset(set(item)):
                status=True
                break
        if(not status):
            fset.append(item)
    #print fset




    """       fset.append(item)
        else:
            for item2 in cannot_be_together:
                                #print item2
                                if len(item2)>=2:
                                    status=True
                                    item11 = set( item )
                                    #print "item11=",item11
                                    item22 = set( item2 )
                                    #print "item22=",item22
                                    if item11.issubset( item22 ):
                                        #print item
                                        status=False
                                        break
                                else:
                                    status = True
                                    item11 = set( item )
                                    # print "item11=",item11
                                    item22 = set( item2 )
                                    # print "item22=",item22
                                    if item22.issubset( item11 ):
                                        # print item
                                        status = False
                                        break


            #print(status)
            if status:
                fset.append(item)
    #print fset
    """
    #print must_have
    finalsetF1=[]
    for item1 in itertools.chain( fset ):
        status=False
        for item2 in must_have:
            if len(item1)==1 and item1==item2:
                status=True
            else:
                if item2 in item1:
                    status=True
        if status:
            finalsetF1.append(item1)

    #print finalsetF1
    return finalsetF1
""""
def tail_count(result,T):

    count=dict()

    for items in T:
        for item in result:
            lenitem=len(item)
            if lenitem==1:
                continue
            if lenitem!=1:
                tempitemset=item[1:]
                #print item[1:]
                #print "hi"
                tempitemset=set(tempitemset)
                #print tempitemset
                if tempitemset.issubset(items):
                    tempitemset1=''.join(tempitemset)
                    count[tempitemset1]=count.get(tempitemset1,0)+1
    #print count
    #print ('Tail count for itemset', count.values())
    #print "tailcount of uniquesets excluding first item in the set",count
"""

def find_count(row,T):
	countofitem = 0
	for i in T:
		for j in row:
			if j not in i:
				break
		else:
			countofitem = countofitem+1
	return countofitem


MISsorteditems = sorted( MIS.items(), key=lambda x: x[1] )
for a,b in MISsorteditems:
        M.append(a)

MISsorted=dict(MISsorteditems)

for key,value in MISsorted.iteritems():
    MISsorted[key] = float(value)

#print(MISsorted)
#print(MISsorted)
#print ("M=",M)
#print type( M )
L=init_func()
#print "List L:" ,L
#print "count of L:",len(L)

for item in L:
    if supportitem[item]>= MISsorted[item]:
        Fk1.append([item])
for item in Fk1:
    finalsetF.append(item)
#print finalsetF
#print F[1]
#level_2_candidate_generation( L, sdc )
#MScandidate_gen(F[k-1],sdc)
#print "Fk1=",Fk1

k=2
while(len(Fk1)!=0):
    F=[]
    if k==2:
        Ck=level_2_candidate_generation(L,sdc)
        #print "Ck=", Ck
    else:
        Ck=MScandidate_gen(Fk1,sdc)
        #Ck=[x for x in Ck if x not in "[]"]



    for t in T:
        for c in Ck:
            if contain(c,t):
                # count dictionary needs string as its key
                str1 = ','.join( c )
                count[str1]=count.get(str1,0)+1
            if contain(c[1:],t):
                str2 = ','.join(c[1:])
                count[str2]=count.get(str2,0)+1

    #print count
    for c in Ck:
        #print "c=",c
        str=','.join(c)
        #print "s=",str
        count[str]=count.get(str,0)
        #print "count of s =",count[str]
        supcount=float(count[str])/len(T)
        first=c[0]
        #print "first=",first

        if supcount >= MISsorted[first]:
            F.append(c)
    #print "first=",F
    for item in F:
        finalsetF.append(item)
    Fk1=F
    #print "Frequent after loop=",Fk1
    k=k+1

#print "FrequentItemSetList:",finalsetF

result=apply_all_constraints(finalsetF,cannot_be_together,must_have)
#print "result=",result

#print "Frequent item sets after cannot_be and must_have",result


#print count
length = 0
size = 0
for row in result:

    if len(row) > length:
        if size>0:
            print '\n\tTotal number of frequent %d-itemsets = %d\n\n' % (length, size)
            #print size
        size = 0
        length +=1
        print 'Frequent %d-uniquesets \n' % length
        #print "\n\n\nstart of"
        #print length
    size +=1
    set = ",".join( row )
    j_output = "{" + set + "}"
    print '\t%d : %s' % (find_count( row, T ), j_output)
    if len(row)>1:
        a = ",".join(row[1:])
        print "Tail count = ",find_count( row[1:], T )
print '\n\tTotal number of frequent %d-itemsets = %d\n\n' % (length, size)



















