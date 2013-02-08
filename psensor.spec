Summary:	A Graphical Temperature Monitor
Name:		psensor
Version:	0.4.4
Release:	1
License:	GPL v2
Group:		X11/Applications
URL:		http://wpitchoune.net/psensor
Source0:	http://wpitchoune.net/psensor/files/%{name}-%{version}-src.tar.gz
# Source0-md5:	6765f61fa2b0c4118e88b0771e628130
Patch0:		make.patch
BuildRequires:	GConf2-devel
BuildRequires:	cairo-devel
BuildRequires:	gcc
BuildRequires:	gtk+2-devel
BuildRequires:	libXNVCtrl-devel
BuildRequires:	lm_sensors-devel
Requires:	desktop-file-utils
Requires:	hddtemp
Requires:	lm_sensors
ExclusiveArch:	%{ix86} %{x8664}
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
%patch0 -p1

%build
%{__make} \
	LIB=%{_lib} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_desktopdir}}

install -Dp %{name} $RPM_BUILD_ROOT%{_bindir}
install -Dp %{name}-server $RPM_BUILD_ROOT%{_bindir}
cp -p %{name}.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{name}-32x32.png $RPM_BUILD_ROOT%{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc LICENSE CHANGES README
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-server
%{_datadir}/%{name}
%{_desktopdir}/%{name}.desktop
