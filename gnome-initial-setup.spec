Name:           gnome-initial-setup
Version:        3.14.4
Release:        5%{?dist}
Summary:        Bootstrapping your OS

License:        GPLv2+
URL:            https://live.gnome.org/GnomeOS/Design/Whiteboards/InitialSetup
Source0:        http://download.gnome.org/sources/%{name}/3.14/%{name}-%{version}.tar.xz

Patch0: gnome-initial-setup-translations-3.14.patch
Patch1: welcome-tour-race.patch
Patch2: 0001-setup-shell-Make-sure-that-the-shell-launches-first.patch
Patch3: 0002-network-Avoid-a-crash-on-locale-change.patch
Patch4: 0003-password-Avoid-a-critical.patch
Patch5: style.patch
Patch6: debug.patch
Patch7: 0001-timezone-Stop-the-geoclue-client.patch
Patch8: fix-enterprise-login.patch

%global nm_version 0.9.6.4
%global glib_required_version 2.36.0
%global gtk_required_version 3.11.3
%global geoclue_version 2.1.2

BuildRequires:  krb5-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  libpwquality-devel
BuildRequires:  pkgconfig(NetworkManager) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-glib) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-util) >= %{nm_version}
BuildRequires:  pkgconfig(libnm-gtk)
BuildRequires:  pkgconfig(accountsservice)
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(cheese)
BuildRequires:  pkgconfig(cheese-gtk) >= 3.3.5
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(geoclue-2.0) >= %{geoclue_version}
BuildRequires:  pkgconfig(gweather-3.0)
BuildRequires:  pkgconfig(goa-1.0)
BuildRequires:  pkgconfig(goa-backend-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk_required_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gio-unix-2.0) >= %{glib_required_version}
BuildRequires:  pkgconfig(gdm)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  krb5-devel
BuildRequires:  ibus-devel
BuildRequires:  rest-devel
BuildRequires:  polkit-devel
BuildRequires:  libsecret-devel

# gnome-initial-setup is being run by gdm
Requires: gdm
Requires: geoclue2 >= %{geoclue_version}
# we install a rules file
Requires: polkit-js-engine
Requires: /usr/bin/gkbd-keyboard-display

Requires(pre): shadow-utils

Provides: user(%name)

%description
GNOME Initial Setup is an alternative to firstboot, providing
a good setup experience to welcome you to your system, and walks
you through configuring it. It is integrated with gdm.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'

# Desktop file does not (and probably will not) ever validate, as it uses
# an absolute path /tmp/-style trigger to determine whether to autostart.
# desktop-file-validate %%{buildroot}/%%{_sysconfdir}/xdg/autostart/gnome-welcome-tour.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/gnome-initial-setup-copy-worker.desktop
desktop-file-validate %{buildroot}%{_datadir}/gdm/greeter/applications/gnome-initial-setup.desktop
desktop-file-validate %{buildroot}%{_datadir}/gdm/greeter/applications/setup-shell.desktop

mkdir -p %{buildroot}%{_localstatedir}/lib/gnome-initial-setup

%find_lang %{name}

%pre
useradd -rM -d /run/gnome-initial-setup/ -s /sbin/nologin %{name} &>/dev/null || :

%files -f %{name}.lang
%doc COPYING README
%{_libexecdir}/gnome-initial-setup
%{_libexecdir}/gnome-initial-setup-copy-worker
%{_libexecdir}/gnome-welcome-tour
%{_sysconfdir}/xdg/autostart/gnome-welcome-tour.desktop
%{_sysconfdir}/xdg/autostart/gnome-initial-setup-copy-worker.desktop
%{_sysconfdir}/xdg/autostart/gnome-initial-setup-first-login.desktop

%{_datadir}/gdm/greeter/applications/gnome-initial-setup.desktop
%{_datadir}/gdm/greeter/applications/setup-shell.desktop
%{_datadir}/gnome-session/sessions/gnome-initial-setup.session
%{_datadir}/gnome-shell/modes/initial-setup.json
%{_datadir}/polkit-1/rules.d/20-gnome-initial-setup.rules

%changelog
* Mon Jul 27 2015 Ray Strode <rstrode@redhat.com> - 3.14.4-5
- Fix login with enterprise accounts
Resolves: #1242861
Related: #1173234

