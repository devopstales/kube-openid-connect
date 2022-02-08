export VERSION=0.1
export C_RELEASE=0.1

.PHONY: all
all:    version

.DEFAULT_GOAL := all

current_dir = $(shell pwd)
token = ${GITHUB_TOKEN}

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

build-client:
	cp kubectl-login.py pyinstaller/kubectl-login.py
	cp requirements.txt pyinstaller/requirements.txt
	docker run -it -v $(current_dir)/pyinstaller/:/src kicsikrumpli/wine-pyinstaller \
		--clean -y \
		--dist ./dist/windows \
		--workpath /tmp \
		-F kubectl-login.py
	docker run -v "$(current_dir)/pyinstaller/:/src/" cdrx/pyinstaller-linux
	rm -f pyinstaller/kubectl-login.py
	rm -f pyinstaller/requirements.txt

deploy-client:
	cd pyinstaller/dist/linux; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_linux.tar.gz kubectl-login; \
	cd ../windows; \
	tar -czf kubectl-login_windows.tar.gz kubectl-login.exe
	mkdir -p pyinstaller/release
	mv pyinstaller/dist/windows/kubectl-login_windows.tar.gz pyinstaller/release
	mv pyinstaller/dist/linux/kubectl-login_linux.tar.gz pyinstaller/release
	gh release create client_v${C_RELEASE} --generate-notes ./pyinstaller/release/*.tar.gz
	rm -rf pyinstaller/release
