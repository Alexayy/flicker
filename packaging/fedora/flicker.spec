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

%files
%license LICENSE
%doc README.md
%{_bindir}/grab-screen
%{python3_sitelib}/flicker*

%changelog
* Mon Jan 01 2025 Aleksa Cakic <aleksa.cakic@gmail.com> - 0.1-1
- Initial package
