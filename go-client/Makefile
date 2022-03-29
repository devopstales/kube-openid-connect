SHELL:=/bin/bash
export VERSION=1.0

.PHONY: all
all:    build

.DEFAULT_GOAL := help

current_dir = $(shell pwd)

#help:	@ List available tasks on this project
help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#'  | awk 'BEGIN {FS = ":.*?@ "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

#build: @ Build binaris with go
build:
	sed -i "s|AppVersion = .*|AppVersion = \"${VERSION}\"|" main.go
	rm -rf dist/{windows,linux,osx,release}
	go build -o dist/linux/kubectl-login main.go
	env GOOS=darwin GOARCH=amd64 go build -o dist/osx/kubectl-login main.go
	env GOOS=windows GOARCH=amd64 go build -o dist/windows/kubectl-login.exe main.go

#package: @ Create archives, brew and choco files
package:
	@echo "🎁 Packaging"
	mkdir -p dist/release

	cd dist/linux; \
	cp ../../../LICENSE .; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_linux.tar.gz kubectl-login LICENSE; \
	sha256sum kubectl-login_linux.tar.gz > kubectl-login_linux.tar.gz.sha256

	CHECKSUM=$$(sha256sum dist/linux/kubectl-login_linux.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_linux#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#version#/${VERSION}/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#checksum_linux#/$$CHECKSUM/" dist/krew/openid-connect.yaml; \
	sed -i "s/#version#/${VERSION}/" dist/krew/openid-connect.yaml;

	cd dist/osx; \
        cp ../../../LICENSE .; \
	chmod +x kubectl-login; \
	tar -czf kubectl-login_osx.tar.gz kubectl-login LICENSE; \
	sha256sum kubectl-login_osx.tar.gz > kubectl-login_osx.tar.gz.sha256

	CHECKSUM=$$(sha256sum dist/osx/kubectl-login_osx.tar.gz | cut -d ' ' -f1); \
	sed -i "s/#checksum_osx#/$$CHECKSUM/" dist/homebrew/kubectl-login.rb; \
	sed -i "s/#checksum_osx#/$$CHECKSUM/" dist/krew/openid-connect.yaml

	cd dist/windows; \
        cp ../../../LICENSE .; \
	zip kubectl-login_windows.zip kubectl-login.exe LICENSE; \
	sha256sum kubectl-login_windows.zip > kubectl-login_windows.zip.sha256

	CHECKSUM=$$(sha256sum dist/windows/kubectl-login_windows.zip | cut -d ' ' -f1); \
	sed -i "s/#checksum_windows#/$$CHECKSUM/" dist/krew/openid-connect.yaml; \
	sed -i "s/#checksum#/$$CHECKSUM/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/tools/VERIFICATION.txt; \
	sed -i "s/#version#/${VERSION}/" dist/choco/kubectl-login.nuspec
	cp dist/windows/kubectl-login_windows.zip dist/choco/tools/
	docker run -v `pwd`/dist/choco/:/src -w /src -it --rm  linuturk/mono-choco pack
	rm -f dist/choco/tools/kubectl-login_windows.zip

#release: @ Create release on github and publish choco package
release:
	mv dist/windows/kubectl-login_windows.zip* dist/release/
	mv dist/linux/kubectl-login_linux.tar.gz* dist/release/
	mv dist/osx/kubectl-login_osx.tar.gz* dist/release/
	mv dist/choco/kubectl-login*.nupkg dist/release/
	@echo "🤖 CD bot is Releasing to GitHub"
	gh release create client_v${VERSION} --generate-notes ./dist/release/*

	@echo "⬇️ Git checkout: homebrew-devopstales"
	git clone git@github.com:devopstales/homebrew-devopstales.git; \
	cd homebrew-devopstales; \
	git config user.name "devopstales"; \
	git config user.email "42894256+devopstales@users.noreply.github.com"; \
	rm -f kubectl-login.rb; \
	cp ../dist/homebrew/kubectl-login.rb .; \
	git add kubectl-login.rb; \
	git commit -m "release ${VERSION}"; \
	git push
	@echo "⬆️ Git push: homebrew-devopstales"

	@echo "⬇️ Git checkout: krew-index"
	git clone git@github.com:devopstales/krew-index.git; \
	cd krew-index/plugins; \
	git config user.name "devopstales"; \
	git config user.email "42894256+devopstales@users.noreply.github.com"; \
	rm -f openid-connect.yaml; \
	cp ../../dist/krew/openid-connect.yaml .; \
	git add openid-connect.yaml; \
	git commit -m "release ${VERSION}"; \
	git push
	@echo "⬆️ Git push: krew-index"

	@echo "🗑️ Cleaning repositoris"
	rm -rf dist/{windows,linux,osx,release}
	rm -f  dist/choco/kubectl-login.*.nupkg
	rm -rf homebrew-devopstales
	rm -rf krew-index

	@echo "🗑️ Cleaning git changes"
	git stash -- dist/choco/kubectl-login.nuspec
	git stash -- dist/choco/tools/VERIFICATION.txt
	git stash -- dist/homebrew/kubectl-login.rb
	git stash -- dist/krew/openid-connect.yaml
	@echo "🚀 Packages are deployed! 🎉"

#release-choco: @ Publish choco package
release-choco:
	@echo "⬆️ Push: Choco"
	docker run -v `pwd`/dist/choco/:/src -w /src -it --rm  linuturk/mono-choco push kubectl-login.${VERSION}.nupkg --key ${CHOCO_TOKEN} --source https://push.chocolatey.org/
