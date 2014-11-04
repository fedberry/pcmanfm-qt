Name:			pcmanfm-qt
Version:		0.8.0
Release:		1%{?dist}
Summary:		Qt port of the LXDE file manager PCManFM

License:		GPLv2+
URL:			https://github.com/lxde/pcmanfm-qt
# https://github.com/lxde/pcmanfm-qt/archive/%%{version}.tar.gz
Source0:		%{name}-%{version}.tar.gz
Patch0:		pcmanfm-qt-0.1.0-libfm120-icontheme.patch

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtDBus)
BuildRequires:	pkgconfig(libmenu-cache)
Requires:		libfm-qt%{?_isa} = %{version}-%{release}

%description
PCManFM-Qt is the Qt port of the LXDE file manager PCManFM.

%package	-n	libfm-qt
Summary:		Companion library for PCManFM-Qt

%description	-n	libfm-qt
Libfm-Qt is a companion library providing components to build 
desktop file managers.

%package	-n	libfm-qt-devel
Summary:		Development files for libfm-qt
Requires:		libfm-qt%{?_isa} = %{version}-%{release}

%description	-n libfm-qt-devel
libfm-qt-devel package contains libraries and header files for
developing applications that use libfm-qt.

%prep
%setup -q

# Honor %%optflags
sed -i.flags \
	-e '\@CMAKE_CXX_FLAGS@s|")| %{optflags} ")|' \
	CMakeLists.txt

# library installation directory
sed -i.lib \
	-e '\@LIBRARY DESTINATION@s|lib|%{_lib}|' \
	-e '\@DESTINATION@s|lib/pkgconfig|%{_lib}/pkgconfig|' \
	libfm-qt/CMakeLists.txt

%build
%cmake . -DCMAKE_BUILD_TYPE=Release
# Kill -O3
find . \( \
	-name CMakeCache.txt \
	-or -name \*.make \
	-or -name link.txt \
	\) \
	-print0 | xargs --null sed -i.opt -e 's|-O3||'
make %{?_smp_mflags}

%install
%make_install \
	INSTALL="install -p"

for f in %{buildroot}%{_datadir}/applications/%{name}*.desktop
do
	desktop-file-validate $f
done

%post -n libfm-qt -p /sbin/ldconfig
%postun -n libfm-qt -p /sbin/ldconfig

%post
update-desktop-database &> /dev/null || :

%postun
update-desktop-database &> /dev/null || :

%files
%doc	AUTHORS
%doc	COPYING
%doc	README

%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/%{name}/

%{_mandir}/man1/%{name}.1*

%files	-n libfm-qt
# Also include same document files
%doc	AUTHORS
%doc	COPYING
%doc	README

%{_libdir}/libfm-qt.so.1*
%{_datadir}/libfm-qt/

%files	-n libfm-qt-devel
%{_libdir}/libfm-qt.so
%{_libdir}/pkgconfig/libfm-qt.pc
%{_includedir}/libfm-qt/

%changelog
* Tue Nov  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-1
- 0.8.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 11 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-5
- Apply git patch for libfm API change

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-3
- Use -DCMAKE_BUILD_TYPE=Release option for cmake

* Mon Apr  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-2
- Call update-desktop-database
- Use make soversion specific in %%files

* Mon Apr  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-1
- Initial packaging
