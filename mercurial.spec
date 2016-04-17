# NOTE
# - Warning: tests will fail if at same time tests are running (shared hw for
#   builders) as fixed port 20059 is used.
# - Warning: tests will fail inside vserver as binding to localhost, peername
#   is not 127.0.0.1 (will be ip of interfaces/0/ip instead)
#
# Conditional build:
%bcond_without	tests	# don't run tests

%define         webapp          hgweb
%define         webappdir       %{_sysconfdir}/webapps/%{webapp}
%define         appdir          %{_datadir}/%{webapp}
%define         cgibindir       %{_prefix}/lib/cgi-bin
Summary:	Mercurial Distributed SCM
Summary(pl.UTF-8):	Mercurial - rozproszony system kontroli wersji
Name:		mercurial
Version:	3.7.3
Release:	1
License:	GPL v2+
Group:		Development/Version Control
Source0:	https://www.mercurial-scm.org/release/%{name}-%{version}.tar.gz
# Source0-md5:	f47c9c76b7bf429dafecb71fa81c01b4
Source1:	gtools.py
Source2:	%{name}-%{webapp}.config
Source3:	%{name}-%{webapp}-httpd.config
Patch0:		%{name}-doc.patch
Patch1:		%{name}-clean-environment.patch
URL:		https://www.mercurial-scm.org/
BuildRequires:	gettext-tools
BuildRequires:	python >= 1:2.6
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-docutils
BuildRequires:	python-pygtk-gtk >= 2:2.0
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_tests:BuildRequires:	unzip}
Requires:	python-%{name} = %{version}-%{release}
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

%package -n python-%{name}
Summary:	Mercurial Distributed SCM - Python libraries
Summary(pl.UTF-8):	Rozproszony system kontroli wersji Mercurial - biblioteki Pythona
Group:		Libraries/Python
Requires:	python-modules >= 1:2.6
Conflicts:	mercurial < 3.5.2-2

%description -n python-%{name}
Mercurial Distributed SCM - Python libraries.

%description -n python-%{name} -l pl.UTF-8
Rozproszony system kontroli wersji Mercurial - biblioteki Pythona.

%package hgweb
Summary:	Scripts for serving Mercurial repositories over HTTP
Summary(pl.UTF-8):	Skrypty do serwowania repozytoriów Mercuriala przez HTTP
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
Requires:	apache-mod_wsgi >= 1.1
Requires:	webapps

%description hgweb
CGI scripts for serving Mercurial repositories.

%description hgweb -l pl.UTF-8
Skrypty CGI do serwowania repozytoriów Mercuriala.

%package hgk
Summary:	GUI for mercurial
Summary(pl.UTF-8):	Graficzny interfejs użytkownika dla systemu Mercurial
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
Requires:	python-modules

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
cp -p %{SOURCE1} hgext/gtools.py

# remove flaky tests failing due to glib deprecation warnings
%{__rm} tests/{test-help.t,test-extension.t,test-alias.t,test-status-color.t,test-i18n.t,test-qrecord.t,test-strict.t,test-duplicateoptions.py}

# fails on builders due to lack of networking
%{__rm} tests/test-clonebundles.t

# flaky test
%{__rm} tests/test-convert-cvs-synthetic.t

%ifarch x32
%{__rm} tests/{test-template-engine.t,test-context.py}
%endif

%build
%py_build
%{__make} -C doc

%if %{with tests}
cd tests
%{__python} run-tests.py %{?_smp_mflags} --verbose
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/mercurial/dummycert.pem

install -d $RPM_BUILD_ROOT{%{cgibindir},%{webappdir}}
install -p *.cgi $RPM_BUILD_ROOT%{cgibindir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{webappdir}/%{webapp}.config
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/apache.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/httpd.conf

install -p contrib/hgk $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
cp -p doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin hgweb -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{webapp}

%triggerun hgweb -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{webapp}

%triggerin hgweb -- apache < 2.2.0, apache-base
%webapp_register httpd %{webapp}

%triggerun hgweb -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{webapp}

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/hg
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files -n python-%{name}
%defattr(644,root,root,755)
%{py_sitedir}/hgext
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/default.d
%{py_sitedir}/%{name}/help
%{py_sitedir}/%{name}/hgweb
%{py_sitedir}/%{name}/httpclient
%{py_sitedir}/%{name}/pure
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
%{py_sitedir}/mercurial-%{version}-py*.egg-info

%files hgweb
%defattr(644,root,root,755)
%attr(755,root,root) %{cgibindir}/hgweb.cgi
%dir %{webappdir}
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/apache.conf
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/hgweb.config
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,http) %{webappdir}/httpd.conf

%files hgk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hgk
