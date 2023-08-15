### RPM external tcmalloc 20230810

%define tag         1abe189ac8bd45cf5876a52f60f7c9c499a21e70
%define branch      master

Source0: git+https://github.com/google/tcmalloc.git?obj=%{branch}/%{tag}&export=tcmalloc-%{realversion}&output=/tcmalloc-%{realversion}.tgz

%prep
%setup -D -T -b 0 -n tcmalloc-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

%build
BAZELOPTS="--batch --output_user_root ../build build -s --verbose_failures --sandbox_debug --distinct_host_configuration=false"
BAZEL_OPTS="$BAZEL_OPTS --cxxopt=-std=c++%{cms_cxx_standard} %{makeprocesses}"

if [ -d ../build ] ; then
  chmod -R u+w  ../build
  rm -rf ../build
fi

bazel $BAZEL_OPTS //tcmalloc:tcmalloc

%install
# TODO: copy things back
