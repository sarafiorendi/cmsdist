### RPM external pyqt 4.8.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
#Source: http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-%realversion.tar.gz
Source: http://cmsrep.cern.ch/cmssw/pyqt-mirror/PyQt-x11-gpl-%realversion.tar.gz
Patch0: pyqt-relocatable-build
Patch1: pyqt-fix-qt-conf-relocation-on-macosx
Requires: python
Requires: qt
Requires: sip

%prep
%setup -n PyQt-x11-gpl-%realversion
# pyqt builds and uses an helper program "qtdirs" to determine where qt is installed.
# We had to patch its sources so that it reads the configuration file qt.conf
# like other qt applications, so that we get the correctly relocated information.
# Notice that in the build section we copy qt.conf from the QT installation to 
# get the correct location.
%patch0 -p1
%patch1 -p0

%build
# See above for explanation.
cp $QT_ROOT/bin/qt.conf . 
# Build with system compiler even when building with gcc 4.6.1, since thats the
# only way one can actually get the cocoa stuff to build. 
case %cmsos in
  osx*_*_gcc421) ;;
  osx*)
    export PATH=/usr/bin:$PATH
  ;;
esac

echo yes | python ./configure.py --verbose -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages \
                                 -e %i/include \
                                `find $QT_ROOT/include/ -type d | xargs -n 1 basename| grep -v include | xargs echo | sed -e 's| | --enable=|g;s|^|--enable=|'` 

make %makeprocesses

%install
make install

mkdir -p %i/etc/profile.d
cat << \EOF_INIT_ME > %i/etc/profile.d/init-standalone.sh
#!/bin/sh
source @GCC_ROOT@/etc/profile.d/init.sh
source @BZ2LIB_ROOT@/etc/profile.d/init.sh
source @EXPAT_ROOT@/etc/profile.d/init.sh
source @DB4_ROOT@/etc/profile.d/init.sh
source @GDBM_ROOT@/etc/profile.d/init.sh
source @ZLIB_ROOT@/etc/profile.d/init.sh
source @OPENSSL_ROOT@/etc/profile.d/init.sh
source @PYTHON_ROOT@/etc/profile.d/init.sh
source @QT_ROOT@/etc/profile.d/init.sh
source @SIP_ROOT@/etc/profile.d/init.sh
source %i/etc/profile.d/init.sh
EOF_INIT_ME

perl -p -i -e "s|\@([^@]*)\@|\$ENV{\$1}|" %i/etc/profile.d/init-standalone.sh

%post
%{relocateConfig}etc/profile.d/init-standalone.sh
