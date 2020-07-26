from fabric import task
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """返回 github 用户名密码自动填充器"""
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )

    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'hellodjango-blog'

    project_root_path = '~/apps/HelloDjango-blog/'

    # supervisorctl 安装在用户本地目录，fabbric 启动的 session 无法读取到这个命令
    # 解决方式：
    # which supervisorctl 查看 supervisorctl 命令的绝对路径 /path/to/supervisorctl
    # 将脚本中的 supervisorctl command 命令替换为上面的绝对路径 /path/to/supervisorctl command

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    # 进入项目根目录，从Git拉取最新的代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 使用 docker 不用再在服务器上进行更新，而是在 docker容器 中进行更新
    # 安装依赖，迁移数据库，收集静态资源
    # with c.cd(project_root_path):
        # c.run('pipenv install --deploy --ignore-pipfile')
        # c.run('pipenv run python manage.py migrate')
        # c.run('pipenv run python manage.py collectstatic --noinput')

    # 重新启动项目
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)

# 自动化部署
# pipenv run fab -H server_ip --prompt-for-login-password -p deploy
# **注意：server_ip格式应该是 [user@]host[:port] 例如：hello@192.168.0.1:1000,默认连接端口是22 **
