appname = aa-rss-to-discord
package = aa_rss_to_discord

help:
	@echo "Makefile for $(appname)"

translationfiles:
	cd $(package) && \
	django-admin makemessages -l en --ignore 'build/*' && \
	django-admin makemessages -l de --ignore 'build/*' && \
	django-admin makemessages -l es --ignore 'build/*' && \
	django-admin makemessages -l ko --ignore 'build/*' && \
	django-admin makemessages -l ru --ignore 'build/*' && \
	django-admin makemessages -l zh_Hans --ignore 'build/*'

compiletranslationfiles:
	cd $(package) && \
	django-admin compilemessages -l en  && \
	django-admin compilemessages -l de  && \
	django-admin compilemessages -l es  && \
	django-admin compilemessages -l ko  && \
	django-admin compilemessages -l ru  && \
	django-admin compilemessages -l zh_Hans

graph_models:
	python ../myauth/manage.py graph_models $(package) --arrow-shape normal -o $(appname)-models.png

build_test:
	rm -rfv dist && \
	rm -rfv build && \
	python3 setup.py sdist bdist_wheel
