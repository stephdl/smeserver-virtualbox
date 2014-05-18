%define name smeserver-virtualbox
%define version 4.3.1
%define release 2
%define rpmver   4.3.1
Summary: smserver rpm to install virtualbox
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source: %{name}-%{version}.tar.gz
License: GNU GPL version 2
URL: http://mirror.de-labrusse.fr
Group: SMEserver/addon
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: %{_prefix}
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 8.0
Requires: VirtualBox-4.3
#Patch0: smeserver-virtualbox-4.3.1_fix_vboxdrv_kernel_module.patch
AutoReqProv: no

%description
smserver rpm to install virtualbox

%changelog
* Sun May 18 2014 stephane de labrusse <stephdl@de-labrusse.fr> 4.3.1-2
- add a force to link service creation

* Wed Mar 19 2014 stephane de labrusse <stephdl@de-labrusse.fr> 4.3.1-1
- added a script to verify if the vboxdrv module is compiled for the kernel used by the system

* Mon Dec 30 2013 JP Pialasse <tests@pialasse.com> 4.3.0-5
- changing naming of contrib for import into buildsys

* Tue Nov 05 2013 stephane de labrusse <stephdl@de-labrusse.fr> 4.3.0-4
- change name to match the virtualbox version

* Sat Oct 19 2013 stephane de labrusse <stephdl@de-labrusse.fr> 4.3.0-3
- Initial release

%prep
%setup
#%patch0 -p1
%build

%install
rm -rf $RPM_BUILD_ROOT
(cd root   ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc COPYING"  >> %{name}-%{version}-filelist

%clean
cd ..
rm -rf %{name}-%{version}

%pre
%preun

%post
if [ $1 > 1 ] ; then
/bin/ln -fs /etc/rc5.d/S20vboxdrv /etc/rc7.d/ >/dev/null 2>&1
/bin/ln -fs /etc/rc5.d/S35vboxautostart-service /etc/rc7.d/ >/dev/null 2>&1
/bin/ln -fs  /etc/rc5.d/S35vboxballoonctrl-service /etc/rc7.d/ >/dev/null 2>&1
/bin/ln -fs  /etc/rc5.d/S35vboxweb-service /etc/rc7.d/ >/dev/null 2>&1
/bin/ln -fs /etc/rc.d/init.d/fix_vboxdrv_kernel_module /etc/rc7.d/S19fix_vboxdrv_kernel_module >/dev/null 2>&1
fi
/usr/bin/vboxmanage setproperty websrvauthlibrary null
%postun
#uninstall
if [ $1 = 0 ] ; then
/bin/rm -rf  /etc/rc7.d/S20vboxdrv 
/bin/rm -rf  /etc/rc7.d/S35vboxautostart-service 
/bin/rm -rf  /etc/rc7.d/S35vboxballoonctrl-service 
/bin/rm -rf  /etc/rc7.d/S35vboxweb-service 
/bin/rm -rf  /etc/rc7.d/S19fix_vboxdrv_kernel_module
fi
%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%attr(755,root,root) /etc/rc.d/init.d/fix_vboxdrv_kernel_module

