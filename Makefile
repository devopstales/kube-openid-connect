export VERSION=0.1

.PHONY: all
all:    version

.DEFAULT_GOAL := all

devel:
	cp server.py docker/
	kim build --tag devopstales/kube-openid-connector:$(VERSION)-devel docker/
	rm -f docker/server.py

version:
	cp server.py docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION) docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm32v7 --build-arg ARCH=arm32v7/ docker/
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm64v8 --build-arg ARCH=arm64v8/ docker/
	rm -f docker/server.py

push-devel:
	docker push devopstales/kube-openid-connector:$(VERSION)-devel

push:
	docker push devopstales/kube-openid-connector:$(VERSION)-arm32v7
	docker push devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker push devopstales/kube-openid-connector:$(VERSION)
	docker manifest create devopstales/kube-openid-connector:latest \
		--amend devopstales/kube-openid-connector:$(VERSION) \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm32v7 \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker manifest push devopstales/kube-openid-connector:latest
