%{!?version: %define version %(make get-version)}
%{!?rel: %define rel %(make get-release)}
%{!?package_name: %define package_name %(make get-package_name)}
%{!?package_summary: %define package_summary %(make get-summary)}
%{!?package_description: %define package_description %(make get-description)}

%{!?formula_name: %define formula_name %(make get-formula_name)}
%{!?state_name: %define state_name %(make get-state_name)}
%{!?saltenv: %define saltenv %(make get-saltenv)}
%{!?pillar_dir: %define pillar_dir %(make get-pillar_dir)}
%{!?formula_dir: %define formula_dir %(make get-formula_dir)}

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:      %{package_name}
Version:   %{version}
Release:   %{rel}%{?dist}
Summary:   %{package_summary}
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
%{package_description}

%package libs
Summary:	Qubes+Salt management override libs
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
%{__python} setup.py install -O1 --skip-build --install-lib %{python_sitearch} --root %{buildroot}
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} BINDIR=%{_bindir} SBINDIR=%{_sbindir} SYSCONFDIR=%{_sysconfdir}

%clean
rm -rf build/ *.pyc *.pyo *.o *.a *~

%post
# Update Salt Configuration
qubesctl saltutil.clear_cache -l quiet --out quiet > /dev/null || true
qubesctl saltutil.sync_all refresh=true -l quiet --out quiet > /dev/null || true

%files
%defattr(-,root,root)
%doc LICENSE README.rst
%attr(750, root, root) %dir /srv/salt/_modules
/srv/salt/_modules/localemod.py*

%files libs
%{python_sitearch}/qubes/*
%{python_sitearch}/qubes.mgmt*-*-py?.?.egg-info

%changelog
