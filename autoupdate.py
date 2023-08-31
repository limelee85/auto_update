import os
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import datetime
import json
import re

path_public = os.getenv('PATH_PUBLIC')
version_path = os.getenv('PATH_VERSION')


def file_path_delete(prev_version,sub_path):

	check_str = ['-r ', '-rf ', '-f ', '..', '../', '\.\.', '\..', '.\.' , '*', '/bin', '/boot', '/dev', '/etc', '/home', '/root', '/usr', '/sys', '/var']
	warn = [s for s in check_str if s in prev_version]

	if (len(warn) > 0) :
		print('## Find Dangerous String ['+prev_version+'] : Skip Remove File')
	else : 
		#os.system('rm "'+path_public+sub_path+prev_version+'"')
		try :
			os.remove(path_public+sub_path+prev_version)
		except FileNotFoundError :
			print('## Not Fonud ['+prev_version+'] : Skip Remove File')
		# 20230831 version file is empty
		except IsADirectoryError :
			print('## Not Found ['+prev_version+'] : Skip Remove File')


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
	#	print(product_id)
			if (product_id == select) : 
				burp_version = i['Version']			
				return ['https://portswigger-cdn.net/burp/releases/download?product='+select+'&version='+burp_version+'&type=WindowsX64','burpsuite_'+select+'_windows-x64_v'+'_'.join(burp_version.split('.'))+'.exe']

# github download 20230731
def github_update(url,select):
	git_parse = json_parse(url)
	regex = re.compile(select)
	for i in git_parse['assets']:
		try :
			regex.match(i['name']).start() 
			return [i['browser_download_url'],i['name']]
		except AttributeError :
			continue

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
		elif (name.find("github") != -1) :
			# github download 20230731
			temp_result = github_update(url,select)
			parse = temp_result[0]
			version = temp_result[1]
			prev_version = prev_version_parse(version_file)
		elif (name == 'PickPick') :
			parse = parser(url,select)[0]['href']
			version = parse.split('/')[-1]+'#'+parse.split('/')[-2]
			prev_version = prev_version_parse(version_file)
		else :
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
update('WireShark','https://www.wireshark.org/download.html','#download-accordion > div:nth-child(1) > details > div > ul > li:nth-child(1) > a','wireshark_version','Network/')
update('Nmap','https://nmap.org/download','b > a','nmap_version','Network/')
update('Bitvise SSH Client','https://www.bitvise.com/ssh-client-download','#content > div','bitvise_version','')
update('DB Browser', 'https://sqlitebrowser.org/dl/','body > div > main > article > div > ul:nth-child(4) > li:nth-child(3) > a','dbbrowser_version','Editor')
update('Python','https://www.python.org/downloads/','#touchnav-wrapper > header > div > div.header-banner > div > div.download-os-windows > p > a','python_version','')
update('Sublime Text','https://www.sublimetext.com/download_thanks?target=win-x64','#direct-downloads > li:nth-child(1) > a:nth-child(1)','sublime_version','Editor/')
update('github_Apktool','https://api.github.com/repos/iBotPeaches/Apktool/releases/latest','apktool_[0-9.]+','apktool_version','Mobile/')
update('ADB', 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip','a','adb_version','Mobile/')
update('github_jadx','https://api.github.com/repos/skylot/jadx/releases/latest','jadx-gui-[0-9.]+-with-jre-win','jadx_version','Mobile/')
update('PickPick','https://picpick.net/download/kr/','#gatsby-focus-wrapper > div > div > div:nth-child(3) > div > p > a:nth-child(2)','pickpick_version','Editor/')

print('#############################################')
print('#                 Update End                #')
print('#############################################')
