Name:           virtaal
Version:        0.4.0
Release:        %mkrel 2
Summary:        Localization and translation editor
Group:          System/Internationalization
License:        GPLv2+
URL:            http://translate.sourceforge.net/wiki/virtaal/index
Source0:        http://downloads.sourceforge.net/translate/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
%py_requires -d
BuildRequires:  gettext
BuildRequires:  intltool
BuildRequires:  python-translate >= 1.2
BuildRequires:  python-lxml
Requires:       python-translate  >= 1.2
Requires:       pygtk2.0
Requires:	pygtk2.0-libglade
Requires:       gnome-python-gtkspell
Requires:	python-lxml
Requires:       python-gobject
# python-pycurl needed for open-tran.eu
Requires:       python-curl
Requires:	python-simplejson
# python-psycopg2 needed for tinytm
Requires:       python-psycopg2
Requires:       xdg-utils

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

%build
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
%{__python} setup.py install --nodepcheck --skip-build --install-data=/usr --root=%buildroot

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
