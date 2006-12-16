Summary:	Mercurial Distributed SCM
Summary(pl):	Mercurial - rozproszony SCM
Name:		mercurial
Version:	0.9.2
Release:	1
License:	GPL v2
Group:		Development/Version Control
Source0:	http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
# Source0-md5:	31529a7d81997f2388ad20df0ba4889e
URL:		http://www.selenic.com/mercurial/
BuildRequires:	asciidoc
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	python >= 2.2.1
%pyrequires_eq  python-modules
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

%description -l pl
Mercurial to szybki, lekki system zarz�dzania kodem �r�d�owym
zaprojektowany do wydajnej obs�ugi bardzo du�ych rozproszonych
projekt�w. Mo�liwo�ci obejmuj�:
- przechowywanie skompresowanych plik�w r�nic i schemat odtwarzania
  O(1)
- pe�ne indeksowanie plik�w i zmian w celu szybkiego przegl�dania
  historii projektu
- silne, oparte na SHA1 sprawdzanie integralno�ci oraz model
  przechowywania z samym do��czaniem
- zdecentralizowany model rozwoju z dowolnym ��czeniem mi�dzy drzewami
- szybki protok� ��czenia po sieci oparty na HTTP
- �atwy w u�yciu interfejs linii polece�
- zintegrowany samodzielny interfejs WWW
- ma�y kod podstawowy w Pythonie
- licencja GPL

%package hgk
Summary:	GUI for mercurial
Summary(pl):	Graficzny interfejs u�ytkownika dla systemu Mercurial
Group:		Development/Version Control
Requires:	%{name} = %{version}-%{release}
%pyrequires_eq  python-modules

%description hgk
A tool called that allows browsing the history of a repository in a
GUI.

To enable it add to .hgrc file:
[extensions]
hgk=

%description hgk -l pl
Narz�dzie pozwalaj�ce na przegl�danie historii repozytorium w
graficznym interfejsie u�ytkownika.

Aby je uaktywni�, nale�y doda� do pliku .hgrc:
[extensions]
hgk=

%prep
%setup -q

%build
python setup.py build
%{__make} -C doc

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install contrib/hgk $RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/man{1,5}
install doc/hg.1 $RPM_BUILD_ROOT%{_mandir}/man1/hg.1
install doc/hgmerge.1 $RPM_BUILD_ROOT%{_mandir}/man1/hgmerge.1
install doc/hgrc.5 $RPM_BUILD_ROOT%{_mandir}/man5/hgrc.5
install doc/hgignore.5 $RPM_BUILD_ROOT%{_mandir}/man5/hgignore.5

%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README
%attr(755,root,root) %{_bindir}/hg
%attr(755,root,root) %{_bindir}/hgmerge
%{py_sitedir}/hgext
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/hgweb
%{py_sitedir}/%{name}/templates
%{py_sitedir}/mercurial-unknown-py2.5.egg-info
%{_mandir}/man1/hg.1.gz
%{_mandir}/man1/hgmerge.1.gz
%{_mandir}/man5/hgrc.5.gz
%{_mandir}/man5/hgignore.5.gz

%files hgk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hgk
