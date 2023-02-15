# murray-dermott-action
A series of Python tools for Murray and Dermott book.

## Instructions for the developers

Before starting playing around with git please install the basic
required packages and perform some configurations:

1. Update the packages repositories:

   ```linux
   $ sudo apt update
   ```

2. Install `git` and `emacs`:

   ```linux
   $ sudo apt install git emacs
   ```

3. Configure git (optional):

   ```linux
   $ git config --global user.name "Jose Guerra Carmenate"
   $ git config --global user.email joseguerracarmenate@gmail.com
   ```

Below is the procedure to fork the repo, create a working copy, modify
your working copy, commit changes to your own fork and pull request to
the main repo:

1. **Fork the repo**. Go to the original repository at
   https://github.com/seap-udea/murray-dermott-action and create a
   `fork` of it.

2. **Create a public and private key pair**. In order to create a
   working copy of the repo in a Linux machine you should creat a pair
   of public and private ssh keys. In the command line run:

   ```linux
   $ ssh-keygen -t rsa
   ```

   When prompt for a password press enter (do not write anything).

   > **NOTE**: Commands starting with `$` must be executed in the
     Linux command line.

   Once your key has been created let's display it:

   ``` $ cat $HOME/.ssh/id_rsa.pub ssh-rsa
   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC98DuynV5aPaP5CWiY8k3GiRwjvh9tHtiTxpzQ48s3pNj8iqxjr8YUuoaJghqenXwjgvxHBkPqtR8x6sWIw+ijV/bsRq49NloQDvr5d9QPsgpHk4omSDr+z9ZTGNKpQnv0YodvuwxuHA87puNWKmwKSk+8hMtG9VI6mnzL/SbzZfDoj+Z6fwSckmDG+XP7he0ARkzXrktkRTTLebA34NoGf5vzL7Xz9gAyFwocrbpeUARVDAV6y3C41mCh90tPeFViMUeGpWES6gsQBdvY1GV5blVoUQMLZH5IDp7hKbJoysKE=
   jorgezuluagacallejas@MacBook-Pro-de-Jorge-2.local
   ```
     
3. **Upload public key to GitHub**. Open your GitHub account, click
   the icon of your profile and look for the option `Settings`. In
   settings search for the option `SSH and GPG keys`. Create a new key
   and copy in the text box the key starting at `ssh-rsa`.

4. **Clone the repo**. Once you upload the public key you can create a
   working copy of the repo in your linux machine. Run:

   ```linux
   $ git clone git@github.com:<name_in_github>/murray-dermott-action.git
   ```

   where `<name_in_github>` is the nickname of your account in
   GitHub. If your name is `JaneDoe` then the command will be:

   ```linux
   $ git clone git@github.com:JaneDoe/murray-dermott-action.git
   ```

### Developing cycle

Once you have a working copy of your repo you are prepared to develop
contributions to the package.

These are the task you will oftenly run once you start working in the
project:

1. **Sync your fork**. In the page of your repo in GitHub press `Sync
   Fork` and then `Update branch`.

2. **Pull the latest changes**. In the directory of the local working
   copy run:

   ```linux
   $ git pull
   ```

   If you have made changes in the repo and you forgot to perform the
   `Sync fork` before start working, an optional command will be:

   ```linux
   $ git pull --autostash
   ```


3. **Work in the project**. Create new files, modify existing files in
   the repository, in summary be a developer.

4. **Add and commit changes**. If you created new files you want to
   add to the repo run:

   ```linux
   $ git add <file>
   ```

   Where `<file>` is the name of the file. For example if you created a new notebook named `test.ipynb` use:

   ```linux
   $ git add test.ipynb
   ```

   You can add multiple files using for instance:

   ```linux
   $ git add *.ipynb
   ```

   Once you have added new files or if you changed already existing files run:

   ```linux
   $ git commit -am "Some text describing changes"
   ```

   where in `"Some text describing changes"` please use a text that
   other developers may understand. Here are some examples: `"New
   notebook created"`, `"README.md updated"`, `"Multiple notebooks
   added and README.md modified"`.

5. **Push changes**. Once you commited changes now you can push them
   to your repo in GitHub:

   ```linux
   $ git push
   ```

6. Now you need to request the main developer to include you changes
   by making a `Pull request`. For this go to the repository webpage
   in GitHub and press `Pull request`. Review if the changes you
   performed on the repo are ok and then press `Create pull request`.

7. Have a cup of chocolate and return to step 1 when you are ready to
   start working again in the project.

### Useful resources

Here are some useful wepages, manuals, tutorials for developers under
a Linux environment:

- https://docs.github.com/en/get-started/quickstart/hello-world. This
  is the basic manual of GitHub.

- https://programarfacil.com/blog/arduino-blog/git-y-github/. A
  complete tutorial on GitHub in spanish, *¡y ole!*.

- https://www.gnu.org/software/emacs/refcards/pdf/refcard.pdf. Keyboard
  commands of emacs.

---------

This is a project developed in collaboration by:

- Daniel Niño-Villegas (daniel.ninov@udea.edu.co)
- Diana Zapata-Zuluaga (dianac.zapata@udea.edu.co)
- Diego A. Acosta-Beltran (diego.acostab@udea.edu.co)
- Emanuel Noreña-Garcia (emanuel.norena@udea.edu.co)
- Evelyn Zagarra-Piedrahita (evelyn.zagarra@udea.edu.co)
- Juanita A. Agudelo-Quiceno (juanita.agudelo@udea.edu.co)
- Leonard A. Gomez-Garcia (leonard.gomez@udea.edu.co)
- Santiago Herrera-Guzmán (santiago.herrerag1@udea.edu.co)
- Sofia Arboleda-Bolivar (sofia.arboledab@udea.edu.co)
- Jorge I. Zuluaga (jorge.zuluaga@udea.edu.co) [Coordinator]  

All of them from the undergraduate program in astronomy of the
University of Antioquia.