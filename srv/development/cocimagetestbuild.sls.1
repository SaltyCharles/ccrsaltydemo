#cocimagetestbuild

###############################################
##
##   Clash of Clans Image Read Test Build
##   Version 1.0.0 
##
###############################################


##############################
##
## Create paths
##
##############################

# Create staging folders
"Create staging folder location":
    file.directory:
        - name: "/stage"
        - mode: 755

##############################
##
## File Downloads
##
##############################

# Download bootstrap for pip install
"Download PIP bootstrap":
    cmd.run:
        - name: "wget https://bootstrap.pypa.io/get-pip.py"
        - cwd: "/stage"
        - require:
            - file: "Create stage file location"

# Download bootstrap for salt install
"Download Salt bootstrap":
    cmd.run:
        - name: "curl -L https://bootstrap.saltstack.com -o install_salt.sh"
        - cwd: "/stage"
        - require:
            - file: "Create stage file location"


##############################
##
## Bootstrap installs
##
##############################

# Execute PIP bootstrap script
"Execute PIP bootstrap":
    cmd.run:
        - name: "python get-pip.py"
        - cwd: "/stage"
        - require:
            - cmd: "Download PIP bootstrap"

# Execute Salt bootstrap script
"Execute Salt bootstrap":
    cmd.run:
        - name: "sh install_salt.sh -M -P git v2015.5.0"
        - cwd: "/stage"
        - require:
            - cmd: "Download Salt bootstrap"


##############################
##
## Package installs
##
##############################

# Install tesserack packages and dependencies
"Install Tesseract pkgs and deps":
    pkg.installed:
        - name: python-mysqldb
        - name: autoconf automake libtool
        - name: libpng12-dev
        - name: libjpeg62-dev
        - name: g++
        - name: libtiff4-dev
        - name: libopencv-dev libtesseract-dev
        - name: git
        - name: cmake
        - name: build-essential
        - name: libleptonica-dev
        - name: liblog4cplus-dev
        - name: libcurl3-dev
        - name: python2.7-dev
        - name: tk8.5 tcl8.5 tk8.5-dev tcl8.5-dev

"Build python-imaging dependencies":
  cmd.run:
    - cwd: "/stage"
    - require:
      - cmd: "Install Tesseract pkgs and deps"
      - names:
        - apt-get -y build-dep python-imaging --fix-missing