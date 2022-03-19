#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	JuicyPixels
Summary:	Picture loading/serialization (in png, jpeg, bitmap, gif, tga, tiff and radiance)
Name:		ghc-%{pkgname}
Version:	3.3.5
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/JuicyPixels
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	70474cc0f75c7541683a7bba14960ee0
URL:		http://hackage.haskell.org/package/JuicyPixels
BuildRequires:	ghc >= 6.12.3
%if %{with prof}
BuildRequires:	ghc-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This library provides saving & loading of different picture formats
for the Haskell language. The aim of the library is to be as
lightweight as possible, you ask it to load an image, and it'll dump
you a big Vector full of juicy pixels. Or squared pixels, or whatever,
as long as they're unboxed.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc README.md %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Gif
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Gif/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Gif/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Gif/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Jpg
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Jpg/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Jpg/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Jpg/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Metadata
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Metadata/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Metadata/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Png
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Png/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Png/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Png/Internal/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Tiff
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Tiff/Internal
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Tiff/Internal/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Tiff/Internal/*.dyn_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/include

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Metadata/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Gif/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Jpg/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Png/Internal/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Picture/Tiff/Internal/*.p_hi
%endif