* Mon Jul 27 2015 Matthias Clasen <mclasen@redhat.com> - 3.14.4-4
- Avoid more criticals on locale change
Related: #1174725

* Wed Jul 15 2015 Matthias Clasen <mclasen@redhat.com> - 3.14.4-3
- Avoid criticals and crashes on locale change
Resolves: #1173234

* Wed Jul 15 2015 Matthias Clasen <mclasen@redhat.com> - 3.14.4-2
- Fix a race condition in launching the welcome tour
Resolves: #1242061

* Thu May 28 2015 Matthias Clasen <mclasen@redhat.com> - 3.14.4-1
- Update to 3.14.4
- Related: #1174725

* Mon Mar 23 2015 Richard Hughes <rhughes@redhat.com> - 3.14.3-1
- Update to 3.14.3
- Resolves: #1174725

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.13.1-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.13.1-3
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Matthias Clasen <mclasen@redhat.com> - 0.13.1-2
- Update translations
- Resolves: #1030342

* Wed Nov  6 2013 Jasper St. Pierre <jasper@redhat.com> - 0.13.1
- Fix build again... sigh.
- Resolves: rhbz#1019973
- Resolves: rhbz#1024370

* Wed Nov  6 2013 Jasper St. Pierre <jasper@redhat.com> - 0.13
- Fix build
- Resolves: rhbz#1019973
- Resolves: rhbz#1024370

* Wed Nov  6 2013 Jasper St. Pierre <jasper@redhat.com> - 0.13
- Update to 0.13
- Resolves: rhbz#1019973
- Resolves: rhbz#1024370

* Tue Jul 30 2013 Petr Kovar <pkovar@redhat.com> - 0.12-2
- Require gnome-getting-started-docs

* Mon Jun 17 2013 Rui Matos <rmatos@redhat.com> - 0.12-1
- Update to 0.12

* Fri Jun  7 2013 Matthias Clasen <mclasen@redhat.com> - 0.11-2
- Require polkit-js-engine

* Tue May 28 2013 Matthias Clasen <mclasen@redhat.com> - 0.11-1
- Update to 0.11

* Fri May 17 2013 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Fix passwordless user creation (#961140)

* Fri May 17 2013 Rui Matos <rmatos@redhat.com> - 0.10-2
- Add upstream patch for AcceptedFreezeException bug 928645

* Tue May 14 2013 Rui Matos <rmatos@redhat.com> - 0.10-1
- Update to 0.10
- Add BuildRequires on polkit-devel
- Update files list

* Thu May  2 2013 Rui Matos <rmatos@redhat.com> - 0.9-2
- Remove unused patches
- Add build requires for ibus

* Tue Apr 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Tue Apr 16 2013 Ray Strode <rstrode@redhat.com> 0.8-4
- Add requires for keyboard viewer app

* Wed Mar 20 2013 Ray Strode <rstrode@redhat.com> 0.8-3
- Add cosimoc fix for gd page transitions

* Wed Mar 20 2013 Ray Strode <rstrode@redhat.com> 0.8-2
- Disable gd page transitions for now since they don't
  completely work right (ask adamw).
- Fix crasher when realmd goes away

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8

* Tue Mar 12 2013 Matthias Clasen <mclasen@redhat.com> - 0.7-1
- Update to 0.7

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 0.6-4
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.6-3
- Rebuilt for libgnome-desktop soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.6-2
- Rebuild for new cogl

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- 0.6

* Fri Jan 11 2013 Matthias Clasen <mclasen@redhat.com> - 0.5-1
- 0.5

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 0.4-2
- Rebuilt for libgweather soname bump

* Thu Nov 22 2012 Matthias Clasen <mclasen@redhat.com> - 0.4-1
- 0.4

* Fri Oct 26 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.3-3
- Add krb5

* Fri Oct 26 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.3-2
- 0.3-2

* Thu Oct 18 2012 Matthias Clsaen <mclasen@redhat.com> - 0.3-1
- 0.3

* Fri Sep 14 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-2
- Add Requires: gdm

* Wed Aug 29 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.2-1
- Update to 0.2

* Fri Jun 08 2012 Jasper St. Pierre <jstpierre@mecheye.net> - 0.1
- Initial packaging.
