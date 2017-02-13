.PHONY: run
run:
	lycos run


.PHONY: format
format:
	yapf -ri .


.PHONY: pep257
pep257:
	pep257 cli lib lycosidae