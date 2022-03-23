export VERSION=0.2

.PHONY: all
all:    version

.DEFAULT_GOAL := help

current_dir = $(shell pwd)

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#local-delete:	@ Delete local dev image with kim
local-delete:
	kim image rm devopstales/kube-openid-connector:$(VERSION)-devel

#local:	@ Build local devel image with kim
local: local-delete
	kim build --tag devopstales/kube-openid-connector:$(VERSION)-devel .

#devel:	@ Build local devel image
devel:
	docker build -t devopstales/kube-openid-connector:$(VERSION)-devel .

#push-devel: @ Docker push devel image
push-devel:
	docker push devopstales/kube-openid-connector:$(VERSION)-devel

#version: @ Build versiond docker image
version:
	docker build -t devopstales/kube-openid-connector:$(VERSION) .
#	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm32v7 --build-arg ARCH=arm32v7/ .
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm64v8 --build-arg ARCH=arm64v8/ .

#push-version: @ Docker push version image
push-version:
#	docker push devopstales/kube-openid-connector:$(VERSION)-arm32v7
	docker push devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker push devopstales/kube-openid-connector:$(VERSION)

#push-latest: @ Docker push version image as latest tag
push-latest:
	docker manifest create devopstales/kube-openid-connector:latest \
		--amend devopstales/kube-openid-connector:$(VERSION) \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker manifest push devopstales/kube-openid-connector:latest
#		--amend devopstales/kube-openid-connector:$(VERSION)-arm32v7 \