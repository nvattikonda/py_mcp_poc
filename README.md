## Starting MCP Quickstart Server

```
uv run mcp_quickstart.py

py_mcp_poc  uv run mcp_quickstart.py
INFO:     Started server process [553101]
INFO:     Waiting for application startup.
[01/04/26 19:12:59] INFO     StreamableHTTP session manager started                    streamable_http_manager.py:109
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Running MCP Inspector

The MCP Inspector uses two ports, one for the Client (UI) and one for the Server (Proxy).

```
docker run --name mcp_inspector --network host \
  -e HOST=0.0.0.0 \
  -e CLIENT_PORT=6274 \
  -e SERVER_PORT=6277 \
  -e MCP_AUTO_OPEN_ENABLED=false \
  ghcr.io/modelcontextprotocol/inspector:0.18.0
  
~ docker run --name mcp_inspector --network host \
  -e HOST=0.0.0.0 \
  -e CLIENT_PORT=6274 \
  -e SERVER_PORT=6277 \
  -e MCP_AUTO_OPEN_ENABLED=false \
  ghcr.io/modelcontextprotocol/inspector:0.18.0

> @modelcontextprotocol/inspector@0.18.0 start
> node client/bin/start.js

Starting MCP inspector...
⚙️  Proxy server listening on 0.0.0.0:6277
🔑 Session token: 9e8e28c495cea56118fb55fd294323c9bb159ebe5352c458e9fbdef47408bad5
   Use this token to authenticate requests or set DANGEROUSLY_OMIT_AUTH=true to disable auth

🚀 MCP Inspector is up and running at:
   http://0.0.0.0:6274/?MCP_PROXY_AUTH_TOKEN=9e8e28c495cea56118fb55fd294323c9bb159ebe5352c458e9fbdef47408bad5

```

**Running MCP Inspector _Disabling_ Proxy server authentication**

```
docker run --name mcp_inspector --network host \
  -e HOST=0.0.0.0 \
  -e CLIENT_PORT=6274 \
  -e SERVER_PORT=6277 \
  -e MCP_AUTO_OPEN_ENABLED=false \
  -e DANGEROUSLY_OMIT_AUTH=true \
  ghcr.io/modelcontextprotocol/inspector:0.18.0
  

~ docker run --name mcp-inspector --network host   -e HOST=0.0.0.0   -e CLIENT_PORT=6274   -e SERVER_PORT=6277   -e MCP_AUTO_OPEN_ENABLED=false -e DANGEROUSLY_OMIT_AUTH=true   ghcr.io/modelcontextprotocol/inspector:0.18.0

> @modelcontextprotocol/inspector@0.18.0 start
> node client/bin/start.js

Starting MCP inspector...
⚙️  Proxy server listening on 0.0.0.0:6277
⚠️   WARNING: Authentication is disabled. This is not recommended.

🚀 MCP Inspector is up and running at:
   http://0.0.0.0:6274
   
```

## Connecting MCP Inspector

* In browser open url http://localhost:6274
* Pick Transport Type: Streamble HTTP
* Add url: http://localhost:8000/mcp
* Pick Connection Type: Via Proxy
* Under Configuration provide
    * Inspector Proxy Address: http://localhost:6277
    * Proxy Session
      Token [If MCP Inspector is started with proxy server authentication is enabled, provide session token value]

## References

* [MCP Inspector](https://github.com/modelcontextprotocol/inspector)
* [MCP Use](https://mcp-use.com/docs/inspector)
    * supports connecting to multiple mcp servers
    * supports interactive chat with LLM integration for testing conversational flows
