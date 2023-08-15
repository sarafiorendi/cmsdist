### RPM external tcmalloc 20230810
## INCLUDE cpp-standard

%define tag         1abe189ac8bd45cf5876a52f60f7c9c499a21e70
%define branch      master

Source0: git+https://github.com/google/tcmalloc.git?obj=%{branch}/%{tag}&export=tcmalloc-%{realversion}&output=/tcmalloc-%{realversion}.tgz
BuildRequires: bazel

%prep
%setup -D -T -b 0 -n tcmalloc-%{realversion}

%build
# clear the build dir
if [ -d ../build ] ; then
  chmod -R u+w  ../build
  rm -rf ../build
fi

BAZEL_OPTS="--batch --output_user_root ../build build -s --verbose_failures --sandbox_debug --distinct_host_configuration=false"
BAZEL_OPTS="$BAZEL_OPTS --cxxopt=-std=c++%{cms_cxx_standard} %{makeprocesses}"

bazel $BAZEL_OPTS //tcmalloc:...

%install
# TODO: copy things back
# cd ../build
# mkdir -p %{i}/lib
# find . -name 'tcmalloc.lo' exec cp {} %{i}/lib/tcmalloc.a \;
# The path is something like build/825dd511a2caee396149d139e69a27b4/execroot/com_google_tcmalloc/bazel-out/k8-fastbuild/bin/tcmalloc/libtcmalloc.lo
