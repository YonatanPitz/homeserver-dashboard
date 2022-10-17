from simplestRPC.srpc_client import SRPCClient


# conects
client = SRPCClient()

ret = client.call_rpc('remote_function', 'xablau!', 12, 108)
print("return: ", ret)

ret = client.call_rpc('customName', 'custom method', 12, 108)
print("return: ", ret)