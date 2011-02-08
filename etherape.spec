Summary:	Graphical network viewer modeled after etherman
Name:		etherape
Version:	0.9.10
Release: 	%mkrel 1
License:	GPLv2+
Group:		Monitoring
URL:		http://etherape.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Requires:	usermode-consoleonly
BuildRequires:	libglade2.0-devel
BuildRequires:	libpcap-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	scrollkeeper
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Etherape is a graphical network monitor for Unix modeled after
etherman. Featuring ether, ip and tcp modes, it displays network
activity graphically. Hosts and links change in size with traffic. 
Color coded protocols display. It supports ethernet, ppp and slip 
devices. It can filter traffic to be shown, and can read traffic 
from a file as well as live from the network. 


%prep
%setup -q

%build
%configure
%make

%install
rm -rf %{buildroot}
%makeinstall_std bindir=%{_sbindir}
mkdir -p %{buildroot}%{_bindir}

mv %{buildroot}/%{_sbindir}/etherape %{buildroot}/%{_sbindir}/etherape.real
ln -sf %{_bindir}/consolehelper %{buildroot}/%{_bindir}/etherape

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="System" \
  --add-category="Monitor" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# pam.d
install -m 755 -d %{buildroot}%{_sysconfdir}/pam.d
cat > %{buildroot}%{_sysconfdir}/pam.d/%{name} << _EOF_
#%PAM-1.0
auth       sufficient	pam_rootok.so
auth       required     pam_console.so
auth       sufficient	pam_timestamp.so
auth       include	system-auth
account    required	pam_permit.so
session    optional	pam_xauth.so
session    optional	pam_timestamp.so
_EOF_

# console.apps
install -m 755 -d %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} << _EOF_
USER=root
PROGRAM=%{_sbindir}/etherape.real
SESSION=true
FALLBACK=false
_EOF_

# fd.o icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
install -m 644 %{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 %{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 %{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# remove files not bundled
rm -rf %{buildroot}%{_datadir}/gnome

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -fr %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING NEWS README* FAQ
%config(noreplace) %{_sysconfdir}/etherape
%config(noreplace) %{_sysconfdir}/pam.d/etherape
%config(noreplace) %{_sysconfdir}/security/console.apps/etherape
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/applications/*.desktop
%{_datadir}/omf/%{name}

