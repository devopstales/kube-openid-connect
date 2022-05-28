export VERSION=1.1

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

#devel-push: @ Docker push devel image
devel-push:
	docker push devopstales/kube-openid-connector:$(VERSION)-devel

#version: @ Build versiond docker image
version:
#	docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
	docker build -t devopstales/kube-openid-connector:$(VERSION)-amd64 --build-arg ARCH=amd64/ .
	docker build -t devopstales/kube-openid-connector:$(VERSION)-arm64v8 --build-arg ARCH=arm64v8/ .
#       docker build -t devopstales/kube-openid-connector:$(VERSION)-arm32v7 --build-arg ARCH=arm32v7/ .


#version-push: @ Docker push version image
version-push:
	docker push devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker push devopstales/kube-openid-connector:$(VERSION)-amd64
	docker manifest create devopstales/kube-openid-connector:$(VERSION) \
		--amend devopstales/kube-openid-connector:$(VERSION)-amd64 \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker manifest push devopstales/kube-openid-connector:$(VERSION)

#       docker push devopstales/kube-openid-connector:$(VERSION)-arm32v7
#               --amend devopstales/kube-openid-connector:$(VERSION)-arm32v7 \

#push-latest: @ Docker push version image as latest tag
push-latest:
	docker manifest create devopstales/kube-openid-connector:latest \
		--amend devopstales/kube-openid-connector:$(VERSION)-amd64 \
		--amend devopstales/kube-openid-connector:$(VERSION)-arm64v8
	docker manifest push devopstales/kube-openid-connector:latest

#		--amend devopstales/kube-openid-connector:$(VERSION)-arm32v7 \

#release: @ Create Github release for server
release:
	@echo "🤖 CD bot is Releasing to GitHub"
	gh release create server_v${VERSION} --generate-notes
