all: help


help:
	@echo "Run update to update bloggers."


scan:
	$(CURDIR)/scan-feeds.py

update: out/report.yml
	$(CURDIR)/update-bloggers
	$(CURDIR)/update-participants.py

weekly: clean out/report.yml
	./weekly-update $@

clean:
	rm -rf out

out/report.yml:
	mkdir -p out
	$(CURDIR)/scan-feeds.py

post-update:
	make -C meta
	make -C meta post-update
	git push
