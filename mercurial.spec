# NOTE
# - Warning: tests will fail if at same time tests are running (shared hw for
#   builders) as fixed port 20059 is used.
# - Warning: tests will fail inside vserver as binding to localhost, peername
#   is not 127.0.0.1 (will be ip of interfaces/0/ip instead)
# - Tests fail with python3 (state as of 6.5.1)
#
# Conditional build:
%bcond_with	tests	# don't run tests

%define         webapp          hgweb
%define         webappdir       %{_sysconfdir}/webapps/%{webapp}
%define         appdir          %{_datadir}/%{webapp}
%define         cgibindir       %{_prefix}/lib/cgi-bin
Summary:	Mercurial Distributed SCM
Summary(pl.UTF-8):	Mercurial - rozproszony system kontroli wersji
Name:		mercurial
Version:	6.5.1
Release:	3
License:	GPL v2+
Group:		Development/Version Control
Source0:	https://www.mercurial-scm.org/release/%{name}-%{version}.tar.gz
# Source0-md5:	fccff6981f362466b8e9e0fa0de0ddb6

Source2:	%{name}-%{webapp}.config
Source3:	%{name}-%{webapp}-httpd.config

Patch1:		%{name}-clean-environment.patch
URL:		https://www.mercurial-scm.org/
BuildRequires:	gettext-tools
BuildRequires:	python3 >= 1:3.6
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-docutils
BuildRequires:	python3-pygobject3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
%{?with_tests:BuildRequires:	unzip}
Requires:	python3-%{name} = %{version}-%{release}
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

%package -n python3-%{name}
Summary:	Mercurial Distributed SCM - Python libraries
Summary(pl.UTF-8):	Rozproszony system kontroli wersji Mercurial - biblioteki Pythona
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.6
Obsoletes:	python-mercurial < 6.5.1
Conflicts:	mercurial < 3.5.2-2

%description -n python3-%{name}
Mercurial Distributed SCM - Python 3 libraries.

%description -n python3-%{name} -l pl.UTF-8
Rozproszony system kontroli wersji Mercurial - biblioteki Pythona 3.

%package hgweb
Summary:	Scripts for serving Mercurial repositories over HTTP
Summary(pl.UTF-8):	Skrypty do serwowania repozytoriów Mercuriala przez HTTP
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
Requires:	apache(mod_wsgi) >= 1.1
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
Requires:	python3-modules

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

%package -n bash-completion-%{name}
Summary:	Bash completion for Mercurial
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów Mercuriala
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0

%description -n bash-completion-%{name}
Bash completion for Mercurial.

%description -n bash-completion-%{name} -l pl.UTF-8
Bashowe dopełnianie parametrów Mercuriala.

%package -n zsh-completion-%{name}
Summary:	Zsh completion for Mercurial
Summary(pl.UTF-8):	Dopełnianie parametrów w zsh dla Mercuriala
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	zsh

%description -n zsh-completion-%{name}
Zsh completion for Mercurial.

%description -n zsh-completion-%{name} -l pl.UTF-8
Dopełnianie parametrów w zsh dla Mercuriala.

%prep
%setup -q

%patch1 -p1

# fails on builders due to lack of networking
%{__rm} tests/test-clonebundles.t

# flaky tests
%{__rm} tests/{test-convert-cvs-synthetic,test-convert-cvs,test-convert-cvs-detectmerge,test-convert-cvsnt-mergepoints,test-convert-cvs-branch,test-parse-date,test-gpg}.t

%{__sed} -i -e '1s|#!/usr/bin/env python3$|#!%{__python3}|' hgweb.cgi
%{__sed} -i -e '1s|#!/usr/bin/env wish$|#!/usr/bin/wish|' contrib/hgk

%build
%py3_build
%{__make} -C doc

%if %{with tests}
cd tests
%{__python3} run-tests.py %{?_smp_mflags} --verbose
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/mercurial/dummycert.pem

