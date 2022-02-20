export VERSION=0.1
export RELEASE=v0.1

.PHONY: all
all:    build

.DEFAULT_GOAL := help

current_dir = $(shell pwd)

#help:	@ List available tasks on this project
help:
    @grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build:
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

release:
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
