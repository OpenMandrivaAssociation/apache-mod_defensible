#Module-Specific definitions
%define apache_version 2.2.6
%define mod_name mod_defensible
%define mod_conf B25_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An Apache 2.x module intended to block spammers using DNSBL
Name:		apache-%{mod_name}
Version:	1.4
Release:	%mkrel 6
Group:		System/Servers
License:	GPL
URL:		http://julien.danjou.info/mod_defensible.html
Source0:	http://julien.danjou.info/mod_defensible/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		mod_defensible-libfool.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	udns-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_defensible is an Apache 2.x module intended to block spammers using DNSBL
servers. It will look at the client IP and check it in one or several DNSBL
servers and return a 403 Forbidden page to the client.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p0

cp %{SOURCE1} %{mod_conf}

%build
rm -f configure
libtoolize --force --copy; aclocal; automake --add-missing --copy --foreign; autoheader; autoconf

export APXS2="/usr/sbin/apxs"

%configure2_5x --localstatedir=/var/lib \
    --with-udns

%make

#%{_sbindir}/apxs -c -I%{_includedir}/mysql -L%{_libdir} -lmysqlclient mod_anticrack.c


%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/%{mod_so} %{buildroot}%{_libdir}/apache-extramodules
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING Changelog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}

