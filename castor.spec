#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc
#
%include	/usr/lib/rpm/macros.java
Summary:	An open source data binding framework for Java
Summary(pl.UTF-8):	Szkielet wiązania danych dla Javy
Name:		castor
Version:	1.2
Release:	0.1
License:	Exolab Software License, BSD-like
Group:		Development/Languages/Java
Source0:	castor-1.2.tar.bz2
# Source0-md5:	3387cdf40b0ab66c1aac1f0fb16ccb5f
URL:		http://castor.codehaus.org/
BuildRequires:	ant
BuildRequires:	ant-trax
BuildRequires:	java-gcj-compat-devel
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Castor is an open source data binding framework for Java. It's
basically the shortest path between Java objects, XML documents and
SQL tables. Castor provides Java to XML binding, Java to SQL
persistence, and then some more.

%description -l pl.UTF-8
Castor to mający otwarte źródła szkielet wiązania danych dla Javy.
Jest zasadniczo najkrótszą ścieżką między obiektami Javy, dokumentami
XML a tabelami SQL. Castor udostępnia wiązania Javy do XML-a,
utrzymywanie Javy do SQL-a i nieco więcej.

%package test
Summary:	Tests for %{name}
Summary(pl.UTF-8):	Testy dla pakietu %{name}
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}
Requires:	junit

%description test
Tests for %{name}.

%description test -l pl.UTF-8
Testy dla pakietu %{name}.

%package xml
Summary:	XML support for Castor
Summary(pl.UTF-8):	Obsługa XML-a dla Castora
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}

%description xml
XML support for Castor.

%description xml -l pl.UTF-8
Obsługa XML-a dla Castora.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%package doc
Summary:	Documentation for %{name}
Summary(pl.UTF-8):	Dokumentacja dla pakietu %{name}
Group:		Documentation

%description doc
Documentation for %{name}.

%description doc -l pl.UTF-8
Dokumentacja dla pakietu %{name}.

%prep
%setup -q

%build

export SHELL=/bin/sh
cd src
ant -Dbuild.compiler=extJavac jar.all
ant javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d $RPM_BUILD_ROOT%{_javadir}/castor/lib
install dist/castor-%{version}-tests.jar            $RPM_BUILD_ROOT%{_javadir}/castor/tests.jar
install dist/castor-%{version}-jdo.jar              $RPM_BUILD_ROOT%{_javadir}/castor/jdo.jar
install dist/castor-%{version}-ddlgen.jar           $RPM_BUILD_ROOT%{_javadir}/castor/ddlgen.jar
install dist/castor-%{version}-xml.jar              $RPM_BUILD_ROOT%{_javadir}/castor/xml.jar
install dist/castor-%{version}-codegen.jar          $RPM_BUILD_ROOT%{_javadir}/castor/codegen.jar
install dist/castor-%{version}-examples.jar         $RPM_BUILD_ROOT%{_javadir}/castor/examples.jar
install dist/castor-%{version}-commons.jar          $RPM_BUILD_ROOT%{_javadir}/castor/commons.jar
install dist/castor-%{version}-examples-sources.jar $RPM_BUILD_ROOT%{_javadir}/castor/examples-sources.jar
install dist/castor-%{version}-anttasks.jar         $RPM_BUILD_ROOT%{_javadir}/castor/anttasks.jar
install dist/castor-%{version}-xml-schema.jar       $RPM_BUILD_ROOT%{_javadir}/castor/xml-schema.jar
install dist/castor-%{version}.jar                  $RPM_BUILD_ROOT%{_javadir}/castor-%{name}.jar

cp -a lib/*.jar $RPM_BUILD_ROOT%{_javadir}/castor/lib

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink

# do this last, since it will delete all build directories
export CLASSPATH=%(build-classpath adaptx)
ant -buildfile src/build.xml doc

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc src%{_sysconfdir}/{CHANGELOG,LICENSE,README}
%attr(755,root,root) %{_bindir}/%{name}
%{_javadir}/castor
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif

%files doc
%defattr(644,root,root,755)
%doc build/doc/*
