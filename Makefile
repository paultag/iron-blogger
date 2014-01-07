all: help


help:
	@echo "Run update to update bloggers."


scan:
	$(CURDIR)/scan-feeds.py

update:
	$(CURDIR)/scan-feeds.py
	$(CURDIR)/update-bloggers
	$(CURDIR)/update-participants.py

post-update:
	make -C meta
	make -C meta post-update
