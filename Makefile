typecheck:
	mypy plexlibrary/

lint:
	pylint plexlibrary/

checklist: lint typecheck

.PHONY: checklist
