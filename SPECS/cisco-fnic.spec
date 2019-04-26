%define vendor_name Cisco
%define vendor_label cisco
%define driver_name fnic

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Epoch: 1
Version: 1.6.0.47
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-fnic/archive?at=1.6.0.47&format=tgz&prefix=driver-cisco-fnic-1.6.0.47#/cisco-fnic-1.6.0.47.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-fnic/archive?at=1.6.0.47&format=tgz&prefix=driver-cisco-fnic-1.6.0.47#/cisco-fnic-1.6.0.47.tar.gz) = f3336601b9d08774b487673f8b0b4e2a797985a2


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
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd)/drivers/scsi/fnic KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd)/drivers/scsi/fnic INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

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
* Tue Dec 18 2018 Deli Zhang <deli.zhang@citrix.com> - 1:1.6.0.47-1
- CP-30005: Upgrade cisco-fnic driver to version 1:1.6.0.47
