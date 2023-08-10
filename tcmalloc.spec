### RPM external tcmalloc 20230810

%define tag         1abe189ac8bd45cf5876a52f60f7c9c499a21e70
%define branch      master

%define tcmake_tag    8593b66738d6d657205584447d43dfe35aca8ecc
%define tcmake_branch master
%define tcmake_version  0.0.1

Source0: git+https://github.com/google/tcmalloc.git?obj=%{branch}/%{tag}&export=tcmalloc-%{realversion}&output=/tcmalloc-%{realversion}.tgz
Source1: git+https://github.com/ObiWahn/tcmalloc-cmake.git?obj=%{tcmake_branch}/%{tcmake_tag}&export=tcmalloc-cmake-%{tcmake_version}&output=tcmalloc-cmake-%{tcmake_version}.tgz

Requires: protobuf abseil-cpp 

%prep
%setup -D -T -b 0 -n tcmalloc-%{realversion}
%setup -D -T -b 1 -n tcmalloc-cmake-%{tcmake_version}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../tcmalloc-cmake-%{tcmake_version} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DTCMALLOC_TEST=OFF \
  -DTCMALLOC_SOURCE_DIR=$(readlink ../tcmalloc-%{realversion}) \
  -DCMAKE_PREFIX_PATH=%{cmake_prefix_path}

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install

