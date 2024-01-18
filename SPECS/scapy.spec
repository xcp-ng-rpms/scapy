%global package_speccommit 10a7bc9582ad6e6af0c8595b69a82fad91f83588
%global usver 2.4.5
%global xsver 3
%global xsrel %{xsver}%{?xscount}%{?xshash}
Name:           scapy
Version:        2.4.5
Release:        %{?xsrel}%{?dist}
Summary:        Interactive packet manipulation tool and network scanner

%global         gituser         secdev
%global         gitname         scapy

License:        GPLv2
URL:            http://www.secdev.org/projects/scapy/
#               https://github.com/secdev/scapy/releases
#               https://bitbucket.org/secdev/scapy/pull-request/80
#               https://scapy.readthedocs.io/en/latest/introduction.html
Source0: scapy-2.4.5.tar.gz

%global         common_desc %{expand:
Scapy is a powerful interactive packet manipulation program built on top
of the Python interpreter. It can be used to forge or decode packets of
a wide number of protocols, send them over the wire, capture them, match
requests and replies, and much more.}


# By default build with python3 subpackage
%bcond_without     python3
%bcond_with        doc

# Build python2 for xs8 for backword compatbility
%if 0%{?xenserver} < 9
%bcond_without python2
%else
%bcond_with python2
%endif

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  sed

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools


%if 0%{?with_python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%endif

%description %{common_desc}

%package -n python%{python3_pkgversion}-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python%{python3_pkgversion}-%{name}}
Provides:       %{name} = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}
%{common_desc}

%if 0%{?with_python2}
%package -n python2-%{name}
Summary:        Interactive packet manipulation tool and network scanner

%{?python_provide:%python_provide python2-%{name}}

%description -n python2-%{name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package doc
Summary:        Interactive packet manipulation tool and network scanner

BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx_rtd_theme

%description doc
%{common_desc}
%endif


%prep
%autosetup -p 1 -n %{name}-%{version}

# Remove shebang
# https://github.com/secdev/scapy/pull/2332
SHEBANGS=$(find ./scapy -name '*.py' -print | xargs grep -l -e '^#!.*env python')
for FILE in $SHEBANGS ; do
    sed -i.orig -e 1d "${FILE}"
    touch -r "${FILE}.orig" "${FILE}"
    rm "${FILE}.orig"
done



%build

%if 0%{?with_python2}
%py2_build
%endif

%py3_build

%if 0%{?with_doc}
make -C doc/scapy html BUILDDIR=_build_doc SPHINXBUILD=sphinx-build-%python3_version

rm -f doc/scapy/_build_doc/html/.buildinfo
rm -f doc/scapy/_build_doc/html/_static/_dummy
%endif



%install
install -dp -m0755 %{buildroot}%{_mandir}/man1
install -Dp -m0644 doc/scapy.1* %{buildroot}%{_mandir}/man1/

%if 0%{?with_python2}
%py2_install
rm -f %{buildroot}%{python2_sitelib}/*egg-info/requires.txt

# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy2
mv -f %{buildroot}%{_bindir}/UTscapy %{buildroot}%{_bindir}/UTscapy2
%endif

%py3_install
rm -f %{buildroot}%{python3_sitelib}/*egg-info/requires.txt

# Rename the executables
mv -f %{buildroot}%{_bindir}/scapy   %{buildroot}%{_bindir}/scapy3
mv -f %{buildroot}%{_bindir}/UTscapy %{buildroot}%{_bindir}/UTscapy3

# Link the default to the python3 version of executables
ln -s %{_bindir}/scapy3   %{buildroot}%{_bindir}/scapy
ln -s %{_bindir}/UTscapy3 %{buildroot}%{_bindir}/UTscapy


# check
# TODO: Need to fix/remove slow/failed test
# cd test/
# ./run_tests_py2 || true
# ./run_tests_py3 || true


%files -n python%{python3_pkgversion}-%{name}
%license LICENSE
%doc %{_mandir}/man1/scapy.1*
%{_bindir}/scapy
%{_bindir}/UTscapy
%{_bindir}/scapy3
%{_bindir}/UTscapy3
%{python3_sitelib}/scapy/
%{python3_sitelib}/scapy-*.egg-info

%if 0%{?with_python2}
%files -n python2-%{name}
%license LICENSE
%{_bindir}/scapy2
%{_bindir}/UTscapy2
%{python2_sitelib}/scapy/
%{python2_sitelib}/scapy-*.egg-info
%endif

%if 0%{?with_doc}
%files doc
%doc doc/scapy/_build_doc/html
%endif


%changelog
* Fri Nov 24 2023 Lin Liu <lin.liu@citrix.com> - 2.4.5-3
- Build py2 for xs8 for backworkd compatibility

* Tue Nov 21 2023 Lin Liu <lin.liu@citrix.com> - 2.4.5-2
- Remove python3-tox from BuildRequires as test not run

* Fri Aug 11 2023 Lin Liu <lin.liu@citrix.com> - 2.4.5-1
- First imported release

