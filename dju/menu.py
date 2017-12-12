from menus.base import Modifier
from menus.menu_pool import menu_pool
from cms.models import Page

class JustMenu(Modifier):
    """
    Menu modifier that add to node template name of the node page
    used to make some page in the menu, just menu items with no links.
    """
    post_cut = False

    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        tpls = dict(Page.objects.filter(id__in=[x.id for x in nodes]).values_list('id', 'template'))
        for node in nodes:
            node.tpl = tpls[node.id]
        return nodes

menu_pool.register_modifier(JustMenu)