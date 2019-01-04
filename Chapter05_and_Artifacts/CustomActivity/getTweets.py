
#!/usr/bin/env bash
sudo apt install python-pip
pip install tweepy
pip install azure-mgmt-storage
pip install pydocumentdb
pip install azure-keyvault

import tweepy
import csv
import os
import sys
import io
import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client
import pydocumentdb.errors as errors

from azure.storage.blob import BlockBlobService
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials


class IDisposable:
    """ A context manager to automatically close an object with a close method
    in a with statement. """
    def __init__(self, obj):
        self.obj = obj
    def __enter__(self):
        return self.obj # bound to target
    def __exit__(self, exception_type, exception_val, trace):
        # extra cleanup in here
        self = None
credentials = None

def auth_callback(server, resource, scope):
    credentials = ServicePrincipalCredentials(
        client_id = '19f9f18b-246c-4ca3-b256-285eebe09231',
        secret = 'a4JSdEUBfXnviXx2eacumkkbps0uGyXqjrMuAl1sgYo=',
        tenant = '3497c22b-7189-4bf5-af2a-f726c53faf6a',
        resource = "https://vault.azure.net"
    )
    token = credentials.token
    return token['token_type'], token['access_token']
    

def insertintoCosmosDB(cdbhost, cdbmasterkey, tweetDate, tweetText):
    tweetmessage = {'tweetDate': str(tweetDate),'id' : str(tweetDate), 'tweetText': tweetText}
    _database_link = 'dbs/tweetdb'
    _collection_link = _database_link + '/colls/tweetcollec'
    with IDisposable(document_client.DocumentClient(cdbhost, {'masterKey': cdbmasterkey} )) as client:
        try:
            client.CreateDocument(_collection_link, tweetmessage, options=False)
        except errors.DocumentDBError as e:
            if e.status_code == 409:
                pass
            else:
                raise errors.HTTPFailure(e.status_code)

def main():
 # Twitter application key
    client = KeyVaultClient(KeyVaultAuthentication(auth_callback))
    _appkey = client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Twitter-appkey", "19bd289d86f449cbb98fd6a51cc63156")
    _appsecret= client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Twitter-appsecret", "510ceec80ef14af28dd961382be78e66")
    _appaccesstoken = client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Twitter-appaccesstoken", "e24ad1dfef6b4392bd6277e9ac51e4b8")
    _appaccesstokensecret = client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Twitter-appaccesstokensecret", "e46bb6b253584ea59d1941bd7f9f1905")
    

    _tweetTag= sys.argv[1] # like Azure 
    _tweetReadSince=  sys.argv[2] #date from when you want to read tweets like '2018/07/28'
    _PipelineRunId= sys.argv[3] #Azure Data Factory Pipeline ID 'testrun' 
    
 # Azure Storage Credential

    _accountname=client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Storage-accountname", "0f9adaf2abb545b38757b37a0d63fc68")
    _accountkey=client.get_secret("https://adfbookkeyvault.vault.azure.net/", "Storage-accountkey", "141200d435694c949a7c011bbf55d40a")
    _InputContainerName='tweetcontainer'
    
# CosmosDB Credential
    _cdbhost = client.get_secret("https://adfbookkeyvault.vault.azure.net/", "cosmosdbURI", "7c885660bce64bd6ae7b44f1c925486c")
    _cdbmasterkey = client.get_secret("https://adfbookkeyvault.vault.azure.net/", "cosmosdbPK", "f220ab6df8d240759435953af5d01e43")
    
#hashtag, tweetreadsince, filename includes pipeline id, 
    auth = tweepy.OAuthHandler(_appkey.value, _appsecret.value)
    auth.set_access_token(_appaccesstoken.value, _appaccesstokensecret.value)
    tweetapi = tweepy.API(auth,wait_on_rate_limit=True)
#local_path=os.path.expanduser("~/Documents")
    local_file_name ="Tweets_" + _tweetTag + _PipelineRunId + ".csv"
    full_path_to_file =os.path.join(os.getcwd(), local_file_name)
    outFile = open(local_file_name,'a')
    fieldnames = ['Tweet_Time', 'Tweet_Desc']
    filewriter = csv.writer(outFile)
    filewriter.writerow(fieldnames)

    for tweet in tweepy.Cursor(tweetapi.search,q=_tweetTag,lang="en", since=_tweetReadSince).items(15):
        try:
            if tweet.text.encode('utf-8') != '' : 
                filewriter.writerow([tweet.created_at,tweet.text.encode('utf-8')])
                insertintoCosmosDB (_cdbhost.value, _cdbmasterkey.value, tweet.created_at,tweet.text.encode('utf-8'))
        except errors.DocumentDBError as e:
            if e.status_code == 409:
                pass
            else:
                raise errors.HTTPFailure(e.status_code)
                print("Error while fetching and storing tweets!!!")
            outFile.close()
            break
    try:
        print full_path_to_file
        print local_file_name
        _blob_service = BlockBlobService(account_name=_accountname.value, account_key=_accountkey.value)
        _blob_service.create_blob_from_path(_InputContainerName, local_file_name, full_path_to_file)
        #print(local_file_name)
    except:
        print("Error while uploading file to Azure Blob Storage !!!")
    
if __name__ == "__main__":
	main()
