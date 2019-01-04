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
%global with_doc 1
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
BuildRequires:    python%{pyver}-ddt
BuildRequires:    python%{pyver}-mox3
BuildRequires:    python%{pyver}-oslo-rootwrap
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-concurrency
BuildRequires:    python%{pyver}-oslo-config
BuildRequires:    python%{pyver}-oslo-context
BuildRequires:    python%{pyver}-oslo-db
BuildRequires:    python%{pyver}-oslo-i18n
BuildRequires:    python%{pyver}-oslo-middleware
BuildRequires:    python%{pyver}-oslo-serialization
BuildRequires:    python%{pyver}-oslo-policy
BuildRequires:    python%{pyver}-oslo-upgradecheck
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-oslo-versionedobjects
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-osprofiler
BuildRequires:    python%{pyver}-subunit
BuildRequires:    python%{pyver}-tooz
BuildRequires:    python%{pyver}-oslo-vmware
BuildRequires:    python%{pyver}-cursive
BuildRequires:    python%{pyver}-os-service-types
BuildRequires:    python%{pyver}-microversion-parse
BuildRequires:    python%{pyver}-jsonschema
BuildRequires:    python%{pyver}-sqlalchemy
BuildRequires:    python%{pyver}-routes
BuildRequires:    python%{pyver}-webob
BuildRequires:    python%{pyver}-keystonemiddleware
BuildRequires:    python%{pyver}-requests
BuildRequires:    python%{pyver}-stestr

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

Requires:         openstack-placement-common = %{version}-%{release}
Requires:         httpd
%if %{pyver} == 2
Requires:         mod_wsgi
%else
Requires:         python%{pyver}-mod_wsgi
%endif

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
Requires:         python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-oslo-versionedobjects >= 1.31.2
Requires:         python%{pyver}-oslo-policy >= 1.35.0
Requires:         python%{pyver}-pbr >= 2.0.0
Requires:         python%{pyver}-requests >= 2.14.2
Requires:         python%{pyver}-six >= 1.10.0

%description -n   python%{pyver}-placement
%{common_desc}

This package contains the Placement Python library.

%package -n python%{pyver}-placement-tests
Summary:        Placement tests
%{?python_provide:%python_provide python%{pyver}-placement-tests}
Requires:       openstack-placement-common = %{version}-%{release}
Requires:       python%{pyver}-hacking >= 0.12.0
Requires:       python%{pyver}-coverage >= 4.0
Requires:       python%{pyver}-fixtures >= 3.0.0
Requires:       python%{pyver}-mock >= 2.0.0
Requires:       python%{pyver}-PyMySQL >= 0.7.6
Requires:       python%{pyver}-oslotest >= 3.2.0
Requires:       python%{pyver}-stestr >= 1.0.0
Requires:       python%{pyver}-testtools >= 1.8.0
Requires:       python%{pyver}-gabbi >= 1.35.0
Requires:       python%{pyver}-wsgi_intercept >= 1.2.2

%description -n python%{pyver}-placement-tests
%{common_desc}

This package contains the Placement Python library tests.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Placement

BuildRequires:    graphviz
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-oslo-config
BuildRequires:    python%{pyver}-oslo-log
BuildRequires:    python%{pyver}-oslo-messaging
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-routes
BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-sphinxcontrib-actdiag
BuildRequires:    python%{pyver}-sphinxcontrib-seqdiag
BuildRequires:    python%{pyver}-sphinx-feature-classification
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
# Build a sample config file to install and policy file to use as documentation
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=etc/placement/config-generator.conf
PYTHONPATH=. oslopolicy-sample-generator-%{pyver} --config-file=etc/placement/policy-generator.conf

%{pyver_build}

%install
%{pyver_install}

export PYTHONPATH=.
%if 0%{?with_doc}
sphinx-build-%{pyver} -W -b html -d doc/build/doctrees doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

install -d -m 750 %{buildroot}%{_localstatedir}/log/placement

# Install config files
install -d -m 755 %{buildroot}%{_sysconfdir}/placement
install -p -D -m 640 etc/placement/placement.conf.sample  %{buildroot}%{_sysconfdir}/placement/placement.conf
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/placement/placement-dist.conf
install -p -D -m 640 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/00-placement-api.conf

# Install empty policy.json file to cover rpm updates with untouched policy files.
install -p -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/placement/policy.json

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-placement

# Install migrate-db.sh scripts under /usr/share/placement/
install -d -m 755 %{buildroot}%{_datarootdir}/placement
install -p -D -m 755 tools/mysql-migrate-db.sh %{buildroot}%{_datarootdir}/placement/mysql-migrate-db.sh
install -p -D -m 755 tools/postgresql-migrate-db.sh %{buildroot}%{_datarootdir}/placement/postgresql-migrate-db.sh

%check
export PYTHON=%{pyver_bin}
OS_TEST_PATH=./placement/tests/unit stestr-%{pyver} run

%pre common
getent group placement >/dev/null || groupadd -r placement
getent passwd placement >/dev/null || \
    useradd -r -g placement -d / -s /bin/bash -c "OpenStack Placement" placement
exit 0

%files common
%license LICENSE
%doc etc/placement/policy.yaml.sample
%{_bindir}/placement-manage
%{_bindir}/placement-status
%dir %{_datarootdir}/placement
%attr(-, root, placement) %{_datarootdir}/placement/placement-dist.conf
%{_datarootdir}/placement/mysql-migrate-db.sh
%{_datarootdir}/placement/postgresql-migrate-db.sh
%dir %{_sysconfdir}/placement
%config(noreplace) %attr(-, root, placement) %{_sysconfdir}/placement/placement.conf
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

# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/placement/commit/?id=1e213276bbecc3cfaf6dfb83ae23b4414567f441
