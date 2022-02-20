class KubectlLogin < Formula
  desc "An application that can be used to easily enable authentication flows via OIDC for a kubernetes cluster. "
  homepage "https://github.com/devopstales/kube-openid-connect/"
  license "Apache-2.0"
  version "#version#"

  if OS.mac?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v#version#/kubectl-login_osx.tar.gz"
    sha256 "#checksum_osx#"
  elsif OS.linux?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v#version#/kubectl-login_linux.tar.gz"
    sha256 "#checksum_linux#"
  end

  def install
    bin.install "kubectl-login"
  end

  test do
    system "kubectl-login test"
  end
end