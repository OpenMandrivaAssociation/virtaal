Name:           virtaal
Version:        0.6.1
Release:        5
Summary:        Localization and translation editor
Group:          System/Internationalization
License:        GPLv2+
URL:            https://translate.sourceforge.net/wiki/virtaal/index
Source0:        http://downloads.sourceforge.net/translate/%{name}-%{version}.tar.bz2
# (Fedora) add some patches from fedora:
Patch0:         virtaal-0.6.1-libtranslate_error_reporting.patch
Patch1:         virtaal-0.5.0-setup_drop_MO_generation.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
%py_requires -d
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  python-translate >= 1.5.1
BuildRequires:  python-lxml
Requires:	iso-codes
Requires:       python-translate  >= 1.5.1
Requires:       pygtk2.0
Requires:	pygtk2.0-libglade
Requires:       gnome-python-gtkspell
Requires:	python-enchant
Requires:	python-lxml
Requires:       python-gobject
# python-pycurl needed for open-tran.eu
Requires:       python-curl
Requires:	python-simplejson
Requires:       xdg-utils
Requires:       python-levenshtein
# python-psycopg needed for tinytm
Suggests:       python-psycopg2

%description
A program for Computer Aided Translation (CAT) built on the Translate Toolkit.

Virtaal includes features that allow a localizer to work effecively including:
syntax highlighting, autocomplete and autocorrect.  Showing only 
the data that is needed through its simple and effective user interface it
ensures that you can focus on the translation task straight away.

By building on the Translate Toolkit, Virtaal is able to edit any of the
following formats: XLIFF, Gettext PO and .mo, Qt .ts, .qph and .qm, Wordfast 
TM, TMX, TBX.  By using the Translate Toolkit converters a translator can edit:
OpenOffice.org SDF, Java (and Mozilla) .properties and Mozilla DTD.
 

%prep
%setup -q -n %{name}-%{version}
%patch0 -p3 -b .libtranslate_error_reporting
%patch1 -p1 -b .drop_MO_generation

%build
# Drop shebang from non-executable python files
find virtaal -type f -and -name '*.py' -and ! -executable -exec  sed -i "sa#!/usr/bin/env pythonaa" {} \;
%{__python} setup.py build
./maketranslations %{name}
pushd po
for po in $(ls *.po | egrep -v de_DE)
do
    mkdir -p locale/$(basename $po .po)/LC_MESSAGES/
    msgfmt $po --output-file=locale/$(basename $po .po)/LC_MESSAGES/%{name}.mo
done
popd

%install
rm -rf %buildroot
%{__python} setup.py install --nodepcheck --skip-build --install-data=%{_prefix} --root=%buildroot

mkdir -p %{buildroot}%{_datadir}/
cp -rp po/locale %{buildroot}%{_datadir}/

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/mime/packages/*
%{_datadir}/virtaal
%{_datadir}/icons/*
%{python_sitelib}/*


%changelog
* Mon Dec 26 2011 Denis Silakov <dsilakov@mandriva.org> 0.6.1-4
+ Revision: 745429
- Drop shebang from non-executables python files

* Sat Nov 06 2010 Funda Wang <fwang@mandriva.org> 0.6.1-3mdv2011.0
+ Revision: 594032
- rebuild for py2.7

  + Michael Scherer <misc@mandriva.org>
    - rebuild for python 2.7

* Tue Jul 27 2010 Ahmad Samir <ahmadsamir@mandriva.org> 0.6.1-1mdv2011.0
+ Revision: 562098
- update to 0.6.1
- add two patchs from Fedora fixing two crashes
- require python-levenshtein

* Sat Jan 30 2010 Jérôme Brenier <incubusss@mandriva.org> 0.5.2-1mdv2010.1
+ Revision: 498392
- new version 0.5.2

* Thu Dec 31 2009 Jérôme Brenier <incubusss@mandriva.org> 0.5.1-1mdv2010.1
+ Revision: 484278
- new version 0.5.1

* Wed Dec 09 2009 Jérôme Brenier <incubusss@mandriva.org> 0.5.0-2mdv2010.1
+ Revision: 475621
- Requires / BuildRequires python-translate >= 1.5.1

* Mon Dec 07 2009 Jérôme Brenier <incubusss@mandriva.org> 0.5.0-1mdv2010.1
+ Revision: 474276
- new version 0.5.0
- drop Patch0 (merged upstream)

* Sat Nov 07 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.1-1mdv2010.1
+ Revision: 462188
- update to new version 0.4.1

* Thu Oct 15 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.0-3mdv2010.0
+ Revision: 457732
- Requires iso-codes and python-enchant (bug #54505)
- Only suggest python-psycopg2, as it's only needed for a tinytm plug-in
- Check for psycopg2 instead of psycopg at start-up: both are supported
  and the Mandriva package suggests psycopg2

* Sun Oct 11 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.0-2mdv2010.0
+ Revision: 456649
- Fix python-curl dependency (bug #54485)

* Tue Aug 11 2009 Frederik Himpe <fhimpe@mandriva.org> 0.4.0-1mdv2010.0
+ Revision: 415218
- Add Requires from Fedora
- Install with --nodepcheck in order to not bloat BuildRequires
- Update to new version 0.4.0
- Update Requires and BuildRequires

* Sat Mar 21 2009 Emmanuel Andry <eandry@mandriva.org> 0.3.1-1mdv2009.1
+ Revision: 360032
- New version 0.3.1
- add missing requires

* Wed Feb 11 2009 Frederik Himpe <fhimpe@mandriva.org> 0.3.0-1mdv2009.1
+ Revision: 339543
- update to new version 0.3.0

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 0.2-3mdv2009.1
+ Revision: 326006
- rebuild

* Tue Nov 25 2008 Götz Waschk <waschk@mandriva.org> 0.2-2mdv2009.1
+ Revision: 306632
- add missing dep on python-lxml

* Tue Oct 21 2008 Funda Wang <fwang@mandriva.org> 0.2-1mdv2009.1
+ Revision: 296133
- fix requires
- import virtaal


