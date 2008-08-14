# NOTE
# - Warning: tests will fail if at same time tests are running (shared hw for
#   builders) as fixed port 20059 is used.
# - Warning: tests will fail inside vserver as binding to localhost, peername
#   is not 127.0.0.1 (will be ip of interfaces/0/ip instead)
#
# Conditional build:
%bcond_without	tests	# don't run tests
#
Summary:	Mercurial Distributed SCM
Summary(pl.UTF-8):	Mercurial - rozproszony SCM
Name:		mercurial
Version:	1.0.1
Release:	3
License:	GPL v2
Group:		Development/Version Control
Source0:	http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
# Source0-md5:	a4ef7eb2c8818404a459e3be05feff6f
Source1:	gtools.py
Patch0:		%{name}-gtools.patch
URL:		http://www.selenic.com/mercurial/
BuildRequires:	asciidoc
BuildRequires:	python >= 1:2.3
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xmlto
%pyrequires_eq	python-modules
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
#%patch0 -p1
install %{SOURCE1} hgext/gtools.py

%build
%{__python} setup.py build
%{__make} -C doc

rm tests/test-hgweb

%{?with_tests:cd tests && %{__python} run-tests.py --verbose}

%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install contrib/hgk $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
install doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install doc/*.5 $RPM_BUILD_ROOT%{_mandir}/man5

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/hg
%{py_sitedir}/hgext
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/hgweb
%{py_sitedir}/%{name}/templates
%if "%{py_ver}" > "2.4"
%{py_sitedir}/*.egg-info
%endif
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*

%files hgk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hgk
