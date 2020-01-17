from __future__ import print_function
import os, re, subprocess


def getGitVersion(repoDir):
    """Return a version string with information about this git checkout.
Version output such that
a)	If the current tag describes the repo, than that tag is shown as the 'public' version
b)	If the current tag does not describe the repo, then the 'public' version is 'no_tag'
c)	The git SHA is always added as '+gXXXX'
d)	Followed by '.clone'  to indicate that this version was generated by a live git repo that had been cloned
e)	If there are un-commited changes in the repo, then '.dirty' is also appended
f)	If it's not a repo at all, then 'local' is returned
g)	If the git SHA is not in any remote branch, then 'not_pushed' is also appened.
    """

    # if git can't describe, either it's not a git repo or git is missing
    try:
        v = subprocess.check_output(['git', '-C', repoDir, 'describe', '--tags', '--dirty', '--long', '--all'])
    except subprocess.CalledProcessError:
        return 'local'

    v = v.rstrip()

    v_parts = v.split('/')
    # print(v_parts)
    description_type = v_parts[0]
    # print('description_type: ', description_type)
    version = v_parts[1:]
    version = '/'.join(version)
    # print(version)
    # # chop off prefix
    # assert v.startswith(tagPrefix)
    # v = v[len(tagPrefix):]
    # v = v.lstrip('-')

    # split up version parts
    parts = version.split('-')
    # print(parts)    

    gitVersion = parts[0]

    # has working tree been modified?
    modified = False
    if parts[-1] == 'dirty':
        modified = True
        parts = parts[:-1]

    print(parts)    
        
    # have commits been added on top of last tagged version?
    # (git describe adds -NNN-gXXXXXXX if this is the case)
    git_sha = None
    if len(parts) > 2 and re.match(r'\d+', parts[-2]) and re.match(r'g[0-9a-f]{7}', parts[-1]):
        git_sha = parts[-1]
        distance = int(parts[-2])

        # print('git_sha:', git_sha)
        # print('distance:', distance)

    if (distance != 0) or (description_type != 'tags'):
        # print(description_type)
        gitVersion = 'no_tag'  # then make it clear that this git sha isn't tagged

    if git_sha is not None:
        gitVersion += '+' + git_sha + '.clone'

    # is the current commit present in aibspi?

    ## check if current commit is in any remote branch
    ##  git branch -r --contains fac826de414ef3fe854dc24493be306ff911bb8c
    ##   output:  origin/master
    r_branches = subprocess.check_output(['git', '-C', repoDir, 'branch', '-r', '--contains', git_sha[1:] ])  #ignore the leading 'g' in the sha-string
    r_branches = r_branches.rstrip()
    print('r_branches: ', r_branches)

    if r_branches is '':
        gitVersion += '.not_pushed'

    ## get the url of the branch 'origin'
    ### git ls-remote --get-url origin
    #### http://aibspi.corp.alleninstitute.org/celltypes/mFISH/create_labels.git
    #### check for aibspi in url name


    if modified:
        gitVersion += '.dirty'

    # print( gitVersion )
    return gitVersion

