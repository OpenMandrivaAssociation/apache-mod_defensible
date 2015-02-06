#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_defensible
%define mod_conf B25_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	An Apache 2.x module intended to block spammers using DNSBL
Name:		apache-%{mod_name}
Version:	1.5
Release:	2
Group:		System/Servers
License:	GPLv2+
URL:		http://julien.danjou.info/mod_defensible.html
Source0:	%{mod_name}-%{version}.tar.xz
Source1:	%{mod_conf}
Patch0:		mod_defensible-1.5-rosa-libfool.patch
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= %{apache_version}
Requires(pre):	apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:	apache-devel >= %{apache_version}
BuildRequires:	apr-devel
BuildRequires:	udns-devel
BuildRequires:	libtool

%description
mod_defensible is an Apache 2.x module intended to block spammers using DNSBL
servers. It will look at the client IP and check it in one or several DNSBL
servers and return a 403 Forbidden page to the client.

%prep

%setup -q -n %{mod_name}-%{version}
%patch0 -p1

cp %{SOURCE1} %{mod_conf}

%build
touch config.h.in
%setup_compile_flags
libtoolize --force --copy; aclocal; automake --add-missing --copy --foreign; autoheader; autoconf
export APXS2="%{_bindir}/apxs"

%configure2_5x --localstatedir=/var/lib \
    --with-udns

%make

#%{_bindir}/apxs -c -I%{_includedir}/mysql -L%{_libdir} -lmysqlclient mod_anticrack.c


%install

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

%files
%doc AUTHORS Changelog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}



%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 1.4-11mdv2012.0
+ Revision: 772615
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.4-10
+ Revision: 678301
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4-9mdv2011.0
+ Revision: 587959
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4-8mdv2010.1
+ Revision: 516087
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4-7mdv2010.0
+ Revision: 406571
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4-6mdv2009.1
+ Revision: 326487
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 1.4-5mdv2009.1
+ Revision: 325690
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-4mdv2009.0
+ Revision: 234926
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-3mdv2009.0
+ Revision: 215566
- fix rebuild
- fix buildroot
- hard code %%{_localstatedir}/lib to ease backports

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 1.4-2mdv2008.1
+ Revision: 182823
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Nov 22 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdv2008.1
+ Revision: 111142
- import apache-mod_defensible


* Thu Nov 22 2007 Oden Eriksson <oeriksson@mandriva.com> 1.4-1mdv2008.1
- initial Mandriva package
