class copo {

    exec {
        "managepy_makemigrations":
            cwd => "$PROJ_DIR/web",
            command => "/usr/bin/python3 manage.py makemigrations",
    }

    exec {
        "managepy_migratedb":
            cwd => "$PROJ_DIR/web",
            command => "/usr/bin/python3 manage.py migrate",
    }

    exec {
        "sql_patch_socialaccount":
            cwd => "$PROJ_DIR/setup",
            command => "mysql -ufshaw -pApple123 copo_development < social_account_setup.sql",
    }

}
