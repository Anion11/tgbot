from settings import vk


class Groups:

    def __init__(self):
        self.group_id = None
        self.domain = None
        self.have_domain = False

    def initDomain(self, domain):
        self.domain = domain
        self.have_domain = True
        group = vk.method("utils.resolveScreenName", {"screen_name": domain})
        self.group_id = -1 * group["object_id"]


