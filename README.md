wide-dhcpv6
===========

repackaged for fedora by David Beveridge


The original software comes from
http://wide-dhcpv6.sourceforge.net/

It was ported to debian/ubuntu and patched for glibc.
http://launchpad.net/ubuntu/+source/wide-dhcpv6/20080615-11.1/


To download and compile this package use the following steps.
Known to work on el5, el6, fc16, fc17, fc18, fc19.

  sudo yum install rpmdevtools gcc make bison flex flex-static 	 (flex-static not required for el5,6)

  rpmdev-setuptree

  cd ~/rpmbuild/SPECS

  wget https://github.com/bevhost/wide-dhcpv6/raw/master/wide-dhcpv6.spec

  spectool -g wide-dhcpv6.spec

(A this point on enterprise linux you need to rename the github source file)
eg:

  mv 594ad0d252acc910b791dbf3caf6c0474581a2b7 wide-dhcpv6-20080615-594ad0d.tar.gz

  mv wide*.gz ../SOURCES/

  rpmbuild -ba wide-dhcpv6.spec


