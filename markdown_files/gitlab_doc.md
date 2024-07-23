## API name

> - History note.

One or two sentence description of what endpoint does.

### Method title

> - History note.

Description of the method.

```plaintext
METHOD /api/v4/endpoint
```

Supported attributes:

| Attribute                | Type     | Required | Description           |
|--------------------------|----------|----------|-----------------------|
| `attribute`              | datatype | Yes      | Detailed description. |
| `attribute`              | datatype | No       | Detailed description. |
| `attribute`              | datatype | No       | Detailed description. |
| `attribute`              | datatype | No       | Detailed description. |

If successful, returns [`<status_code>`](rest/index.md#status-codes) and the following
response attributes:

| Attribute                | Type     | Description           |
|--------------------------|----------|-----------------------|
| `attribute`              | datatype | Detailed description. |
| `attribute`              | datatype | Detailed description. |

Example request:

```shell
curl --header "PRIVATE-TOKEN: <your_access_token>" \
  --url "https://gitlab.example.com/api/v4/endpoint?parameters"
```

Example response:

```json
[
  {
  }
]
```
