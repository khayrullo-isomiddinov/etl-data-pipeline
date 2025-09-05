.PHONY: build init-db load-papaya load-kumquat dedup analytics views test clean all

build:
	docker compose build
init-db:
	docker compose run --rm aumovio python scripts/create_db.py

load-papaya:
	docker compose run --rm aumovio python scripts/load_papaya.py

load-kumquat:
	docker compose run --rm aumovio python scripts/load_kumquat.py

dedup:
	docker compose run --rm aumovio python scripts/dedup_labels.py

analytics:
	docker compose run --rm aumovio python scripts/run_analytics.py

views:
	docker compose run --rm aumovio python scripts/create_views.py

test:
	docker compose run --rm aumovio pytest -q

clean:
	rm -f databases/*.db reports/*.csv

all: build init-db load-papaya load-kumquat dedup analytics
	@echo "Full pipeline complete! DB is in ./databases, reports are in ./reports"
