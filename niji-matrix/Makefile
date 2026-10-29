.PHONY: validate content-validate planning-validate catalog audit-libraries reader-prose-audit status test quality

validate:
	python3 scripts/validate.py
	python3 scripts/validate_planning.py
	python3 scripts/audit_duplicates.py --fail-on exact

content-validate:
	python3 scripts/validate.py

planning-validate:
	python3 scripts/validate_planning.py

catalog:
	python3 scripts/library_catalog.py

audit-libraries:
	python3 scripts/audit_duplicates.py --fail-on exact

reader-prose-audit:
	python3 scripts/audit_reader_prose.py

status:
	python3 scripts/pipeline_status.py

test:
	python3 -m unittest discover -s tests

quality: validate reader-prose-audit test catalog
