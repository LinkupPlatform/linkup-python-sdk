from linkup import LinkupClient
import json

client = LinkupClient()

result = client.search("What are the 10 major events in the life of Abraham Lincoln ?")

print(json.dumps(result, indent=4))
