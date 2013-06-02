# NOTE
# - Warning: tests will fail if at same time tests are running (shared hw for
#   builders) as fixed port 20059 is used.
# - Warning: tests will fail inside vserver as binding to localhost, peername
#   is not 127.0.0.1 (will be ip of interfaces/0/ip instead)
#
# Conditional build:
%bcond_without	tests	# don't run tests
#
%define         webapp          hgweb
%define         webappdir       %{_sysconfdir}/webapps/%{webapp}
%define         appdir          %{_datadir}/%{webapp}
%define         cgibindir       %{_prefix}/lib/cgi-bin

Summary:	Mercurial Distributed SCM
Summary(pl.UTF-8):	Mercurial - rozproszony SCM
Name:		mercurial
Version:	2.6
Release:	2
License:	GPL v2
Group:		Development/Version Control
Source0:	http://mercurial.selenic.com/release/%{name}-%{version}.tar.gz
# Source0-md5:	d012d8bb5f85369d3b6a630a80667170
Source1:	gtools.py
Source2:	%{name}-%{webapp}.config
# TODO: provide default config
Source3:	%{name}-%{webapp}-apache.config
Source4:	%{name}-%{webapp}-httpd.config
Patch0:		%{name}-doc.patch
Patch1:		%{name}-clean-environment.patch
URL:		http://mercurial.selenic.com/
BuildRequires:	gettext-devel
BuildRequires:	python >= 1:2.4
BuildRequires:	python-devel
BuildRequires:	python-docutils
BuildRequires:	python-pygtk-gtk
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_tests:BuildRequires:	unzip}
%pyrequires_eq	python-modules
Conflicts:	apache-base < 2.4.0-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mercurial is a fast, lightweight source control management system
designed for efficient handling of very large distributed projects.
Features include:
- O(1) delta-compressed file storage and retrieval scheme
- Complete cross-indexing of file and changesets for efficient
  exploration of project history
- Robust SHA1-based integrity checking and append-only storage model
- Decentralized development model with arbitrary merging between trees
- High-speed HTTP-based network merge protocol
- Easy-to-use command-line interface
- Integrated stand-alone web interface
- Small Python codebase
- GPL license

%description -l pl.UTF-8
Mercurial to szybki, lekki system zarządzania kodem źródłowym
zaprojektowany do wydajnej obsługi bardzo dużych rozproszonych
projektów. Możliwości obejmują:
- przechowywanie skompresowanych plików różnic i schemat odtwarzania
  O(1)
- pełne indeksowanie plików i zmian w celu szybkiego przeglądania
  historii projektu
- silne, oparte na SHA1 sprawdzanie integralności oraz model
  przechowywania z samym dołączaniem
- zdecentralizowany model rozwoju z dowolnym łączeniem między drzewami
- szybki protokół łączenia po sieci oparty na HTTP
- łatwy w użyciu interfejs linii poleceń
- zintegrowany samodzielny interfejs WWW
- mały kod podstawowy w Pythonie
- licencja GPL

%package hgweb
Summary:	Scripts for serving mercurial repositories over HTTP
Summary(pl.UTF-8):	Skrypty do serwowania repozytoriów mercuriala przez HTTP
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
Requires:	apache-mod_wsgi >= 1.1
Requires:	webapps

%description hgweb
CGI scripts for serving mercurial repositories

%description hgweb -l pl.UTF-8
Skrypty CGI do serwowania repozytorió w mercuriala

%package hgk
Summary:	GUI for mercurial
Summary(pl.UTF-8):	Graficzny interfejs użytkownika dla systemu Mercurial
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq	python-modules

%description hgk
A tool called that allows browsing the history of a repository in a
GUI.

To enable it add to .hgrc file:
[extensions]
hgk=

%description hgk -l pl.UTF-8
Narzędzie pozwalające na przeglądanie historii repozytorium w
graficznym interfejsie użytkownika.

Aby je uaktywnić, należy dodać do pliku .hgrc:
[extensions]
hgk=

%prep
%setup -q
%patch0 -p1
%patch1 -p0
install %{SOURCE1} hgext/gtools.py

%build
%{__python} setup.py build
%{__make} -C doc

%{?with_tests:cd tests && %{__python} run-tests.py %{?_smp_mflags} --verbose}

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{cgibindir}
install *.cgi $RPM_BUILD_ROOT%{cgibindir}/

install -d $RPM_BUILD_ROOT%{webappdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{webappdir}/%{webapp}.config

install %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/apache.conf
install %{SOURCE4} $RPM_BUILD_ROOT%{webappdir}/httpd.conf

install contrib/hgk $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
install doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin hgweb -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{webapp}

%triggerun hgweb -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{webapp}

%triggerin hgweb -- apache-base
%webapp_register httpd %{webapp}

%triggerun hgweb -- apache-base
%webapp_unregister httpd %{webapp}

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/hg
%{py_sitedir}/hgext
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/help
%{py_sitedir}/%{name}/hgweb
%{py_sitedir}/%{name}/httpclient
%{py_sitedir}/%{name}/templates
%dir %{py_sitedir}/%{name}/locale
%lang(da) %{py_sitedir}/%{name}/locale/da
%lang(de) %{py_sitedir}/%{name}/locale/de
%lang(el) %{py_sitedir}/%{name}/locale/el
%lang(fr) %{py_sitedir}/%{name}/locale/fr
%lang(it) %{py_sitedir}/%{name}/locale/it
%lang(ja) %{py_sitedir}/%{name}/locale/ja
%lang(pt_BR) %{py_sitedir}/%{name}/locale/pt_BR
%lang(ro) %{py_sitedir}/%{name}/locale/ro
%lang(ru) %{py_sitedir}/%{name}/locale/ru
%lang(sv) %{py_sitedir}/%{name}/locale/sv
%lang(zh_CN) %{py_sitedir}/%{name}/locale/zh_CN
%lang(zh_TW) %{py_sitedir}/%{name}/locale/zh_TW
%if "%{py_ver}" > "2.4"
%{py_sitedir}/*.egg-info
%endif
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files hgweb
%defattr(644,root,root,755)
%dir %{cgibindir}
%attr(755,root,root) %{cgibindir}/*.cgi
%dir %{webappdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/hgweb.config
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/httpd.conf

%files hgk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hgk
