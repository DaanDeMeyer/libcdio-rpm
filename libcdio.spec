Name:           libcdio
Version:        0.70
Release:        1
Epoch:          0
Summary:        A CD-ROM input and control library

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.gnu.org/software/libcdio/
Source0:        http://ftp.gnu.org/gnu/libcdio/libcdio-0.70.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libcddb-devel
BuildRequires:  pkgconfig
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
This library provides an interface for CD-ROM access. It can be used
by applications that need OS- and device-independent access to CD-ROM
devices.

%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q


%build
%configure --disable-vcd-info
# Parallel build fails
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :
fi

%postun
/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.libcdio THANKS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_infodir}/*


%files devel
%defattr(-,root,root,-)
%{_includedir}/cdio
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Sun Sep  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.70-0.fdr.1
- Updated to 0.70.

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.69-0.fdr.1
- Updated to 0.69.
- Removed broken iso-read.
- Split Requires(pre,post).
- Added BuildReq pkgconfig.

* Mon Mar 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.68-0.fdr.1
- Initial RPM release.

