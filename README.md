# Folder description

1. ``code2docs-ui``: This consists of the main UI of the SaaS.
2. ``backend``: This is for backend code, which will be interacted with the ``demo-ui`` and the actual SaaS code (**under construction**).
3. ``demo-ui`` (Depreciated): This consist of the demo page in the frontend and the landing page in the frontend

# Setup

## code2docs-ui

1. Go to ``code2docs-ui`` directory

```
cd code2docs
```

2. Install all dependencies

```
npm i
```

3. Run locally

```
npm run dev
```

4. To access the main page, go to

```
http://localhost:5173/
```

## backend

1. Go to the backend directory

```
cd backend
```

2. Build and run the container

```
docker compose up --build
```

## demo-ui [Depreciated]

1. Go to the demo-ui directory

```
cd demo-ui
```

2. Intstall all dependencies

```
npm i
```

3. Run locally

```
npm run dev
```

4. To access the demo page, go to

```
http://localhost:5173/
```
