Name:		seabios
Version:	1.9.0
Release:	3
Summary:	Open-source legacy BIOS implementation
Group:		Emulators
License:	LGPLv3
URL:		http://www.coreboot.org/SeaBIOS
Source0:	http://code.coreboot.org/p/seabios/downloads/get/%{name}-%{version}.tar.gz
BuildRequires:	python iasl
ExclusiveArch:	%{ix86} x86_64 %arm
Requires:	%{name}-bin = %{version}-%{release}

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1

%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.

%ifarch %{ix86} x86_64
%package bin
Summary: Seabios for x86
Buildarch: noarch

%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.
%endif

%prep
%setup -q

# Makefile changes version to include date and buildhost
sed -i 's,VERSION=%{version}.*,VERSION=%{version},g' Makefile

%build
export CC=gcc
mkdir -p bfd
ln -s %{_bindir}/ld.bfd bfd/ld
export PATH=$PWD/bfd:$PATH

make .config
sed -i 's,CONFIG_DEBUG_LEVEL=.*,CONFIG_DEBUG_LEVEL=%{debug_level},g' .config

%ifarch %{ix86} x86_64
export CFLAGS="$RPM_OPT_FLAGS"
make PYTHON=%__python2
%endif

%install
mkdir -p %{buildroot}%{_datadir}/seabios
%ifarch %{ix86} x86_64
install -m 0644 out/bios.bin %{buildroot}%{_datadir}/seabios
%endif

%files
%doc COPYING COPYING.LESSER README

%ifarch %{ix86} x86_64
%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios.bin
%endif
