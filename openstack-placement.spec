
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1
%global distro  RDO

%global common_desc \
OpenStack Placement provides an HTTP service for managing, selecting, and \
claiming providers of classes of inventory representing available resources \
in a cloud.

Name:             openstack-placement
Version:          3.0.0
Release:          1%{?dist}
Summary:          OpenStack Placement

License:          ASL 2.0
URL:              http://git.openstack.org/cgit/openstack/placement/

Source0:          https://tarballs.openstack.org/placement/%{name}-%{upstream_version}.tar.gz
#

Source1:          placement-dist.conf
Source2:          placement.logrotate
Source3:          placement-api.conf
Source4:          policy.json

BuildArch:        noarch
BuildRequires:    openstack-macros
BuildRequires:    intltool
BuildRequires:    python3-devel
BuildRequires:    git
BuildRequires:    python3-os-traits
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr
BuildRequires:    python3-six
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-ddt
BuildRequires:    python3-mox3
BuildRequires:    python3-oslo-rootwrap
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-concurrency
BuildRequires:    python3-oslo-config
BuildRequires:    python3-oslo-context
BuildRequires:    python3-oslo-db
BuildRequires:    python3-oslo-middleware
BuildRequires:    python3-oslo-serialization
BuildRequires:    python3-oslo-policy
BuildRequires:    python3-oslo-upgradecheck
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-oslotest
BuildRequires:    python3-osprofiler
BuildRequires:    python3-subunit
BuildRequires:    python3-tooz
BuildRequires:    python3-oslo-vmware
BuildRequires:    python3-cursive
BuildRequires:    python3-os-service-types
BuildRequires:    python3-os-resource-classes
BuildRequires:    python3-microversion-parse
BuildRequires:    python3-jsonschema
BuildRequires:    python3-sqlalchemy
BuildRequires:    python3-routes
BuildRequires:    python3-webob
BuildRequires:    python3-keystonemiddleware
BuildRequires:    python3-requests
BuildRequires:    python3-stestr

%description
%{common_desc}

%package common
Summary:          Components common to all OpenStack Placement services
Requires:         python3-placement = %{version}-%{release}

%description common
%{common_desc}

This package contains scripts, config and dependencies shared
between all the OpenStack Placement services.

%package api
Summary:          OpenStack Placement API service

Requires:         openstack-placement-common = %{version}-%{release}
Requires:         httpd
Requires:         python3-mod_wsgi

%description api
%{common_desc}

This package contains the Placement service, which will initially
allow for the management of resource providers.

%package -n       python3-placement
Summary:          Placement Python libraries
%{?python_provide:%python_provide python3-placement}

Requires:         python3-sqlalchemy >= 1.2.19
Requires:         python3-routes >= 2.3.1
Requires:         python3-webob >= 1.8.2
Requires:         python3-keystonemiddleware >= 4.18.0
Requires:         python3-jsonschema >= 2.6.0
Requires:         python3-microversion-parse >= 0.2.1
Requires:         python3-os-traits >= 2.2.0
Requires:         python3-os-resource-classes >= 0.5.0
Requires:         python3-oslo-concurrency >= 3.26.0
Requires:         python3-oslo-config >= 2:6.7.0
Requires:         python3-oslo-context >= 2.19.2
Requires:         python3-oslo-db >= 4.40.0
Requires:         python3-oslo-log >= 3.36.0
Requires:         python3-oslo-middleware >= 3.31.0
Requires:         python3-oslo-serialization >= 2.18.0
Requires:         python3-oslo-upgradecheck >= 0.2.0
Requires:         python3-oslo-utils >= 3.37.0
Requires:         python3-oslo-policy >= 1.35.0
Requires:         python3-pbr >= 2.0.0
Requires:         python3-requests >= 2.14.2
Requires:         python3-six >= 1.10.0

%description -n   python3-placement
%{common_desc}

This package contains the Placement Python library.

%package -n python3-placement-tests
Summary:        Placement tests
%{?python_provide:%python_provide python3-placement-tests}
Requires:       openstack-placement-common = %{version}-%{release}
Requires:       python3-hacking >= 0.12.0
Requires:       python3-coverage >= 4.0
Requires:       python3-fixtures >= 3.0.0
Requires:       python3-mock >= 2.0.0
Requires:       python3-PyMySQL >= 0.7.6
Requires:       python3-oslotest >= 3.4.0
Requires:       python3-stestr >= 1.0.0
Requires:       python3-testtools >= 1.8.0
Requires:       python3-gabbi >= 1.35.0
Requires:       python3-wsgi_intercept >= 1.2.2

%description -n python3-placement-tests
%{common_desc}

This package contains the Placement Python library tests.

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Placement

BuildRequires:    graphviz
BuildRequires:    python3-openstackdocstheme
BuildRequires:    python3-oslo-config
BuildRequires:    python3-oslo-log
BuildRequires:    python3-oslo-messaging
BuildRequires:    python3-oslo-utils
BuildRequires:    python3-routes
BuildRequires:    python3-sphinx
BuildRequires:    python3-sphinxcontrib-actdiag
BuildRequires:    python3-sphinxcontrib-seqdiag
BuildRequires:    python3-sphinx-feature-classification
BuildRequires:    python3-sqlalchemy
BuildRequires:    python3-webob

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
PYTHONPATH=. oslo-config-generator --config-file=etc/placement/config-generator.conf
PYTHONPATH=. oslopolicy-sample-generator --config-file=etc/placement/policy-generator.conf

%{py3_build}

%install
%{py3_install}

export PYTHONPATH=.
%if 0%{?with_doc}
sphinx-build -W -b html -d doc/build/doctrees doc/source doc/build/html
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
export PYTHON=%{__python3}
OS_TEST_PATH=./placement/tests/unit stestr run

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

%files -n python3-placement
%license LICENSE
%{python3_sitelib}/placement
%{python3_sitelib}/placement_db_tools
%{python3_sitelib}/openstack_placement-*.egg-info
%exclude %{python3_sitelib}/placement/tests

%files -n python3-placement-tests
%license LICENSE
%{python3_sitelib}/placement/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Wed May 13 2020 RDO <dev@lists.rdoproject.org> 3.0.0-1
- Update to 3.0.0

* Thu Apr 30 2020 RDO <dev@lists.rdoproject.org> 3.0.0-0.1.0rc1
- Update to 3.0.0.0rc1


