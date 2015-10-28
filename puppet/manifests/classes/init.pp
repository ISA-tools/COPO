class init {

    group { "puppet":
        ensure => "present",
    }

    # Update the system
    exec { "update-apt":
        command => "sudo apt-get update",
    }

    # Install the first set of dependencies from apt
    package {
        ["build-essential", "curl", "gcc", "git", "libxml2-dev", "libxslt1-dev", "libffi-dev", "libssl-dev", "libncurses5-dev", "python3", "python3-dev", "python3-pip", "python3-setuptools", "python-virtualenv", "redis-server", "mongodb-server", "mysql-server-5.6"]:
        ensure => installed,
        require => Exec['update-apt'] # The system update needs to run first
    }

    # Install the project dependencies from pip
    exec { "pip-install-requirements":
        command => "sudo /usr/bin/pip3 install -r $PROJ_DIR/setup/requirements.txt",
        tries => 2,
        timeout => 600, # This might take a while
        require => Package["build-essential", "curl", "gcc", "git", "libxml2-dev", "libxslt1-dev", "libffi-dev", "libssl-dev", "libncurses5-dev", "python3", "python3-dev", "python3-pip", "python3-setuptools", "python-virtualenv"], # The package dependencies needs to run first
        logoutput => on_failure,
    }

    exec { "pip-install-mysql-connector-django":
        command => "sudo /usr/bin/pip3 install mysql-connector-python --allow-external mysql-connector-python",
        timeout => 60,
        require => Package["build-essential", "curl", "gcc", "git", "libxml2-dev", "libxslt1-dev", "libffi-dev", "libssl-dev", "libncurses5-dev", "python3", "python3-dev", "python3-pip", "python3-setuptools", "python-virtualenv"], # The package dependencies needs to run first
        logoutput => on_failure,
    }

    # Create the database
    exec { "create-databases":
        command =>"sudo $PROJ_DIR/setup/createdb.sh copo_development fshaw Apple123",
        require => Package["build-essential", "curl", "gcc", "git", "libxml2-dev", "libxslt1-dev", "libffi-dev", "libssl-dev", "libncurses5-dev", "python3", "python3-dev", "python3-pip", "python3-setuptools", "python-virtualenv"], # The package dependencies needs to run first       
        timeout => 600, # This definitely takes a while
        logoutput => on_failure,
    }

}
