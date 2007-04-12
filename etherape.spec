Summary:	Graphical network viewer modeled after etherman
Name:		etherape
Version:	0.9.6
Release: 	%mkrel 4
License:	GPL
Group:		Monitoring
URL:		http://etherape.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:		etherape-0.9.5-desktopfile.patch
Requires:	usermode-consoleonly
BuildRequires:	libglade2.0-devel
BuildRequires:	libpcap-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	scrollkeeper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description
Etherape is a graphical network monitor for Unix modeled after
etherman. Featuring ether, ip and tcp modes, it displays network
activity graphically. Hosts and links change in size with traffic. 
Color coded protocols display. It supports ethernet, ppp and slip 
devices. It can filter traffic to be shown, and can read traffic 
from a file as well as live from the network. 


%prep
%setup -q
%patch0 -p1 -b .olddesktop

%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal-1.7 -I m4 ; autoconf; automake-1.7 --add-missing --copy
%configure2_5x
make

%install
rm -rf %{buildroot}
%makeinstall_std bindir=%{_sbindir}

mv %{buildroot}/%{_sbindir}/etherape %{buildroot}/%{_sbindir}/etherape.real
ln -sf %{_bindir}/consolehelper %{buildroot}/%{_sbindir}/etherape

# menu
install -d %{buildroot}/%{_menudir}
cat << EOF > %{buildroot}/%{_menudir}/%{name}
?package(%{name}): \
  command="%{_sbindir}/etherape" \
  needs="x11" \
  section="System/Monitoring" \
  title="Etherape" \
  longtitle="Graphical network viewer" \
  icon="monitoring_section.png" \
  xdg=true
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="System;Monitor" \
  --add-category="X-MandrivaLinux-System-Monitoring" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

# pam.d
install -m 755 -d %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} << _EOF_
#%PAM-1.0
auth       sufficient	pam_rootok.so
auth       sufficient	pam_timestamp.so
%if %mdkversion >= 200700
auth       required     system-auth
%else
auth       required     pam_stack.so service=system-auth
%endif
session    required	pam_permit.so
session    optional	pam_xauth.so
session    optional	pam_timestamp.so
account    required	pam_permit.so
_EOF_

# console.apps
install -m 755 -d %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} << _EOF_
USER=root
PROGRAM=%{_sbindir}/etherape.real
SESSION=true
FALLBACK=false
_EOF_

# install desktop file to new location
install -D -m 644 etherape.desktop %{buildroot}%{_datadir}/applications/etherape.desktop

# remove files not bundled
rm -rf %{buildroot}%{_datadir}/gnome

%find_lang %{name}

%post
%update_menus

%postun
%clean_menus

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README* FAQ
%config(noreplace) %{_sysconfdir}/etherape
%config(noreplace) %{_sysconfdir}/pam.d/etherape
%config(noreplace) %{_sysconfdir}/security/console.apps/etherape
%{_sbindir}/*
%{_mandir}/man1/*
%{_menudir}/*
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/omf/%{name}

