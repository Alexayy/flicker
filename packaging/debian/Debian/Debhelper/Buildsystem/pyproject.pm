package Debian::Debhelper::Buildsystem::pyproject;
use strict;
use warnings;
use parent 'Debian::Debhelper::Buildsystem::pybuild';

sub new {
    my ($class, @rest) = @_;
    $ENV{PYBUILD_SYSTEM} = 'pyproject';
    return $class->SUPER::new(@rest);
}

1;
