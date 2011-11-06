%define _disable_ld_no_undefined 1

# Info about conditional builds:
#
# The logic is opposite.  A parameter listed below as 'bcond_with' will
# not build by default, but will if '--with <param>' is passed to 
# rpmbuild.  The oposite is true for anything listed as 'bcond_without'
# will build by default, but can be disabled by passing '--without <param>'
# to rpmbuild.
#
# See: http://www.rpm.org/wiki/PackagerDocs/ConditionalBuilds
#

%bcond_with tests
%bcond_with dbqp_tests

# plugins which are enabled by default
%bcond_without auth_http
%bcond_without auth_file
%bcond_without auth_ldap
%bcond_without auth_pam
%bcond_without debug
%bcond_without filtered_replicator
%bcond_without logging_query
%bcond_without mysql_protocol
%bcond_without pbms
%bcond_without simple_user_policy
%bcond_without slave

# plugins disabled by default, either missing deps
# or need to be 'figured out' why they're not building 
%bcond_with haildb
%bcond_with blitzdb
%bcond_with rabbitmq
%bcond_with gearman_udf
%bcond_with logging_gearman

%define drizzledmessage_major 0
%define libname %mklibname drizzledmessage %{drizzledmessage_major}
%define develname %mklibname -d drizzledmessage

%define drizzle1_major 1
%define drizzle1_libname %mklibname drizzle %{drizzle1_major}
%define drizzle1_develname %mklibname -d drizzle %{drizzle1_major}

%define drizzle2_major 3
%define drizzle2_libname %mklibname drizzle %{drizzle2_major}
%define drizzle2_develname %mklibname -d drizzle %{drizzle2_major}

Summary:	A Lightweight SQL Database for Cloud and Web 
Name:		drizzle
Version:	2011.10.28
Release:	%mkrel 1
# All sources under drizzled/ are GPLv2.  
# Sources under plugin/ are either GPLv2 or BSD.
License:	GPLv2 and BSD
Group:		System/Servers
URL:		http://launchpad.net/drizzle
# This is going to change every time
Source0:	http://launchpad.net/drizzle/fremont/2011-10-25/+download/drizzle7-2011.10.28.tar.gz
Source1:	drizzled.cnf
Source2:	drizzle.cnf
Source3:	drizzled.init
# Generates plugin-configs.patch from config files in conf.d.  NOTE:
# conf.d is not included in the SRPM, this script is here for the packagers
# convenience to generate the plugin-configs.patch.
Source4:	gen_plugin_configs_patch.sh
# Patches
Patch3:		drizzle7-2011.01.07-tests.patch
# temporary fix for: https://bugs.launchpad.net/drizzle/+bug/712194
Patch7:		plugin-configs.patch
Patch9:		drizzle7-2011.06.19-linkage_fix.diff
Patch10:	drizzle7-2011.08.24-fmtstr.diff
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	boost-devel >= 1.39
BuildRequires:	curl-devel
BuildRequires:	doxygen
BuildRequires:	doxygen
BuildRequires:  gcc-c++ >= 4.4
BuildRequires:	gettext-devel
BuildRequires:	gnutls-devel
BuildRequires:	gperf
BuildRequires:	intltool
BuildRequires:	libevent-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	ncurses-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	protobuf-devel
BuildRequires:	readline-devel
BuildRequires:	zlib-devel
%if %{with haildb}
BuildRequires:	haildb-devel
%endif
%if %{with gearman_udf}
BuildRequires: libgearman-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Drizzle is a transactional SQL92 compliant relational database, geared towards
a plugin based architecture.

%package -n	%{libname}
Summary:	Common Libraries Shared by %{name} Client and Server
Group:		System/Libraries
Requires:	%{libname} >= %{version}-%{release}
Provides:	drizzle-lib = %{version}-%{release}

%description -n	%{libname}
Common Libraries Shared by %{name} Client and Server

%package -n	%{develname}
Summary:	Header Files and Development Libraries for %{name}
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	drizzle-devel = %{version}-%{release}

%description -n	%{develname}
This package contains the header files and development libraries for %{name}.
If you like to develop programs using %{name}, you will need to install
%{name}-devel.

%package -n	%{drizzle1_libname}
Summary:	Drizzle Client & Protocol Library v1
Group:		System/Libraries
Provides:	drizzle-client = %{version}-%{release}

