SHELL:=/bin/bash
export VERSION=0.2

.PHONY: all
all:    build

.DEFAULT_GOAL := help

current_dir = $(shell pwd)

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#build: @ Build binaris with go
build:
	rm -rf dist/{windows,linux,osx,release}
	go build -o dist/linux/kubectl-login main.go
	env GOOS=darwin GOARCH=amd64 go build -o dist/osx/kubectl-login main.go
	env GOOS=windows GOARCH=amd64 go build -o dist/windows/kubectl-login.exe main.go

#package: @ Create archives, brew and choco files
package:
	@echo "🎁 Packaging"
	mkdir -p dist/release

	cd dist/linux; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_linux.tar.gz kubectl-login; \
	sha256sum dist/linux/kubectl-login_linux.tar.gz > dist/linux/kubectl-login_linux.tar.gz.sha256

	CHECKSUM=$$(sha256sum dist/linux/kubectl-login_linux.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_linux#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#version#/${VERSION}/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#checksum_linux#/$$CHECKSUM/" dist/krew/openid-connect.yaml; \
	sed -i "s/#version#/${VERSION}/" dist/krew/openid-connect.yaml;

	cd dist/osx; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_osx.tar.gz kubectl-login; \
	sha256sum dist/linux/kubectl-login_osx.tar.gz > dist/linux/kubectl-login_osx.tar.gz.sha256

	CHECKSUM=$$(sha256sum dist/osx/kubectl-login_osx.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_osx#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#checksum_osx#/$$CHECKSUM/" dist/krew/openid-connect.yaml

	cd dist/windows; \
	zip kubectl-login_windows.zip kubectl-login.exe; \
	sha256sum dist/linux/kubectl-login_windows.zip > dist/linux/kubectl-login_windows.zip.sha256

	CHECKSUM=$$(sha256sum dist/windows/kubectl-login_windows.zip | cut -d ' ' -f1); \
	ed -i "s/#checksum_windows#/$$CHECKSUM/" dist/krew/openid-connect.yaml; \
	sed -i "s/#checksum#/$$CHECKSUM/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/kubectl-login.nuspec
	cp dist/windows/kubectl-login_windows.zip dist/choco/tools/
	docker run -v `pwd`/dist/choco/:/src -w /src -it --rm  linuturk/mono-choco pack
	rm -f dist/choco/tools/kubectl-login_windows.zip

#release: @ Create release on github and publish choco package
release:
	@echo "🤖 CD bot is DReleasing

	mv dist/windows/kubectl-login_windows.zip* dist/release/
	mv dist/linux/kubectl-login_linux.tar.gz* dist/release/
	mv dist/osx/kubectl-login_osx.tar.gz* dist/release/
	mv dist/choco/kubectl-login*.nupkg dist/release/
	gh release create client_v${VERSION} --generate-notes ./dist/release/*

#	docker run -v `pwd`/dist/choco/:/src -w /src -it --rm  linuturk/mono-choco push kubectl-login.${VERSION}.nupkg --key ${CHOCO_TOKEN} --source https://push.chocolatey.org/

	git clone git@github.com:devopstales/homebrew-devopstales.git; \
	cd homebrew-devopstales; \
	git config user.name "devopstales"; \
	git config user.email "42894256+devopstales@users.noreply.github.com"; \
	rm -f kubectl-login.rb; \
	cp ../dist/homebrew/kubectl-login.rb .; \
	git add kubectl-login.rb && git commit -m "release ${VERSION}"; \
	git push

	git clone git@github.com:devopstales/krew-index.git; \
	cd krew-index/plugins; \
	git config user.name "devopstales"; \
	git config user.email "42894256+devopstales@users.noreply.github.com"; \
	rm -f openid-connect.yaml; \
	cp ../../dist/krew/openid-connect.yaml; \
	git add openid-connect.yaml && git commit -m "release ${VERSION}"; \
	git push

#	rm -rf dist/{windows,linux,osx,release}
#	rm -rf homebrew-devopstales
#	rm -rf krew-index
	@echo "🚀 Packages are deployed!"

