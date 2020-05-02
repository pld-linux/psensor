# TODO: ATI ADL on bcond?
#
# Conditional build:
%bcond_without	appindicator	# application indicators support
%bcond_with	unity		# Unity support
%bcond_without	nvidia		# NVidia GPU support (using libXNVCtrl)
%bcond_with	ati		# ATI GPU support (using libatiadl)

Summary:	A Graphical Temperature Monitor
Summary(pl.UTF-8):	Graficzny monitor temperatury
Name:		psensor
Version:	1.2.0
Release:	4
License:	GPL v2
Group:		X11/Applications
Source0:	http://wpitchoune.net/psensor/files/%{name}-%{version}.tar.gz
# Source0-md5:	0d8ac0a1312e96f2101ecc7c684e2863
Patch0:		%{name}-json.patch
Patch1:		%{name}-sh.patch
URL:		http://wpitchoune.net/psensor/
#%{?with_ati:BuildRequires:	libatiadlxx, adl_defines.h}
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake
BuildRequires:	curl-devel
BuildRequires:	gettext-tools >= 0.16
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	gtk+3-devel >= 3.4
BuildRequires:	help2man
BuildRequires:	json-c-devel >= 0.12
%{?with_nvidia:BuildRequires:	libXNVCtrl-devel}
%if %{with appindicator}
BuildRequires:	libappindicator-gtk3-devel
%else
BuildConflicts:	libappindicator-gtk3-devel
%endif
BuildRequires:	libatasmart-devel
BuildRequires:	libgtop-devel >= 2.0
BuildRequires:	libmicrohttpd-devel
BuildRequires:	libnotify-devel
%if %{with unity}
BuildRequires:	libunity-devel >= 3.4.2
%else
BuildConflicts:	libunity-devel
%endif
BuildRequires:	lm_sensors-devel
BuildRequires:	pkgconfig
BuildRequires:	udisks2-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	glib2 >= 1:2.26
Requires:	gtk+3 >= 3.4
Requires:	json-c >= 0.12
Requires:	hddtemp
Requires:	hicolor-icon-theme
%{?with_unity:BuildRequires:	libunity >= 3.4.2}
Requires:	lm_sensors
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Psensor is a graphical hardware temperature monitor for Linux.

It draws realtime charts and raises alerts about:
- the temperature of the motherboard and CPU sensors (using
  lm-sensors).
- the temperature of the NVidia GPUs (using XNVCtrl)
%if %{with ati}
- the temperature of ATI GPUs (using ATI ADL SDK)
%endif
- the temperature of the Hard Disk Drives (using hddtemp, libatasmart
  or udisks2)
- the rotation speed of the fans
- the temperature of a remote computer
- the CPU load

Alerts are using Desktop Notification and a specific GTK+ status icon.

%description -l pl.UTF-8
Psensor to graficzny monitor temperatury sprzętu dla Linuksa.

Rysuje w czasie rzeczywistym wykresy i zgłasza alarmy dotyczące:
- temperatury płyty głównej i czujników procesora (przy użyciu
  lm-sensors)
- temperatury GPU firmy NVidia (przy użyciu XNVCtrl)
%if %{with ati}
- temperatury GPU formy ATI (przy użyciu ATI ADL SDK)
%endif
- temperatury dysków twardych (przy użyciu hddtemp, libatasmart lub
  udisks2)
- prędkości obrotowej wentylatorów
- temperatury komputerów zdalnych
- obciążenia procesora

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# disable cppcheck: it's developer tool
%configure \
	%{!?with_nvidia:ac_cv_NVCtrl_NVCtrl_h=no} \
	ac_cv_prog_HAVE_CPPCHECK=no \
	%{?with_ati:--with-libatiadl}
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

# unsupported themes, or size. remove
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/ubuntu-mono-dark
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/ubuntu-mono-light
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/hicolor/14x14

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_desktop_database
%update_icon_cache hicolor

%postun
%glib_compile_schemas
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/psensor
%attr(755,root,root) %{_bindir}/psensor-server
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/psensor.gschema.xml
%{_mandir}/man1/psensor.1*
%{_mandir}/man1/psensor-server.1*
%{_desktopdir}/psensor.desktop
%{_iconsdir}/hicolor/*x*/apps/psensor.png
%{_iconsdir}/hicolor/scalable/apps/psensor*.svg
