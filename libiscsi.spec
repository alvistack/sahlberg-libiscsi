# Copyright 2024 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global source_date_epoch_from_changelog 0

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: libiscsi
Epoch: 100
Version: 1.19.0+20231103.08f79ebf
Release: 1%{?dist}
Summary: iSCSI client library
License: LGPL-2.1-or-later
URL: https://github.com/sahlberg/libiscsi/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libgcrypt-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: rdma-core-devel

%description
libiscsi is a library for attaching to iSCSI resources across a network.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%configure \
    --disable-silent-rules \
    --disable-werror \
    --enable-examples=no \
    --enable-manpages=no \
    --enable-shared \
    --enable-static=no \
    --enable-test-tool=no \
    --enable-tests=no
%make_build

%install
%make_build install DESTDIR=%{buildroot}
rm -rf %{buildroot}/%{_mandir}
find %{buildroot} -type f -name '*.la' -exec rm -rf {} \;

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libiscsi9
Summary: iSCSI client library and utilities

%description -n libiscsi9
libiscsi is a library for attaching to iSCSI resources across a network.

%package -n libiscsi-devel
Summary: iSCSI client development libraries
Requires: libiscsi9 = %{epoch}:%{version}-%{release}

%description -n libiscsi-devel
The libiscsi-devel package includes the header files for libiscsi.

%package -n libiscsi-utils
Summary: iSCSI Client Utilities
Requires: libiscsi = %{epoch}:%{version}-%{release}

%description -n libiscsi-utils
The libiscsi-utils package provides a set of assorted utilities to
connect to iSCSI servers without having to set up the Linux iSCSI

%post -n libiscsi9 -p /sbin/ldconfig
%postun -n libiscsi9 -p /sbin/ldconfig

%files -n libiscsi9
%license COPYING
%{_libdir}/*.so.*

%files -n libiscsi-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libiscsi.pc

%files -n libiscsi-utils
%{_bindir}/*
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n libiscsi-devel
Summary: iSCSI client development libraries
Requires: libiscsi = %{epoch}:%{version}-%{release}

%description -n libiscsi-devel
The libiscsi-devel package includes the header files for libiscsi.

%package -n libiscsi-utils
Summary: iSCSI Client Utilities
Requires: libiscsi = %{epoch}:%{version}-%{release}

%description -n libiscsi-utils
The libiscsi-utils package provides a set of assorted utilities to
connect to iSCSI servers without having to set up the Linux iSCSI
initiator.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/*.so.*

%files -n libiscsi-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libiscsi.pc

%files -n libiscsi-utils
%{_bindir}/*
%endif

%changelog