%description -n	%{drizzle1_libname}
libdrizzle is the the client and protocol library for the Drizzle project. The
server, drizzled, will use this as for the protocol library, as well as the
client utilities and any new projects that require low-level protocol
communication (like proxies). Other language interfaces (PHP extensions, SWIG,
...) should be built off of this interface.

%package -n	%{drizzle1_develname}
Summary:	Drizzle Client & Protocol Library - Header files
Group:		Development/C
Requires:	%{drizzle1_libname} >= %{version}-%{release}
# because libdrizzle-0.8-*.src.rpm is dead:
Obsoletes:	%{mklibname drizzle -d}
Provides:	drizzle1-client-devel = %{version}-%{release}

%description -n %{drizzle1_develname}
Development files for the Drizzle Client & Protocol Library v1

%package -n	%{drizzle2_libname}
Summary:	Drizzle Client & Protocol Library v2
Group:		System/Libraries
Provides:	drizzle-client = %{version}-%{release}

%description -n	%{drizzle2_libname}
libdrizzle is the the client and protocol library for the Drizzle project. The
server, drizzled, will use this as for the protocol library, as well as the
client utilities and any new projects that require low-level protocol
communication (like proxies). Other language interfaces (PHP extensions, SWIG,
...) should be built off of this interface.

%package -n	%{drizzle2_develname}
Summary:	Drizzle Client & Protocol Library - Header files
Group:		Development/C
Requires:	%{drizzle2_libname} >= %{version}-%{release}
Provides:	drizzle2-client-devel = %{version}-%{release}

%description -n %{drizzle2_develname}
Development files for the Drizzle Client & Protocol Library v1

%package	client
Summary:	Client Utilities for %{name}
Group:		System/Servers
Requires:	%{libname} >= %{version}-%{release}
#Requires:	libdrizzle

%description	client
Client utilities for %{name}.

%package	server
Summary:	Server Daemon and Utilities for %{name}
Group:		System/Servers
Requires:	%{libname} >= %{version}-%{release}
Provides:	drizzle-server = %{version}-%{release}

%description	server
Server daemon and utilities for %{name}.

# OPTIONAL PLUGINS
%if %{with auth_file}
%package	plugin-auth-file
Summary:	File Based Authentication Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-auth-file
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the File Based Authentication plugin.
%endif

%if %{with auth_http}
%package	plugin-auth-http
Summary:	HTTP Authentication Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-auth-http
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the HTTP Authentication plugin.
%endif

%if %{with auth_ldap}
%package	plugin-auth-ldap
Summary:	LDAP Authentication Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}
Requires:	openldap

%description	plugin-auth-ldap
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the LDAP Authentication plugin.
%endif

%if %{with auth_pam}
%package	plugin-auth-pam
Summary:	PAM Authentication Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-auth-pam
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the PAM Authentication plugin.
%endif

%if %{with blitzdb_plugin}
%package	plugin-blitzdb
Summary:	BlitzDB Storage Engine Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-blitzdb
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the BlitzDB Storage Engine plugin.
%endif

%if %{with debug}
%package	plugin-debug
Summary:	Debug Console Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-debug
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Debug Console plugin.
%endif

%if %{with filtered_replicator}
%package	plugin-filtered-replicator
Summary:	Filtered Replicator Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-filtered-replicator
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Filtered Replicator plugin.
%endif

%if %{with haildb}
%package	plugin-haildb
Summary:	HailDB Storage Engine Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}
#Requires:	haildb

%description	plugin-haildb
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the HailDB Storage Engine plugin.
%endif

%if %{with gearman_udf}
%package	plugin-gearman-udf
Summary:	Gearman User Defined Functions Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-gearman-udf
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Gearman User Defined Functions plugin.
%endif

%if %{with logging_gearman}
%package	plugin-logging-gearman
Summary:	Gearman Logging Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-logging-gearman
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Gearman Logging plugin.
%endif

%if %{with logging_query}
%package	plugin-logging-query
Summary:	Query Logging Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-logging-query
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Query Logging plugin.
%endif 

%if %{with mysql_protocol}
%package	plugin-mysql-protocol
Summary:	MySQL Protocol Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-mysql-protocol
Drizzle is a database optimized for Cloud and Net applications. It is designed 
for massive concurrency on modern multi-cpu/core architecture. The code is 
originally derived from MySQL.

This package includes the MySQL Protocol plugin.
%endif

%if %{with pbms}
%package	plugin-pbms
Summary:	PrimeBase Blob Streaming Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-pbms
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the PrimeBase Blob Streaming plugin.
%endif 

