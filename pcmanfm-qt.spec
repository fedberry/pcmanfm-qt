Name:			pcmanfm-qt
Version:		0.1.0
Release:		3%{?dist}
Summary:		Qt port of the LXDE file manager PCManFM

License:		GPLv2+
URL:			http://pcmanfm.sourceforge.net/
Source0:		http://downloads.sourceforge.net/pcmanfm/%{name}-%{version}-Source.tar.bz2

BuildRequires:	cmake
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel
BuildRequires:	libfm-devel >= 1.1.0
BuildRequires:	libX11-devel
BuildRequires:	qt-devel
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
%setup -q -n %{name}-%{version}-Source

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

#???
pushd %{buildroot}/%{_libdir}
ln -sf libfm-qt.so.0{.0.0,}
popd

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

%files	-n libfm-qt
# Also include same document files
%doc	AUTHORS
%doc	COPYING
%doc	README

%{_libdir}/libfm-qt.so.0*
%{_datadir}/libfm-qt/

%files	-n libfm-qt-devel
%{_libdir}/libfm-qt.so
%{_libdir}/pkgconfig/libfm-qt.pc
%{_includedir}/libfm-qt/

%changelog
* Mon Apr  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-3
- Use -DCMAKE_BUILD_TYPE=Release option for cmake

* Mon Apr  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-2
- Call update-desktop-database
- Use make soversion specific in %%files

* Mon Apr  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-1
- Initial packaging
