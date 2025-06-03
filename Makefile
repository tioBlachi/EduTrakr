up:
    COMPOSE_BAKE=1 docker compose up --build

down:
    docker compose down

rebuild:
    COMPOSE_BAKE=1 docker compose up --build --force-recreate
