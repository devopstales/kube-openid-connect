SHELL:=/bin/bash
export VERSION=0.1

.PHONY: all
all:    build

.DEFAULT_GOAL := all

current_dir = $(shell pwd)

build:
	rm -rf dist
	go build -o dist/linux/kubectl-login main.go
	env GOOS=darwin GOARCH=amd64 go build -o dist/osx/kubectl-login main.go
	env GOOS=windows GOARCH=amd64 go build -o dist/windows/kubectl-login.exe main.go
#	docker run -v $(pwd):/src -w /src -it --rm  linuturk/mono-choco new kubectl-login

package:
	mkdir -p dist/release
	cd dist/linux; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_linux.tar.gz kubectl-login
	CHECKSUM=$$(sha256sum dist/linux/kubectl-login_linux.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_linux#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#version#/${VERSION}/" dist/homebrew/kubectl-login.rb

	cd dist/osx; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_osx.tar.gz kubectl-login
	CHECKSUM=$$(sha256sum dist/osx/kubectl-login_osx.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_osx#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb

	cd dist/windows; \
	zip kubectl-login_windows.zip kubectl-login.exe

	CHECKSUM=$$(sha256sum dist/windows/kubectl-login_windows.zip | cut -d ' ' -f1); \
	sed -i "s/#checksum#/$$CHECKSUM/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/kubectl-login.nuspec
	cp dist/windows/kubectl-login_windows.zip dist/choco/tools/
	docker run -v `pwd`/dist/choco/:/src -w /src -it --rm  linuturk/mono-choco pack
	rm -f dist/choco/tools/kubectl-login_windows.zip

release:
	mv dist/windows/kubectl-login_windows.zip dist/release/
	mv dist/linux/kubectl-login_linux.tar.gz dist/release/
	mv dist/osx/kubectl-login_osx.tar.gz dist/release/
	mv dist/choco/kubectl-login*.nupkg dist/release/
	gh release create client_v${VERSION} --generate-notes ./dist/release/*
	rm -rf dist/{windows,linux,osx,release}

