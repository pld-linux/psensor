Summary:	A Graphical Temperature Monitor
Name:		psensor
Version:	0.6.2.19
Release:	4
License:	GPL v2
Group:		X11/Applications
URL:		http://wpitchoune.net/psensor
Source0:	http://wpitchoune.net/psensor/files/%{name}-%{version}.tar.gz
# Source0-md5:	ddc21cbb36c6c622f7b5c1c7eb277374
BuildRequires:	GConf2-devel
BuildRequires:	cairo-devel
BuildRequires:	curl-devel
BuildRequires:	gettext-tools
BuildRequires:	gtk+3-devel
BuildRequires:	json-c-devel
BuildRequires:	libXNVCtrl-devel
BuildRequires:	libgtop-devel
BuildRequires:	libmicrohttpd-devel
BuildRequires:	libnotify-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	pkgconfig
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hddtemp
Requires:	hicolor-icon-theme
Requires:	lm_sensors
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Psensor is a graphical hardware temperature monitor for Linux.

It is based on:
- lm-sensors for retrieving hardware temperatures
- GTK for the UI
- Cairo for the graph drawing
- NVidia library for retrieving NVidia GPUs temperature (not included
  - licensing problem)

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

# unsupported themes, or size. remove
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/ubuntu-mono-dark
%{__rm} -r $RPM_BUILD_ROOT%{_iconsdir}/ubuntu-mono-light
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/14x14

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
%attr(755,root,root) %{_bindir}/psensor
%attr(755,root,root) %{_bindir}/psensor-server
%{_mandir}/man1/psensor-server.1*
%{_mandir}/man1/psensor.1*
/etc/xdg/autostart/psensor.desktop
%{_desktopdir}/psensor.desktop
%{_iconsdir}/hicolor/*/apps/psensor*.*
%{_datadir}/%{name}
