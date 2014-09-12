#
# Conditional build:
%bcond_with	tests		# do perform "make test"; disabled fusermount restricted
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	Fuse
Summary:	Fuse - write filesystems in Perl using FUSE
#Summary(pl.UTF-8):	
Name:		perl-Fuse
Version:	0.09_3
Release:	1
# same as perl (REMOVE THIS LINE IF NOT TRUE)
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-authors/id/D/DP/DPAVLIN/Fuse-0.09_3.tar.gz
# Source0-md5:	f14c2e1c58eeefabcb87753289963a3b
# generic URL, check or change before uncommenting
#URL:		http://search.cpan.org/dist/Fuse/
BuildRequires:	libfuse-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This lets you implement filesystems in perl, through the FUSE
(Filesystem in USErspace) kernel/lib interface.

FUSE expects you to implement callbacks for the various functions.

In the following definitions, "errno" can be 0 (for a success),
-EINVAL, -ENOENT, -EONFIRE, any integer less than 1 really.

You can import standard error constants by saying something like
"use POSIX qw(EDOTDOT ENOANO);".

Every constant you need (file types, open() flags, error values,
etc) can be imported either from POSIX or from Fcntl, often both.
See their respective documentations, for more information.



# %description -l pl.UTF-8
# TODO

%prep
%setup -q -n %{pdir}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make} \
	CC="%{__cc}" \
	OPTIMIZE="%{rpmcflags}"

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Changes README
%{perl_vendorarch}/Fuse.pm
%dir %{perl_vendorarch}/auto/Fuse/
%attr(755,root,root) %{perl_vendorarch}/auto/Fuse/*.so
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
