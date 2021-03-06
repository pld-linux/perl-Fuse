#
# Conditional build:
%bcond_with	tests		# do perform "make test"; disabled fusermount restricted

%define		pdir	Fuse
Summary:	Fuse - write filesystems in Perl using FUSE
Name:		perl-Fuse
Version:	0.16.1
Release:	1
# same as perl (REMOVE THIS LINE IF NOT TRUE)
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/DPATES/%{pdir}-%{version}.tar.gz
# Source0-md5:	29534329808d8cf42fc78ca26c6fa698
URL:		http://search.cpan.org/dist/Fuse/
BuildRequires:	libfuse-devel
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This lets you implement filesystems in perl, through the FUSE
(Filesystem in USErspace) kernel/lib interface.

FUSE expects you to implement callbacks for the various functions.

In the following definitions, "errno" can be 0 (for a success),
- -EINVAL, -ENOENT, -EONFIRE, any integer less than 1 really.

You can import standard error constants by saying something like "use
POSIX qw(EDOTDOT ENOANO);".

Every constant you need (file types, open() flags, error values, etc)
can be imported either from POSIX or from Fcntl, often both. See their
respective documentations, for more information.

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
%{perl_vendorarch}/auto/Fuse/autosplit.ix
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
