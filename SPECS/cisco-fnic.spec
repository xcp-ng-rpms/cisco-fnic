%define vendor_name Cisco
%define vendor_label cisco
%define driver_name fnic

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Epoch: 1
Version: 2.0.0.59
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-fnic/archive?at=2.0.0.59&format=tgz&prefix=driver-cisco-fnic-2.0.0.59#/cisco-fnic-2.0.0.59.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-fnic/archive?at=2.0.0.59&format=tgz&prefix=driver-cisco-fnic-2.0.0.59#/cisco-fnic-2.0.0.59.tar.gz) = aa205fdfe10ecb5a60c5149edda447a82cb6eda5


BuildRequires: gcc
BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Fri Mar 06 2020 Deli Zhang <deli.zhang@citrix.com> - 1:2.0.0.59-1
- CP-33193: Update fnic driver to 1:2.0.0.59-1

* Mon Dec 9 2019 Tom Goring <tom.goring@citrix.com> - 1:2.0.0.54-1
- CP-32639: Upgrade cisco-fnic driver to version 1:2.0.0.54

* Tue Dec 18 2018 Deli Zhang <deli.zhang@citrix.com> - 1:1.6.0.47-1
- CP-30005: Upgrade cisco-fnic driver to version 1:1.6.0.47
