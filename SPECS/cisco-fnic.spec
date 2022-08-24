%global package_speccommit 16b569cf7aabbf0b444b8eb0370bc8800f15401b
%global usver 2.0.0.59
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 2.0.0.59
%define vendor_name Cisco
%define vendor_label cisco
%define driver_name fnic

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Epoch: 1
Version: 2.0.0.59
Release: %{?xsrel}%{?dist}
License: GPL
Source0: cisco-fnic-2.0.0.59.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

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

%{?_cov_results_package}

%changelog
* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 2.0.0.59-2
- CP-38416: Enable static analysis

* Fri Jan 07 2022 Deli Zhang <deli.zhang@citrix.com> - 1:2.0.0.59-1
- CP-37626: Upgrade cisco-fnic driver to version 1:2.0.0.59

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 1.6.0.47-2
- CP-35517: Fix build for koji

* Tue Dec 18 2018 Deli Zhang <deli.zhang@citrix.com> - 1:1.6.0.47-1
- CP-30005: Upgrade cisco-fnic driver to version 1:1.6.0.47
