# yonyon (Python)

Official Python client for the public [yonyon.ai](https://yonyon.ai) agent API, generated from the
OpenAPI spec at https://yonyon.ai/.well-known/openapi.json.

The API is public and read only. There is no key and no login. Rate limit: 10 requests per IP per
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

Every operation has `sync`, `sync_detailed`, `asyncio` and `asyncio_detailed` variants. Operations
live in `yonyon.api.default` (`ask_nlweb`, `ask_yonatan`, `list_projects`, `batch`, `create_job`,
`get_job`, and the index routes); models live in `yonyon.models`.

API docs: https://yonyon.ai/developers. The npm CLI in the parent folder covers the same API.

## Regenerate

```bash
uvx --from openapi-python-client openapi-python-client generate \
  --path openapi.json --config openapi-generator-config.yml --meta uv --output-path . --overwrite
uv build
```

Refresh `openapi.json` from https://yonyon.ai/.well-known/openapi.json first. Keep this README and
the `[project.urls]` block in `pyproject.toml` after regenerating.

## License

MIT. See [LICENSE](../LICENSE).
