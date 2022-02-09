# download link
http://git-scm.com/download/win

# check installation and version
git --version

# basic configurations
git config --global user.name 'Giwon Shin'
git config --global user.email 'giwone1330@gmail.com'

# check my status
git status

# add files to staging area - the files in the staging area are being tracked of changes
git add file.ext
git add .
# remove
git rm --chached file.ext

# commit
git commit -m 'any commit message'

# creating gitignore file
touch .gitignore
* write the file.ext and /folders you don't want to commit

# make branch
git branch test_branch

# checkout current branch to new branch
git checkout test_branch
----------------------------------------------------

# git with remote repository - github
# check the remote repository
git remote

# add a remote origin = github
git remote add origin https://github.com/giwone1330/test_demo.git
git remote
## now it should display >>origin

# push commited files to github - first push
git push -u origin master
# push commited files to github - second~ push
git push

# clone github repository
git clone <url>
# update local repository with remote repository
git pull