%global milestone .0rc1
%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x815AFEC729392386480E076DCC0DFE2D21C023C9

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order bashate os-api-ref whereto
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1
%global distro  RDO

%global common_desc \
OpenStack Placement provides an HTTP service for managing, selecting, and \
claiming providers of classes of inventory representing available resources \
in a cloud.

Name:             openstack-placement
Version:          10.0.0
Release:          0.1%{?milestone}%{?dist}
Summary:          OpenStack Placement

License:          Apache-2.0
URL:              http://git.openstack.org/cgit/openstack/placement/

Source0:          https://tarballs.openstack.org/placement/%{name}-%{upstream_version}.tar.gz
#
# patches_base=10.0.0.0rc1
#

Source1:          placement-dist.conf
Source2:          placement.logrotate
Source3:          placement-api.conf
Source4:          policy.json
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/placement/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif
BuildRequires:    openstack-macros
BuildRequires:    intltool
BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    git-core
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

%description -n   python3-placement
%{common_desc}

This package contains the Placement Python library.

%package -n python3-placement-tests
Summary:        Placement tests
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

%description      doc
%{common_desc}

This package contains documentation files for Placement.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n openstack-placement-%{upstream_version} -S git

find . \( -name .gitignore -o -name .placeholder \) -delete

find placement -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i /^.*whereto/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%install
%pyproject_install

# Build a sample config file to install and policy file to use as documentation
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslo-config-generator --config-file=etc/placement/config-generator.conf
PYTHONPATH="%{buildroot}/%{python3_sitelib}" oslopolicy-sample-generator --config-file=etc/placement/policy-generator.conf

%if 0%{?with_doc}
%tox -e docs
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
%tox -e %{default_toxenv}

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
%{python3_sitelib}/openstack_placement-*.dist-info
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
* Fri Sep 15 2023 RDO <dev@lists.rdoproject.org> 10.0.0-0.1.0rc1
- Update to 10.0.0.0rc1


