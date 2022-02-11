export VERSION=0.1
export RELEASE=v0.1

.PHONY: all
all:    version

.DEFAULT_GOAL := all

current_dir = $(shell pwd)

devel-delete:
	kim image rm devopstales/kube-openid-connector:$(VERSION)-devel
#	rm -f  docker/server.py
#	rm -rf docker/templates
#	rm -rf docker/static

devel:
	cp server.py    docker/
	cp -r templates docker/
	cp -r static    docker/
	kim build --tag devopstales/kube-openid-connector:$(VERSION)-devel docker/
	rm -f  docker/server.py
#	rm -rf docker/templates
#	rm -rf docker/static

version:
	cp server.py docker/
	cp -r templates docker/
	cp -r static    docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION) docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm32v7 --build-arg ARCH=arm32v7/ docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm64v8 --build-arg ARCH=arm64v8/ docker/
	rm -f docker/server.py
	rm -rf docker/templates
	rm -rf docker/static

push-version:
	docker push devopstales/kube-openid-connector:$(VERSION)-arm32v7
	docker push devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker push devopstales/kube-openid-connector:$(VERSION)

push-latest:
	docker manifest create devopstales/kube-openid-connector:latest \
		--amend devopstales/kube-openid-connector:$(VERSION) \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm32v7 \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker manifest push devopstales/kube-openid-connector:latest
