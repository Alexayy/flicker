Name:           flicker
Version:        0.1
Release:        1%{?dist}
Summary:        Screenshot hotkey listener

License:        MIT
URL:            https://github.com/Alexayy/flicker
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(PyQt5)
BuildRequires:  python3dist(pynput)

%description
Flicker provides global hotkeys for taking screenshots on Linux.

%prep
%setup -q

%build
%py3_build

%install
%py3_install
install -Dm644 flicker.service "%{buildroot}%{_unitdir}/flicker.service"
install -Dm644 resources/flicker.png "%{buildroot}%{_datadir}/flicker/flicker.png"
install -Dm644 resources/flicker.desktop "%{buildroot}%{_sysconfdir}/xdg/autostart/flicker.desktop"

%files
%license LICENSE
%doc README.md
%{_bindir}/grab-screen
%{python3_sitelib}/flicker*
%{_unitdir}/flicker.service
%{_datadir}/flicker/flicker.png
%{_sysconfdir}/xdg/autostart/flicker.desktop

%changelog
* Mon Jan 01 2025 Aleksa Cakic <aleksa.cakic@gmail.com> - 0.1-1
- Initial package
