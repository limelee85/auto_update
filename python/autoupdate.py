import os
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import datetime
import json

path_public = os.getenv('PATH_PUBLIC')
version_path = os.getenv('PATH_VERSION')


def file_path_delete(prev_version,sub_path):

	check_str = ['-r ', '-rf ', '-f ', '..', '../', '\.\.', '\..', '.\.' , '*']
	warn = 0
	for i in check_str:
		if (prev_version.find(i) != -1 ):
			warn = 1

	if (warn == 1) :
		print('## Find Dangerous String ['+prev_version+'] : Skip Remove File')
	else : 
		os.system('rm "'+path_public+sub_path+prev_version+'"')


def prev_version_parse(path):
	vf = open(version_path+path,'r')
	prev_version = vf.read().replace('\n', '')
	vf.close()
	return prev_version

def lastest_version_write(path, version):
	vf = open(version_path+path,'w')
	vf.write(version)
	vf.close()

def parser(url, select) :
	URL = url
	# 230707 : add allow_redirects option => adb 302 response
	v = requests.get(URL , allow_redirects=False)
	result = bs(v.text, 'html.parser')
	#print(result.select(select))
	return(result.select(select))

def json_parse(url):
	URL = url
	v = requests.get(URL)
	#print(json.loads(v.text)['ResultSet']['Results'][0]['builds'][0]['ProductId'])
	return(json.loads(v.text))
	


def burp_update(url,select):
	burp_parse = json_parse(url)
	# NEW 20230615 // 20230706 edit
	for j in burp_parse['ResultSet']['Results']:
	#burp_parse = burp_parse['ResultSet']['Results'][0]['builds']
		for i in j['builds'] :
        #for i in burp_parse :
			product_id = i['ProductId']
#		print(product_id)
			if (product_id == select) : 
				burp_version = i['Version']			
				return ['https://portswigger-cdn.net/burp/releases/download?product='+select+'&version='+burp_version+'&type=WindowsX64','burpsuite_'+select+'_windows-x64_v'+'_'.join(burp_version.split('.'))+'.exe']

	# OLD
	''' 
	product_id = burp_parse
	pi_path = ['ResultSet','Results',0,'builds',0,'ProductId']
	while (product_id != 'community'):
		product_id = burp_parse
		for i in pi_path :
			product_id = product_id[i]
		pi_path[2] = pi_path[2]+1
		#print(burp_parse['ResultSet']['Results'][0]['builds'])

	else :
		pi_path[2] = pi_path[2]-1
		pi_path[5] = 'Version'
		burp_version = burp_parse
		for i in pi_path :
			burp_version = burp_version[i]

		return ['https://portswigger-cdn.net/burp/releases/download?product='+select+'&version='+burp_version+'&type=WindowsX64','burpsuite_'+select+'_windows-x64_v'+'_'.join(burp_version.split('.'))+'.exe']
	'''

def update(name,url,select,version_file,sub_path) :

	try: 
		if (name == 'Burp Suite Pro' or name == 'Burp Suite Community'):
			temp_result = burp_update(url,select)
			parse = temp_result[0]
			version = temp_result[1]
			prev_version = prev_version_parse(version_file)
		elif (name == 'Bitvise SSH Client') :
			parse = parser(url,select)[0]
			parse = parse.find('a')['href']+'#'+parse.text.split(',')[0].split(':')[1].strip()
			version = parse.split('/')[-1]
			prev_version = prev_version_parse(version_file)
		elif (name != 'Burp Suite Pro') :
			parse = parser(url,select)[0]['href']
			version = parse.split('/')[-1]
			prev_version = prev_version_parse(version_file)



		if (version != prev_version) :
			## update
			print('# '+name+' Update '+prev_version+' to '+version)
			print('## Remove previous version')
			file_path_delete(prev_version,sub_path)
			print('## Download lastest version')
			os.system('wget -O '+path_public+sub_path+version.split('#')[0]+' "'+parse+'"')
			lastest_version_write(version_file,version)
			print('## Complete!')
		else :
			print('# '+name+' is latest version : Skip')
	except IndexError as e:
		print('# '+name+' occurs Error! : '+ str(e))


print('\n\n\n#############################################')
print('# Update Start : '+str(datetime.datetime.now())+' #')
print('#############################################')

update('Burp Suite Pro','https://portswigger.net/burp/releases/data?pageSize=2','pro','burppro_version','Proxy/')
update('Burp Suite Community','https://portswigger.net/burp/releases/data?pageSize=2','community','burpcom_version','Proxy/')
update('Python','https://www.python.org/downloads/','#touchnav-wrapper > header > div > div.header-banner > div > div.download-os-windows > p > a','python_version','')
update('Sublime Text','https://www.sublimetext.com/download_thanks?target=win-x64','#direct-downloads > li:nth-child(1) > a:nth-child(1)','sublime_version','')
update('WireShark','https://www.wireshark.org/download.html','#download-accordion > div:nth-child(1) > details > div > ul > li:nth-child(1) > a','wireshark_version','Network/')
update('Apktool','https://ibotpeaches.github.io/Apktool/install/','#navbar > ul > li:nth-child(7) > a','apktool_version','Mobile/')
update('Nmap','https://nmap.org/download','b > a','nmap_version','Network/')
update('Bitvise SSH Client','https://www.bitvise.com/ssh-client-download','#content > div','bitvise_version','')
update('DB Browser', 'https://sqlitebrowser.org/dl/','body > div > main > article > div > ul:nth-child(4) > li:nth-child(3) > a','dbbrowser_version','')
update('ADB', 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip','a','adb_version','Mobile/')

print('#############################################')
print('#                 Update End                #')
print('#############################################')

# jadx curl -s https://api.github.com/repos/skylot/jadx/releases/latest | grep "browser_download_url.*with-jre.*zip" | cut -d : -f 2,3 | tr -d \" | wget -i -
# frida server curl -s https://api.github.com/repos/frida/frida/releases/latest | grep "browser_download_url.*server.*android.*"
