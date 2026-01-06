from mcp.server.fastmcp import FastMCP

from prompts import register_prompts
from resources import register_resources
from tools import register_tools

# https://github.com/modelcontextprotocol/python-sdk/issues/1168 (streamable_http_path trailing path issue)
# Initialize FastMCP server
mcp = FastMCP("mcp_poc_server", instructions="server demos different capabilities of mcp", port=8000,
              host="0.0.0.0", streamable_http_path="/mcp/", stateless_http=True,
              json_response=True)

# register tools
register_tools(mcp)
# register resources
register_resources(mcp)
# register prompts
register_prompts(mcp)


def main():
    # Initialize and run the server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
