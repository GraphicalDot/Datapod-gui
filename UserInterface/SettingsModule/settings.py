##documentation available at https://pypi.org/project/simple-settings/

import ipfsapi

bigchaindb_app_id = '9f9cbef4'
bigchaindb_app_key = 'c9017b4d69146e5d51d2a3da8a2f1c82'
bigchaindb_testnet_url = 'https://test.bigchaindb.com'

ipfs_ip = "localhost"
ipfs_port = 5001
api_server = "http://localhost:8888/"
jwt_secret = "a"



TIME_ZONE =  'Asia/Kolkata'


def indian_time():
    india  = timezone(TIME_ZONE)
    n_time = datetime.now(india)
    return n_time.strftime("%b %d %Y %H:%M:%S")