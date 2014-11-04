%if 0%{?fedora} >= 22
%global	baseqt	qt5
%else
%global	baseqt	qt4
%endif

Name:			pcmanfm-qt
Version:		0.8.0
Release:		2%{?dist}
Summary:		Qt port of the LXDE file manager PCManFM

License:		GPLv2+
URL:			https://github.com/lxde/pcmanfm-qt
# https://github.com/lxde/pcmanfm-qt/archive/%%{version}.tar.gz
Source0:		%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(libfm) >= 1.2.0
BuildRequires:	pkgconfig(libmenu-cache)
# Qt 4
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(QtGui)
BuildRequires:	pkgconfig(QtDBus)
# Qt 5
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5X11Extras)
# Qt5LinguistTools
BuildRequires:	qt5-qttools-devel
BuildRequires:	pkgconfig(xcb)
Requires:		pcmanfm-%{baseqt} = %{version}-%{release}

%description
PCManFM-Qt is the Qt port of the LXDE file manager PCManFM.

%package	-n pcmanfm-qt-common
Summary:	Common files for pcmanfm-qt
BuildArch:	noarch

%description	-n pcmanfm-qt-common
This package contains common files for pcmanfm-qt.

%package	-n pcmanfm-qt4
Summary:	Qt 4 based pcmanfm-qt
Requires:	libfm-qt4%{?_isa} = %{version}-%{release}
Requires:	pcmanfm-qt-common = %{version}-%{release}

%description	-n pcmanfm-qt4
This package of pcmanfm-qt is based on Qt 4.

%package	-n pcmanfm-qt5
Summary:	Qt 5 based pcmanfm-qt5
Requires:	libfm-qt5%{?_isa} = %{version}-%{release}
Requires:	pcmanfm-qt-common = %{version}-%{release}

%description	-n pcmanfm-qt5
This package of pcmanfm-qt is based on Qt 5.

%package	-n libfm-qt-common
Summary:		Common files for libfm-qt
BuildArch:		noarch

%description -n libfm-qt-common
This package contains common files for libfm-qt.

%package	-n libfm-qt-devel-common
Summary:	Common files for libfm-qt development packages
BuildArch:	noarch

%description	-n libfm-qt-devel-common
This package contains common files for libfm-qt development
packages.

%package	-n	libfm-qt4
Summary:		Companion library for PCManFM-Qt using Qt 4
Obsoletes:		libfm-qt < 0.8.0-1.999
Provides:		libfm-qt = %{version}-%{release}
Provides:		libfm-qt%{?_isa} = %{version}-%{release}
Requires:		libfm-qt-common = %{version}-%{release}

%description	-n	libfm-qt4
Libfm-Qt is a companion library providing components to build 
desktop file managers. This package uses Qt 4.

%package	-n	libfm-qt4-devel
Summary:		Development files for libfm-qt using Qt 4
Requires:		libfm-qt%{?_isa} = %{version}-%{release}
Requires:		libfm-qt-devel-common = %{version}-%{release}
Obsoletes:		libfm-qt-devel < 0.8.0-1.999
Provides:		libfm-qt-devel = %{version}-%{release}
Provides:		libfm-qt-devel%{?_isa} = %{version}-%{release}

%description	-n libfm-qt4-devel
libfm-qt4-devel package contains libraries and header files for
developing applications that use libfm-qt. This package uses Qt 4.
Requires:		libfm-qt-devel-common = %{version}-%{release}


%package	-n	libfm-qt5
Summary:		Companion library for PCManFM-Qt using Qt 5
Requires:		libfm-qt-common = %{version}-%{release}

%description	-n	libfm-qt5
Libfm-Qt is a companion library providing components to build 
desktop file managers. This package uses Qt 5.

%package	-n	libfm-qt5-devel
Summary:		Development files for libfm-qt using Qt 5
Requires:		libfm-qt5%{?_isa} = %{version}-%{release}
Requires:		libfm-qt-devel-common = %{version}-%{release}

%description	-n libfm-qt5-devel
libfm-qt5-devel package contains libraries and header files for
developing applications that use libfm-qt. This package uses Qt 5.



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
TOPDIR=$(pwd)
INSTDIR=$TOPDIR/TMPINSTDIR

mkdir qt4 qt5

pushd qt4
%cmake .. -DCMAKE_BUILD_TYPE=Release
popd

pushd qt5
{
 export USE_QT5=1
 %cmake .. -DCMAKE_BUILD_TYPE=Release
}
popd

