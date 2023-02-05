import argparse
import requests
from ping3 import ping


def RegisterAgent(apiEndpoint, secret, name):
    try:
        response = requests.get(
            apiEndpoint + '/registerAgent?secret='+secret+'&name='+name)
        if response.status_code == 200:
            return response.json()['agentId']
        else:
            raise Exception('Error registering agent')
    except Exception as e:
        print(e)
        return None


def GetNodeList(apiEndpoint, secret):
    try:
        response = requests.get(apiEndpoint + '/getNodeList?secret='+secret)
        if response.status_code == 200:
            return response.json()['nodes']
        else:
            raise Exception('Error getting node list')
    except Exception as e:
        print(e)
        return None


def RegisterRecord(apiEndpoint, secret, agentId, nodeId, lantency):
    try:
        response = requests.get(apiEndpoint + '/registerRecord?secret=' +
                                secret+'&agentId='+agentId+'&nodeId='+nodeId+'&lantency='+lantency)
        if not response.status_code == 200:
            raise Exception('Error registering record')
    except Exception as e:
        print(e)


# Accept args from command line
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--apiEndpoint',
                    help='API Endpoint URL. eg. https://pinging.vercel.app/api', required=True)
parser.add_argument(
    '-s', '--secret', help='Agent Secret. eg. 9cWxVbX35UL2Dhj4', required=True)
parser.add_argument('-n', '--name', help='Agent Friendly Name', required=True)
args = parser.parse_args()

# Register agent
agentId = RegisterAgent(args.apiEndpoint, args.secret, args.name)
if agentId == None:
    print('Agent registration failed')
    exit()

# Get node list
nodeList = GetNodeList(args.apiEndpoint, args.secret)
if nodeList == None:
    print('Failed to get node list')
    exit()

# Ping nodes
for node in nodeList:
    print('Pinging ' + node['hostname'])
    lantency = ping(node['hostname'], unit='ms')
    if lantency == None or lantency == False:
        lantency = -1
    lantency = int(lantency)
    print('Lantency: ' + str(lantency))
    RegisterRecord(args.apiEndpoint, args.secret,
                   str(agentId), str(node['id']), str(lantency))
