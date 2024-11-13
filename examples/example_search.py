from linkup import LinkupClient, LinkupClientResponse

client = LinkupClient()

query: str = "What are the 10 major events in the life of Abraham Lincoln ?"
response: LinkupClientResponse = client.search(query=query)

print(f"Linkup answer:\n{response.content}\n")
print("Sources:\n")
for source in response.sources:
    print(f"{source.name} ({source.url}): {source.snippet}\n")
