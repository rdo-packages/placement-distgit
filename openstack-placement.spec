# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 0
%global with_trans %{!?_without_trans:1}%{?_without_trans:0}
%global distro  RDO
# Workaround until placement has an actual release

%global common_desc \
OpenStack resource provider inventory allocation service

Name:             openstack-placement
Epoch:            1
Version:          1.0.0
Release:          1
Summary:          OpenStack Placement

License:          ASL 2.0
URL:              http://openstack.org/projects/placement/

# Workaround until placement has an actual release
# Source0:          https://tarballs.openstack.org/nova/nova-upstream_version.tar.gz
#Source0:          https://github.com/openstack/placement/archive/%{commit_SHA}.tar.gz
Source0:          placement-dist.conf
Source1:          placement.logrotate
Source2:          placement-api.conf
Source3:          policy.json
 
BuildArch:        noarch
BuildRequires:    openstack-macros
BuildRequires:    intltool
BuildRequires:    python%{pyver}-devel
BuildRequires:    git
BuildRequires:    python%{pyver}-os-traits >= 0.4.0
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-oslo-policy

Requires:         openstack-placement-api = %{epoch}:%{version}-%{release}

%description 
%{common_desc}

%package api
Summary:          OpenStack Placement API service

Requires:         httpd
Requires:         mod_wsgi

%description api
%{common_desc}

This package contains the Placement service, which will initially
allow for the management of resource providers.

%package -n       python%{pyver}-placement
Summary:          Placement Python libraries
%{?python_provide:%python_provide python%{pyver}-placement}

%description -n   python%{pyver}-placement
%{common_desc}

This package contains the Placement Python library.

%prep
%autosetup -n openstack-placement-master -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find placement -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
%{pyver_bin} setup.py build

%install
%{pyver_install}

install -d -m 750 %{buildroot}%{_localstatedir}/log/placement

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/placement
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/placement/placement-dist.conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/00-placement-api.conf

# Install empty policy.json file to cover rpm updates with untouched policy files.
install -p -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/placement/policy.json

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-placement

%files
%license LICENSE
%dir %{_datarootdir}/placement
%attr(-, root, placement) %{_datarootdir}/placement/placement-dist.conf
%dir %{_sysconfdir}/placement
%config(noreplace) %attr(-, root, placement) %{_sysconfdir}/placement/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-placement
%dir %attr(0750, placement, root) %{_localstatedir}/log/placement

%files api
%config(noreplace) %{_sysconfdir}/httpd/conf.d/00-placement-api.conf
%{_bindir}/placement-api

%files -n python%{pyver}-placement
%license LICENSE
%{pyver_sitelib}/placement
%{pyver_sitelib}/placement-*.egg-info
%exclude %{pyver_sitelib}/placement/tests

%changelog

