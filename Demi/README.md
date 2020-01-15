# With Docker

## Build

```
docker build --tag icup2020_example .
```

## Run

```
docker run --publish 50123:50123 --interactive --tty --rm icup2020_example
```

# With GNU Make

This example uses GNU Make. You may use any other free (= at no charge) build system.

## Setup

```
make setup
```

## Run

```
make
```

# Usage
```
-i --ip :ip to listen on for requests
    [default 0.0.0.0]

-p --port:port to listen on for requests
    [default 50123]
```
