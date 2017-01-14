import nltk
import glob
import os

def get_text(filename):
	file_content = open(filename).read()
	tokens = nltk.word_tokenize(file_content)
	#print tokens
	
	if not os.path.exists("Corpus having Tokens"):
	    os.makedirs("Corpus having Tokens")
	file_name = filename.split('\\')[1].split('.')[0]
	print file_name
	file = open('Corpus having Tokens/%s'%file_name+'.txt','w')
	for every in tokens:
		if every not in ('<', '>', 'html','pre','/pre','/html',':','$','{','^','#','@','&',')','*','=','|','[',']','(','-','?','!','.','}','/','`',"''",'``',"'",'%'':',',',';',):
			file.writelines(every.encode('utf-8').lower()+'\n')	

####################################################################
########  the files are picked up from the folder named Corpus  ####
def main():
	for filename in glob.glob('CACM-corpus\*.html'):
		get_text(filename)

main()