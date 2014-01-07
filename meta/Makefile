all: build


build: render


render:
	make -C notes

clean:
	rm -rf output

prod-render: clean
	make -C notes PELICAN_CONFIG=../prod.py

upload: prod-render
	cd output; \
	rsync -vr \
		. \
		tag@pault.ag:/srv/www/nginx/iron-blogger/

post-update: upload

.PHONY: render build all upload
