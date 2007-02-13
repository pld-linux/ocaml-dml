# $Revision: 1.15 $, $Date: 2006/04/16 10:20:54 
%define		ocaml_ver	1:3.09.2
Summary:	Dynamic code generation library for OCaml
Summary(pl.UTF-8):	Biblioteka do dynamicznej generacji kodu dla OCamla
Name:		ocaml-dml
Version:	0.2.1
Release:	7
License:	LGPL
Group:		Libraries
URL:		http://oops.tepkom.ru/dml/
Source0:	http://oops.tepkom.ru/dml/dml-%{version}.tar.gz
# Source0-md5:	a92f091dfc9b81861a62de53a6801a12
Patch0:		%{name}-mklib.patch
Patch1:		%{name}-ocaml_version.patch
Patch2:		%{name}-ocaml3.09.patch
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Dynamic Caml is a library that provides dynamic (or run-time) code
generation capabilities for Objective Caml programmer.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
Dynamic Caml jest biblioteką dostarczającą możliwości dynamicznej (w
czasie wykonania programu) generacji kodu programom napisanym w
OCamlu.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	Dynamic code generation library - development part
Summary(pl.UTF-8):	Biblioteka do dynamicznej generacji kodu - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
%requires_eq	ocaml-camlp4

%description devel
Dynamic Caml is a library that provides dynamic (or run-time) code
generation capabilities for Objective Caml programmer.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Dynamic Caml jest biblioteką dostarczającą możliwości dynamicznej (w
czasie wykonania programu) generacji kodu programom napisanym w
OCamlu.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n dml-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
./configure \
	-cc '%{__cc} %{rpmcflags} -fPIC' \
	-libdir %{_libdir}/ocaml/dml
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{dml,camlp4}
%{__make} install \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/dml \
	P4LIB=$RPM_BUILD_ROOT%{_libdir}/ocaml/camlp4
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s dml/dll*.so .)

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/{evalint,matrix,power,tab}.dml \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/dml
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/dml/META <<EOF
requires = ""
version = "%{version}"
directory = "+dml"
archive(byte) = "rtcg.cma rtcgbyte.cma"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/dml
%attr(755,root,root) %{_libdir}/ocaml/dml/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc README ChangeLog docs/dml.ps
%{_libdir}/ocaml/camlp4/*.cm[ao]
%{_libdir}/ocaml/dml/*.cm[ia]*
%{_libdir}/ocaml/dml/*.a
%{_libdir}/ocaml/dml/*.mli
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/dml
