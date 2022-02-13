class KubectlLogin < Formula
  desc "An application that can be used to easily enable authentication flows via OIDC for a kubernetes cluster. "
  homepage "https://github.com/devopstales/kube-openid-connect/"
  license "Apache-2.0"
  version "0.1"

  if OS.mac?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v0.1/kubectl-login_osx.tar.gz"
    sha256 "bed8b7bf796129943adabcda66fd3574e508a384040074a1be3561a70f32cd81"
  elsif OS.linux?
    url "https://github.com/devopstales/kube-openid-connect/releases/download/client_v0.1/kubectl-login_linux.tar.gz"
    sha256 "f57602e427507b91b2b4a25fc5786c7514d3ea3243bd191f9feae6d79d69a9c7"
  end

  def install
    bin.install "kubectl-login"
  end

  test do
    system "kubectl-login test"
  end
end