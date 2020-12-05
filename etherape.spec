Summary:	Graphical network viewer modeled after etherman
Name:		etherape
Version:	0.9.19
Release: 	1
License:	GPLv2+
Group:		Monitoring
URL:		https://etherape.sourceforge.net
Source0:	https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:	gnome-doc-utils
BuildRequires:	pkgconfig(libpcap)
BuildRequires:	pkgconfig(goocanvas-2.0)
BuildRequires:	pkgconfig(popt)
BuildRequires:	scrollkeeper
BuildRequires:	itstool

Requires:	usermode-consoleonly

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
%make_build

%install
%make_install bindir=%{_sbindir}

mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}/%{_sbindir}/%{name} %{buildroot}/%{_sbindir}/%{name}.real
ln -sf %{_bindir}/consolehelper %{buildroot}/%{_bindir}/%{name}

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
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

%find_lang %{name} --with-gnome

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING NEWS README* FAQ
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
