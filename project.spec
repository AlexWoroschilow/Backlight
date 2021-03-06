Summary: Ambient light brightness 
Name: ambient-light-brightness
Version: 0.1
Release: %(date +"%Y%m%d")
Source0: %{name}-%{version}.tar.gz
Group: Application/Web
License: MIT
Requires: python3 python3-qt5 python3-pygame

%description
Read the ambient light sensor data if present and adjust the backlight according to the abient light. 
If the ssytem has no ambient light sensor, the program will get the ambient light level using the camera 

%prep
%setup -q

%install

install -d $RPM_BUILD_ROOT/usr/bin
cp ambient-light-brightness $RPM_BUILD_ROOT/usr/bin

install -d $RPM_BUILD_ROOT/usr/share/applications
cp Ambient-light-brightness.desktop $RPM_BUILD_ROOT/usr/share/applications

install -d $RPM_BUILD_ROOT/etc/udev/rules.d
cp 80-ambient-light-brightness.rules $RPM_BUILD_ROOT/etc/udev/rules.d


%files
%attr(644,root,root) /etc/udev/rules.d/80-ambient-light-brightness.rules
%attr(755,root,root) /usr/share/applications/Ambient-light-brightness.desktop
%attr(755,root,root) /usr/bin/ambient-light-brightness


