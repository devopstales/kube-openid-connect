export VERSION=0.1
export RELEASE=v0.1

.PHONY: all
all:    build

.DEFAULT_GOAL := all

current_dir = $(shell pwd)

build:
	rm -rf dist
	go build -o dist/linux/kubectl-login main.go
	env GOOS=darwin GOARCH=amd64 go build -o dist/osx/kubectl-login main.go
	env GOOS=windows GOARCH=amd64 go build -o dist/windows/kubectl-login.exe main.go

release:
	mkdir -p dist/release
	cd dist/linux; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_linux.tar.gz kubectl-login

	cd dist/windows; \
	tar -czf kubectl-login_windows.tar.gz kubectl-login.exe

	cd dist/osx; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_osx.tar.gz kubectl-login
	mv dist/windows/kubectl-login_windows.tar.gz release
	mv dist/linux/kubectl-login_linux.tar.gz release
	mv dist/kubectl-login_osx.tar.gz release
	gh release create client_v${C_RELEASE} --generate-notes ./dist/release/*.tar.gz
	rm -rf dist

