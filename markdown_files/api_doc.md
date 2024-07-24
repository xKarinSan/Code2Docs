## Entity

### Methods
**GET**
- /entity
- /entity/:id

**POST**
- /entity

**PUT**
- /entity/:id

**DELETE**
- /entity/:id
<hr>

## GET  
### /entity
**Description**
Return an array of Entity

**Headers**
N/A

**Body Parameters**
N/A

**Query Parameters**
N/A

**Response**
If successful, return `200` and the following response attribute(s):

| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `entities`              | array | An array of all the entities |

Example:
```
{
    'entities':[
        {
            'id':id,
            'name':'name',
            'desc':'desc'
        },
        ...
    ]
}

```

If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Retrieval failed" |

Example:
```
{
    'message':"Retrieval failed."
}
```


### entity/:id
**Description**
return an entity with a given ID

**Headers**
N/A

**Body Parameters**
N/A

**Query Parameters**
| Attribute          Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `id`              | integer | Yes      | The ID of an entity |

**Response**
If an `Entity` is found, return `200` and the following response attribute(s):

| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `entity`              | object | An JSON representation of the Entity |

Example:
```
{
    'entity':{
        'id':id,
        'name':'name',
        'desc':'desc'
    }
}

```

If the Entity is not found, return `404` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Entity not found" |

Example:
```
{
    'message':"Entity not found."
}
```


If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Retrieval failed" |

Example:
```
{
    'message':"Retrieval failed."
}
```

## POST  
### /entity
**Description**
Create a new Entity

**Headers**
N/A

**Body Parameters**
| Attribute         | Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `name`              | string | Yes      | The name of an entity |
| `desc`              | string | Yes      | The description of an entity |

**Query Parameters**
N/A

**Response**
If successful, return `100` and the following response attribute(s):

| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `message`              | array | Success message "Creation successful"|

Example:
```
{
    'message': "Creation successful"
}

```

If missing parameters or invalid, return `400` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Invalid parameters |

Example:
```
{
    'message':"Invalid parameters."
}
```

If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Retrieval failed" |

Example:
```
{
    'message':"Retrieval failed."
}
```

## PUT  
### /entity:id
**Description**
Update an existing Entity

**Headers**
N/A

**Body Parameters**
| Attribute         | Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `name`              | string | Yes      | The name of an entity |
| `desc`              | string | Yes      | The description of an entity |

**Query Parameters**
| Attribute          Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `id`              | integer | Yes      | The ID of an entity |

**Response**
If successful, return `100` and the following response attribute(s):
| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `message`              | array | Success message "Update successful"|

Example:
```
{
    'message': "Creation successful"
}

```

If the Entity is not found, return `404` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Entity not found" |

Example:
```
{
    'message':"Entity not found."
}
```

If missing parameters or invalid, return `400` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Invalid parameters |

Example:
```
{
    'message':"Invalid parameters."
}
```

If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Retrieval failed" |

Example:
```
{
    'message':"Update failed."
}
```

## Delete  
### /entity:id
**Description**
Update an existing Entity
**Headers**
N/A
**Body Parameters**
N/A
**Query Parameters**
| Attribute          Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `id`              | integer | Yes      | The ID of an entity |
**Response**
If successful, return `100` and the following response attribute(s):
| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `message`              | array | Success message "Deletion successful"|

Example:
```
{
    'message': "Deletion successful"
}

```

If the Entity is not found, return `404` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Entity not found" |
Example:
```
{
    'message':"Entity not found."
}
```

If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Deletion failed" |

Example:
```
{
    'message':"Deletion failed."
}
```

