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

%global common_desc \
OpenStack Placement provides an HTTP service for managing, selecting, and \
claiming providers of classes of inventory representing available resources \
in a cloud.

Name:             openstack-placement
Version:          XXX
Release:          XXX
Summary:          OpenStack Placement

License:          ASL 2.0
URL:              http://git.openstack.org/cgit/openstack/placement/

Source0:          https://tarballs.openstack.org/placement/placement-%{upstream_version}.tar.gz
Source1:          placement-dist.conf
Source2:          placement.logrotate
Source3:          placement-api.conf
Source4:          policy.json

BuildArch:        noarch
BuildRequires:    openstack-macros
BuildRequires:    intltool
BuildRequires:    python%{pyver}-devel
BuildRequires:    git
BuildRequires:    python%{pyver}-os-traits
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-six
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-os-testr

%description
%{common_desc}

%package common
Summary:          Components common to all OpenStack Placement services
Requires:         python%{pyver}-placement = %{version}-%{release}

%description common
%{common_desc}

This package contains scripts, config and dependencies shared
between all the OpenStack Placement services.

%package api
Summary:          OpenStack Placement API service

Requires:         placement-common = %{version}-%{release}
Requires:         httpd
Requires:         mod_wsgi

%description api
%{common_desc}

This package contains the Placement service, which will initially
allow for the management of resource providers.

%package -n       python%{pyver}-placement
Summary:          Placement Python libraries
%{?python_provide:%python_provide python%{pyver}-placement}

Requires:         python%{pyver}-sqlalchemy >= 1.0.10
Requires:         python%{pyver}-routes >= 2.3.1
Requires:         python%{pyver}-webob >= 1.8.2
Requires:         python%{pyver}-keystonemiddleware >= 4.17.0
Requires:         python%{pyver}-jsonschema >= 2.6.0
Requires:         python%{pyver}-microversion-parse >= 0.2.1
Requires:         python%{pyver}-os-traits
Requires:         python%{pyver}-oslo-concurrency >= 3.26.0
Requires:         python%{pyver}-oslo-config >= 2:6.1.0
Requires:         python%{pyver}-oslo-context >= 2.19.2
Requires:         python%{pyver}-oslo-db >= 4.40.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-log >= 3.36.0
Requires:         python%{pyver}-oslo-middleware >= 3.31.0
Requires:         python%{pyver}-oslo-serialization >= 2.18.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:         python%{pyver}-pbr
Requires:         python%{pyver}-requests >= 2.14.2
Requires:         python%{pyver}-six >= 1.10.0

%description -n   python%{pyver}-placement
%{common_desc}

This package contains the Placement Python library.

%package -n python%{pyver}-placement-tests
Summary:        Placement tests
%{?python_provide:%python_provide python%{pyver}-placement-tests}
Requires:       openstack-placement = %{version}-%{release}

%description -n python%{pyver}-placement-tests
%{common_desc}

This package contains the Placement Python library tests.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Placement

BuildRequires:    graphviz

# Required to build module documents
BuildRequires:    python%{pyver}-oslo-config
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-routes
BuildRequires:    python%{pyver}-sphinxcontrib-actdiag
BuildRequires:    python%{pyver}-sphinxcontrib-seqdiag
BuildRequires:    python%{pyver}-sqlalchemy
BuildRequires:    python%{pyver}-webob

%description      doc
%{common_desc}

This package contains documentation files for Placement.
%endif

%prep
%autosetup -n openstack-placement-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find placement -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

# Remove the requirements file so that pbr hooks don't add it
# to distutils requiers_dist config
%py_req_cleanup

%build
%{pyver_build}

%install
%{pyver_install}

export PYTHONPATH=.
%if 0%{?with_doc}
sphinx-build-%{pyver} -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

install -d -m 750 %{buildroot}%{_localstatedir}/log/placement

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/placement
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/placement/placement-dist.conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/00-placement-api.conf

# Install empty policy.json file to cover rpm updates with untouched policy files.
install -p -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/placement/policy.json

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-placement

%check
OS_TEST_PATH=./placement/tests/unit ostestr -c 2

%pre common
getent group placement >/dev/null || groupadd -r placement
getent passwd placement >/dev/null || \
    useradd -r -g placement -d / -s /bin/bash -c "OpenStack Placement" placement
exit 0

%files

%files common
%license LICENSE
%dir %{_datarootdir}/placement
%attr(-, root, placement) %{_datarootdir}/placement/placement-dist.conf
%dir %{_sysconfdir}/placement
%config(noreplace) %attr(-, root, placement) %{_sysconfdir}/placement/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-placement
%dir %attr(0750, placement, root) %{_localstatedir}/log/placement

%files api
%license LICENSE
%config(noreplace) %{_sysconfdir}/httpd/conf.d/00-placement-api.conf
%{_bindir}/placement-api

%files -n python%{pyver}-placement
%license LICENSE
%{pyver_sitelib}/placement
%{pyver_sitelib}/openstack_placement-*.egg-info
%exclude %{pyver_sitelib}/placement/tests

%files -n python%{pyver}-placement-tests
%license LICENSE
%{pyver_sitelib}/placement/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

