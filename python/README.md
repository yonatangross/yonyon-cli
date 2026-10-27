# yonyon (Python)

Official Python client for the public [yonyon.ai](https://yonyon.ai) agent API, generated from the
OpenAPI spec at https://yonyon.ai/.well-known/openapi.json.

The HTTP API this client wraps is public and read only. There is no key and no login. (The separate
MCP server at `/api/mcp` has one write tool, `book_intro_call`, which books a real call; it is not
part of this client.) Rate limit: 10 requests per IP per
minute, shared across `/ask`, `/api/chat` and `/api/v1`.

## Install

```bash
pip install yonyon
```

Requires Python 3.11 or newer.

## Use

```python
from yonyon import Client
from yonyon.api.default import list_projects

client = Client(base_url="https://yonyon.ai")

with client as c:
    projects = list_projects.sync(client=c)
    response = list_projects.sync_detailed(client=c)  # status code, headers, raw body
```

Each operation has `sync`, `sync_detailed`, `asyncio` and `asyncio_detailed` variants, except the
five CORS preflight modules (`*_preflight`), which have only `sync_detailed` and `asyncio_detailed`
(they return a `Response[Any]` with no parsed model). Operations
live in `yonyon.api.default` (`ask_nlweb`, `ask_yonatan`, `list_projects`, `batch`, `create_job`,
`get_job`, and the index routes); models live in `yonyon.models`.

Server-side callers: use `ask_nlweb` (`POST /ask`) to ask questions. `ask_yonatan` (`POST /api/chat`)
is the browser chat endpoint and checks the `Origin` header, so a default `Client` gets HTTP 403 from it.
To call it anyway, set `Origin` to the same value as `base_url`, as the npm CLI does:
`Client(base_url="https://yonyon.ai", headers={"Origin": "https://yonyon.ai"})`. This client reads the
whole response and returns the answer as plain text; it does not stream. For token-by-token output,
call the endpoint yourself with httpx `client.stream("POST", "/api/chat", ...)` on
`client.get_httpx_client()`.

API docs: https://yonyon.ai/developers. The npm CLI in the parent folder covers the same API.

## Regenerate

```bash
uvx --from openapi-python-client openapi-python-client generate \
  --path openapi.json --config openapi-generator-config.yml --meta uv --output-path . --overwrite
uv build
```

Refresh `openapi.json` from https://yonyon.ai/.well-known/openapi.json first. The generator rewrites
`README.md` and `pyproject.toml`, so restore both after regenerating: this README, `LICENSE`, and all
the hand-set `[project]` metadata (description, authors, license, license-files, keywords,
`[project.urls]`) plus the `build-system` bound.

## License

MIT. See [LICENSE](https://github.com/yonatangross/yonyon-cli/blob/main/python/LICENSE).
