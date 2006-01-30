Summary:	Mercurial Distributed SCM
Summary(pl):	Mercurial - rozproszony SCM
Name:		mercurial
Version:	0.8
Release:	1
License:	GPL v2
Group:		Development/Version Control
Source0:	http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
# Source0-md5:	4d418e96dd232d804799fca3458ba2b6
URL:		http://www.selenic.com/mercurial/
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
Mercurial to szybki, lekki system zarz±dzania kodem ¼ród³owym
zaprojektowany do wydajnej obs³ugi bardzo du¿ych rozproszonych
projektów. Mo¿liwo¶ci obejmuj±:
- przechowywanie skompresowanych plików ró¿nic i schemat odtwarzania
  O(1)
- pe³ne indeksowanie plików i zmian w celu szybkiego przegl±dania
  historii projektu
- silne, oparte na SHA1 sprawdzanie integralno¶ci oraz model
  przechowywania z samym do³±czaniem
- zdecentralizowany model rozwoju z dowolnym ³±czeniem miêdzy drzewami
- szybki protokó³ ³±czenia po sieci oparty na HTTP
- ³atwy w u¿yciu interfejs linii poleceñ
- zintegrowany samodzielny interfejs WWW
- ma³y kod podstawowy w Pythonie
- licencja GPL

%prep
%setup -q

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python setup.py install \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CONTRIBUTORS README comparison.txt notes.txt
%attr(755,root,root) %{_bindir}/*
%dir %{py_sitedir}/%{name}
%attr(755,root,root) %{py_sitedir}/%{name}/*.so
%{py_sitedir}/%{name}/*.py[co]
%{py_sitedir}/%{name}/templates
