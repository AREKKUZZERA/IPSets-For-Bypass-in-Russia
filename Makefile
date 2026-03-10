.PHONY: test validate build deterministic-check release-validate

test:
	python -m pytest -q

validate:
	python -m scripts.validate --input-mode=hybrid

build:
	python -m scripts.build --input-mode=hybrid --profile=full --deterministic --checksums

deterministic-check:
	python -m scripts.check_deterministic_build --input-mode=hybrid --profile=full

release-validate:
	@if [ -z "$(TAG)" ]; then echo "Usage: make release-validate TAG=v1.2.3"; exit 1; fi
	python -m scripts.release_validate "$(TAG)"
