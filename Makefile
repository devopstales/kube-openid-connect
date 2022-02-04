export VERSION=0.1
export RELEASE=v0.1

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

build-client:
	pyinstaller --onefile --noconfirm --noconsole --clean --log-level=WARN --key=${BUILDSECRET} --strip kubectl-auth.py
	cp dist/kubectl-auth dist/kubeauth

deploy-client:
	git tag ${RELEASE}
	git push --force --tags
