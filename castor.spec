Summary:	An open source data binding framework for Java
Summary(pl.UTF-8):	Szkielet wiązania danych dla Javy
Name:		castor
Version:	0.9.6
Release:	1.1
License:	Exolab Software License, BSD-like
Group:		Development/Languages/Java
Source0:	http://dist.codehaus.org/castor/0.9.6/%{name}-%{version}-src.tgz
# Source0-md5:	3ec1b9623f04b86f157738bd3f10a847
URL:		http://castor.codehaus.org/
BuildRequires:	adaptx
BuildRequires:	ant
BuildRequires:	cglib
BuildRequires:	jakarta-oro
BuildRequires:	jakarta-regexp
BuildRequires:	jdbc-stdext
BuildRequires:	jdk
BuildRequires:	jndi
BuildRequires:	jta
BuildRequires:	junit
BuildRequires:	ldapsdk
BuildRequires:	perl-base
BuildRequires:	xerces-j
Requires:	adaptx
Requires:	cglib
Requires:	jakarta-regexp
Requires:	java
Requires:	jdbc-stdext
Requires:	jndi
Requires:	jta
Requires:	ldapjdk
Requires:	oro
Requires:	xerces-j
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
find . -name "*.jar" -exec rm -f {} \;
perl -p -i -e 's|org.apache.xerces.utils.regex|org.apache.xerces.impl.xpath.regex|g;' \
src/main/org/exolab/castor/util/XercesRegExpEvaluator.java
find . -name "*.java" -exec perl -p -i -e 's|assert\(|assertTrue\(|g;' {} \;
find . -name "*.java" -exec perl -p -i -e 's|_test.name\(\)|_test.getName\(\)|g;' {} \;

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
export CLASSPATH=%(build-classpath adaptx cglib jdbc-stdext jndi jta junit ldapjdk oro regexp xerces-j2)
ant -buildfile src/build.xml jar
ant -buildfile src/build.xml CTFjar
ant -buildfile src/build.xml javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -d $RPM_BUILD_ROOT%{_javadir}
install dist/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install dist/%{name}-%{version}-xml.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-xml-%{version}.jar
install dist/CTF-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-tests-%{version}.jar
cd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}.jar; do
	ln -sf ${jar} $(echo $jar| sed  -e "s|-%{version}||g")
done
cd -

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%{__cp} -pr build/doc/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

# do this last, since it will delete all build directories
export CLASSPATH=%(build-classpath adaptx)
ant -buildfile src/build.xml doc

# like magic
%jpackage_script org.exolab.castor.builder.SourceGenerator %{nil} %{nil} xerces-j2:%{name} %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc src%{_sysconfdir}/{CHANGELOG,LICENSE,README}
%attr(755,root,root) %{_bindir}/%{name}
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar

%files test
%defattr(644,root,root,755)
%{_javadir}/%{name}-tests-%{version}.jar
%{_javadir}/%{name}-tests.jar

%files xml
%defattr(644,root,root,755)
%{_javadir}/%{name}-xml-%{version}.jar
%{_javadir}/%{name}-xml.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}

%files doc
%defattr(644,root,root,755)
%doc build/doc/*