install -d $RPM_BUILD_ROOT{%{cgibindir},%{webappdir}}
install -p *.cgi $RPM_BUILD_ROOT%{cgibindir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{webappdir}/%{webapp}.config
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/apache.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{webappdir}/httpd.conf

install -p contrib/hgk $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
cp -p doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

#py_comp $RPM_BUILD_ROOT%{py3_sitedir}

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
%doc CONTRIBUTORS README.rst
%attr(755,root,root) %{_bindir}/hg
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files -n python3-%{name}
%defattr(644,root,root,755)
%{py3_sitedir}/hgdemandimport
%{py3_sitedir}/hgext
%{py3_sitedir}/hgext3rd
%dir %{py3_sitedir}/%{name}
%{py3_sitedir}/%{name}/__pycache__
%attr(755,root,root) %{py3_sitedir}/%{name}/*.so
%{py3_sitedir}/%{name}/*.py
%dir %{py3_sitedir}/%{name}/cext
%{py3_sitedir}/%{name}/cext/__pycache__
%{py3_sitedir}/%{name}/cext/*.py
%attr(755,root,root) %{py3_sitedir}/%{name}/cext/*.so
%{py3_sitedir}/%{name}/cffi
%{py3_sitedir}/%{name}/defaultrc
%{py3_sitedir}/%{name}/dirstateutils
%{py3_sitedir}/%{name}/helptext
%{py3_sitedir}/%{name}/hgweb
%{py3_sitedir}/%{name}/interfaces
%{py3_sitedir}/%{name}/pure
%{py3_sitedir}/%{name}/revlogutils
%{py3_sitedir}/%{name}/stabletailgraph
%{py3_sitedir}/%{name}/templates
%{py3_sitedir}/%{name}/testing
%dir %{py3_sitedir}/%{name}/thirdparty
%{py3_sitedir}/%{name}/thirdparty/__pycache__
%{py3_sitedir}/%{name}/thirdparty/*.py
%{py3_sitedir}/%{name}/thirdparty/attr
%attr(755,root,root) %{py3_sitedir}/%{name}/thirdparty/*.so
%dir %{py3_sitedir}/%{name}/thirdparty/zope
%{py3_sitedir}/%{name}/thirdparty/zope/__pycache__
%{py3_sitedir}/%{name}/thirdparty/zope/*.py
%dir %{py3_sitedir}/%{name}/thirdparty/zope/interface
%{py3_sitedir}/%{name}/thirdparty/zope/interface/__pycache__
%{py3_sitedir}/%{name}/thirdparty/zope/interface/*.py
%attr(755,root,root) %{py3_sitedir}/%{name}/thirdparty/zope/interface/*.so
%{py3_sitedir}/%{name}/upgrade_utils
%{py3_sitedir}/%{name}/utils
%dir %{py3_sitedir}/%{name}/locale
%lang(da) %{py3_sitedir}/%{name}/locale/da
%lang(de) %{py3_sitedir}/%{name}/locale/de
%lang(el) %{py3_sitedir}/%{name}/locale/el
%lang(fr) %{py3_sitedir}/%{name}/locale/fr
%lang(it) %{py3_sitedir}/%{name}/locale/it
%lang(ja) %{py3_sitedir}/%{name}/locale/ja
%lang(pt_BR) %{py3_sitedir}/%{name}/locale/pt_BR
%lang(ro) %{py3_sitedir}/%{name}/locale/ro
%lang(ru) %{py3_sitedir}/%{name}/locale/ru
%lang(sv) %{py3_sitedir}/%{name}/locale/sv
%lang(zh_CN) %{py3_sitedir}/%{name}/locale/zh_CN
%lang(zh_TW) %{py3_sitedir}/%{name}/locale/zh_TW
%{py3_sitedir}/mercurial-%{version}-py*.egg-info

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

%files -n bash-completion-%{name}
%defattr(644,root,root,755)
%{bash_compdir}/hg

%files -n zsh-completion-mercurial
%defattr(644,root,root,755)
%{zsh_compdir}/_hg
