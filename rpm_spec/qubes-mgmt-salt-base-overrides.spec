%{!?version: %define version %(cat version)}

#%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:      qubes-mgmt-salt-base-overrides
Version:   %{version}
Release:   1%{?dist}
Summary:   Custom modules to override existing Salt modules due to upstream bugs or implementation conflicts
License:   GPL 2.0
URL:	   http://www.qubes-os.org/

Group:     System administration tools
BuildArch: noarch
Requires:  salt
Requires:  salt-minion
Requires:  qubes-mgmt-salt-config
Requires:  qubes-mgmt-salt-base-overrides-libs

%define _builddir %(pwd)

%description
Custom modules to override existing Salt modules due to upstream bugs or implementation conflicts

%package libs
Summary:   Qubes+Salt management override libs
Group:     System administration tools
Requires:  salt
Requires:  salt-minion
Requires:  qubes-mgmt-salt-config
Requires:  python
Requires:  python-wrapt
BuildRequires:  python2-devel

%description libs
Qubes+Salt management override libs.

%prep
# we operate on the current directory, so no need to unpack anything
# symlink is to generate useful debuginfo packages
rm -f %{name}-%{version}
ln -sf . %{name}-%{version}
%setup -T -D

%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --install-lib %{python_sitelib} --root %{buildroot}
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%clean
rm -rf build/ *.pyc *.pyo *.o *.a *~

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/salt/_modules
/srv/salt/_modules/localemod.py*

%files libs
%{python_sitelib}/qubessaltpatches/*
%{python_sitelib}/qubessaltpatches*-*-py?.?.egg-info

%changelog
