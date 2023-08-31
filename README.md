~/Documents/2023-08-31-Streamlit-Homework/

(описание здесь)

TODO

Set remote Gitlab / Github repo 

открыть Git Bash в папке

Gitlab

что-то одно из трёх: 
-- не забыть придумать и ввести GIT-PROJECT-TAG (Ctrl-H автозамена в этом тексте)

git push --set-upstream http://git-lab.socio.loc/zhigmytovcv/GIT-PROJECT-TAG.git master
git remote add gl http://git-lab.socio.loc/zhigmytovcv/GIT-PROJECT-TAG.git

git push --set-upstream http://git-lab.socio.loc/epics/GIT-PROJECT-TAG.git master
git remote add gl http://git-lab.socio.loc/epics/GIT-PROJECT-TAG.git

git push --set-upstream http://git-lab.socio.loc/features/GIT-PROJECT-TAG.git master
git remote add gl http://git-lab.socio.loc/features/GIT-PROJECT-TAG.git 




Github 

что-то одно из трёх: 
-- не забыть придумать и ввести GIT-PROJECT-TAG

gh repo create sccntr/GIT-PROJECT-TAG --private
git remote add gh https://github.com/sccntr/GIT-PROJECT-TAG.git
git push --set-upstream gh master

посмотреть:
git remote -v




