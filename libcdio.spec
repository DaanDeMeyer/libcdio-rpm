Name:           libcdio
Version:        0.77
Release:        2%{?dist}
Summary:        CD-ROM input and control library

Group:          Applications/Multimedia
License:        GPL
URL:            http://www.gnu.org/software/libcdio/
Source0:        http://ftp.gnu.org/gnu/libcdio/libcdio-0.77.tar.gz
Source1:        http://ftp.gnu.org/gnu/libcdio/libcdio-0.77.tar.gz.sig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  libcddb-devel >= 0.9.4
BuildRequires:  pkgconfig doxygen
BuildRequires:  ncurses-devel
Requires(post): /sbin/ldconfig
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
This library provides an interface for CD-ROM access. It can be used
by applications that need OS- and device-independent access to CD-ROM
devices.

%package        devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q
f=src/cd-paranoia/doc/jp/cd-paranoia.1.in
iconv -f euc-jp -t utf-8 -o $f.utf8 $f && mv $f.utf8 $f


%build
%configure \
	--disable-vcd-info \
	--disable-dependency-tracking \
	--disable-cddb \
	--disable-rpath
make %{?_smp_mflags}
cd doc/doxygen
./run_doxygen


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/{jp,ja}

rm -rf examples
mkdir -p examples/C++
cp -a example/{*.c,README} examples
cp -a example/C++/{*.cpp,README} examples/C++


%check || :
# disable test using local CDROM
%{__sed} -i -e  "s/am__EXEEXT_1 =.*$/am__EXEEXT_1 =/g" test/Makefile
make check


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

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README README.libcdio THANKS TODO
%{_bindir}/*
%{_libdir}/*.so.*
%{_infodir}/*
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*


%files devel
%defattr(-,root,root,-)
%doc doc/doxygen/html examples
%{_includedir}/cdio
%{_includedir}/cdio++
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.77-2
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Adrian Reber <adrian@lisas.de> - 0.77-1
- Updated to 0.77

* Mon Sep 18 2006 Adrian Reber <adrian@lisas.de> - 0.76-3
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-2
- Rebuilt

* Mon Sep 26 2005 Adrian Reber <adrian@lisas.de> - 0.76-1
- Updated to 0.76.
- Included doxygen generated documentation into -devel
- Included examples into -devel

* Mon Aug 01 2005 Adrian Reber <adrian@lisas.de> - 0.75-4
- disable test accessing local CDROM drive (#164266)

* Wed Jul 27 2005 Adrian Reber <adrian@lisas.de> - 0.75-3
- Rebuilt without libcddb dependency (#164270)

* Tue Jul 26 2005 Adrian Reber <adrian@lisas.de> - 0.75-2
- Rebuilt

* Thu Jul 14 2005 Adrian Reber <adrian@lisas.de> - 0.75-1
- Updated to 0.75.

* Fri Jun 03 2005 Adrian Reber <adrian@lisas.de> - 0.74-2
- Updated to 0.74.

* Sun Apr 24 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.73-2
- BuildRequire ncurses-devel (for cdda-player and cd-paranoia).
- Run test suite during build.
- Install Japanese man pages.

* Sun Apr 24 2005 Adrian Reber <adrian@lisas.de> - 0.73-1
- Updated to 0.73.

* Fri Mar 18 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.70-2
- Fix FC4 build (#151468).
- Build with dependency tracking disabled.

* Sun Sep  5 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.70-0.fdr.1
- Updated to 0.70.

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.69-0.fdr.1
- Updated to 0.69.
- Removed broken iso-read.
- Split Requires(pre,post).
- Added BuildReq pkgconfig.

* Mon Mar 29 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.68-0.fdr.1
- Initial RPM release.

