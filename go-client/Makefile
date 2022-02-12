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
	echo "release client"
