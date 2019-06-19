#!/bin/python3
import os
import urllib
import configparser
import shutil
import glob
import re

from urllib import parse
from urllib import request
from ftplib import FTP
from packaging import version

class PyswordRepo():
    configuration = configparser.ConfigParser()
    BetaList = ["crosswire beta"]
    repoconfigname = ""
    swordpath = ""
    repo_gz = ""
    repo_dir = ""
    repo_path = ""
    pyrepo_list = ""
    master_repo_list_name = ""
    raw_repo_list = ""
    master_server = ""
    master_server_repo = ""
    timestamp_file_list = ""
    repoconfigname = ""
    configfile = ""
    tempdir = ""
    protocolstrings = { 'ftpsource':'ftp://', 'FTPSource':'ftp://' }
    pyrepo_outdated_list = ""
    betarepos = 'false'
    pymaster_list = ""


    languages = [
        'leu', 'nhu', 'sr', 'yap', 'mgc', 'ded', 'ycn', 'kmu', 'yre', 'agx_cyrl', 'gup', 'sgz', 'kmh', 'yut', 'mvn', 'ffm', 'maz',
        'pa', 'agm', 'huv', 'xtm', 'stp', 'box', 'yva', 'ktm', 'meq', 'myu', 'tl', 'poh', 'bjp', 'bao', 'tbo', 'quc', 'fi', 'rkb',
        'zad', 'zos', 'nog_cyrl', 'qve', 'xtd', 'tee', 'kon', 'bvd', 'txu', 'tuc', 'kk', 'mox', 'rmq', 'got', 'agt', 'blw', 'kbd',
        'bzh', 'pab', 'myw', 'ntp', 'mhl', 'pib', 'cap', 'vls', 'ce', 'hr', 'cmn', 'nhi', 'otq', 'cpb', 'aly', 'mib', 'guh', 'ubr',
        'mwc', 'nmw', 'ssx', 'alt', 'sn', 'dhg', 'qxo', 'cwe', 'bco', 'tgp', 'sey', 'kql', 'zpi', 'nn', 'bg', 'lin', 'ady_cyrl',
        'gym', 'bss', 'ho', 'tnk', 'mav', 'tbl', 'yby', 'grc', 'otm', 'npl', 'jae', 'usp', 'be', 'gum', 'tiy', 'nas', 'ro', 'upv',
        'xav', 'yuj', 'kwf', 'ata', 'dgr', 'lgl', 'tsw', 'gng', 'pls', 'bbb', 'pt', 'tav', 'mg', 'arl', 'ur_deva', 'cux', 'tte', 'sps',
        'tcs', 'nhy', 'mop', 'ino', 'ko', 'nif', 'hwc', 'xon', 'boj', 'hla', 'cac', 'zca', 'tnp', 'az', 'syr', 'adz', 'dgz', 'ssg', 'tna',
        'bnp', 'mpt', 'emp', 'crx', 'pri', 'dad', 'my', 'gag_latn', 'myk', 'ctu', 'uli', 'nb', 'mbs', 'aon', 'mxt', 'nou', 'blz', 'kpg',
        'yss', 'yad', 'srn', 'noa', 'ura', 'as', 'apz', 'eu', 'bua_cyrl', 'quh', 'wer', 'als', 'gvf', 'anv', 'jiv', 'ngu', 'big', 'zas',
        'aey', 'zlm', 'eri', 'geb', 'llg', 'hub', 'auy', 'kmr_latn', 'aui', 'fuh', 'atb', 'spy', 'kew', 'mxp', 'bbr', 'mlp', 'tpa', 'tfr',
        'daa', 'ken', 'nsn', 'bdd', 'bgs', 'aia', 'amp', 'kmg', 'cya', 'kyc', 'mit', 'mto', 'cui', 'arb', 'etr', 'ml', 'beu', 'nab', 'mcd',
        'fuf', 'gu', 'spp', 'gah', 'glk', 'con', 'cu', 'und', 'ape', 'cbu', 'nhg', 'cab', 'cav', 'qvc', 'ug', 'tbg', 'trc', 'ntj', 'nay',
        'msm', 'bn', 'ghs', 'zar', 'tue', 'poe', 'nuy', 'zat', 'kkl', 'ame', 'xla', 'ulk', 'zaw', 'tke', 'ncl', 'jic', 'qub', 'auc', 'acr',
        'klv', 'bps', 'soq', 'alq', 'aoi', 'maj', 'dar_cyrl', 'amr', 'es_minimumversion', 'hbo', 'caf', 'kap_cyrl', 'ht', 'atg', 'mux', 'hui',
        'kwj', 'nhe', 'zty', 'tlf', 'huu', 'mek', 'spm', 'jac', 'kpx', 'zaa', 'kqf', 'dwr', 'wbp', 'tr', 'ttc', 'tos', 'ksr', 'mcp', 'kue', 'ur',
        'cpa', 'aoj', 'hto', 'kgk', 'cco', 'bmu', 'tg', 'byx', 'hix', 'ka', 'kum', 'gdr', 'chq', 'nlg', 'guo', 'mwp', 'chk', 'qvh', 'gdn', 'gun',
        'kjh', 'qup', 'nbq', 'okv', 'dop', 'tif', 'zxx', 'rug', 'aso', 'yka', 'cta', 'tk_latn', 'top', 'mks', 'knf', 'dah', 'sbe', 'bzd', 'ese',
        'gof', 'ba_cyrl', 'aau', 'bkx', 'mgh', 'ote', 'sim', 'qxh', 'agd', 'cao', 'jvn', 'sq', 'tvk', 'apw', 'fr', 'djk', 'bpr', 'yml', 'aak',
        'bmh', 'bqc', 'nhr', 'kmr_cyrl', 'snn', 'shp', 'sus', 'nho', 'rwo', 'med', 'os', 'mbt', 'mkl', 'gwi', 'lac', 'wos', 'et', 'kqc', 'mqj',
        'maq', 'dww', 'wnu', 'pir', 'aer', 'bjr', 'tod', 'miz', 'for', 'too', 'plu', 'cs', 'de', 'nop', 'lzh', 'qvm', 'klt', 'tgo', 'cof', 'bch',
        'are', 'cso', 'arn', 'zpv', 'sml', 'wat', 'tku', 'bmk', 'te', 'kud', 'tpi', 'cut', 'zac', 'urt', 'msc', 'cjs_cyrl', 'sue', 'yaa', 'gnn',
        'ksd', 'azz', 'km', 'nca', 'gam', 'ubu', 'kaa_cyrl', 'wap', 'kpf', 'byr', 'kbc', 'ory', 'zsr', 'qvn', 'cpu', 'tzo', 'usa', 'bef', 'ipi',
        'apr', 'wsk', 'knv', 'kn', 'kaq', 'bba', 'tk_cyrl', 'ikk', 'hch', 'crh_cyrl', 'tzj', 'toj', 'urw', 'mlh', 'rmy', 'sja', 'lbb', 'zh', 'tuo',
        'tew', 'mph', 'ta', 'bkd', 'lif', 'kgf', 'heg', 'mva', 'cuc', 'msy', 'mbc', 'ckb', 'nin', 'mmo', 'kek', 'gai', 'zao', 'qvs', 'hop', 'omw',
        'gul', 'sua', 'cak', 'gvn', 'wmw', 'wmt', 'bsp', 'nd', 'id', 'nii', 'agu', 'ja', 'zab', 'abx', 'hvn', 'pes', 'th', 'att', 'mcf', 'roo', 'gez',
        'kms', 'gfk', 'mau', 'tpt', 'gvc', 'xsi', 'hus', 'xnn', 'kgp', 'far', 'sgb', 'tuf', 'amx', 'ixl', 'nss', 'hy', 'meu', 'cme', 'eko', 'uvl',
        'gui', 'kyz', 'kkc', 'tlh', 'cbr', 'snc', 'uk', 'sxb', 'nch', 'hi', 'gmv', 'rgu', 'cuk', 'sw', 'kyf', 'prf', 'bla', 'rop', 'tnc', 'cjv',
        'ky_cyrl', 'hlt', 'nwi', 'opm', 'ar', 'cv_cyrl', 'mpx', 'car', 'dgc', 'kbq', 'nak', 'quf', 'kpr', 'gaw', 'bus', 'cot', 'sri', 'mig', 'ru',
        'pio', 'mqb', 'mpm', 'kyg', 'swh', 'bzj', 'nvm', 'tnn', 'gd', 'ppo', 'ksj', 'kbh', 'am', 'vmy', 'taj', 'ake', 'azb', 'kje', 'ikw', 'gub',
        'es', 'row', 'tbz', 'uz_cyrl', 'txq', 'bgt', 'cgc', 'gv', 'kup', 'gag_cyrl', 'br', 'mih', 'cnt', 'tsg', 'xbi', 'mr', 'poi', 'lv', 'nl',
        'amm', 'kvg', 'cbc', 'qwh', 'bxh', 'ztq', 'tbc', 'bsn', 'kto', 'seh', 'hot', 'mca', 'mir', 'pl', 'ctp', 'qvz', 'suz', 'knj', 'dng', 'aai',
        'ckt_cyrl', 'amu', 'atd', 'so', 'dik', 'ntu', 'wim', 'it', 'enm', 'zpo', 'amf', 'esk', 'udu', 'zam', 'tt_cyrl', 'sv', 'qxn', 'zpq', 'bon',
        'rro', 'ziw', 'ter', 'sah_cyrl', 'bkq', 'acf', 'fa', 'awx', 'naf', 'kmo', 'kdl', 'azg', 'tpz', 'tab', 'zpl', 'waj', 'maa', 'qvw', 'chd', 'chr',
        'ong', 'mdy', 'apn', 'ndj', 'amk', 'mcq', 'tca', 'tet', 'zpm', 'emi', 'muy', 'el', 'dob', 'otn', 'agr', 'kyq', 'snp', 'zav', 'pad', 'lex', 'dwy',
        'kde', 'vid', 'mic', 'gyr', 'cub', 'cop', 'cni', 'mee', 'aom', 'yal', 'mal', 'msk', 'bjv', 'ood', 'en', 'zpu', 'zpc', 'ign', 'mbl', 'nfa', 'mxq',
        'ruf', 'viv', 'kdc', 'cbs', 'lt', 'prs', 'mna', 'tim', 'wrs', 'lcm', 'bhl', 'lww', 'lez', 'nnq', 'tac', 'soy', 'av_cyrl', 'kbm', 'wro', 'cy', 'mjc',
        'kmk', 'zyp', 'sll', 'not', 'ngp', 'hu', 'kaa_latn', 'npi', 'wnc', 'cbt', 'ceb', 'he', 'kpw', 'yaq', 'ch', 'abt', 'amn', 'eo', 'agn', 'ky_arab', 'tyv',
        'wed', 'nhw', 'cbv', 'ptp', 'smk', 'lid', 'mil', 'poy', 'urb', 'lez_cyrl', 'avt', 'cbi', 'awb', 'kne', 'aby', 'ebk', 'yle', 'srm', 'ssd', 'sl', 'af', 'ian',
        'chf', 'vi', 'mzz', 'kwd', 'cpy', 'mn', 'wuv', 'ga', 'cax', 'mie', 'xal', 'mi', 'cpc', 'srq', 'mti', 'apy', 'gia', 'zpz', 'pma', 'akh', 'gnw', 'yrk_cyrl',
        'msb', 'kpj', 'kjs', 'pwg', 'hns', 'la', 'wal', 'pon', 'crn', 'sab', 'inb', 'boa', 'myy', 'buk', 'aii', 'zia', 'bea', 'toc', 'aaz', 'cle', 'clu', 'arp', 'mco',
        'bvr', 'xed', 'zai', 'ury', 'pah', 'kwi', 'ots', 'caa', 'mbh', 'ncj', 'tkr_cyrl', 'ppk', 'bqp', 'fue', 'enq', 'wiu', 'kos', 'uz_latn', 'apu', 'dug', 'mxb',
        'imo', 'cjo', 'agg', 'khz', 'pot', 'qul', 'chz', 'iou', 'yuw', 'kqw', 'lbk', 'sny', 'bki', 'da', 'to', 'acu', 'mcb', 'rai', 'nys', 'swp', 'haw', 'alp', 'ons',
        'taw', 'mpp', 'kpl', 'mmx', 'notavailable', 'apb', 'spl', 'mam', 'nyu', 'kze', 'mio', 'ncu', 'bhg', 'ptu', 'pao', 'mbj', 'cnl', 'mkn', 'mbb', 'iws', 'faa',
        'obo', 'nko', 'cbk', 'kvn', 'fai', 'mps', 'bmr'
        ]

    def __init__(self, swrdpath = os.path.join(os.path.dirname(os.path.realpath(__file__)),".bibles"), repoconf = ".heathenrepo"):
        self.swordpath = swrdpath
        self.repoconfigname = repoconf
        self.configfile = os.path.join(self.swordpath,self.repoconfigname)
        if os.path.exists(self.configfile) == False:
            self.repo_dir = "mods.d"
            self.repo_gz = self.repo_dir+".tar.gz"
            self.configfile = os.path.join(self.swordpath,self.repoconfigname)
            self.repo_path = os.path.join(self.swordpath,self.repo_dir)
            self.pyrepo_list = os.path.join(self.repo_path,".python_helpful_confs")
            self.pyrepo_outdated_list = os.path.join(self.repo_path,".python_helpful_confs.outdated")
            self.master_repo_list_name = 'masterRepoList.conf'
            self.raw_repo_list = os.path.join(self.swordpath,self.master_repo_list_name)
            self.master_server = 'ftp.crosswire.org'
            self.master_server_repo = 'pub/sword'
            self.timestamp_file_list = os.path.join(self.swordpath,".ftptimestamps")
            self.tempdir = os.path.join(self.swordpath,".temp")
            self.pymaster_list = os.path.join(self.swordpath, ".py"+self.master_repo_list_name)
            if os.path.exists(self.swordpath) == False:
                os.makedirs(self.swordpath)
            self.configuration['MAIN'] = {
                'master repo list' : 'masterRepoList.conf', 'master repo list localpath':self.raw_repo_list, 'pymaster repo list':self.pymaster_list, 'python repo list':self.pyrepo_list,
                'python repo outdated list':self.pyrepo_outdated_list, 'master server':self.master_server, 'master server repo path':self.master_server_repo,
                'sword home':self.swordpath, 'repo directory':self.repo_dir,  'repo path':self.repo_path, 'repo tar.gz':self.repo_gz, 'time stamp filelist':self.timestamp_file_list,
                'temporary directory':self.tempdir}
            with open(self.configfile,'w') as conf:
                self.configuration.write(conf)
        self.configuration.read(self.configfile)
        self.swordpath = self.configuration['MAIN']['sword home']
        self.repo_gz = self.configuration['MAIN']['repo tar.gz']
        self.repo_dir = self.configuration['MAIN']['repo directory']
        self.repo_path = self.configuration['MAIN']['repo path']
        self.pyrepo_list = self.configuration['MAIN']['python repo list']
        self.pyrepo_outdated_list = self.configuration['MAIN']['python repo outdated list']
        self.master_repo_list_name = self.configuration['MAIN']['master repo list']
        self.raw_repo_list = self.configuration['MAIN']['master repo list localpath']
        self.pymaster_list = self.configuration['MAIN']['pymaster repo list']
        self.master_server = self.configuration['MAIN']['master server']
        self.master_server_repo = self.configuration['MAIN']['master server repo path']
        self.timestamp_file_list = self.configuration['MAIN']['time stamp filelist']
        self.tempdir = self.configuration['MAIN']['temporary directory']

    def save_config():
        self.configuration['MAIN']['python repo outdated list'] = pyrepo_outdated_list
        self.configuration['MAIN']['sword home'] = swordpath
        self.configuration['MAIN']['repo tar.gz'] = repo_gz
        self.configuration['MAIN']['repo directory'] = repo_dir
        self.configuration['MAIN']['repo path'] = repo_path
        self.configuration['MAIN']['pymaster repo list'] = pymaster_list
        self.configuration['MAIN']['python repo list'] = pyrepo_list
        self.configuration['MAIN']['master repo list'] = master_repo_list_name
        self.configuration['MAIN']['master repo list localpath'] = raw_repo_list
        self.configuration['MAIN']['master server'] = master_server
        self.configuration['MAIN']['master server repo path'] = master_server_repo
        self.configuration['MAIN']['time stamp filelist'] = timestamp_file_list
        with open(self.configfile,'w') as conf:
            self.configuration.write(conf)

    def check_ftp_timestamp(self,server, filepath):
        ftp = FTP(server)
        ftp.login()
        timestamp = ftp.voidcmd('MDTM {}'.format(filepath))[4:].strip()
        ftp.close()
        return [server, filepath, timestamp]

    def ftp_new(self, timestamp):
        server = timestamp[0]
        serverfile = timestamp[1]
        servertimestamp = timestamp[2]

        config = configparser.ConfigParser()
        if os.path.exists(self.timestamp_file_list):
            config.read(self.timestamp_file_list)

        if server in config:
            if serverfile in config[server]:
                if config[server][serverfile] == servertimestamp:
                    return False
                else:
                    config[server][serverfile] = servertimestamp
                    with open(self.timestamp_file_list,'w') as conf:
                        config.write(conf)
                    return True
            else:
                config[server][serverfile] = servertimestamp
                with open(self.timestamp_file_list,'w') as conf:
                    config.write(conf)
                return True
        else:
            config[server]={serverfile:servertimestamp}
            with open(self.timestamp_file_list,'w') as conf:
                config.write(conf)
            return True


    def update_repo_list(self):
        if self.ftp_new(self.check_ftp_timestamp(self.master_server,os.path.join(self.master_server_repo,self.master_repo_list_name))):
            download = os.path.join(self.swordpath,self.master_repo_list_name)
            urldownload = urllib.parse.urljoin("ftp://"+self.master_server,os.path.join(self.master_server_repo,self.master_repo_list_name))
            urllib.request.urlretrieve(urldownload, download)
            return True
        else:
            return False

    def process_repo_list(self):
        config = configparser.ConfigParser(delimiters="|")
        config.read(self.raw_repo_list)
        configures = configparser.ConfigParser()

        for servername in config['Repos']:
            beta = 'false'
            serverdetails = config['Repos'][servername].split('|')
            reesespieces = servername.split("=")
            proto = self.protocolstrings[reesespieces[1]]
            if reesespieces[2] in self.BetaList:
                beta = 'true'
            configures[reesespieces[2]] = {'path' : serverdetails[1], 'url':serverdetails[0], 'proto':proto, 'date added':reesespieces[0], 'beta':beta}

        with open(self.pymaster_list,'w') as conf2:
            configures.write(conf2)


    def download_repos(self):
        config = configparser.ConfigParser()
        config.read(self.pymaster_list)
        returnList = {}
        outdated = os.path.join(self.repo_path,"outdated")
        betapath = os.path.join(self.repo_path,'beta')
        if os.path.exists(outdated) == False:
            os.makedirs(outdated)
        if os.path.exists(self.repo_path) == False:
            os.makedirs(self.repo_path)
        if os.path.exists(self.tempdir) == False:
            os.makedirs(self.tempdir)

        beta = False
        returnList = { 'updatedrepos':{}}
        for server in config.sections():
            url = config[server]['url']
            proto = config[server]['proto']
            serverfilepath = os.path.join(config[server]['path'], self.repo_gz)
            urldirty = "{}{}".format(proto,url)
            process_url = urllib.parse.urljoin(urldirty,config[server]['path'])
            if self.ftp_new(self.check_ftp_timestamp(url, serverfilepath)):
                ## delete server from outdated?
                localfile=os.path.join(self.swordpath,self.repo_gz)
                urllib.request.urlretrieve(urllib.parse.urljoin(urldirty,serverfilepath), localfile )
                returnList[server] = { "path":serverfilepath, "url":url, "proto":proto }

                shutil.unpack_archive(localfile,self.tempdir)
                directorylist = glob.glob(os.path.join(os.path.join(self.tempdir,self.repo_dir),"*.conf"))
                dontcopy = self.process_mod_confs(directorylist, url, config[server]['path'], proto, config[server]['beta'])

                os.remove(localfile)

                for files in dontcopy:
                    thefile = os.path.join(os.path.join(self.tempdir,self.repo_dir),files)
                    shutil.copy(thefile, outdated)
                    os.remove(thefile)

                directorylist = os.listdir(os.path.join(self.tempdir,self.repo_dir))
                thepath = self.repo_path
                if config[server]['beta'] == 'true':
                    thepath = betapath

                for files in directorylist:
                    thefile = os.path.join(os.path.join(self.tempdir,self.repo_dir),files)
                    shutil.copy(thefile, thepath)
                    os.remove(thefile)
                returnList['updatedrepos'][server] = directorylist
        return returnList

    def initiate_repo(self):
        masterlist = os.path.join(self.master_server_repo,self.master_repo_list_name)
        urldownload = urllib.parse.urljoin("ftp://{}".format(self.master_server), masterlist)
        if os.path.exists(self.raw_repo_list):
            if self.ftp_new(urllib.parse.urljoin(self.master_server,masterlist)):
                urllib.request.urlretrieve(urldownload, self.raw_repo_list)
        else:
            urllib.request.urlretrieve(urldownload, self.raw_repo_list)

        self.process_repo_list()

        self.download_repos()

    def process_mod_confs(self, listit, server, serverpath, serverproto, beta):
        config = configparser.ConfigParser()
        config2 = configparser.ConfigParser()
        outdated = os.path.join(self.repo_path,"outdated")
        if os.path.exists(self.repo_path) == False:
            os.makedirs(self.repo_path)
        if os.path.exists(outdated) == False:
            os.makedirs(outdated)
        if os.path.exists(self.pyrepo_list):
            config.read(self.pyrepo_list)
        if os.path.exists(self.pyrepo_outdated_list):
            config2.read(self.pyrepo_outdated_list)

        returnlist = []
        for package in listit:
            dance = False
            configdancer = False

            temps = os.path.join(os.path.join(self.tempdir,self.repo_dir),package)

            packageinfo = self.read_mod_conf(temps)

            packname = "{}-{}".format(os.path.basename(package),packageinfo['name'].strip("[]"))
            if beta == 'true':
                betapath = os.path.join(self.repo_path,'beta')
                if os.path.exists(betapath) == False:
                    os.makedirs(betapath)
                if packname in config:
                    config[packname]['beta available'] = 'yes'
                packname+="-beta"
                package = os.path.basename(package)
                packageinfo['full_path'] = os.path.join(betapath,package)
            if beta == 'false':
                if packname+"-beta" in config:
                    packageinfo['beta available'] = 'yes'
                else:
                    packageinfo['beta available'] = 'no'
            if 'lang' not in packageinfo:
                    packageinfo['lang'] = "notavailable"
            if "#" in packageinfo['lang']:
                packageinfo['lang'] = packageinfo['lang'].split('#')[0].strip().rstrip()
            if " " in packageinfo['lang']:
                packageinfo['lang'] = packageinfo['lang'].replace(" ","_")
            if "-" in packageinfo['lang']:
                packageinfo['lang'] = packageinfo['lang'].replace("-","_")
            packageinfo['server url'] = server
            packageinfo['server path'] = serverpath
            packageinfo['server proto'] = serverproto

            #check if package is in config

            if packname in config:
                # if we are updating

                #if package is in config and both have their versions listed

                ###############
                #########33

                if packageinfo['lang'] == config[packname]['lang']:
                    #if outdated configs named package is less than the new one

                    if version.parse(config[packname]['version'].strip().rstrip()) < version.parse(packageinfo['version'].strip().rstrip()):
                        temp = dict(config[packname])
                        del config[packname]
                        config[packname] = packageinfo
                        if not os.path.exists(outdated):
                            os.makedirs(outdated)
                        if packname not in config2:
                            oldpath  = temp['full_path']
                            newpath =  os.path.join(outdated,os.path.basename(package))
                            temp['full_path'] = newpath
                            config2[packname] = temp
                            try:
                                shutil.copy(oldpath, newpath)
                                os.remove(oldpath)
                            except:
                                print("hmm")
                        else:
                            dance = True
                            dancer = temp
                    else:
                        dance = True
                        dancer = packageinfo
                        returnlist.append(package)
                        #if config package isnt in outdated packages

                else:
                    package = os.path.basename(package)
                    shutil.copy(os.path.join(os.path.join(self.tempdir,self.repo_dir),package),os.path.join(os.path.join(self.tempdir,self.repo_dir),package+"-"+packageinfo['lang']))
                    os.remove(os.path.join(os.path.join(self.tempdir,self.repo_dir),package))
                    packname+="-"+packageinfo['lang']
                    package+="-"+packageinfo['lang']

                    packageinfo['full_path'] = os.path.join(self.repo_path,package)
                    if packname in config:
                        if version.parse(config[packname]['version']) < version.parse(packageinfo['version']):
                            temp = dict(config[packname])
                            del config[packname]
                            config[packname] = packageinfo
                            if not os.path.exists(outdated):
                                os.makedirs(outdated)
                            if packname not in config2:
                                oldpath  = temp['full_path']
                                newpath =  os.path.join(outdated,package)
                                temp['full_path'] = newpath
                                config2[packname] = temp
                                shutil.copy(oldpath, newpath)
                            else:
                                dance = True
                                dancer = temp
                        else:
                            dance = True
                            dancer = packageinfo
                            returnlist.append(package)
                            #if config package isnt in outdated packages
                    else:
                        config[packname] = packageinfo
                if dance:
                    package = os.path.basename(package)
                    if packname in config2:
                        outdated = os.path.join(self.repo_path,"outdated")
                        if not os.path.exists(outdated):
                            os.makedirs(outdated)
                        outdatedhere = os.path.join(outdated)
                        if configdancer:
                            shutil.copy(dancer['full_path'],os.path.join(outdatedhere,package))
                            os.remove(dancer['full_path'])
                            dancer['full_path'] = os.path.join(outdatedhere,package)
                        if version.parse(dancer['version']) < version.parse(config2[packname]['version']):
                            outdated_key = "{}-{}".format(packname,dancer['version'])
                            if outdated_key not in config2:
                                config2[outdated_key] = dancer
                                oldpath = dancer['full_path']
                                config2[outdated_key]['full_path'] = os.path.join(outdatedhere,package)
                        else:
                            outdated_key = "{}-{}".format(packname,config2[packname]['version'])
                            if outdated_key in config2:
                                if version.parse(config2[packname]['version']) > version.parse(config2[outdated_key]['version']):
                                    del config2[outdated_key]
                                    config2[outdated_key] = config2[packname]
                                    del config2[packname]
                                    config2[packname] = dancer

                            else:
                                config2[outdated_key] = config2[packname]
                                del config2[packname]
                                config2[packname] = dancer
                    else:
                        config2[packname] = dancer

            else:
                config[packname] = packageinfo

        with open(self.pyrepo_list,'w') as conf:
            config.write(conf)
        with open(self.pyrepo_outdated_list,'w') as conf2:
            config2.write(conf2)

        return returnlist



    def read_mod_conf(self,package):
        with open(package) as config:
            lines = config.readlines()
        config.close()
        packageinfo={}
        packageinfo['name']=(lines.pop(0)).strip().rstrip().lower()
        packageinfo['full_path']=os.path.join(self.repo_path,os.path.basename(package))
        lastkey = 'trash'
        for line in lines:
            linepieces=line.split("=",1)
            normalizedkeyname = linepieces[0].strip().rstrip().lower()
            if len(linepieces) > 1 and normalizedkeyname not in packageinfo.keys():
                normalizedvalue = linepieces[1].replace('%','PERCENT').replace(':','COLON').strip().rstrip().lower().replace('=','EQUALSIGN')
                packageinfo[normalizedkeyname] = normalizedvalue
                lastkey = normalizedkeyname
            elif lastkey != 'trash':
                packageinfo[lastkey]+=" "+normalizedkeyname.replace('%','PERCENT').replace(':','COLON').replace('=','EQUALSIGN')
            else:
                lastkey = 'trash'
        return packageinfo

    def search_section_module(self, string, section, outdated=False, beta=False):
        config = configparser.ConfigParser()
        returnlist = []
        if outdated:
            config.read(self.pyrepo_outdated_list)
            if beta:
                beta=False
                print("cant do beta with outdated, derp")
        else:
            config.read(self.pyrepo_list)
        for keyname in config.keys():
            if section in config[keyname]:
                if re.search(string.lower(), config[keyname][section].lower()):
                    returnlist.append([keyname,config[keyname]])
        return returnlist

    def uninstall_module(self, modulename):
        config = configparser.ConfigParser()
        config.read(self.pyrepo_list+".installed")
        if modulename in config.keys():
            installedfiles = config[modulename]['installed files'].strip().split('## ')
            installedfiles.remove('')
            for installedfile in installedfiles:
                try:
                    os.remove(installedfile)
                except:
                    print("file already gone or bad permissions")

            if os.path.basename(os.path.dirname(installedfiles[0])) == config[modulename]['name'].strip('[]'):
                try:
                    os.rmdir(os.path.dirname(installedfiles[0]))
                except:
                    print("Directory wasnt empty")
            del config[modulename]
            with open(self.pyrepo_list+".installed",'w') as conf2:
                config.write(conf2)
            return True
        else:
            return False


    def find_module(self,modulename, installed=False, p="", outdated=False, beta=False, lang=""):
        config = configparser.ConfigParser()
        if outdated:
            config.read(self.pyrepo_outdated_list)
            if beta:
                beta=False
                print("cant do beta with outdated, derp")
        if installed:
            config.read(self.pyrepo_list+".installed")
        else:
            config.read(self.pyrepo_list)
        a=".conf"
        b="-"
        c="beta"
        modules = []
        if modulename+a+b+modulename+p in config.keys():
            modules.append([modulename+a+b+modulename+p,config[modulename+a+b+modulename+p]])
        elif modulename in config.keys():
            modules.append([modulename, config[modulename]])
        if beta:
            if modulename+a+b+modulename+b+c+p in config.keys():
                modules.append([modulename+a+b+modulename+b+c+p,config[modulename+a+b+modulename+b+c+p]])
            elif modulename+b+c+p in config.keys():
                modules.append([modulename+b+c+p,config[modulename+b+c+p]])
        if lang != "":
            if lang != "all":
                if modulename+a+b+modulename+b+lang+p in config.keys():
                    modules.append([modulename+a+b+modulename+b+lang+p,config[modulename+a+b+modulename+b+langu+p]])
                elif modulename+b+lang+p in config.keys():
                    modules.append([modulename+b+lang+p, config[modulename+b+lang+p]])
            else:
                for langu in self.languages:
                    if modulename+a+b+modulename+b+langu+p in config.keys():
                        modules.append([modulename+a+b+modulename+b+langu+p,config[modulename+a+b+modulename+b+langu+p]])
                    elif modulename+b+langu+p in config.keys():
                        modules.append([modulename+b+langu,config[modulename+b+langu+p]])
        return modules

    def get_module(self,mod,installpath, preferzip=True, beta=True):
        installedfiles=""
        success = False
        if preferzip and not beta:
            if mod['server path'].strip('/') == 'sword':
                zippath = os.path.join(mod['server path'],'packages/rawzip')
            else:
                faye = mod['server path'].rsplit('/',1)
                zippath = os.path.join(faye[0],'packages/rawzip')

        path = os.path.join(mod['server path'],mod['datapath'])
        try:
            ftp = FTP(mod['server url'])
            ftp.login()
            files = ftp.nlst(path)

        except:
            print("No files at path")
            return False

        if preferzip and not beta:
            try:
                ftp = FTP(mod['server url'])
                ftp.login()
                zipfiles = ftp.nlst(zippath)

            except:
                print("No files at path")
                return False

        theurl = mod['server proto']+mod['server url']
        if preferzip and not beta:
            for x in zipfiles:
                if x.lower() == os.path.join(zippath,mod['name'].strip('[]')+".zip"):
                    localfile = os.path.join(installpath,os.path.basename(x))
                    download = urllib.parse.urljoin(theurl,x)

                    try:
                        urllib.request.urlretrieve(download,localfile)
                    except:
                        theurl = urllib.parse.urljoin(theurl,zippath)
                        download = urllib.parse.urljoin(theurl,x)
                        urllib.request.urlretrieve(download,localfile)

                    installedfiles+="## "+localfile
                    success = True

        if not success:
            for x in files:
                localfile = os.path.join(installpath,os.path.basename(x))
                download = urllib.parse.urljoin(theurl,x)
                try:
                    urllib.request.urlretrieve(download,localfile)
                except:
                    theurl = urllib.parse.urljoin(theurl,path)
                    download = urllib.parse.urljoin(theurl,x)
                    urllib.request.urlretrieve(download,localfile)
                installedfiles+="## "+localfile
                success = True
        return [mod,success,installedfiles]

    def update_modules_list(self,uptobeta=False):
        if not os.path.exists(self.pyrepo_list+".installed"):
            return None
        installedconfig = configparser.ConfigParser()
        installedconfig.read(self.pyrepo_list+".installed")
        config = configparser.ConfigParser()
        config.read(self.pyrepo_list)

        def check(install):
            if install in config.keys():
                if version.parse(installedconfig[install]['version']) < version.parse(config[install]['version']):
                    if installedconfig[install]['lang'] == config[install]['lang']:
                        return [True,install]
                    else:
                        langedkey = install+"-"+installedconfig[install]['lang']
                        if  langedkey in config.keys():
                            if version.parse(installedconfig[install]['version']) < version.parse(config[langedkey]['version']):
                                return [True,langedkey]
                return [ False ]

        out_of_date_list = []
        installed = self.list_installed_modules()
        for install in installed:
            ziper = check(install)
            if ziper[0]:
                out_of_date_list.append([install,ziper[1]])
            if uptobeta:
                betainstall = install+"-beta"
                ziper = check(betainstall)
                if ziper[0]:
                    out_of_date_list.append([install,ziper[1]])
        return out_of_date_list

    def install_module(self,keyname, outdated=False, beta=False, preferzip=True, custominstallpath=[False,""]):
        #success = False
        config = configparser.ConfigParser()
        #installedfiles=""
        installedconfig = configparser.ConfigParser()
        if os.path.exists(self.pyrepo_list+".installed"):
            installedconfig.read(self.pyrepo_list+".installed")
        if outdated:
            config.read(self.pyrepo_outdated_list)
            if beta:
                beta=False
                print("cant do beta with outdated, derp")
                return None
        else:
            config.read(self.pyrepo_list)
        if beta:
            if keyname+"-beta" in config.keys():
                keyname+="-beta"
        if keyname in config.keys():
            if custominstallpath[0]:
                installpath = custominstallpath[1]
                installedkeyname = keyname+"_CUSTOMPATH"
            else:
                installpath = os.path.join(self.swordpath,config[keyname]['datapath'])
                installedkeyname = keyname
            if os.path.exists(installpath) == False:
                os.makedirs(installpath)
            info = self.get_module(config[keyname],installpath,preferzip=preferzip,beta=False)

            if installedkeyname in installedconfig.keys():
                del installedconfig[installedkeyname]

            installedconfig[installedkeyname] = info[0]
            installedconfig[installedkeyname]['installed files'] = info[2]
            with open(self.pyrepo_list+".installed",'w') as conf2:
                installedconfig.write(conf2)
            return [keyname, info[1]]
        return None

    def list_installed_modules(self):
        if os.path.exists(self.pyrepo_list+".installed"):
            installedconfig = configparser.ConfigParser()
            installedconfig.read(self.pyrepo_list+".installed")
        else:
            return None
        returnlist = []
        for key in installedconfig.keys():
            if key != 'DEFAULT':
                returnlist.append(key)
        return returnlist

    def strapit(self, found):
        installed = configparser.ConfigParser()
        installed.read(self.pyrepo_list+".installed")
        ibm_path = os.path.join(self.swordpath,"ibm")
        if not os.path.exists(ibm_path):
            os.makedirs(ibm_path)
        ibm_path_confs = os.path.join(ibm_path,"mods.d")
        if not os.path.exists(ibm_path_confs):
            os.makedirs(ibm_path_confs)
        for key in found:
            ibm_location = os.path.join(ibm_path,installed[key]['datapath'])
            if not os.path.exists(ibm_location):
                os.makedirs(ibm_location)
            files = installed[key]['installed files'].split("## ")
            files.remove('')
            newinstallfiles = ""
            for thefile in files:
                newfile = os.path.join(ibm_location,os.path.basename(thefile))
                shutil.copy(thefile,newfile)
                newinstallfiles+="## "+newfile
                os.remove(thefile)
            modconf = installed[key]['full_path']
            installed[key]['full_path'] = os.path.join(ibm_path_confs,os.path.basename(modconf))
            installed[key]['installed files'] = newinstallfiles
            installed[key]['datapath'] = os.path.join("ibm",installed[key]['datapath'])
            shutil.copy(modconf,installed[key]['full_path'])
        with open(self.pyrepo_list+".installed", 'w') as conf:
            installed.write(conf)



    def find_installed_modules(self):
        found = []
        if os.path.exists(self.repo_path):
            config = configparser.ConfigParser()
            if os.path.exists(self.pyrepo_list+".installed"):
                config.read(self.pyrepo_list+".installed")
            modconfs = glob.glob(os.path.join(self.repo_path,"*.conf*"))

            for modconf in modconfs:
                if not os.path.isdir(modconf):
                    packageinfo = self.read_mod_conf(modconf)
                    key = os.path.basename(modconf)+"-"+packageinfo['name'].strip('[]')
                    if 'datapath' in packageinfo:
                        fulldatapath = os.path.join(self.swordpath,packageinfo['datapath'])
                        if os.path.exists(fulldatapath):
                            filelist = os.listdir(fulldatapath)
                            if len(filelist) != 0:

                                installedfiles = ""

                                for thefile in filelist:
                                    localfile = os.path.join(self.swordpath,os.path.join(packageinfo['datapath'],thefile))
                                    installedfiles+="## "+localfile
                                if key not in config.keys():
                                    config[key] = packageinfo
                                else:
                                    del config[key]
                                    config[key] = packageinfo
                                config[key]['installed files'] = installedfiles
                                found.append(key)

            with open(self.pyrepo_list+".installed",'w') as conf2:
                config.write(conf2)
        return found

    def move_module(self, oldmodule, newmodule):
        installedconfig = configparser.ConfigParser()
        installedconfig.read(self.pyrepo_list+".installed")
        config = configparser.ConfigParser()
        config.read(self.pyrepo_list)
        installedfiles = installedconfig[oldmodule]['installed files'].split("## ")
        installedfiles.remove("")
        confdata_path = os.path.join(os.path.join(self.swordpath,config[newmodule]['datapath']))
        if not os.path.exists(confdata_path):
            os.makedirs(confdata_path)
        newinstall_line=""
        for swordfile in installedfiles:
            newfile = os.path.join(confdata_path,os.path.basename(swordfile))
            shutil.copy(swordfile,newfile)
            os.remove(swordfile)
            newinstall_line+="## "+newfile
        del installedconfig[oldmodule]
        installedconfig[newmodule] = config[newmodule]
        installedconfig[newmodule]['installed files'] = newinstall_line
        with open(self.pyrepo_list+".installed", 'w') as conf2:
            installedconfig.write(conf2)

    def bootstrap_ibm(self):
        found = self.find_installed_modules()
        self.strapit(found)
        self.initiate_repo()
        modules = self.update_modules_list()
        didnt_make_it = []
        if len(modules) == 0:
            for module in found:
                self.move_module(module,module)

        else:
            for module in modules:
                if module[0] != module[1]:
                    self.move_module(module[0],module[1])
                else:
                    didnt_make_it.append(module[0])
                found.remove(module[0])
            for module in found:
                self.move_module(module,module)

        return found






#pyrepoz = PyswordRepo(swrdpath = "/home/user/HR-Tools/.bibles" ,repoconf=".heathenrepo")
#did = pyrepoz.bootstrap_ibm()
#print(did)
#pyrepoz.initiate_repo()
#pyrepoz.update_repo_list()
#pyrepoz.download_repos()
#pyrepoz.install_module('drc.conf-drc')
#print(pyrepoz.search_section_module("king james",'about'))
#listinstall = pyrepoz.update_modules_list()
#pyrepoz.install_module('augustine.conf-augustine-ru')
#print(listinstall)
#for x in listinstall:
#    pyrepoz.install_module(x[1])
