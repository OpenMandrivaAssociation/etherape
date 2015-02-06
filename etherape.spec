Summary:	Graphical network viewer modeled after etherman
Name:		etherape
Version:	0.9.12
Release: 	4
License:	GPLv2+
Group:		Monitoring
URL:		http://etherape.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Requires:	usermode-consoleonly
Requires:       libbonoboui
Requires:       libgnomeui2
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	libpcap-devel
BuildRequires:	desktop-file-utils
BuildRequires:	scrollkeeper
BuildRequires:	imagemagick

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
%configure2_5x
%make

%install
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

%files -f %{name}.lang
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

