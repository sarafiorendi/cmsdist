### RPM external bazel 0.11.1

Source: https://github.com/bazelbuild/bazel/releases/download/%{realversion}/bazel-%{realversion}-dist.zip
BuildRequires: java-env
%prep

%define __unzip unzip -d bazel-%{realversion}

%setup -q -n bazel-%{realversion}
sed -i -e 's|^## Release 0.11.1|## Release 0.9.0|' CHANGELOG.md
sed -i -e 's|^\( *\)supports_gold_linker *=.*|\1supports_gold_linker = False|' ./tools/cpp/unix_cc_configure.bzl

%build
bash ./compile.sh

%install
mkdir %{i}/bin
cp output/bazel %{i}/bin/.