# Kill -O3
for dir in \
	qt4 qt5
do
	pushd $dir
	find . \( \
		-name CMakeCache.txt \
		-or -name \*.make \
		-or -name link.txt \
		\) \
		-print0 | xargs --null sed -i.opt -e 's|-O3||'
	make %{?_smp_mflags}

	make install \
		DESTDIR=$INSTDIR \
		INSTALL="install -p"

	mv $INSTDIR%{_bindir}/pcmanfm-{qt,$dir}
	mv $INSTDIR%{_mandir}/man1/pcmanfm-{qt,$dir}.1
	mv $INSTDIR%{_datadir}/applications/pcmanfm-{qt,$dir}.desktop
	mv $INSTDIR%{_datadir}/applications/pcmanfm-{qt,$dir}-desktop-pref.desktop

	for f in $INSTDIR%{_datadir}/applications/pcmanfm-$dir*.desktop
	do
		sed -i \
			-e "\@Exec=@s|pcmanfm-qt |pcmanfm-${dir} |" \
			-e "\@Name=@s|PCManFM |PCManFM-${dir} |" \
				$f
	done

	popd
done

%install
mkdir -p %{buildroot}
cp -a TMPINSTDIR/* \
	%{buildroot}

for f in %{buildroot}%{_datadir}/applications/%{name}*.desktop
do
	desktop-file-validate $f
done

ln -sf pcmanfm-%{baseqt} %{buildroot}%{_bindir}/pcmanfm-qt
ln -sf pcmanfm-%{baseqt}.desktop \
	%{buildroot}%{_datadir}/applications/pcmanfm-qt.desktop
ln -sf pcmanfm-%{baseqt}-desktop-pref.desktop \
	%{buildroot}%{_datadir}/applications/pcmanfm-qt-desktop-pref.desktop
# Careful!!
ln -sf pcmanfm-%{baseqt}.1.gz %{buildroot}%{_mandir}/man1/pcmanfm-qt.1.gz

%post -n libfm-qt4 -p /sbin/ldconfig
%postun -n libfm-qt4 -p /sbin/ldconfig
%post -n libfm-qt5 -p /sbin/ldconfig
%postun -n libfm-qt5 -p /sbin/ldconfig

%post -n pcmanfm-qt4
update-desktop-database &> /dev/null || :

%postun -n pcmanfm-qt4
update-desktop-database &> /dev/null || :

%post -n pcmanfm-qt5
update-desktop-database &> /dev/null || :

%postun -n pcmanfm-qt5
update-desktop-database &> /dev/null || :


%files -n pcmanfm-qt-common
%doc	AUTHORS
%doc	COPYING
%doc	README
%{_datadir}/%{name}/

%files
%{_bindir}/pcmanfm-qt
%{_datadir}/applications/pcmanfm-qt.desktop
%{_datadir}/applications/pcmanfm-qt-desktop-pref.desktop
%{_mandir}/man1/pcmanfm-qt.1*

%files	-n pcmanfm-qt4
%{_bindir}/pcmanfm-qt4
%{_datadir}/applications/pcmanfm-qt4.desktop
%{_datadir}/applications/pcmanfm-qt4-desktop-pref.desktop
%{_mandir}/man1/pcmanfm-qt4.1*

%files	-n pcmanfm-qt5
%{_bindir}/pcmanfm-qt5
%{_datadir}/applications/pcmanfm-qt5.desktop
%{_datadir}/applications/pcmanfm-qt5-desktop-pref.desktop
%{_mandir}/man1/pcmanfm-qt5.1*

%files	-n libfm-qt4
%{_libdir}/libfm-qt.so.1*

%files	-n libfm-qt5
%{_libdir}/libfm-qt5.so.1*

%files	-n libfm-qt4-devel
%{_libdir}/libfm-qt.so
%{_libdir}/pkgconfig/libfm-qt.pc

%files	-n libfm-qt5-devel
%{_libdir}/libfm-qt5.so
%{_libdir}/pkgconfig/libfm-qt5.pc

%files	-n libfm-qt-common
# Also include same document files
%doc	AUTHORS
%doc	COPYING
%doc	README
%{_datadir}/libfm-qt/

%files	-n libfm-qt-devel-common
%{_includedir}/libfm-qt/


%changelog
* Tue Nov  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-2
- Support both Qt4 and Qt5, default to Qt5 for F-22

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
