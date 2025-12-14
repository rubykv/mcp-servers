# mcp-servers
mcp servers for tools integration

In this monorepo, we have different servers for different tools integration.

Some of these servers are already available in the marketplace so you may not want to create a new server for them.

But if you want to create your own server for a tool and want to register them with windsurf local, you can do it here.

Install mcp by running `pip install mcp`.

## How to create a new server
1. Create a new directory in the `servers` directory.
2. Create a new file `client.py` in the directory.
3. Implement the required methods in the `client.py` file.
4. Add the server to the `servers.py` file.
5. Endorse the tools by annotating the methods with `@tool`.

## Run the server
1. Run the server by running `python server.py`.

## Register the MCP server
1. Register the MCP server by clicking on the "plug" icon on the right side of the screen on Windsurf.

2. Click on the icon shown in the image
![alt text](<settings_screen.png>).

3. This opens a config file.

4. For each of the servers in the `servers.py` file, we would need to make an entry in the config file.

5. Once added in config, these servers are now registered with Windsurf.

6. Restart Windsurf to apply the changes. 

7. Click on the "plug" icon again and you should see the server in the list. If its disabled by default, click on the name and debug to see if there are any errors.

8. Use cascade to debug further if needed.

9. Once server is enabled, you can use the tools in the cascade from any Windsurf window.
