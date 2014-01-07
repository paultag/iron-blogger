all: help


help:
	@echo "Run update to update bloggers."


scan:
	$(CURDIR)/scan-feeds.py


update:
	$(CURDIR)/update-participants.py
	$(CURDIR)/update-bloggers
