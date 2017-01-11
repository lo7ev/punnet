#genes
first_gene = input("Enter first genotype:\n")
second_gene = input("Enter second genotype:\n")

#epistasis
if input("Are there any epistasis?(y/n)\n")=='y':
	if input("Dominant or recessive?(D/r)\n")=='D':
		epistasis = input("Enter epistasis gene name(A,B,C...):\n")
		etype='D'
	else:
		epistasis = input("Enter epistasis gene name(a,b,c...):\n")
		etype='r'
else:
	epistasis = None

#Incomplete dominance
if input("Are there any incomplete dominance?(y/n):\n")=='y':
	incomplete_gene = input("What genes have incomplete dominance?(Aa,Bb,AaBb):\n")	
else:
	incomplete_gene = None

#gomets
def gomets(gene):
	list=[]
	for i in range(2):
		for j in range(2,4):
			list.append(gene[i]+gene[j])
	return list		

#add to dicionary
def add(dict, key):
	if key in dict:
		dict[key]+=1
	else:
		dict[key]=1
	return dict
	
#simple phenotypes
def phens(phenotypes, key):
	if 97 <= ord(key[0]) <= 122 and 97 <= ord(key[2]) <= 122:
		temp = table[i][j]
		phenotypes = add(phenotypes, temp)	
						
	if 65 <= ord(key[0]) <= 90 and 97 <= ord(key[2]) <= 122:
		temp = table[i][j][0] + '-' + table[i][j][2:4]
		phenotypes = add(phenotypes, temp)
	
	if 97 <= ord(key[0]) <= 122 and 65 <= ord(key[2]) <= 90:			
		temp=table[i][j][:2] + table[i][j][2] + '-'
		phenotypes = add(phenotypes, temp)		
	
	if 65 <= ord(key[0]) <= 90 and 65 <= ord(key[2]) <= 90:			
		temp = table[i][j][0] + '-' + table[i][j][2] + '-'
		phenotypes = add(phenotypes, temp)
	return phenotypes

#incomplete phens adding
def in_add(dict, key, position):
	if 65 <= ord(key[position]) <= 90:
		if position == 2:	
			temp = key[0:2] + key[position] +'-'
		else:
			temp = key[position] + '-' + key[2:4]
		dict = add(dict, temp) 
	else:	
		dict = add(dict, key)
	return dict
	
#incomplete phenotypes
def inphens(phenotypes, key, incomp):
	if incomp!=None:
		length = len(incomp)
		if length == 4:
			phenotypes = add(phenotypes, key)
		elif length == 2:
			if key[:2] == incomp:
				phenotypes = in_add(phenotypes, key, 2)
			elif key[2:4]==incomp:
				phenotypes = in_add(phenotypes, key, 0)
			else:
				if key[0] == incomp[0]:
					phenotypes = in_add(phenotypes, key, 2)
				elif key[2] == incomp[0]:
					phenotypes = in_add(phenotypes, key, 0)
				else:
					phenotypes = phens(phenotypes, key)			
	else:
		phenotypes = phens(phenotypes, key)
	return phenotypes

#list of gomets
first_gom = gomets(first_gene)
second_gom = gomets(second_gene)

#output information
table = []
genotypes={}
phenotypes={}

#fill table headings
for i in range(5):
	table.append([])
	if i == 0:
		table[0].append('_X_')
	else:
		table[0].append('_'+first_gom[i-1]+'_')
		table[i].append('_'+second_gom[i-1]+'_')
#fill table
for i in range(1,5):
	#fill the table
	for j in range(1,5):
		if 65 <= ord(table[0][j][1]) <= 90 and 65 <= ord(table[0][j][2]) <= 90:
			table[i].append(table[0][j][1] + table[i][0][1] + table[0][j][2] + table[i][0][2])
		elif 65 <= ord(table[0][j][1]) <= 90 and 97 <= ord(table[0][j][2])  <= 122:
			table[i].append(table[0][j][1] + table[i][0][1] + table[i][0][2] + table[0][j][2])
		elif 97 <= ord(table[0][j][1]) <= 122 and 65 <= ord(table[0][j][2]) <= 90:
			table[i].append(table[i][0][1] + table[0][j][1] + table[0][j][2] + table[i][0][2])
		else:
			table[i].append(table[i][0][1] + table[0][j][1] + table[i][0][2] + table[0][j][2])
		current = table[i][j]
		#count genotypes
		genotypes = add(genotypes, current)	
		
		#count phenotypes
		if epistasis!=None:
			#Dominant epistasis
			if etype=='D':
				if current[0]==epistasis:
					temp = epistasis + '-'*3
					phenotypes = add(phenotypes, temp)	
				elif current[2]==epistasis:
					temp = '-'*2 + epistasis + '-'
					phenotypes = add(phenotypes, temp)
				else:
					phenotypes = inphens(phenotypes, current, incomplete_gene)
			#recessive epistasis
			elif etype=='r':
				if current[0]==epistasis:
					temp = epistasis*2+'-'*2
					phenotypes = add(phenotypes, temp)
				elif current[2]==epistasis:
					temp = '-'*2 + epistasis*2
					phenotypes = add(phenotypes, temp)
				else:
					phenotypes = inphens(phenotypes, current, incomplete_gene)
		#if no epistasis
		else:
			phenotypes = inphens(phenotypes, current, incomplete_gene)
			
#output	
print()			 
for i in table:
	for j in i:
		print(j, end="  ")
	print("\n", end="")	
print()
print("Genotypes:")
for i in genotypes:
	print(i + ':' + str(genotypes[i]), end="  ")
print()
print("Phenotypes:")
for i in phenotypes:
	print(i + ':' + str(phenotypes[i]), end="  ")
print()
