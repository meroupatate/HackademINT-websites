import jenkins
from src.ldap import LDAP_USER, LDAP_PASSWORD


def get_server():
    return jenkins.Jenkins('https://jenkins.hackademint.org', username=LDAP_USER, password=LDAP_PASSWORD)


def get_websites_jobs():
    server = get_server()
    jobs = server.get_job_info_regex('^(?!.*priv.*).*hackademint\.org$', 1, 1)
    job_status = [{ "url": job["name"], "color": job["color"] } for job in jobs]
    return job_status
