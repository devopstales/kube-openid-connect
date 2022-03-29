class KubectlLogin < Formula
  desc "An application that can be used to easily enable authentication flows via OIDC for a kubernetes cluster. "
  homepage "https://github.com/devopstales/kube-openid-connect/"
  license "Apache-2.0"
  version "1.0"

  if OS.mac?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v1.0/kubectl-login_osx.tar.gz"
    sha256 "c96dda6c7135dfb58a3b72fec7aea29a090f13780b45bf2bcc8368451887fc9f"
  elsif OS.linux?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v1.0/kubectl-login_linux.tar.gz"
    sha256 "cc760ca6fd80d215e5b42a6f5c38a4dcb38707a8fc7b4ee336cd9204e3b4f2f6"
  end

  def install
    bin.install "kubectl-login"
  end

  test do
    system "kubectl-login test"
  end
end