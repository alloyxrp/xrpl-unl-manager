#!/usr/bin/env python3
import argparse
import sys
import utils
import json
import os

argparser=argparse.ArgumentParser(description="Encodes an XRP Ledger UNL from a file containing either a JSON list or line-separated validator names")
argparser.add_argument("-f","--list-file", default='./unl-list.json', type=str, help="Defines the UNL file to be parsed")
# cmdgroup.set_defaults()

argparser.add_argument("-v","--version", default=1,type=int,
                            help="Defines the version of the UNL.")
argparser.add_argument("-kf","--keys-file", default='./unl-generator-token.txt', type=str, help="Defines the keys-pair file used to sign the UNL")
argparser.add_argument("-kp","--validators-keys-path", default='./configfiles/', type=str, help="Defines the root path for the validators")
argparser.add_argument("-o","--output-file", type=str,default='./encoded-list.json',help="Defines the output file.")

aa=argparser.parse_args()
# print (aa,aa.keys_file)

def parseValidatorTokenFile(vtokenfname):
    """Parses the validator-token.txt file and return a json object

    Arguments:
        vtokenfname {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    with open(vtokenfname,'r') as f:
        vkcont=f.read()

    
    vtokenstr=vkcont.split('[validator_token]')[1].strip()
    
    vtokenstr=vtokenstr.replace('\n','')
    # print(vtokenstr)
    return (utils.decodeValidatorToken(vtokenstr))

def parseListFile(listfname:str):
    """Parses the list file
        The list file could be either line list of validators' names OR
        a file with a json array. starts with '['

    Arguments:
        listfname {str} -- [description]
    """
    with open(listfname,'r') as f:
        fcont=f.read()
    fcont=fcont.strip()
    
    if fcont.startswith('['):
        # it's json array
        return json.loads(fcont)
    else:
        # it should be a line list
        flines=fcont.split('\n')
        for l in flines:
            if l.strip().startswith('#'):
                # it's commented out
                flines.remove(l)
        return flines
    
vtoken=parseValidatorTokenFile(aa.keys_file)
# print(vtoken)

mvallist=parseListFile(aa.list_file)
# print(mvallist)

vkpath=os.path.abspath(aa.validators_keys_path)
# print(vkpath)

# print(aa.version)

# print(aa.output_file)

munl=utils.createUNL(mvallist,vtoken,aa.version,vkpath)
# print(munl)
# print (json.dumps(munl))

with open(aa.output_file,'w') as f:
    json.dump(munl,f)

print ('Finished!!!')
