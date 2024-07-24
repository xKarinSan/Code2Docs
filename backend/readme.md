# Backend

## Setup
1. Go to the backend folder
```
cd backend
```
2. Install the dependencies in `requirements.txt`
```
pip install -r requirments.txt
```
3. Set up the environment variables in your `.env` file as such:
```
OPENAI_API_KEY = <open_ai_api_key>
OPENAI_MODEL = <fine_tuned_openai_model>
```
4. Run the project locally
```
python main.py
```
<hr>

## Routes

## GET
### /healthcheck
**Description**
This endpoint is for healthcheck. It will return a "Hello World" message if the API is working correctly.
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
| `message`              | string | Success message "Hello World"|

Example:
```
{
    'message': "Hello World"
}

```


## POST  
### /demo
**Description**
This documents the contents and returns a combined markdown string.

**Headers**
N/A

**Body Parameters**
| Attribute         | Type      | Required | Description           |
|-------------------|----------|----------|-----------------------|
| `file`              | string | Yes      | The name of an entity |

**Query Parameters**
N/A

**Response**
If successful, return `200` and the following response attribute(s):

| Attribute               | Type  | Description                  |
|-------------------------|-------|------------------------------|
| `data`              | string | The combined markdown documentation string of the contents in the zip file|

Example:
```
{
    'data': "Markdown documentation string"
}

```

If an incorrect file format (other than `.zip` files), return `400` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Invalid files" |

Example:
```
{
    'message': "Invalid files"
}
```


If unsuccessful, return `500` and the following response attribute(s):
| Attribute               | Type   | Description                  |
|-------------------------|--------|------------------------------|
| `message`              | string | Error message "Failed to generate documentation" |

Example:
```
{
    'message': "Failed to generate documentation."
}
```