%if %{with rabbitmq}
%package	plugin-rabbitmq
Summary:	RabbitMQ Transaction Log Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-rabbitmq
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the RabbitMQ Transaction Log plugin.
%endif 

%if %{with simple_user_policy}
%package	plugin-simple-user-policy
Summary:	Simple User Policy Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-simple-user-policy
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Simple User Policy plugin.
%endif

%if %{with slave}
%package	plugin-slave
Summary:	Slave Replication Plugin for %{name}
Group:		System/Servers
Requires:	%{name}-server >= %{version}-%{release}

%description	plugin-slave
Drizzle is a database optimized for Cloud and Net applications. It is designed
for massive concurrency on modern multi-cpu/core architecture. The code is
originally derived from MySQL.

This package includes the Slave Replication plugin.
%endif

%prep
%setup -q -n drizzle7-%{version}

# Patches
%patch3 -p1 -b .tests
%patch7 -p1 -b .plugin-configs
%patch9 -p0
%patch10 -p0

%build
%serverbuild

autoreconf -fi

# FIX ME: Warnings treated as errors in mock, but not straight builds... ???
export CXXFLAGS="${CXXFLAGS} -Wno-error"

# need to handle optional plugins properly
OPTS="--disable-rpath
    --localstatedir=/var/lib/drizzle
    --without-auth-test-plugin
    --without-hello-world-plugin
    --without-tableprototester-plugin"

# use for tmp location
mkdir -p conf.d

function optionally_include() {
    plugin=$1
    enabled=$2
    dash_plugin=$(echo $plugin | sed 's/_/-/g')
    if [ $enabled -eq 1 ]; then
        OPTS="${OPTS} --with-${dash_plugin}-plugin --disable-${dash_plugin}-plugin"
        cp -a plugin/${plugin}/plugin.cnf conf.d/${dash_plugin}.cnf
    else
        OPTS="${OPTS} --without-${dash_plugin}-plugin --disable-${dash_plugin}-plugin"
    fi
}

# unfortunately have to list all the optional plugins here as
# we can't do a for loop with % macros
optionally_include auth_http %{with auth_http}
optionally_include auth_file %{with auth_file}
optionally_include auth_ldap %{with auth_ldap}
optionally_include auth_pam %{with auth_pam}
optionally_include debug %{with debug}
optionally_include filtered_replicator %{with filtered_replicator}
optionally_include haildb %{with haildb}
optionally_include logging_query %{with logging_query}
optionally_include mysql_protocol %{with mysql_protocol}
optionally_include pbms %{with pbms}
optionally_include rabbitmq %{with rabbitmq}
optionally_include simple_user_policy %{with simple_user_policy}
optionally_include gearman_udf %{with gearman_udf}
optionally_include logging_gearman %{with logging_gearman}
optionally_include slave %{with slave}

%configure2_5x $OPTS
%make

%check
%if %{with tests}
%{__make} test
%endif

# new style tests
%if %{with dbqp_tests}
%{__make} test-dbqp
%endif

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}%{_sysconfdir}/drizzle
install -d %{buildroot}%{_sysconfdir}/drizzle/conf.d
install -d %{buildroot}%{_localstatedir}/log/drizzle
install -d %{buildroot}%{_localstatedir}/lib/drizzle
install -d %{buildroot}%{_localstatedir}/run/drizzle

%makeinstall_std AM_INSTALL_PROGRAM_FLAGS=""

# fix broken symlink
rm -f %{buildroot}%{_sbindir}/drizzled %{buildroot}%{_sbindir}/drizzled
pushd %{buildroot}%{_sbindir}
    ln -s drizzled7 drizzled
popd

# supporting files
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/drizzle/drizzled.cnf
install -m0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/drizzle/drizzle.cnf
install -m0755 %{SOURCE3} %{buildroot}%{_initrddir}/drizzled

# plugin configs
pushd conf.d
for i in $(echo *); do
    install -m0644 $i %{buildroot}%{_sysconfdir}/drizzle/conf.d/
done
popd

