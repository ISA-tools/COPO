COPO
====

COPO streamlines the process of data deposition to public repositories by hiding much of the complexity of metadata capture and data management from the end-user. The ISA infrastructure (www.isa-tools.org) is leveraged to provide the interoperability between metadata formats required for seamless deposition to repositories and to facilitate links to data analysis platforms. Logical groupings of artefacts (e.g. PDFs, raw data, contextual supplementary information) relating to a body of work are stored in COPO collections and represented by common standards, which are publicly searchable. Bundles of multiple data objects themselves can then be deposited directly into public repositories through COPO interfaces.

The Web directory contains the actual project, with project_copo being the main django project, and apps containing the bulk of the source code in web_copo. There are other directories in apps, and these are additional django application dependencies used throughout the project.

This fork adds setup of a development environment using Vagrant with Puppet for provisioning dependencies.

Installation:

`vagrant up`

To start COPO, login with `vagrant ssh` navigate to `/vagrant/web` and do `python3 manage.py runserver 0.0.0.0:8000`

Connect from host machine to `127.0.0.1:8000/copo/`
