#
# spec file for package wide-dhcpv6
#
# Copyright (c) 2013 Beveridge Internet Hosting
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# The primary reason for making this package is that the normal dhcp with
# fedora/redhat did not support DHCPv6 Prefix Delegation client on PPP 
#
# Source0 is the unmodified original BSD Source
# Source1 is the unmodified ubuntu bits including glibc patches
# Source2 is the redhat bits, some of which I took from a SUSE build of this.
#
# use "spectool -g wide-dhcpv6.spec" to download the sources and
# rename the commit string to the correct name (shown in the download).
#

%global ubuntu_release 11.1
%global my_release 2
%global commit 594ad0d252acc910b791dbf3caf6c0474581a2b7
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global rh_dir %{name}-%{commit}

%if 0%{?fedora} >= 15
%global systemd systemd-units
%endif
%if 0%{?fedora} >= 18
%global systemd systemd
%endif
%{?_unitdir:%global with_systemd 1}

Name:           wide-dhcpv6
BuildRequires:  bison flex %{?systemd}
%{?fedora:BuildRequires: flex-static}
License:        BSD
Group:          System Environment/Daemons
Summary:        DHCP Client and Server for IPv6
Version:        20080615
Url:            https://github.com/bevhost/wide-dhcpv6
Release:        %{ubuntu_release}.%{my_release}%{dist}
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        https://launchpad.net/ubuntu/+archive/primary/+files/%{name}_%{version}-%{ubuntu_release}.debian.tar.gz
Source2:        %{url}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This is the DHCPv6 package from WIDE project. For more information visit the
project web site at http://wide-dhcpv6.sourceforge.net/

DHCPv6 allows prefix delegation and host configuration for the IPv6 network
protocol even over PPP.

Multiple network interfaces are supported by this DHCPv6 package.

This package contains the server and the client.


%prep
rm -rf %{_builddir}/%{name}-%{version}
%setup -q -n %{name}-%{version} -a 1 -a 2
for p in %{_builddir}/%{name}-%{version}/debian/patches/*.patch; do
        patch -p1 < $p;
done


%build
./configure --prefix=/usr \
        --libdir=%{_libdir} \
        --mandir=%{_mandir} \
        --sysconfdir=%{_sysconfdir}/%{name} \
        --enable-libdhcp=no
make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sysconfdir}/ppp
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_mandir}/man{8,5}
mkdir -p %{buildroot}%{_sharedstatedir}/dhcpv6/
mkdir -p %{buildroot}/var/run/dhcpv6/
install -m 755 dhcp6c dhcp6s dhcp6relay dhcp6ctl %{buildroot}%{_sbindir}
install -m 644 dhcp6c.8 %{buildroot}/%{_mandir}/man8
install -m 644 dhcp6s.8 %{buildroot}/%{_mandir}/man8
install -m 644 dhcp6relay.8 %{buildroot}/%{_mandir}/man8
install -m 644 dhcp6ctl.8 %{buildroot}/%{_mandir}/man8
install -m 644 dhcp6c.conf.5 %{buildroot}/%{_mandir}/man5
install -m 644 dhcp6s.conf.5 %{buildroot}/%{_mandir}/man5
install -m 755 debian/scripts/dhcp6c-script %{buildroot}%{_sysconfdir}/%{name}/dhcp6c-script
install -m 644 dhcp6c.conf.sample %{buildroot}%{_sysconfdir}/%{name}/dhcp6c.conf
install -m 644 dhcp6s.conf.sample %{buildroot}%{_sysconfdir}/%{name}/dhcp6s.conf
install -m 644 %{rh_dir}/etc/sysconfig/* %{buildroot}%{_sysconfdir}/sysconfig/
install -m 755 %{rh_dir}/etc/ppp/* %{buildroot}%{_sysconfdir}/ppp/
%if 0%{?with_systemd}
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{rh_dir}/usr/lib/systemd/system/* %{buildroot}%{_unitdir}/
%else
mkdir -p %{buildroot}%{_initrddir}
install -m 755 %{rh_dir}/etc/init.d/* %{buildroot}%{_initrddir}/
%endif

%post
if [ "$1" -eq 0 ] ; then
%if 0%{?with_systemd}
/bin/systemctl --no-reload disable dhcp6c.service > /dev/null 2>&1 || :
/bin/systemctl --no-reload disable dhcp6r.service > /dev/null 2>&1 || :
/bin/systemctl --no-reload disable dhcp6s.service > /dev/null 2>&1 || :
%else
/sbin/chkconfig dhcp6c off
/sbin/chkconfig dhcp6r off
/sbin/chkconfig dhcp6s off
%endif
fi
exit 0

%preun
if [ "$1" -eq 0 ] ; then
%if 0%{?with_systemd}
/bin/systemctl --no-reload disable dhcp6c.service > /dev/null 2>&1 || :
/bin/systemctl --no-reload disable dhcp6r.service > /dev/null 2>&1 || :
/bin/systemctl --no-reload disable dhcp6s.service > /dev/null 2>&1 || :
/bin/systemctl stop dhcp6c.service > /dev/null 2>&1 || :
/bin/systemctl stop dhcp6r.service > /dev/null 2>&1 || :
/bin/systemctl stop dhcp6s.service > /dev/null 2>&1 || :
%else
/sbin/service dhcp6c stop > /dev/null 2>&1
/sbin/service dhcp6r stop > /dev/null 2>&1
/sbin/service dhcp6s stop > /dev/null 2>&1
/sbin/chkconfig --del dhcp6c
/sbin/chkconfig --del dhcp6r
/sbin/chkconfig --del dhcp6s
%endif
fi
exit 0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CHANGES COPYRIGHT debian/copyright debian/changelog
%{_sbindir}/*
%{_mandir}/man?/*
%dir %{_sharedstatedir}/dhcpv6
%dir %{_localstatedir}/run/dhcpv6
%config(noreplace) /%{_sysconfdir}/sysconfig/dhcp*
%config(noreplace) /%{_sysconfdir}/%{name}/dhcp6c.conf
%config(noreplace) /%{_sysconfdir}/%{name}/dhcp6s.conf
/%{_sysconfdir}/ppp/*
%if 0%{?with_systemd}
/%{_unitdir}/*
%else
/%{_initrddir}/*
%endif
/%{_sysconfdir}/%{name}/dhcp6c-script

%changelog
* Mon May 6 2013 dave@bevhost.com 20080615-11.1.2
- use macros in spec file wherever possible
- move redhat source to github
- add support for systemd

* Wed Apr 24 2013 dave@bevhost.com 20080615-11.1.1
- Move sysconfdir from /etc to /etc/wide-dhcpv6 to match man pages
- add /etc/ppp/ipv6-up.local.sample (and down)

* Sun Apr 07 2013 dave@bevhost.com
- change patches to work from builddir rather than sourcedir
- add dist name to release
- add conditional statment for fedora buildrequires

* Fri Apr 05 2013 dave@bevhost.com
- spelling fix
- rename patches to include packagename
- change make to work on x86_64
- remove -o -g from install commands so you don't have to be root to build

* Tue Apr 02 2013 dave@bevhost.com
- converted from debian package