# cleanup
rm -f %{buildroot}%{_datadir}/drizzle7/drizzle.server
rm -f %{buildroot}%{_libdir}/drizzle7/*.*a
rm -f %{buildroot}%{_libdir}/*.*a

%pre server
getent group drizzle >/dev/null || groupadd -r drizzle
getent passwd drizzle >/dev/null || \
useradd -r -g drizzle -d /var/lib/drizzle -s /sbin/nologin \
-c "Drizzle Server User" drizzle
exit 0


%post server
if [ $1 = 1 ]; then
    /sbin/chkconfig --add drizzled
fi
if [ $1 -ge 1 ]; then
    /sbin/service drizzled condrestart || :
fi

%preun server
if [ $1 = 0 ]; then
    /sbin/service drizzled stop || :
    /sbin/chkconfig --del drizzled
fi

%clean
rm -rf %{buildroot}

%files
%defattr (-,root,root,-) 
%doc AUTHORS COPYING NEWS README
%dir %{_sysconfdir}/drizzle
%dir %{_sysconfdir}/drizzle/conf.d
%{_mandir}/man1/drizzle.1*
%{_mandir}/man1/drizzleimport.1*
%{_mandir}/man1/drizzleslap.1*
%{_mandir}/man8/drizzled.8*

%files -n %{libname}
%defattr (-,root,root,-) 
%{_libdir}/libdrizzledmessage.so.%{drizzledmessage_major}*

%files -n %{develname}
%defattr (-,root,root,-) 
%{_includedir}/drizzle7
%{_libdir}/libdrizzledmessage.so
%{_libdir}/pkgconfig/drizzle7.pc

%files -n %{drizzle1_libname}
%defattr (-,root,root,-)
%{_libdir}/libdrizzle.so.%{drizzle1_major}*

%files -n %{drizzle1_develname}
%defattr (-,root,root,-)
%{_includedir}/libdrizzle-1.0
%{_libdir}/libdrizzle.so
%{_libdir}/pkgconfig/libdrizzle-1.0.pc

%files -n %{drizzle2_libname}
%defattr (-,root,root,-)
%{_libdir}/libdrizzle-2.0.so.%{drizzle2_major}*

%files -n %{drizzle2_develname}
%defattr (-,root,root,-)
%{_includedir}/libdrizzle-2.0
%{_libdir}/libdrizzle-2.0.so
%{_libdir}/pkgconfig/libdrizzle-2.0.pc

%files client
%defattr (-,root,root,-) 
%config(noreplace) %{_sysconfdir}/drizzle/drizzle.cnf
%{_bindir}/drizzle*

%files server
%defattr (-,root,root,-) 
%attr(0755,drizzle,drizzle) %dir %{_localstatedir}/log/drizzle
%attr(0755,drizzle,drizzle) %dir %{_localstatedir}/lib/drizzle
%attr(0755,drizzle,drizzle) %dir %{_localstatedir}/run/drizzle
%config(noreplace) %{_sysconfdir}/drizzle/drizzled.cnf
%{_mandir}/man8/drizzled7.8*
%{_initrddir}/drizzled
%{_sbindir}/drizzled7
%{_sbindir}/drizzled
# These are core plugins bundled with -server
%{_libdir}/drizzle7/libascii_plugin.so
%{_libdir}/drizzle7/libbenchmark_plugin.so
%{_libdir}/drizzle7/libcharlength_plugin.so
%{_libdir}/drizzle7/libcompression_plugin.so
%{_libdir}/drizzle7/libconnection_id_plugin.so
%{_libdir}/drizzle7/libcrc32_plugin.so
%{_libdir}/drizzle7/libdefault_replicator_plugin.so
# %{_libdir}/drizzle7/liberrmsg_stderr_plugin.so
%{_libdir}/drizzle7/libfunction_dictionary_plugin.so
%{_libdir}/drizzle7/libhello_events_plugin.so
%{_libdir}/drizzle7/libhex_functions_plugin.so
%{_libdir}/drizzle7/libhttp_functions_plugin.so
%{_libdir}/drizzle7/libjson_server_plugin.so
%{_libdir}/drizzle7/liblength_plugin.so
%{_libdir}/drizzle7/liblogging_stats_plugin.so
%{_libdir}/drizzle7/libmd5_plugin.so
%{_libdir}/drizzle7/libmulti_thread_plugin.so
%{_libdir}/drizzle7/libperformance_dictionary_plugin.so
%{_libdir}/drizzle7/libquery_log_plugin.so
%{_libdir}/drizzle7/librand_function_plugin.so
%{_libdir}/drizzle7/libregex_policy_plugin.so
%{_libdir}/drizzle7/libreverse_function_plugin.so
%{_libdir}/drizzle7/libshow_schema_proto_plugin.so
%{_libdir}/drizzle7/libshutdown_function_plugin.so
%{_libdir}/drizzle7/libstorage_engine_api_tester_plugin.so
%{_libdir}/drizzle7/libsubstr_functions_plugin.so
# %{_libdir}/drizzle7/libsyslog_plugin.so
%{_libdir}/drizzle7/libtrigger_dictionary_plugin.so
%{_libdir}/drizzle7/libutility_dictionary_plugin.so
%{_libdir}/drizzle7/libuuid_function_plugin.so
%{_libdir}/drizzle7/libversion_plugin.so
%{_datadir}/locale/ar/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/bn/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ca/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/cs/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/cy/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/da/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/de/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/el/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/en_AU/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/en_GB/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/eo/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/es/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/eu/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/fo/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/fr/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/gl/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/he/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/hi/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/hu/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/id/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/it/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ja/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ko/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ml/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/mr/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ms/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/mt/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/nb/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/nl/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/oc/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/pl/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/pt/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/pt_BR/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ro/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ru/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/sk/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/sq/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/sv/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/ta/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/te/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/tr/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/uk/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/zh_CN/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/zh_HK/LC_MESSAGES/drizzle7.mo
%{_datadir}/locale/fil/LC_MESSAGES/drizzle7.mo

# OPTIONAL PLUGINS
%if %{with auth_file}
%files plugin-auth-file
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/auth-file.cnf
%{_libdir}/drizzle7/libauth_file_plugin.so
%endif

%if %{with auth_http}
%files plugin-auth-http
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/auth-http.cnf
%{_libdir}/drizzle7/libauth_http_plugin.so
%endif

%if %{with auth_ldap}
%files plugin-auth-ldap
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/auth-ldap.cnf
%{_libdir}/drizzle7/libauth_ldap_plugin.so
%{_libdir}/drizzle7/libauth_schema_plugin.so
%{_datadir}/drizzle7/README.auth_ldap
%{_datadir}/drizzle7/drizzle_create_ldap_user
%{_datadir}/drizzle7/drizzle_openldap.ldif
%{_datadir}/drizzle7/drizzle_openldap.schema
%endif

%if %{with auth_pam}
%files plugin-auth-pam
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/auth-pam.cnf
%{_libdir}/drizzle7/libauth_pam_plugin.so
%endif

%if %{with blitzdb_plugin}
%files plugin-blitzdb
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/blitzdb.cnf
%{_libdir}/drizzle7/libblitzdb_plugin.so
%endif

%if %{with debug}
%files plugin-debug
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/debug.cnf
%{_libdir}/drizzle7/libdebug_plugin.so
%endif

%if %{with filtered_replicator}
%files plugin-filtered-replicator
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/filtered-replicator.cnf
%{_libdir}/drizzle7/libfiltered_replicator_plugin.so
%endif

%if %{with gearman_udf}
%files plugin-gearman-udf
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/gearman-udf.cnf
%{_libdir}/drizzle7/libgearman_udf_plugin.so
%endif

%if %{with haildb}
%files plugin-haildb
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/haildb.cnf
%{_libdir}/drizzle7/libhaildb_plugin.so
%endif

%if %{with logging_gearman}
%files plugin-logging-gearman
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/logging-gearman.cnf
%{_libdir}/drizzle7/liblogging_gearman_plugin.so
%endif

%if %{with logging_query}
%files plugin-logging-query
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/logging-query.cnf
%{_libdir}/drizzle7/liblogging_query_plugin.so
%endif

%if %{with mysql_protocol}
%files plugin-mysql-protocol
%defattr (-,root,root,-)
# mysql_protocol is static
# %%{_libdir}/drizzle7/libmysql_protocol_plugin.so
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/mysql-protocol.cnf
%endif

%if %{with pbms}
%files plugin-pbms
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/pbms.cnf
%{_libdir}/drizzle7/libpbms_plugin.so
%endif

%if %{with rabbitmq}
%files plugin-rabbitmq
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/rabbitmq.cnf
%{_libdir}/drizzle7/librabbitmq_plugin.so
%endif

%if %{with simple_user_policy}
%files plugin-simple-user-policy
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/simple-user-policy.cnf
%{_libdir}/drizzle7/libsimple_user_policy_plugin.so
%endif

%if %{with slave}
%files plugin-slave
%defattr (-,root,root,-)
%config(noreplace) %{_sysconfdir}/drizzle/conf.d/slave.cnf
%{_libdir}/drizzle7/libslave_plugin.so
%endif
