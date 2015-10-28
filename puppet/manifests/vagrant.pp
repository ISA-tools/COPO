import "classes/*.pp"

$PROJ_DIR = "/vagrant"

Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {

    class {
        init: before => Class[copo];
        copo:;
    }
}

include dev
