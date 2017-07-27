Name: pcmanfm-qt
Version: 0.11.3
Release: 6%{?dist}
Summary: LxQt file manager PCManFM
License: GPLv2+
URL: http://lxqt.org
Source0: https://github.com/lxde/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires: %{?fedora:cmake}%{!?fedora:cmake3} >= 3.0
BuildRequires: pkgconfig(lxqt) >= 0.11.0
BuildRequires: pkgconfig(Qt5Help)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(libfm)
BuildRequires: pkgconfig(libmenu-cache)
BuildRequires: pkgconfig(exiv2)
BuildRequires: pkgconfig(libfm-qt)
BuildRequires: desktop-file-utils
BuildRequires: kf5-kwindowsystem-devel
BuildRequires: doxygen
Requires: lxqt-common >= 0.10.0
Obsoletes: pcmanfm-qt5 < 0.9.0
Provides:  pcmanfm-qt5 = %{version}-%{release}
Obsoletes: pcmanfm-qt4 <= 0.9.0
Obsoletes: pcmanfm-qt-common <= 0.9.0

# gvfs is optional depencency at runtime, so we add a weak dependency here
Recommends:    gvfs


%description
%{summary}

%post
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

%prep
%setup -q

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
	%{cmake_lxqt} -DBUILD_DOCUMENTATION=ON -DPULL_TRANSLATIONS=NO ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

for dfile in pcmanfm-qt-desktop-pref pcmanfm-qt; do
	desktop-file-edit \
		--remove-category=LXQt --add-category=X-LXQt \
		--remove-category=Help --add-category=X-Help \
		--remove-only-show-in=LXQt \
		%{buildroot}/%{_datadir}/applications/${dfile}.desktop
done

%files
%doc AUTHORS
%{_bindir}/pcmanfm-qt
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-desktop-pref.desktop
%{_docdir}/pcmanfm-qt
%{_mandir}/man1/pcmanfm-qt.*

%changelog
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat May 20 2017 Christian Dersch <lupinix@mailbox.org> - 0.11.3-5
- recommend gvfs

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Christian Dersch <lupinix@mailbox.org> - 0.11.3-3
- rebuilt

* Wed Jan 18 2017 Christian Dersch <lupinix@mailbox.org> - 0.11.3-2
- moved translations to lxqt-l10n

* Mon Jan 16 2017 Christian Dersch <lupinix@mailbox.org> - 0.11.3-1
- new version

* Mon Sep 26 2016 Helio Chissini de Castro <helio@kde.org> - 0.11.1-1
- new upstream version. 
- pcmanfm-qt not provides linfm anymore, comes from an external package

* Tue Jul 26 2016 Helio Chissini de Castro <helio@kde.org> - 0.10.0-4
- Make it available for other desktops
- Reference https://bugzilla.redhat.com/show_bug.cgi?id=1347905

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 13 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.0-2
- Prepare to use new cmake infra for epel

* Mon Nov 02 2015 Helio Chissini de Castro <helio@kde.org> - 0.10.0-1
- New upstream version

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.0-10
- rebuild (exiv2)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.0-8
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 04 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-7
- Add provides for pcmanfm-qt5 to avoid older comps lxqt break

* Wed Feb 25 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.9.0-6
- Fix directory ownership

* Wed Feb 18 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-5
- Fix duplicated files caused for qm template

* Fri Feb 13 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-4
- Ownership of share/pcmanfm-qt directories
- libfm-qt5 alnguage files added
- Obsoletes libfm-qt4-devel
- Moved COPYING to the new tag license

* Mon Feb 09 2015 Helio Chissini de Castro <helio@kde.org> - 0.9.0-2
- Fixed download dir

* Sun Feb 08 2015 Helio Chissini de Castro <hcastro@redhat.com> - 0.9.0-1
- New upstream release 0.9.0

* Tue Feb 03 2015 Helio Chissini de Castro <hcastro@redhat.com> - 0.9.0-0.1
- Preparing for 0.9.0 release
- Obsoletes pcmanfm-qt5 and pcmanfm-qt-common packages as no more qt4 versions will be done

* Tue Nov  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-2
- Support both Qt4 and Qt5, default to Qt5 for F-22

* Tue Nov  4 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.8.0-1
- 0.8.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.1.0-5
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
