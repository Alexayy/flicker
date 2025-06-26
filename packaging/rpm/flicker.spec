Name:           flicker
Version:        0.1.0
Release:        1%{?dist}
Summary:        Screenshot hotkey listener

License:        MIT
URL:            https://github.com/Alexayy/flicker
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3, python3-pyqt5, python3-pynput

%description
Flicker is a lightweight screenshot utility that listens for global hotkeys and
spawns a helper to capture the screen or windows.

%prep
%autosetup -n %{name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
install -Dpm644 resources/flicker.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/flicker.png
install -Dpm644 resources/flicker.desktop %{buildroot}%{_datadir}/applications/flicker.desktop
install -Dpm644 flicker.service %{buildroot}%{_unitdir}/flicker.service

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/flicker*
%{_datadir}/icons/hicolor/256x256/apps/flicker.png
%{_datadir}/applications/flicker.desktop
%{_unitdir}/flicker.service

%changelog
* Wed Oct 26 2023 Example Packager <packager@example.com> - 0.1.0-1
- Initial package
