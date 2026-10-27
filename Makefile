.PHONY: install run debug clean lint lint-strict package

install:
	uv sync

run:
	uv run python3 -m pacman.main config.json

package:
	uv sync
	rm -rf build dist
	uv run --with pyinstaller pyinstaller --noconfirm --clean pacman.spec
	cp -r assets config.json dist/pacman/
	cp PACKAGE_README.txt dist/pacman/README.txt
	cd dist && zip -r pacman-linux.zip pacman

debug:
	uv run python3 -m pdb -m pacman.main config.json

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	uv run flake8 src/
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict